from flask import Flask
import sys
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

app = Flask(__name__)
configure_azure_monitor()
tracer = trace.get_tracer(__name__)

@app.route('/')
def home():
    with tracer.start_as_current_span("home-request"):
        pass
    # Force immediate flush instead of waiting for batch timer
    from opentelemetry.sdk.trace import TracerProvider
    provider = trace.get_tracer_provider()
    if hasattr(provider, 'force_flush'):
        provider.force_flush()
    return "Hello! This app is being monitored by Azure Monitor and Application Insights."

if __name__ == '__main__':
    app.run()
