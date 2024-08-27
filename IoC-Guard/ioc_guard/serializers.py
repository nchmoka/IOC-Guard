from rest_framework import serializers
import re

class DomainSerializer(serializers.Serializer):
    domain = serializers.CharField()

    def validate_domain(self, value):
        # Simple regex to check for valid domain names
        domain_regex = re.compile(
            r'^(?=.{1,255}$)(?!-)[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,})$'
        )
        if not domain_regex.match(value):
            raise serializers.ValidationError("Invalid domain format.")
        return value

class IPSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()

class HashSerializer(serializers.Serializer):
    hash_value = serializers.CharField()

    def validate_hash_value(self, value):
        # Validate MD5, SHA1, or SHA256 hash formats
        if len(value) == 32:  # MD5
            hash_regex = re.compile(r'^[a-fA-F0-9]{32}$')
        elif len(value) == 40:  # SHA1
            hash_regex = re.compile(r'^[a-fA-F0-9]{40}$')
        elif len(value) == 64:  # SHA256
            hash_regex = re.compile(r'^[a-fA-F0-9]{64}$')
        else:
            raise serializers.ValidationError("Invalid hash format. Supported formats: MD5, SHA1, SHA256.")
        
        if not hash_regex.match(value):
            raise serializers.ValidationError("Invalid hash value.")
        return value
