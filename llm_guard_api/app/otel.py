from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from .config import MetricsConfig, TracingConfig
from .version import __version__


def _configure_tracing(tracing_config: TracingConfig, resource: Resource) -> None:
    trace.set_tracer_provider(TracerProvider(resource=resource))

    if tracing_config is None:
        return

    if tracing_config.exporter == "otel_http":
        exporter = OTLPSpanExporter(endpoint=tracing_config.endpoint)
    elif tracing_config.exporter == "console":
        exporter = ConsoleSpanExporter()

    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))


def _configure_metrics(metrics_config: MetricsConfig, resource: Resource) -> None:
    if metrics_config is None:
        return

    if metrics_config.exporter == "console":
        reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
    elif metrics_config.exporter == "otel_http":
        reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=metrics_config.endpoint))
    elif metrics_config.exporter == "prometheus":
        reader = PrometheusMetricReader()

    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)


def instrument_app(
    app: FastAPI, app_name: str, tracing_config: TracingConfig, metrics_config: MetricsConfig
) -> None:
    resource = Resource(
        attributes={
            SERVICE_NAME: app_name,
            SERVICE_VERSION: __version__,
        }
    )

    _configure_tracing(tracing_config, resource)
    _configure_metrics(metrics_config, resource)

    FastAPIInstrumentor.instrument_app(
        app,
        excluded_urls="healtz,readyz,metrics",
        meter_provider=metrics.get_meter_provider(),
        tracer_provider=trace.get_tracer_provider(),
    )
