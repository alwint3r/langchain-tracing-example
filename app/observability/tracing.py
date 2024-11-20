from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_tracing(service_name: str, otlp_endpoint: str):
    tracer_provider = TracerProvider(
        resource=Resource.create({"service.name": service_name}),
    )
    trace.set_tracer_provider(tracer_provider)

    jaeger_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
    )

    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

    return tracer_provider


def instrument_app(app, tracer_provider):
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
