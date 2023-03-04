"""
Обработка исключений через middleware.

Данные о запросе и само исключение (включая трассировку)
передаются логеру для дальнейшей обработки в соответствии с его настройками.

Обработка выполняется только если в настройках приложения (website/settings.py)
выключен режим отладки DEBUG = False.

"""

import logging

from django.shortcuts import render

from .settings import DEBUG

logger = logging.getLogger(__name__)


class MiddlewareAllException:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.debug(f">>>>  Выполнен '__init__' класса MiddlewareAllException.")

    def __call__(self, request):
        logger.debug(f">>>>  Выполнен код класса MiddlewareAllException ДО обработки VIEW.")
        response = self.get_response(request)
        logger.debug(f">>>>  Выполнен код класса MiddlewareAllException ПОСЛЕ обработки VIEW.")
        return response

    @staticmethod
    def process_exception(request, exception):

        if DEBUG:
            return None

        # выбираем информацию из request для включения в лог
        request_info_to_logger = {
            'request': request,
            'path': request.path,
            'method': request.method,
            'user': request.user.username if request.user.is_authenticated else 'not_authenticated',
            'user_id': request.user.id if request.user.is_authenticated else 'not_authenticated',
            'META.CONTENT_LENGTH': request.META.get('CONTENT_LENGTH', ''),
            'META.CONTENT_TYPE': request.META.get('CONTENT_TYPE', ''),
            'META.QUERY_STRING': request.META.get('QUERY_STRING', ''),
            'META.HTTP_ACCEPT': request.META.get('HTTP_ACCEPT', ''),
            'META.REMOTE_HOST': request.META.get('REMOTE_HOST', ''),

            # If the server uses nginx as a reverse proxy or load balancing, the value returned is 127.0.0.1,
            # which can be obtained using HTTP_X_FORWARDED_FOR:
            'META.REMOTE_ADDR': request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META
            else request.META.get('REMOTE_ADDR', ''),
        }

        # дополняем информацию из методов request для включения в лог
        methods = {
            "GET": 'request.GET',
            "POST": 'request.POST',

            "PUT": 'request.PUT',
            "PATCH": 'request.PATCH',
            "DELETE": 'request.DELETE'
        }

        if request.method in methods.keys():
            try:
                for key in eval(methods[request.method]).keys():
                    if not key == 'csrfmiddlewaretoken':
                        request_info_to_logger[methods[request.method] + "." + key] = eval(methods[request.method])[key]
            except (KeyError, AttributeError):
                pass

        # exc_info - полное сообщение об исключении с трассировкой
        logger.error(str(request_info_to_logger) + '\n' + str(exception), exc_info=True)

        return render(request, 'blog/exception_page.html')
