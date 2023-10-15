# Import necessary libraries
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests  
from .models import PatientPaymentHistory
bot_token = "6679177225:AAHmCT_RgvEWPsGluHygBF3miHt_lwgVQSQ"
chat_id = "-1001858420706"

@receiver(post_save, sender=PatientPaymentHistory)
def send_payment_description(sender, instance, **kwargs):
    payment_date_str = instance.payment_date.strftime("%Y-%m-%d")
    
    payment_description = (
        f"Patient Full Name: {instance.appointment.patient.first_name} {instance.appointment.patient.last_name}\n"
        f"Amount Paid: {instance.amount} Birr\n"
        f"Payment Date: {payment_date_str}\n"
        f"Payment Reason: {instance.payment_reason}"
    )

   
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": payment_description
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send the message. Status code:", response.status_code)
        print("Response content:", response.content)
