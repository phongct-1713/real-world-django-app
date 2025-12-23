from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializers import UsersRegistrationSerializer

@api_view(['POST'])
def register_user(request):

    payload = request.data.get('user') or request.data
    serializer = UsersRegistrationSerializer(data=payload)

    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {
                'user': {
                    'name': user.name,
                    'email': user.email,
                    'password': user.password
                } 
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        { 'errors': serializer.errors },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET', 'PUT', 'DELETE'])
def get_user(request, user_id):

    try:
        user = Users.objects.get(id=user_id)

    except Users.DoesNotExist:

        return Response(
            { 'error': 'User not found' },
            status = status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = UsersRegistrationSerializer(user)

        return Response(
            { 'user': serializer.data },
            status = status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        serializer = UsersRegistrationSerializer(user, data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'user': {
                        'name': user.name,
                        'email': user.email,
                        'password': user.password
                    } 
                },
                status=status.HTTP_200_OK
            )

        return Response(
            { 'errors': serializer.errors },
            status = status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        user.delete()

        return Response(
            status = status.HTTP_204_NO_CONTENT
        )