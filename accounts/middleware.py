from django.utils.timezone import now


class LastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Safe check for user attribute
        if hasattr(request, "user") and request.user.is_authenticated:
            try:
                request.user.updated_at = now()
                request.user.save(update_fields=["updated_at"])
            except Exception as e:
                # Log the error but don't break the request
                print(f"Error updating user last seen: {e}")

        response = self.get_response(request)
        return response
