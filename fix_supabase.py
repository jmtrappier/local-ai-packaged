#!/usr/bin/env python3
"""
fix_supabase.py

Ce script se concentre uniquement sur la résolution du problème de conflit dans le dépôt Supabase.
"""

import os
import subprocess
import shutil
import sys

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

def clean_supabase():
    """Supprime complètement le répertoire supabase et le reclone proprement."""
    # Supprimer le répertoire supabase s'il existe
    if os.path.exists("supabase"):
        print("Suppression du répertoire supabase existant...")
        try:
            shutil.rmtree("supabase")
            print("Répertoire supabase supprimé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression du répertoire supabase: {e}")
            return False
    
    # Cloner le dépôt Supabase
    print("Clonage du dépôt Supabase...")
    try:
        run_command([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ])
        
        # Configurer sparse checkout
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
        
        print("Dépôt Supabase cloné avec succès.")
        return True
    except Exception as e:
        print(f"Erreur lors du clonage du dépôt Supabase: {e}")
        return False

def create_override_file():
    """Crée le fichier docker-compose.override.yml pour Supabase."""
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

def copy_env_file():
    """Copie le fichier .env dans supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")
    
    if not os.path.exists(env_example_path):
        print(f"Erreur: Le fichier {env_example_path} n'existe pas.")
        return False
    
    try:
        shutil.copyfile(env_example_path, env_path)
        print(f"Fichier {env_example_path} copié vers {env_path} avec succès.")
        return True
    except Exception as e:
        print(f"Erreur lors de la copie du fichier .env: {e}")
        return False

def main():
    print("=== Réparation du dépôt Supabase ===")
    
    # Nettoyer et recloner le dépôt Supabase
    if not clean_supabase():
        print("Échec de la réparation du dépôt Supabase.")
        return
    
    # Créer le fichier docker-compose.override.yml
    if not create_override_file():
        print("Échec de la création du fichier docker-compose.override.yml.")
        return
    
    # Copier le fichier .env
    if not copy_env_file():
        print("Échec de la copie du fichier .env.")
        return
    
    print("=== Réparation terminée avec succès ===")
    print("Vous pouvez maintenant exécuter start_services.py pour démarrer les services.")
    print("Exemple: py start_services.py --profile gpu-nvidia")

if __name__ == "__main__":
    main() 