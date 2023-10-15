
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncDate
from tests.models import PatientPaymentHistory,LabTestOrder,LabTestResult
from .serializer import PaymentDataSerializer,PatientSearilizers,ZoneSearializers,RegionSearializers,WoredaSearializers,UserPercentageSerializer
from users.models import Region,Zone,Woreda,Patient,User
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view

from users.models import Appointment,Patient



# endpoint to return a detail of a single patient
@api_view(['GET'])
def get_patient_details(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        appointment = Appointment.objects.get(patient=patient, is_active=True)
        
        pending_orders = LabTestOrder.objects.filter(appointment =appointment,order_status = "Pending")
        
        paid_orders = LabTestOrder.objects.filter(appointment =appointment,order_status = "Paid")
        
        completed_orders = LabTestOrder.objects.filter(appointment =appointment,order_status = "Lab completed")
        
        lab_results = LabTestResult.objects.filter(labtestorder__in=completed_orders)

       
        patient_data = {
            
            'patient_id': patient.id,
            'name': f"{patient.first_name} {patient.last_name}",
            'age': patient.age,
            'gender': patient.gender,
            'contact_number': patient.contact_number,
            'appointment': {'appointment_id': appointment.id, 'with doctor': appointment.doctor.username,'appointment_date':appointment.appointment_date},
            'pending_orders': [{'Test Name': order.labtest.name, 
                                 'Order Date':order.order_date,
                                 'Order_status': order.order_status} for order in pending_orders],
             'paid_orders': [{'Test Name': order.labtest.name, 
                                 'Order Date':order.order_date,
                                 'Order_status': order.order_status} for order in paid_orders],
            'completed_orders': [{'Test Name': order.labtest.name, 
                                 'Order Date':order.order_date,
                                 'Order_status': order.order_status} for order in completed_orders],
            
            'results': [{'Test Name': result.labtestorder.labtest.name, 'result': result.result,'result comment':result.result_comment} for result in lab_results],
        }

        return Response(patient_data, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({'detail': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)


# endpoint to show a number of users by percentage
class UserPercentageView(APIView):
    def get(self, request):
        total_users = User.objects.count()
        user_roles = User.Role.choices

        percentages = []
        for role, role_display in user_roles:
            count = User.objects.filter(role=role).count()
            percentage = (count / total_users) * 100
            percentages.append({
                'role': role_display,
                'percentage': percentage,
            })

        serializer = UserPercentageSerializer(percentages, many=True)
        return Response(serializer.data)




class PaymentDataAPIView(APIView):
    def get(self, request):
        
        payment_sum_by_date = (
            PatientPaymentHistory.objects
            .annotate(payment_date_date=TruncDate('payment_date'))
            .values('payment_date_date')
            .annotate(total_payment=Sum('amount'))
            .order_by('payment_date_date')
        )

        
        payment_data = [
            {
                'date': payment_info['payment_date_date'],
                'total_payment': payment_info['total_payment']
            }
            for payment_info in payment_sum_by_date
        ]

       
        serializer = PaymentDataSerializer(payment_data, many=True)

        return Response(serializer.data)
    


from django.http import JsonResponse


class ZonePatientCountAPI(APIView):
    def get(self, request):
        
        queryset = Zone.objects.annotate(patient_count=Count('woreda__patient')).filter(patient_count__gt=0).values('zone_name', 'patient_count')

        
        data = list(queryset)

        return JsonResponse(data, safe=False)
    




@api_view(['GET'])
def patient_list(request):
    patients = Patient.objects.all()
    searializer = PatientSearilizers(patients,many=True)
    return Response(searializer.data)

@api_view(['GET'])
def regionView(request):
    regions = Region.objects.all()
    serializer = RegionSearializers(regions,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def zoneView(request):
    zones = Zone.objects.all()
    serializer = ZoneSearializers(zones,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def WoredaView(request):
    woredas = Woreda.objects.all()
    serializer = WoredaSearializers(woredas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def zones_by_region(request, region_id):
    try:
        region = Region.objects.get(pk=region_id)
    except Region.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    zones = Zone.objects.filter(region=region)
    serializer = ZoneSearializers(zones, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def woredas_by_zone(request, zone_id):
    try:
        zone = Zone.objects.get(pk=zone_id)
    except Zone.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    woredas = Woreda.objects.filter(zone=zone)
    serializer = WoredaSearializers(woredas, many=True)
    return Response(serializer.data)








