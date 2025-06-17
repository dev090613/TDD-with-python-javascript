from accounts.models import Token, User

class PasswordlessAuthenticationBackend:
    def authenticate(self, request, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)

        except Token.DoesNotExist:
            return None

        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, email):
        try:
            user = User.objects.get(email=email)
            return user

        except User.DoesNotExist:
            return
