# ADK Agent Deployment Samples

This repository contains sample agents and scripts for deploying them using the Agent Development Kit (ADK).

> 📺 You can watch the accompanying [YouTube Video](https://www.youtube.com/watch?v=NEhWsMUz3ro).

## Related Resources

### ADK Crash Course (including Agent2Agent A2A and MCP integration)

For a comprehensive **crash course** on Google ADK covering Agent2Agent (A2A) Protocol and Model Context Protocol (MCP), check out the 1.5-hour tutorial that goes into much more detail about setting up ADK agents.

> 🎓 Watch the **FREE crash course:** [YouTube Video](https://www.youtube.com/watch?v=s6-Ofu-uu2k)

### ADK Builder Pack

I have compiled a complete toolkit for building production-ready ADK agents, including:

- ✅ Full source code for agent development using ADK, Agent2Agent and MCP
- ✅ Complete documentation, lesson plans and cheat sheets for working with the ADK.
- ✅ Handy scripts for deploying ADK agents (**relevant to this repository!**)
- ✅ Included `.cursor/rules` for use with AI code editors
- ✅ Comprehensive pytest test suite

> 🚀 **Get it now:** [ADK Builder Pack](https://gum.co/u/h9uqww5i1)

## ☕ Support Me

If you find this tutorial series and codebase helpful in your AI agent development journey, consider buying me a coffee! Your support helps me create more educational content on AI and agent development.

<a href="https://buymeacoffee.com/aioriented" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" >
</a>

## Prerequisites

1.  **Google Cloud SDK (`gcloud`)**: Ensure you have `gcloud` installed and authenticated. You can find instructions [here](https://cloud.google.com/sdk/docs/install).
2.  **Project Root `Dockerfile.template`**: A `Dockerfile.template` file must exist in the root of this project. This template is used to generate a specific `Dockerfile` for the agent. It should look something like this:

    ```Dockerfile
    # Use the official ADK base image
    FROM us-docker.pkg.dev/agent-development-kit/adk-images/adk-agent-base:latest

    # Copy the agent-specific code and dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # The __AGENT_DIR__ placeholder will be replaced by the script
    COPY agents/__AGENT_DIR__ /app/agents/__AGENT_DIR__

    # Set the agent directory environment variable for the ADK
    ENV AGENT_DIR=__AGENT_DIR__

    # Run the agent
    CMD ["adk", "run"]
    ```

## Step 1: Set Up Your Environment

First, you need to set the necessary environment variables for your Google Cloud project.

```bash
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="your-gcp-region" # e.g., us-central1
```

Replace `"your-gcp-project-id"` and `"your-gcp-region"` with your actual Google Cloud project ID and desired region.

## Step 2: Create a Staging Directory

To ensure a clean build, we'll create a temporary directory that will contain only the files needed for our agent.

```bash
mkdir temp_staging
cd temp_staging
```

## Step 3: Prepare the Source Code

Copy the agent code and the general requirements into the staging directory.

```bash
# Create the directory structure gcloud expects
mkdir agents

# Copy the agent code
cp -r ../multitool_agent ./agents/

# Copy the project's requirements
cp ../requirements.txt .

# Ensure Python treats the 'agents' directory as a package
touch agents/__init__.py
```

## Step 4: Create the Dockerfile

The `gcloud run deploy --source` command looks for a `Dockerfile` in the directory you point it to. We need to create one from our `Dockerfile.template`.

You will need to manually create the `Dockerfile` from `Dockerfile.template`. Open `../Dockerfile.template`, replace the `__AGENT_DIR__` placeholder with `multitool_agent`, and save the new file as `Dockerfile` inside the `temp_staging` directory.

Your `temp_staging` directory should now look like this:

```
temp_staging/
├── Dockerfile
├── agents/
│   ├── __init__.py
│   └── multitool_agent/
│       ├── __init__.py
│       └── agent.py
└── requirements.txt
```

## Step 5: Deploy to Cloud Run

Now, from the root of the project (not inside `temp_staging`), run the deployment command. We'll name our service `multitool-agent-service`.

```bash
# Make sure you are in the project's root directory
cd ..

# Deploy!
gcloud run deploy multitool-agent-service \
  --source temp_staging \
  --region "$GOOGLE_CLOUD_LOCATION" \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --memory=1Gi \
  --allow-unauthenticated
```

Google Cloud Build will now use the contents of the `temp_staging` directory to build a container image and deploy it to Cloud Run.

## Step 6: Clean Up

Once the deployment is successful, you can remove the temporary staging directory.

```bash
rm -rf temp_staging
```

### A Note on Interactive Prompts

When you run a deployment, `gcloud` may prompt you to allow unauthenticated invocations. To run these scripts in a non-interactive way (e.g., in a CI/CD pipeline), you can set the default behavior for your project:

```bash
gcloud run services update-iam-policy-binding [SERVICE_NAME] \
    --region=[REGION] \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --project=[PROJECT_ID]
```

Replace `[SERVICE_NAME]`, `[REGION]`, and `[PROJECT_ID]` with your specific service name, region, and project ID. This command grants public access to the service, which is a common requirement for public-facing web services or APIs.
