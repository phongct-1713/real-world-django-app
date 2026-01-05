from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .serializers import ProfileSerializer

class ProfileRetrieveAPIView(APIView):
    """
    Retrieve a user's profile.
    """
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer

    def get(self, request, username):
        try:
            profile = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('A profile with this username was not found.')

        serializer = self.serializer_class(profile, context={'request': request})
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)


class ProfileFollowAPIView(APIView):
    """
    Follow and unfollow users.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def post(self, request, username):
        """Follow a user."""
        follower = request.user

        try:
            followee = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('A profile with this username was not found.')

        if follower.pk == followee.pk:
            return Response(
                {'errors': {'detail': 'You cannot follow yourself.'}},
                status=status.HTTP_400_BAD_REQUEST
            )

        follower.follow(followee)

        serializer = self.serializer_class(followee, context={'request': request})
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, username):
        """Unfollow a user."""
        follower = request.user

        try:
            followee = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('A profile with this username was not found.')

        follower.unfollow(followee)

        serializer = self.serializer_class(followee, context={'request': request})
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)
