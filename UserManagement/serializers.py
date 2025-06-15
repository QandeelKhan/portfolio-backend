# from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer


# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields = ['id', 'username', 'password',
#                   'email', 'first_name', 'last_name']


# class UserSerializer(BaseUserSerializer):
#     class Meta(BaseUserSerializer.Meta):
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']


from xml.dom import ValidationErr
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from UserManagement.models import User
from rest_framework.validators import ValidationError

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# to generate a token for password reset
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from UserManagement.utils import Util
from rest_framework.fields import BooleanField


class UserRegistrationSerializer(ModelSerializer):
    # we are writing this because we need confirm password field in our registration request
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    tc = BooleanField(
        error_messages={
            'required': 'You must accept the terms and conditions.',
            'invalid': 'You must enter a valid boolean value.'
        }
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # validating password and confirm password while validating, we get the data of views.py from fronted in attrs.so after getting that we can filter through attrs here,we can call it "data" as well rather then attrs.this validate method will call only when in views.py we mention the is_valid() method.
    def validate(self, attrs):
        # because password is a dict,so we can get and filter it as attrs.get()
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            # Raise a validation error with the field and type information
            raise serializers.ValidationError({
                'password': ['The passwords do not match.'],
                'type': 'mismatch'
            })
            # if there's an error it will raise exception otherwise return the attrs
        return attrs

        # because it's a custom user model so we need to overwrite the create method, will not require to overwrite if not a custom user model.
    def create(self, validate_data):
        # returning User in validated data using create_user method
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ['role']  # Add other fields if needed


class UserProfileSerializer(ModelSerializer):
    # role = RoleSerializer()  # Serialize the Role information

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'profile_image', 'tc',
                  'is_active', 'is_staff', 'created_at', 'updated_at']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password_confirm = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password_confirm']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password does not match')
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # uid = user.id # will give user id but we don't want to get id original,we want to save it in encoded form and latter on use that id through that encoded form
            # this urlsafe_base64_encode()   method can't integers,it takes bytes so if we put "user.id" in it it will not work. thats why we use "force_bytes" to convert our integer value to bytes and then encoding will work
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("encoded UID ", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password reset token ', token)
            # generating a link of uid and token and set it port on frontend port
            link = 'http://localhost:5173/api/user/reset/'+uid+'/'+token
            # --------only for testing on backend: 
            # get the link in terminal to get test on the backend side, and then pass the password + password_confirm json object in post req.
            backendTestingLink = 'http://localhost:8000/api/reset-password/'+uid+'/'+token
            print('password reset link for backend testing only', backendTestingLink)
            # --------only for testing on backend: 
            # send above generated link to the email of the user.settings in settings.py file.and create a file as utils.py for sending email function using django
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_mail(data)
            return attrs
        else:
            raise ValidationErr('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password_confirm = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password_confirm']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        uid = self.context.get('uid')
        token = self.context.get('token')

        # Initialize user variable
        user = None

        if password != password_confirm:
            raise serializers.ValidationError('Password does not match')

        try:
            # converting decoded uid to str
            id = smart_str(urlsafe_base64_decode(uid))
            # getting user from that id
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not valid or Expired')

            user.set_password(password)
            user.save()
            return attrs

        except User.DoesNotExist:
            raise ValidationError('No user found for the provided UID')

        except DjangoUnicodeDecodeError as identifier:
            raise ValidationError("Token is not Valid or Expired")


# from django.contrib.auth.models import User

class GoogleLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        # Extract access token and its expiry time
        access_token = str(refresh.access_token)
        
        # Get the current time with microseconds
        now_with_microseconds = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        
        # Calculate the new expiration time by adding the token's lifetime to the current time
        access_expires = now_with_microseconds + datetime.timedelta(seconds=refresh.access_token.lifetime.total_seconds())

        # Format the expiration time with microseconds
        access_expires_formatted = access_expires.strftime('%Y-%m-%dT%H:%M:%S.%f')

        # Include access token and its formatted expiry time in the response
        data['access'] = access_token
        data['accessExpires'] = access_expires_formatted

        return data