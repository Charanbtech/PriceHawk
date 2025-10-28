# backend/core/utils.py
import logging

def setup_logging(app=None):
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)
    if app:
        app.logger = logging.getLogger("pricehawk")
    return logging.getLogger("pricehawk")
