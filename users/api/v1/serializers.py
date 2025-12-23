from rest_framework import serializers
from .models import Users

class UsersRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        user = Users.objects.create(
            name = validated_data['name'],
            email = validated_data['email'],
            bio = validated_data.get('bio', ''),
            image = validated_data.get('image', ''),
            password = validated_data['password']
        )
        user.save()
        return user