from rest_framework import serializers
from .models import Contract

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'title', 'description', 'expiry_date', 'status',
                 'parties_involved', 'pdf_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_parties_involved(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Parties involved must be a list")
        return value

    def create(self, validated_data):
        # Associate the contract with the current user
        user = self.context['request'].user
        return Contract.objects.create(user=user, **validated_data)
