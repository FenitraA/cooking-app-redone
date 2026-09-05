from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import AppUser

class MyTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["username"] = user.username

        return token

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class AppUserSerializer(serializers.ModelSerializer):
    household_name = serializers.CharField(
        source="household.name",
        read_only=True,
    )

    class Meta:
        model = AppUser
        exclude = (
            "password",
            "groups",
            "user_permissions",
        )