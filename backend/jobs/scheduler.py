# backend/jobs/scheduler.py
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .tasks import refresh_prices, clean_old_notifications, generate_price_forecasts

logger = logging.getLogger(__name__)
_scheduler = None

def init_scheduler(app):
    """
    Initialize and start the background scheduler for periodic tasks.
    
    Tasks:
    - refresh_prices: Check and update product prices (every 2 hours)
    - clean_old_notifications: Remove old notifications (daily at midnight)
    - generate_price_forecasts: Generate price forecasts (daily at 1 AM)
    """
    global _scheduler
    
    if _scheduler:
        logger.info("Scheduler already initialized")
        return _scheduler
    
    logger.info("Initializing background scheduler")
    
    _scheduler = BackgroundScheduler(
        job_defaults={
            'coalesce': True,  # Combine multiple waiting instances
            'max_instances': 1  # Only one instance of each job can run at a time
        }
    )
    
    # Price refresh job - every 2 hours
    _scheduler.add_job(
        lambda: refresh_prices(app),
        'interval',
        hours=2,
        id='refresh_prices',
        replace_existing=True,
        next_run_time=None  # Start on next interval
    )
    
    # Notification cleanup job - daily at midnight
    _scheduler.add_job(
        lambda: clean_old_notifications(app),
        CronTrigger(hour=0, minute=0),
        id='clean_old_notifications',
        replace_existing=True
    )
    
    # Forecast generation job - daily at 1 AM
    _scheduler.add_job(
        lambda: generate_price_forecasts(app),
        CronTrigger(hour=1, minute=0),
        id='generate_price_forecasts',
        replace_existing=True
    )
    
    # Start the scheduler
    _scheduler.start()
    logger.info("Background scheduler started")
    
    return _scheduler
