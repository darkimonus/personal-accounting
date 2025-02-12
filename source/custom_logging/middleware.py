import time
import psutil
import logging

from django.core.cache import cache
from django.conf import settings
from http import HTTPStatus

from custom_logging.config import (
    REQUEST_BODY,
    RESPONSE_BODY,
    INFO_BODY,
    RESPONSE_INFO_BODY,
)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            start_process = time.monotonic()
            ###
            response = self.get_response(request)
            ###
            finish_process = time.monotonic()

            sessionid = request.COOKIES.get("sessionid")
            time_process = finish_process - start_process
            time_delta = f"{time_process:.6f} sec"
            user = request.user
            csrftoken = request.COOKIES.get("csrftoken") or None
            try:
                method_name = (str(request.resolver_match._func_path).partition("views.")[2] or None)
            except AttributeError:
                method_name = None
            request_path = request.get_full_path()
            request_method = request.method
            referer = request.headers.get("Referer")
            query_string = request.META.get("QUERY_STRING")
            request_headers = request.headers
            user_ip = request.META.get("REMOTE_ADDR")

            try:
                request_body = request.body.decode('utf-8')
            except Exception as e:
                logger = logging.getLogger("error")
                logger.error(f"Unexpected error while processing request body: {e}")
                return response

            if len(request_body) == 0:
                request_body = "No Data"

            if len(query_string) == 0:
                query_string = None

            status_code = response.status_code
            response_headers = response.headers
            # Added try block so middleware handles responses without data
            try:
                response_data = response.data
            except Exception:
                response_data = None

            if status_code < HTTPStatus.BAD_REQUEST or status_code == HTTPStatus.NOT_FOUND:
                if settings.LOGGING_DEBUG == "True":
                    logger = logging.getLogger("debug")

                    request_info = INFO_BODY.format(
                        request_headers,
                        request,
                        referer,
                        query_string,
                        request_body,
                        user_ip
                    )
                    request_msg = REQUEST_BODY.format(
                        user,
                        sessionid,
                        csrftoken,
                        method_name,
                        request_path,
                        request_method,
                        status_code,
                        request_info,
                    )
                    logger.debug(msg=request_msg)

                    response_info = RESPONSE_INFO_BODY.format(
                        response_headers,
                        response,
                        referer,
                        query_string,
                        response_data,
                    )
                    response_msg = RESPONSE_BODY.format(
                        user,
                        sessionid,
                        csrftoken,
                        method_name,
                        request_method,
                        time_delta,
                        status_code,
                        response_info,
                    )
                    logger.debug(msg=response_msg)

                    return response

                if settings.LOGGING_INFO == "True":
                    logger = logging.getLogger("info")

                    request_info = INFO_BODY.format(
                        request_headers,
                        request,
                        referer,
                        query_string,
                        request_body,
                        user_ip
                    )
                    request_msg = REQUEST_BODY.format(
                        user,
                        sessionid,
                        csrftoken,
                        method_name,
                        request_path,
                        request_method,
                        status_code,
                        request_info,
                    )
                    logger.info(msg=request_msg)

                    response_info = RESPONSE_INFO_BODY.format(
                        response_headers,
                        response,
                        referer,
                        query_string,
                        "...",
                    )
                    response_msg = RESPONSE_BODY.format(
                        user,
                        sessionid,
                        csrftoken,
                        method_name,
                        request_method,
                        time_delta,
                        status_code,
                        response_info,
                    )
                    logger.info(msg=response_msg)
                    return response
                return response
            if settings.LOGGING_ERROR == "True" and status_code != HTTPStatus.NOT_FOUND:
                logger = logging.getLogger("error")
                request_info = INFO_BODY.format(
                    request_headers,
                    request,
                    referer,
                    query_string,
                    request_body,
                    user_ip
                )
                request_msg = REQUEST_BODY.format(
                    user,
                    sessionid,
                    csrftoken,
                    method_name,
                    request_path,
                    request_method,
                    status_code,
                    request_info,
                )
                logger.error(msg=request_msg)

                response_info = RESPONSE_INFO_BODY.format(
                    response_headers,
                    response,
                    referer,
                    query_string,
                    response_data,
                )
                response_msg = RESPONSE_BODY.format(
                    user,
                    sessionid,
                    csrftoken,
                    method_name,
                    request_method,
                    time_delta,
                    status_code,
                    response_info,
                )
                logger.error(msg=response_msg)

                return response
            return response
        except Exception as e:
            logger = logging.getLogger("error")
            logger.error(e)
            return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        request_data = request.body.decode("utf-8")
        user_ip = request.META.get("REMOTE_ADDR")
        cache.set(user_ip, request_data)
        return None

    @staticmethod
    def system_data():
        cpu = psutil.cpu_times()
        memory = psutil.virtual_memory()
        discs = psutil.disk_usage(f"{settings.BASE_DIR}")

        system_data = {"CPU": cpu, "MEMORY": memory, "DISCS": discs}
        return system_data
