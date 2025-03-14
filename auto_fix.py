#!/usr/bin/env python3
"""
auto_fix.py

Ce script résout automatiquement tous les problèmes sans interaction utilisateur.
"""

import os
import subprocess
import sys
import time
import shutil

def run_command(cmd, cwd=None, check=True):
    """Exécute une commande shell et l'affiche."""
    print("Exécution:", " ".join(cmd))
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        if check:
            raise
        return e

def fix_override_file():
    """Répare le fichier docker-compose.override.yml."""
    override_path = os.path.join("supabase", "docker", "docker-compose.override.yml")
    
    # Créer le répertoire parent si nécessaire
    os.makedirs(os.path.dirname(override_path), exist_ok=True)
    
    # Écrire le contenu correct dans le fichier
    with open(override_path, 'w') as f:
        f.write("""version: '3.8'

services:
  kong:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.supabase.rule=Host(`${SUPABASE_HOSTNAME:-localhost}`)"
      - "traefik.http.routers.supabase.entrypoints=websecure"
      - "traefik.http.routers.supabase.tls.certresolver=letsencrypt"
      - "traefik.http.services.supabase.loadbalancer.server.port=8000"
""")
    
    print(f"Fichier {override_path} créé avec succès.")
    return True

def resolve_conflict():
    """Résout le conflit dans docker-compose.yml."""
    conflict_file = os.path.join("supabase", "docker", "docker-compose.yml")
    
    if not os.path.exists("supabase"):
        print("Le répertoire supabase n'existe pas. Aucun conflit à résoudre.")
        return True
    
    if not os.path.exists(conflict_file):
        print(f"Le fichier {conflict_file} n'existe pas. Aucun conflit à résoudre.")
        return True
    
    # Vérifier si nous sommes dans un répertoire git
    if not os.path.exists(os.path.join("supabase", ".git")):
        print("Le répertoire supabase n'est pas un dépôt git. Tentative de réparation alternative...")
        
        # Supprimer le répertoire supabase et le recréer
        try:
            shutil.rmtree("supabase")
            print("Répertoire supabase supprimé avec succès.")
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du répertoire supabase: {e}")
            return False
    
    # Se déplacer dans le répertoire supabase
    os.chdir("supabase")
    
    try:
        # Vérifier s'il y a un conflit
        result = run_command(["git", "status"], check=False)
        if "both modified:" in result.stdout and "docker/docker-compose.yml" in result.stdout:
            # Accepter la version distante (--theirs)
            run_command(["git", "checkout", "--theirs", "docker/docker-compose.yml"])
            
            # Marquer le conflit comme résolu
            run_command(["git", "add", "docker/docker-compose.yml"])
            
            # Créer un commit pour la résolution
            run_command(["git", "commit", "-m", "Résolution automatique du conflit dans docker-compose.yml"])
            
            print("Conflit résolu avec succès!")
        else:
            print("Aucun conflit détecté dans docker-compose.yml.")
        
        return True
    except Exception as e:
        print(f"Erreur lors de la résolution du conflit: {e}")
        return False
    finally:
        # Revenir au répertoire d'origine
        os.chdir("..")

def clean_and_restart():
    """Nettoie l'environnement et redémarre le processus."""
    # Arrêter tous les conteneurs Docker
    run_command(["docker", "compose", "down"], check=False)
    
    # Supprimer le répertoire supabase s'il existe
    if os.path.exists("supabase"):
        try:
            shutil.rmtree("supabase")
            print("Répertoire supabase supprimé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression du répertoire supabase: {e}")
    
    # Exécuter le script de démarrage des services
    profile = "gpu-nvidia"  # Par défaut, utiliser GPU NVIDIA
    
    # Vérifier si un profil a été spécifié en argument
    if len(sys.argv) > 1:
        if sys.argv[1] in ["cpu", "gpu-nvidia", "gpu-amd", "none"]:
            profile = sys.argv[1]
    
    print(f"Démarrage des services avec le profil '{profile}'...")
    run_command([sys.executable, "start_services.py", "--profile", profile], check=False)

def main():
    print("=== Réparation automatique et démarrage des services ===")
    
    # Méthode 1: Essayer de réparer les fichiers
    print("Méthode 1: Réparation des fichiers...")
    fix_override_file()
    resolve_conflict()
    
    # Méthode 2: Si la méthode 1 échoue, nettoyer et redémarrer
    print("Méthode 2: Nettoyage et redémarrage...")
    clean_and_restart()
    
    print("=== Fin de la réparation automatique ===")

if __name__ == "__main__":
    main() 