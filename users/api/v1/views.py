from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from .serializers import UserRegistrationSerializer

User = get_user_model()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions: allow if user is staff/superuser
        if request.user and request.user.is_staff:
            return True
        # Otherwise only the user themselves may edit/delete their object
        return obj == request.user


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):
    """CRUD operations for users.

    - POST   /users/        -> create (registration)
    - GET    /users/        -> list users
    - GET    /users/{pk}/   -> retrieve
    - PUT    /users/{pk}/   -> update
    - PATCH  /users/{pk}/   -> partial_update
    - DELETE /users/{pk}/   -> destroy
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        # use serializer to create user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # create tokens
        refresh = RefreshToken.for_user(user)
        data = serializer.data
        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        return Response(data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        # Allow anyone to register
        if self.action == 'create':
            return [permissions.AllowAny()]
        # For list and retrieve, require authenticated users
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # For update/partial_update/destroy, require owner or admin
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        # Default
        return [permissions.IsAuthenticated()]
