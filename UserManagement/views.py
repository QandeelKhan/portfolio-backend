from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate, logout
from django.shortcuts import redirect
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView, status, View
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from UserManagement.renderers import UserRenderer
from UserManagement.serializers import (
    SendPasswordResetEmailSerializer,
    UserChangePasswordSerializer,
    UserLoginSerializer,
    UserPasswordResetSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    GoogleLoginSerializer,
)
import datetime


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    # Get the access token from the refresh token
    access = refresh.access_token
    # Get the lifetime of the access token in seconds
    lifetime = access.lifetime.total_seconds()
    # Get the current time in seconds
    now = datetime.datetime.now().timestamp()
    # Add the lifetime and the current time to get the accessExpires value in seconds
    accessExpires = now + lifetime
    # Convert the value to a string
    # Create a datetime object from the number of seconds since the epoch
    accessExpires = datetime.datetime.fromtimestamp(accessExpires)
    # Convert the datetime object to a string in ISO 8601 format
    accessExpires = accessExpires.isoformat()
    accessExpires = str(accessExpires)
    # Return the token object with the accessExpires property
    return {
        'refresh': str(refresh),
        'access': str(access),
        'accessExpires': accessExpires
    }


# -------------------converted to the viewsets for the purpose of routing and consistency--------
# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     renderer_classes = [UserRenderer]

#     def perform_create(self, serializer):
#         user = serializer.save()
#         token = get_token_for_user(user)
#         self.headers.update({'Authorization': f"Bearer {token['access']}"})


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        # Do not raise an exception
        if serializer.is_valid(raise_exception=False):
            # If the data is valid, save the user and return a success response
            user = serializer.save()
            token = get_token_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        else:
            # If the data is invalid, return an error response with the serializer errors
            errors = serializer.errors
            return Response({'errors': errors, 'msg': 'Registration Failed'}, status=status.HTTP_400_BAD_REQUEST)
            # serializer can return 2 objects. 1 serializer.data gives us data, 2 serializer.errors gives us "errors" from serializer if happened so we can access and manage error styles in frontend as well if we want

# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     renderer_classes = [UserRenderer, JSONRenderer]
#     parser_classes = [JSONParser]

#     def perform_create(self, serializer):
#         user = serializer.save()
#         token = get_token_for_user(user)
#         self.headers.update({'Authorization': f"Bearer {token['access']}"})
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    # renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_token_for_user(user)
            self.headers.update({'Authorization': f"Bearer {token['access']}"})
            return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {"non_field_errors": ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)


# not in use------
# class GoogleLoginAPIView(APIView):
#     permission_classes = []

#     def post(self, request):
#         serializer = GoogleLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.validated_data
#             return Response({"token": user.auth_token.key})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# not in use------


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def get_object(self):
        return self.request.user


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password link sent Successfully. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully.'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

# not in use----
# class CommentCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         serializer = CommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         comment = serializer.save(author=request.user)
#         return Response(CommentSerializer(comment).data, status=201)

# -------------------converted to the viewsets for the purpose of routing and consistency--------
# --------using view sets


# class UserRegistrationViewSet(viewsets.GenericViewSet):
#     serializer_class = UserRegistrationSerializer
#     renderer_classes = [UserRenderer]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token = get_token_for_user(user)
#         return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


# class UserLoginViewSet(viewsets.GenericViewSet):
#     serializer_class = UserLoginSerializer
#     # renderer_classes = [UserRenderer]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.data.get('email')
#         password = serializer.data.get('password')
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             token = get_token_for_user(user)
#             self.headers.update({'Authorization': f"Bearer {token['access']}"})
#             return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'errors': {"non_field_errors": ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)


# class UserProfileViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserProfileSerializer

#     def get_queryset(self):
#         return models.User.objects.filter(id=self.request.user.id)


# class UserChangePasswordViewSet(viewsets.GenericViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserChangePasswordSerializer

#     def get_object(self):
#         return self.request.user

#     def update(self, request, *args, **kwargs):
#         # your custom logic for changing user password
#         pass


# class SendPasswordResetEmailViewSet(viewsets.GenericViewSet):
#     renderer_classes = [UserRenderer]
#     serializer_class = SendPasswordResetEmailSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # your custom logic for sending password reset email
#         return Response({'msg': 'Password link sent Successfully. Please check your Email'}, status=status.HTTP_200_OK)


# class UserPasswordResetViewSet(viewsets.GenericViewSet):
#     renderer_classes = [UserRenderer]
#     serializer_class = UserPasswordResetSerializer

#     def create(self, request, uid, token, *args, **kwargs):
#         serializer = self.get_serializer(
#             data=request.data, context={'uid': uid, 'token': token})
#         serializer.is_valid(raise_exception=True)
#         # your custom logic for resetting user password
#         return Response({'msg': 'Password Reset Successfully.'}, status=status.HTTP_200_OK)


# class LogoutViewSet(viewsets.GenericViewSet):
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         logout(request)
#         return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


# # class CommentCreateViewSet(viewsets.ModelViewSet):
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = CommentSerializer

# #     def get_queryset(self):
# #         return models.Comment.objects.filter(author=self.request.user)

# #     def perform_create(self, serializer):
# #         serializer.save(author=self.request.user)
