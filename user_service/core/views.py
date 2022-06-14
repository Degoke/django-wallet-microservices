from urllib import response
from core.models import User
from rest_framework import viewsets, status, generics
from core.serializers import (
    UserSerializer,
    LoginSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework_simplejwt.tokens import RefreshToken

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']

            user = User.objects.create_user(email, password, first_name, last_name)
            details = UserSerializer(user).data
            response_data = {"details": details}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            data = {"details": serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                details = {
                    "refresh": str(refresh),
                    "access": str(access),
                    "user": UserSerializer(user).data
                }

                data = {"details": details}

                return Response(data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                data = {"details": f"User with email {email} does not exist"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {"details": serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class GetUsersView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)
