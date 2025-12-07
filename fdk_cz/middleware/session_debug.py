# fdk_cz/middleware/session_debug.py

import logging

logger = logging.getLogger(__name__)


class SessionDebugMiddleware:
    """
    Middleware for debugging session persistence issues.
    Logs session state at the beginning and end of each request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log session state BEFORE processing request
        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.info(f"[SESSION DEBUG - REQUEST START]")
            logger.info(f"  Path: {request.path}")
            logger.info(f"  Method: {request.method}")
            logger.info(f"  User: {request.user.username}")
            logger.info(f"  Session Key: {request.session.session_key}")
            logger.info(f"  Session Data: {dict(request.session.items())}")
            logger.info(f"  Session Modified: {request.session.modified}")
            logger.info(f"  Session Accessed: {request.session.accessed}")

        # Process the request
        response = self.get_response(request)

        # Log session state AFTER processing request
        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.info(f"[SESSION DEBUG - REQUEST END]")
            logger.info(f"  Path: {request.path}")
            logger.info(f"  User: {request.user.username}")
            logger.info(f"  Session Key: {request.session.session_key}")
            logger.info(f"  Session Data: {dict(request.session.items())}")
            logger.info(f"  Session Modified: {request.session.modified}")
            logger.info(f"  Session Accessed: {request.session.accessed}")

            # Check if session cookie is being set
            if hasattr(response, 'cookies'):
                session_cookie = response.cookies.get('sessionid')
                if session_cookie:
                    logger.info(f"  Session Cookie: {session_cookie.value}")
                else:
                    logger.warning(f"  ⚠️ No session cookie in response!")

        return response
