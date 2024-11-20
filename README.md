# LangChain Tracing Example

This repo contains an example of tracing in a LLM chatbot/agent app using OpenTelemetry and Langfuse.

## Setup

Create a `.env` file in the root of the project with the following content:

```shell
AZURE_OPENAI_API_KEY=XXXXXXXXXXXXXX
AZURE_OPENAI_API_BASE=https://XXXXXXXXXXXXXXX/
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
TAVILY_API_KEY=XXXXXXXXXXXXXX
LANGFUSE_SECRET_KEY="sk-lf-XXXXXXXXXXXX"
LANGFUSE_PUBLIC_KEY="pk-lf-XXXXXXXXXXXX"
LANGFUSE_HOST="http://localhost:3000"
```