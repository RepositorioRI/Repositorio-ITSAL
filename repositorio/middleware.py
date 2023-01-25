from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from repositorio.views import paginaError

class Custom404Middleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return paginaError(request, exception)