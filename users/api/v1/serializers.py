from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import UserProfile

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(source='profile.bio', allow_blank=True, required=False)
    image = serializers.CharField(source='profile.image', allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'image']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # create / update profile
        UserProfile.objects.update_or_create(user=user, defaults={
            'bio': profile_data.get('bio', ''),
            'image': profile_data.get('image', ''),
        })

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if profile_data:
            UserProfile.objects.update_or_create(user=instance, defaults={
                'bio': profile_data.get('bio', getattr(instance.profile, 'bio', '')),
                'image': profile_data.get('image', getattr(instance.profile, 'image', '')),
            })

        return instance