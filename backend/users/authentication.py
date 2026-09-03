from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # First try the normal Authorization header
        header = self.get_header(request)

        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            # Otherwise look for the token in the cookie
            raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token