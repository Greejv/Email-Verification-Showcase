from rest_framework import serializers
from .models import Email


# serializer pre ukladanie Emailov do databazy
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = 'id', 'email', 'verified'
        extra_kwargs = {
            'verified': {'required': False, 'read_only': True}
        }
