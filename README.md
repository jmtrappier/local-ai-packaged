# Self-hosted AI Package

**Self-hosted AI Package** is an open, docker compose template that
quickly bootstraps a fully featured Local AI and Low Code development
environment including Ollama for your local LLMs, Open WebUI for an interface to chat with your N8N agents, and Supabase for your database, vector store, and authentication. 

This is Cole's version with a couple of improvements and the addition of Supabase, Open WebUI, Flowise, SearXNG, and Traefik!
Postgres was also removed since Supabase runs Postgres under the hood.
Also, the local RAG AI Agent workflow from the video will be automatically in your 
n8n instance if you use this setup instead of the base one provided by n8n!

## Important Links

- [Local AI community](https://thinktank.ottomator.ai/c/local-ai/18) forum over in the oTTomator Think Tank

- [GitHub Kanban board](https://github.com/users/coleam00/projects/2/views/1) for feature implementation and bug squashing.

- [Original Local AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit) by the n8n team

- Download my N8N + OpenWebUI integration [directly on the Open WebUI site.](https://openwebui.com/f/coleam/n8n_pipe/) (more instructions below)

![n8n.io - Screenshot](https://raw.githubusercontent.com/n8n-io/self-hosted-ai-starter-kit/main/assets/n8n-demo.gif)

Curated by <https://github.com/n8n-io> and <https://github.com/coleam00>, it combines the self-hosted n8n
platform with a curated list of compatible AI products and components to
quickly get started with building self-hosted AI workflows.

### What's included

✅ [**Self-hosted n8n**](https://n8n.io/) - Low-code platform with over 400
integrations and advanced AI components

✅ [**Supabase**](https://supabase.com/) - Open source database as a service -
most widely used database for AI agents

✅ [**Ollama**](https://ollama.com/) - Cross-platform LLM platform to install
and run the latest local LLMs

✅ [**Open WebUI**](https://openwebui.com/) - ChatGPT-like interface to
privately interact with your local models and N8N agents

✅ [**Flowise**](https://flowiseai.com/) - No/low code AI agent
builder that pairs very well with n8n

✅ [**Qdrant**](https://qdrant.tech/) - Open-source, high performance vector
store with an comprehensive API. Even though you can use Supabase for RAG, this was
kept unlike Postgres since it's faster than Supabase so sometimes is the better option.

✅ [**SearXNG**](https://searxng.org/) - Open-source, free internet metasearch engine which aggregates 
results from up to 229 search services. Users are neither tracked nor profiled, hence the fit with the local AI package.

✅ [**Traefik**](https://traefik.io/) - Managed HTTPS/TLS for custom domains with integrated dashboard

## Prerequisites

Before you begin, make sure you have the following software installed:

- [Python](https://www.python.org/downloads/) - Required to run the setup script
- [Git/GitHub Desktop](https://desktop.github.com/) - For easy repository management
- [Docker/Docker Desktop](https://www.docker.com/products/docker-desktop/) - Required to run all services

## Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/coleam00/local-ai-packaged.git
cd local-ai-packaged
```

Before running the services, you need to set up your environment variables for Supabase following their [self-hosting guide](https://supabase.com/docs/guides/self-hosting/docker#securing-your-services).

1. Make a copy of `.env.example` and rename it to `.env` in the root directory of the project
2. Set the following required environment variables:
   ```bash
   ############
   # N8N Configuration
   ############
   N8N_ENCRYPTION_KEY=
   N8N_USER_MANAGEMENT_JWT_SECRET=

   ############
   # Supabase Secrets
   ############
   POSTGRES_PASSWORD=
   JWT_SECRET=
   ANON_KEY=
   SERVICE_ROLE_KEY=
   DASHBOARD_USERNAME=
   DASHBOARD_PASSWORD=
   POOLER_TENANT_ID=
   ```

> [!IMPORTANT]
> Make sure to generate secure random values for all secrets. Never use the example values in production.

3. Set the following environment variables if deploying to production, otherwise leave commented:
   ```bash
   ############
   # Traefik Config
   ############

   N8N_HOSTNAME=n8n.yourdomain.com
   WEBUI_HOSTNAME=:openwebui.yourdomain.com
   FLOWISE_HOSTNAME=:flowise.yourdomain.com
   SUPABASE_HOSTNAME=:supabase.yourdomain.com
   OLLAMA_HOSTNAME=:ollama.yourdomain.com
   SEARXNG_HOSTNAME=searxng.yourdomain.com
   TRAEFIK_DASHBOARD_HOSTNAME=traefik.yourdomain.com
   LETSENCRYPT_EMAIL=your-email-address
   ```   

---

The project includes a `start_services.py` script that handles starting both the Supabase and local AI services. The script accepts a `--profile` flag to specify which GPU configuration to use.

### For Nvidia GPU users

```bash
python start_services.py --profile gpu-nvidia
```

> [!NOTE]
> If you have not used your Nvidia GPU with Docker before, please follow the
> [Ollama Docker instructions](https://github.com/ollama/ollama/blob/main/docs/docker.md).

### For AMD GPU users on Linux

```bash
python start_services.py --profile gpu-amd
```

### For Mac / Apple Silicon users

If you're using a Mac with an M1 or newer processor, you can't expose your GPU to the Docker instance, unfortunately. There are two options in this case:

1. Run the starter kit fully on CPU:
   ```bash
   python start_services.py --profile cpu
   ```

2. Run Ollama on your Mac for faster inference, and connect to that from the n8n instance:
   ```bash
   python start_services.py --profile none
   ```

   If you want to run Ollama on your mac, check the [Ollama homepage](https://ollama.com/) for installation instructions.

#### For Mac users running OLLAMA locally

If you're running OLLAMA locally on your Mac (not in Docker), you need to modify the OLLAMA_HOST environment variable in the n8n service configuration. Update the x-n8n section in your Docker Compose file as follows:

```yaml
x-n8n: &service-n8n
  # ... other configurations ...
  environment:
    # ... other environment variables ...
    - OLLAMA_HOST=host.docker.internal:11434
```

Additionally, after you see "Editor is now accessible via: http://localhost:5678/":

1. Head to http://localhost:5678/home/credentials
2. Click on "Local Ollama service"
3. Change the base URL to "http://host.docker.internal:11434/"

### For everyone else

```bash
python start_services.py --profile cpu
```

## Deploying to the Cloud

### Prerequisites for the below steps

- Linux machine (preferably Unbuntu) with Nano, Git, and Docker installed

### Extra steps

Before running the above commands to pull the repo and install everything:

1. Run the commands as root to open up the necessary ports:
   - ufw enable
   - ufw allow 8000 && ufw allow 3001 && ufw allow 3000 && ufw allow 5678 && ufw allow 80 && ufw allow 443
   - ufw allow 8080 (if you want to expose SearXNG and the Traefik dashboard)
   - ufw allow 11434 (if you want to expose Ollama)
   - ufw reload

2. Set up A records for your DNS provider to point your subdomains you'll set up in the .env file for Traefik
to the IP address of your cloud instance.

   For example, A record to point n8n to [cloud instance IP] for n8n.yourdomain.com

## ⚡️ Quick start and usage

The main component of the self-hosted AI starter kit is a docker compose file
pre-configured with network and disk so there isn't much else you need to
install. After completing the installation steps above, follow the steps below
to get started.

1. Open <http://localhost:5678/> in your browser to set up n8n. You'll only
   have to do this once. You are NOT creating an account with n8n in the setup here,
   it is only a local account for your instance!
2. Open the included workflow:
   <http://localhost:5678/workflow/vTN9y2dLXqTiDfPT>
3. Create credentials for every service:
   
   Ollama URL: http://ollama:11434

   Postgres (through Supabase): use DB, username, and password from .env. IMPORTANT: Host is 'db'
   Since that is the name of the service running Supabase

   Qdrant URL: http://qdrant:6333 (API key can be whatever since this is running locally)

   Google Drive: Follow [this guide from n8n](https://docs.n8n.io/integrations/builtin/credentials/google/).
   Don't use localhost for the redirect URI, just use another domain you have, it will still work!
   Alternatively, you can set up [local file triggers](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.localfiletrigger/).
4. Select **Test workflow** to start running the workflow.
5. If this is the first time you're running the workflow, you may need to wait
   until Ollama finishes downloading Llama3.1. You can inspect the docker
   console logs to check on the progress.
6. Make sure to toggle the workflow as active and copy the "Production" webhook URL!
7. Open <http://localhost:3000/> in your browser to set up Open WebUI.
You'll only have to do this once. You are NOT creating an account with Open WebUI in the 
setup here, it is only a local account for your instance!
8. Go to Workspace -> Functions -> Add Function -> Give name + description then paste in
the code from `n8n_pipe.py`

   The function is also [published here on Open WebUI's site](https://openwebui.com/f/coleam/n8n_pipe/).

9. Click on the gear icon and set the n8n_url to the production URL for the webhook
you copied in a previous step.
10. Toggle the function on and now it will be available in your model dropdown in the top left! 

To open n8n at any time, visit <http://localhost:5678/> in your browser.
To open Open WebUI at any time, visit <http://localhost:3000/>.

With your n8n instance, you'll have access to over 400 integrations and a
suite of basic and advanced AI nodes such as
[AI Agent](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/),
[Text classifier](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.text-classifier/),
and [Information Extractor](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.information-extractor/)
nodes. To keep everything local, just remember to use the Ollama node for your
language model and Qdrant as your vector store.

> [!NOTE]
> This starter kit is designed to help you get started with self-hosted AI
> workflows. While it's not fully optimized for production environments, it
> combines robust components that work well together for proof-of-concept
> projects. You can customize it to meet your specific needs

## Upgrading

To update all containers to their latest versions (n8n, Open WebUI, etc.), run these commands:

```bash
# Stop all services
docker compose -p localai -f docker-compose.yml -f supabase/docker/docker-compose.yml down

# Pull latest versions of all containers
docker compose -p localai -f docker-compose.yml -f supabase/docker/docker-compose.yml pull

# Start services again with your desired profile
python start_services.py --profile <your-profile>
```

Replace `<your-profile>` with one of: `cpu`, `gpu-nvidia`, `gpu-amd`, or `none`.

Note: The `start_services.py` script itself does not update containers - it only restarts them or pulls them if you are downloading these containers for the first time. To get the latest versions, you must explicitly run the commands above.

## Troubleshooting

Here are solutions to common issues you might encounter:

### Supabase Issues

- **Supabase Pooler Restarting**: If the supabase-pooler container keeps restarting itself, follow the instructions in [this GitHub issue](https://github.com/supabase/supabase/issues/30210#issuecomment-2456955578).

- **Supabase Analytics Startup Failure**: If the supabase-analytics container fails to start after changing your Postgres password, delete the folder `supabase/docker/volumes/db/data`.

- **If using Docker Desktop**: Go into the Docker settings and make sure "Expose daemon on tcp://localhost:2375 without TLS" is turned on

- **Supabase Service Unavailable** - Make sure you don't have an "@" character in your Postgres password! If the connection to the kong container is working (the container logs say it is receiving requests from n8n) but n8n says it cannot connect, this is generally the problem from what the community has shared. Other characters might not be allowed too, the @ symbol is just the one I know for sure!

### GPU Support Issues

- **Windows GPU Support**: If you're having trouble running Ollama with GPU support on Windows with Docker Desktop:
  1. Open Docker Desktop settings
  2. Enable WSL 2 backend
  3. See the [Docker GPU documentation](https://docs.docker.com/desktop/features/gpu/) for more details

- **Linux GPU Support**: If you're having trouble running Ollama with GPU support on Linux, follow the [Ollama Docker instructions](https://github.com/ollama/ollama/blob/main/docs/docker.md).

## 👓 Recommended reading

n8n is full of useful content for getting started quickly with its AI concepts
and nodes. If you run into an issue, go to [support](#support).

- [AI agents for developers: from theory to practice with n8n](https://blog.n8n.io/ai-agents/)
- [Tutorial: Build an AI workflow in n8n](https://docs.n8n.io/advanced-ai/intro-tutorial/)
- [Langchain Concepts in n8n](https://docs.n8n.io/advanced-ai/langchain/langchain-n8n/)
- [Demonstration of key differences between agents and chains](https://docs.n8n.io/advanced-ai/examples/agent-chain-comparison/)
- [What are vector databases?](https://docs.n8n.io/advanced-ai/examples/understand-vector-databases/)

## 🎥 Video walkthrough

- [Cole's Guide to the Local AI Starter Kit](https://youtu.be/pOsO40HSbOo)

## 🛍️ More AI templates

For more AI workflow ideas, visit the [**official n8n AI template
gallery**](https://n8n.io/workflows/?categories=AI). From each workflow,
select the **Use workflow** button to automatically import the workflow into
your local n8n instance.

### Learn AI key concepts

- [AI Agent Chat](https://n8n.io/workflows/1954-ai-agent-chat/)
- [AI chat with any data source (using the n8n workflow too)](https://n8n.io/workflows/2026-ai-chat-with-any-data-source-using-the-n8n-workflow-tool/)
- [Chat with OpenAI Assistant (by adding a memory)](https://n8n.io/workflows/2098-chat-with-openai-assistant-by-adding-a-memory/)
- [Use an open-source LLM (via HuggingFace)](https://n8n.io/workflows/1980-use-an-open-source-llm-via-huggingface/)
- [Chat with PDF docs using AI (quoting sources)](https://n8n.io/workflows/2165-chat-with-pdf-docs-using-ai-quoting-sources/)
- [AI agent that can scrape webpages](https://n8n.io/workflows/2006-ai-agent-that-can-scrape-webpages/)

### Local AI templates

- [Tax Code Assistant](https://n8n.io/workflows/2341-build-a-tax-code-assistant-with-qdrant-mistralai-and-openai/)
- [Breakdown Documents into Study Notes with MistralAI and Qdrant](https://n8n.io/workflows/2339-breakdown-documents-into-study-notes-using-templating-mistralai-and-qdrant/)
- [Financial Documents Assistant using Qdrant and](https://n8n.io/workflows/2335-build-a-financial-documents-assistant-using-qdrant-and-mistralai/) [Mistral.ai](http://mistral.ai/)
- [Recipe Recommendations with Qdrant and Mistral](https://n8n.io/workflows/2333-recipe-recommendations-with-qdrant-and-mistral/)

## Tips & tricks

### Accessing local files

The self-hosted AI starter kit will create a shared folder (by default,
located in the same directory) which is mounted to the n8n container and
allows n8n to access files on disk. This folder within the n8n container is
located at `/data/shared` -- this is the path you'll need to use in nodes that
interact with the local filesystem.

**Nodes that interact with the local filesystem**

- [Read/Write Files from Disk](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.filesreadwrite/)
- [Local File Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.localfiletrigger/)
- [Execute Command](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executecommand/)

## 📜 License

This project (originally created by the n8n team, link at the top of the README) is licensed under the Apache License 2.0 - see the
[LICENSE](LICENSE) file for details.

# Local AI Package avec Traefik

Ce projet configure un environnement local d'IA comprenant plusieurs services, dont Supabase, Ollama, n8n, et d'autres, tous orchestrés avec Docker Compose et Traefik comme reverse proxy.

## Prérequis

- Docker et Docker Compose
- Python 3.6+
- Git

## Configuration initiale

1. Clonez ce dépôt :
   ```bash
   git clone <URL_DU_REPO>
   cd local-ai-packaged
   ```

2. Créez un fichier `.env` à partir du modèle `.env.example` :
   ```bash
   cp .env.example .env
   ```
   Modifiez les valeurs dans le fichier `.env` selon vos besoins.

3. Nettoyez les anciennes installations de Caddy (si vous avez migré depuis Caddy) :
   ```bash
   python clean_caddy.py
   ```

## Démarrage des services

Utilisez le script `start_services.py` pour démarrer tous les services :

### Pour CPU uniquement :
```bash
python start_services.py --profile cpu
```

### Pour GPU NVIDIA :
```bash
python start_services.py --profile gpu-nvidia
```

### Pour GPU AMD :
```bash
python start_services.py --profile gpu-amd
```

Le script effectue les opérations suivantes :
1. Crée le fichier `docker-compose.override.yml` pour Supabase avec les configurations Traefik
2. Clone ou met à jour le dépôt Supabase
3. Prépare l'environnement Supabase
4. Génère une clé secrète pour SearXNG
5. Arrête les conteneurs existants
6. Démarre Supabase
7. Attend l'initialisation de Supabase
8. Démarre les services d'IA locaux

## Accès aux services

Une fois les services démarrés, vous pouvez y accéder via les URLs suivantes :

- n8n : https://localhost ou https://${N8N_HOSTNAME}
- Open WebUI : https://localhost:3000 ou https://${WEBUI_HOSTNAME}
- Flowise : https://localhost:3001 ou https://${FLOWISE_HOSTNAME}
- Ollama : https://localhost:11434 ou https://${OLLAMA_HOSTNAME}
- Supabase : https://localhost:8000 ou https://${SUPABASE_HOSTNAME}
- SearXNG : https://localhost:8080 ou https://${SEARXNG_HOSTNAME}
- Tableau de bord Traefik : https://localhost:8080 ou https://${TRAEFIK_DASHBOARD_HOSTNAME}

## Résolution des problèmes

### Problèmes de mise à jour du dépôt Supabase

Si vous rencontrez des erreurs lors de la mise à jour du dépôt Supabase en raison de modifications locales, le script tentera automatiquement de sauvegarder vos modifications, de mettre à jour le dépôt, puis de réappliquer vos modifications.

### Problèmes avec Docker

Si Docker ne fonctionne pas correctement, assurez-vous que :
1. Le service Docker est en cours d'exécution
2. Vous avez les permissions nécessaires pour exécuter Docker
3. Votre installation Docker est à jour

### Problèmes avec Traefik

Si Traefik ne fonctionne pas correctement :
1. Vérifiez les logs de Traefik : `docker logs traefik`
2. Assurez-vous que les ports 80 et 443 ne sont pas utilisés par d'autres services
3. Vérifiez que les variables d'environnement dans le fichier `.env` sont correctement configurées

## Personnalisation

### Modification des configurations Traefik

Les configurations Traefik se trouvent dans :
- `traefik.yml` : Configuration principale
- `traefik/dynamic/services.yml` : Configuration des services et middlewares

### Ajout de nouveaux services

Pour ajouter un nouveau service avec Traefik :
1. Ajoutez le service dans `docker-compose.yml`
2. Ajoutez les labels Traefik appropriés
3. Mettez à jour `traefik/dynamic/services.yml` si nécessaire

## Sécurité

Pour la production, assurez-vous de :
1. Modifier toutes les valeurs par défaut dans le fichier `.env`
2. Activer HTTPS avec des certificats valides
3. Configurer des mots de passe forts pour tous les services
4. Limiter l'accès réseau aux services sensibles
