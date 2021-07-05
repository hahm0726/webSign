from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = "__all__"

    def create(self, validated_data):
        ModelClass = self.Meta.model
        
        instance = ModelClass._default_manager.create(**validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance