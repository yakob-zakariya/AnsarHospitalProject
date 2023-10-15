from rest_framework import serializers
from users.models import Region,Zone,Woreda,Patient

class PatientSearilizers(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        
class RegionSearializers(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class ZoneSearializers(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class WoredaSearializers(serializers.ModelSerializer):
    class Meta:
        model = Woreda
        fields = '__all__'

class PaymentDataSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d')
    total_payment = serializers.FloatField()
    
class UserPercentageSerializer(serializers.Serializer):
    role = serializers.CharField()
    percentage = serializers.FloatField()
    

