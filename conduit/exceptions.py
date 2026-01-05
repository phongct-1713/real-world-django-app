from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    """
    Custom exception handler for REST framework that formats errors consistently.
    """
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error,
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    """Handle generic errors."""
    if response is not None:
        response.data = {'errors': response.data}
    return response


def _handle_authentication_error(exc, context, response):
    """Handle authentication errors."""
    if response is not None:
        response.data = {
            'errors': {
                'detail': 'Authentication credentials were not provided.'
            }
        }
    return response
