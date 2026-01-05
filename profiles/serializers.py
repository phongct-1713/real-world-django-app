from rest_framework import serializers
from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profiles.
    """
    username = serializers.CharField(read_only=True)
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'bio', 'image', 'following']
        read_only_fields = ['username']

    def get_following(self, obj):
        """
        Check if the current user is following this profile.
        """
        request = self.context.get('request', None)
        
        if request is None:
            return False
        
        if not request.user.is_authenticated:
            return False
        
        return request.user.is_following(obj)
