from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI
from opentelemetry import trace
from .observability.tracing import setup_tracing, instrument_app
from .llms.chat.route import router as chat_router
from .llms.agent.route import router as agent_router
import os

service_name = os.environ["APP_NAME"]
otlp_span_exporter_endpoint = os.environ["OTLP_SPAN_EXPORTER_ENDPOINT"]
tracer_provider = setup_tracing(service_name, otlp_span_exporter_endpoint)

app = FastAPI()
instrument_app(app, tracer_provider)

# Get tracer for this module
tracer = trace.get_tracer(__name__)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(agent_router, prefix="/agent", tags=["Agent"])


@app.get("/")
async def index():
    return {"message": "Hello, World!"}
