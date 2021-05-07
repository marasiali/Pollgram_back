from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers


class RegisterSerializer(DefaultRegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])

class LoginSerializer(DefaultLoginSerializer):
    username = None
    
    def __init__(self, *args, **kwargs):
        super(DefaultLoginSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].required = True