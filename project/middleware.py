"""
Middleware to update custom business metrics on each request
"""
import logging
from project.custom_metrics import update_business_metrics

logger = logging.getLogger(__name__)


class BusinessMetricsMiddleware:
    """
    Updates custom business metrics (users, orders, etc.) periodically
    Updates every request (can be optimized to update every N requests)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.update_interval = 50  # Update metrics every N requests
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Update metrics periodically (every N requests)
        self.request_count += 1
        if self.request_count % self.update_interval == 0:
            try:
                update_business_metrics()
                logger.debug("Business metrics updated")
            except Exception as e:
                logger.error(f"Failed to update business metrics: {e}")
        
        return response
