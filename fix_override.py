#!/usr/bin/env python3
"""
fix_override.py

Ce script vérifie et répare le fichier docker-compose.override.yml qui pourrait être mal formaté.
"""

import os
import yaml
import sys

def fix_override_file():
    """Vérifie et répare le fichier docker-compose.override.yml."""
    override_path = os.path.join("supabase", "docker", "docker-compose.override.yml")
    
    if not os.path.exists(override_path):
        print(f"Le fichier {override_path} n'existe pas. Création du fichier...")
        create_override_file(override_path)
        return True
    
    print(f"Vérification du fichier {override_path}...")
    
    try:
        # Essayer de charger le fichier YAML pour vérifier sa validité
        with open(override_path, 'r') as f:
            content = f.read()
            yaml_content = yaml.safe_load(content)
            
            # Vérifier si le contenu est un dictionnaire (mapping)
            if not isinstance(yaml_content, dict):
                print(f"Le fichier {override_path} n'est pas correctement formaté. Réparation...")
                create_override_file(override_path)
            else:
                print(f"Le fichier {override_path} est correctement formaté.")
                return True
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {override_path}: {e}")
        print("Réparation du fichier...")
        create_override_file(override_path)
    
    return True

def create_override_file(file_path):
    """Crée un fichier docker-compose.override.yml correctement formaté."""
    try:
        # Créer le répertoire parent si nécessaire
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Écrire le contenu correct dans le fichier
        with open(file_path, 'w') as f:
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
        
        print(f"Fichier {file_path} créé avec succès.")
        return True
    except Exception as e:
        print(f"Erreur lors de la création du fichier {file_path}: {e}")
        return False

def main():
    print("=== Vérification et réparation du fichier docker-compose.override.yml ===")
    
    if fix_override_file():
        print("Le fichier docker-compose.override.yml a été vérifié et réparé si nécessaire.")
        print("Vous pouvez maintenant exécuter resolve_conflict.py puis start_services.py.")
    else:
        print("Échec de la réparation du fichier docker-compose.override.yml.")
        print("Veuillez vérifier manuellement le fichier.")
    
    print("=== Fin de la vérification et réparation ===")

if __name__ == "__main__":
    main() 