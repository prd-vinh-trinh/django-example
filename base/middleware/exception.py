import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(f"Exception caught in middleware: {exception}", exc_info=True)
        response_data = {
            "error": str(exception),
            "message": "An error occurred while processing your request. Please try again later."
        }
        return JsonResponse(response_data, status=500)
