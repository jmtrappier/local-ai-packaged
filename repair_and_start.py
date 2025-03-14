#!/usr/bin/env python3
"""
repair_and_start.py

Ce script exécute les scripts de réparation et redémarre le processus de démarrage.
"""

import os
import subprocess
import sys
import time

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

def run_python_script(script_name):
    """Exécute un script Python."""
    print(f"Exécution du script {script_name}...")
    try:
        # Vérifier si le script existe
        if not os.path.exists(script_name):
            print(f"Erreur: Le script {script_name} n'existe pas.")
            return False
        
        # Exécuter le script
        result = run_command([sys.executable, script_name], check=False)
        
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution du script {script_name}.")
            return False
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'exécution du script {script_name}: {e}")
        return False

def main():
    print("=== Réparation et démarrage des services ===")
    
    # Exécuter le script de réparation du fichier docker-compose.override.yml
    if not run_python_script("fix_override.py"):
        print("Échec de la réparation du fichier docker-compose.override.yml.")
        return
    
    # Exécuter le script de résolution des conflits
    if not run_python_script("resolve_conflict.py"):
        print("Échec de la résolution des conflits.")
        return
    
    print("Attente de 3 secondes avant de redémarrer les services...")
    time.sleep(3)
    
    # Demander le profil à utiliser
    print("Quel profil souhaitez-vous utiliser pour démarrer les services?")
    print("1. CPU uniquement (--profile cpu)")
    print("2. GPU NVIDIA (--profile gpu-nvidia)")
    print("3. GPU AMD (--profile gpu-amd)")
    print("4. Aucun (--profile none)")
    
    choice = input("Entrez votre choix (1-4): ")
    
    profile = "cpu"  # Par défaut
    
    if choice == "2":
        profile = "gpu-nvidia"
    elif choice == "3":
        profile = "gpu-amd"
    elif choice == "4":
        profile = "none"
    
    # Exécuter le script de démarrage des services
    print(f"Démarrage des services avec le profil '{profile}'...")
    run_command([sys.executable, "start_services.py", "--profile", profile], check=False)
    
    print("=== Fin de la réparation et du démarrage ===")

if __name__ == "__main__":
    main() 