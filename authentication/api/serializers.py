from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'company_name', 'personal_telephone', 'office_telephone', 'address', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        user = CustomUser(email=self.validated_data['email'],
                          first_name=self.validated_data['first_name'],
                          last_name=self.validated_data['last_name'],
                          state_of_residence=self.validated_data['company_name'],
                          personal_telephone=self.validated_data['personal_telephone'],
                          office_telephone=self.validated_data['office_telephone'],
                          address=self.validated_data['address'],)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password == password2:
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'password': 'Passwords must match.'})


class DashboardSerializer(serializers.Serializer):
    total_emissions = serializers.FloatField()
    fuel_categories = serializers.ListField(child=serializers.CharField())
    fuel_emissions_data = serializers.ListField(child=serializers.FloatField())
    waste_categories = serializers.ListField(child=serializers.CharField())
    waste_emissions_data = serializers.ListField(child=serializers.FloatField())
    electricity_categories = serializers.ListField(child=serializers.CharField())
    electricity_emissions_data = serializers.ListField(child=serializers.FloatField())
    heating_categories = serializers.ListField(child=serializers.CharField())
    heating_emissions_data = serializers.ListField(child=serializers.FloatField())
    home_heating_categories = serializers.ListField(child=serializers.CharField())
    home_heating_emissions_data = serializers.ListField(child=serializers.FloatField())
