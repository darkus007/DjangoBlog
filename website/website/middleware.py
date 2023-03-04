"""
Добавляем обработку исключений через middleware.

"""
import logging

from django.http import HttpResponse

logger = logging.getLogger(__name__)


class MiddlewareAllException:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        logger.debug(f">>>>  Выполнен '__init__' класса MiddlewareAllException.")

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        logger.debug(f">>>>  Выполнен код класса MiddlewareAllException ДО обработки VIEW.")

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        logger.debug(f">>>>  Выполнен код класса MiddlewareAllException ПОСЛЕ обработки VIEW.")

        return response

    @staticmethod
    def process_exception(request, exception):
        logger.error(exception, exc_info=True)   # exc_info - полное сообщение об исключении с трассировкой
        # return None
        return HttpResponse(f'<h3>Выполнена обработка исключения в Django Middleware: {exception}</h3>')
