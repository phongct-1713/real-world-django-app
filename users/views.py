from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)

class RegistrationAPIView(APIView):
    """
    Allow any user to register a new account.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user_data = request.data.get('user', {})

        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    Allow any user to login.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user_data = request.data.get('user', {})

        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)

        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(APIView):
    """
    Get and update current user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request):
        user_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user,
            data=user_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
