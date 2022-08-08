from appearance.models import SiteLayOut
from rest_framework import serializers

class SiteLayOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteLayOut
        fields = '__all__'

    def create(self, validated_data):
        return SiteLayOut.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
