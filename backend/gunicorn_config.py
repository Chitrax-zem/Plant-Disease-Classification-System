"""Gunicorn configuration for production deployment"""
import os
import multiprocessing

# Server socket - use PORT environment variable
bind = f"0.0.0.0:{os.getenv('PORT', '5001')}"

# Worker processes - limited for free tier
workers = int(os.getenv('WEB_CONCURRENCY', 1))
threads = 2

# Timeout - higher for ML inference
timeout = 120
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Process naming
proc_name = "plant-disease-api"

# Max requests before restart (helps with memory leaks)
max_requests = 500
max_requests_jitter = 25