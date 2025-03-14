#!/usr/bin/env python3
"""
clean_caddy.py

Ce script vérifie si Caddy est toujours présent dans le système et le supprime si nécessaire.
Il nettoie également le cache Docker pour s'assurer que les anciennes images ne sont pas utilisées.
"""

import os
import subprocess
import platform
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

def check_docker_images():
    """Vérifie si l'image Caddy est présente dans Docker."""
    print("Vérification des images Docker...")
    try:
        result = run_command(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"], check=False)
        if result.returncode == 0:
            caddy_images = [img for img in result.stdout.splitlines() if "caddy" in img.lower()]
            if caddy_images:
                print(f"Images Caddy trouvées: {caddy_images}")
                return caddy_images
            else:
                print("Aucune image Caddy trouvée dans Docker.")
                return []
        else:
            print("Impossible de vérifier les images Docker. Docker est-il en cours d'exécution?")
            return []
    except Exception as e:
        print(f"Erreur lors de la vérification des images Docker: {e}")
        return []

def remove_docker_images(images):
    """Supprime les images Docker spécifiées."""
    if not images:
        return
    
    print(f"Suppression des images Caddy: {images}")
    for image in images:
        try:
            run_command(["docker", "rmi", image], check=False)
        except Exception as e:
            print(f"Erreur lors de la suppression de l'image {image}: {e}")

def clean_docker_cache():
    """Nettoie le cache Docker pour s'assurer que les anciennes images ne sont pas utilisées."""
    print("Nettoyage du cache Docker...")
    try:
        run_command(["docker", "system", "prune", "-f"], check=False)
        print("Cache Docker nettoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors du nettoyage du cache Docker: {e}")

def check_docker_compose_files():
    """Vérifie si des références à Caddy existent dans les fichiers docker-compose."""
    print("Vérification des fichiers docker-compose pour les références à Caddy...")
    
    files_to_check = ["docker-compose.yml", "docker-compose.override.yml"]
    references_found = False
    
    for file in files_to_check:
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    if "caddy" in content.lower():
                        print(f"Références à Caddy trouvées dans {file}:")
                        lines = content.splitlines()
                        for i, line in enumerate(lines):
                            if "caddy" in line.lower():
                                print(f"  Ligne {i+1}: {line}")
                        references_found = True
            except Exception as e:
                print(f"Erreur lors de la lecture de {file}: {e}")
    
    if not references_found:
        print("Aucune référence à Caddy trouvée dans les fichiers docker-compose.")
    
    return references_found

def main():
    print("=== Nettoyage de Caddy ===")
    
    # Vérifier les images Docker
    caddy_images = check_docker_images()
    
    # Vérifier les fichiers docker-compose
    check_docker_compose_files()
    
    # Supprimer les images Caddy si elles existent
    if caddy_images:
        remove_docker_images(caddy_images)
    
    # Nettoyer le cache Docker
    clean_docker_cache()
    
    print("=== Nettoyage terminé ===")
    print("Vous pouvez maintenant exécuter start_services.py pour démarrer les services avec Traefik.")

if __name__ == "__main__":
    main() 