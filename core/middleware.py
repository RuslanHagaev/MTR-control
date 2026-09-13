from threading import local


_user_storage = local()


def get_current_user():
    return getattr(
        _user_storage,
        "user",
        None,
    )


class CurrentUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        _user_storage.user = (
            request.user
            if request.user.is_authenticated
            else None
        )

        try:
            response = self.get_response(request)
        finally:
            _user_storage.user = None

        return response