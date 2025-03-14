#!/usr/bin/env python3
"""
resolve_conflict.py

Ce script résout automatiquement les conflits de fusion dans le fichier docker-compose.yml
du dépôt Supabase en acceptant les modifications distantes (version du serveur).
"""

import os
import subprocess
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

def resolve_conflict():
    """Résout le conflit dans docker-compose.yml en acceptant la version distante."""
    conflict_file = os.path.join("supabase", "docker", "docker-compose.yml")
    
    if not os.path.exists(conflict_file):
        print(f"Erreur: Le fichier {conflict_file} n'existe pas.")
        return False
    
    print(f"Résolution du conflit dans {conflict_file}...")
    
    # Vérifier si nous sommes dans un répertoire git
    if not os.path.exists(os.path.join("supabase", ".git")):
        print("Erreur: Le répertoire supabase n'est pas un dépôt git.")
        return False
    
    # Se déplacer dans le répertoire supabase
    os.chdir("supabase")
    
    try:
        # Accepter la version distante (--theirs)
        run_command(["git", "checkout", "--theirs", "docker/docker-compose.yml"])
        
        # Marquer le conflit comme résolu
        run_command(["git", "add", "docker/docker-compose.yml"])
        
        # Créer un commit pour la résolution
        run_command(["git", "commit", "-m", "Résolution automatique du conflit dans docker-compose.yml"])
        
        print("Conflit résolu avec succès!")
        return True
    except Exception as e:
        print(f"Erreur lors de la résolution du conflit: {e}")
        return False
    finally:
        # Revenir au répertoire d'origine
        os.chdir("..")

def main():
    print("=== Résolution de conflit Git ===")
    
    if resolve_conflict():
        print("Le conflit a été résolu. Vous pouvez maintenant exécuter start_services.py à nouveau.")
    else:
        print("Échec de la résolution du conflit. Veuillez résoudre manuellement le conflit:")
        print("1. Naviguez vers le répertoire supabase: cd supabase")
        print("2. Ouvrez le fichier en conflit: nano docker/docker-compose.yml")
        print("3. Résolvez les conflits marqués par <<<<<<< HEAD, =======, et >>>>>>>")
        print("4. Enregistrez le fichier")
        print("5. Marquez le conflit comme résolu: git add docker/docker-compose.yml")
        print("6. Créez un commit: git commit -m 'Résolution manuelle du conflit'")
        print("7. Revenez au répertoire principal: cd ..")
        print("8. Exécutez à nouveau start_services.py")
    
    print("=== Fin de la résolution de conflit ===")

if __name__ == "__main__":
    main() 