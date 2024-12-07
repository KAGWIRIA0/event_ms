from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['name']
        db_table = 'client'

class Event(models.Model):
        EVENT_STATUS = [
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('Approved', 'Approved'),
        ]
        event_name = models.CharField(max_length=100)
        client = models.ForeignKey(User, on_delete=models.CASCADE)
        details = models.TextField()
        number_of_guests = models.IntegerField(default=0)
        date = models.DateField()
        status = models.CharField(max_length=40, choices=EVENT_STATUS, default='pending')
        cost = models.DecimalField(max_digits=50, decimal_places=2)


        def __str__(self):
            return f"{self.event_name}-{self.date}"
        class Meta:
           verbose_name = "Event"
           verbose_name_plural = "Events"
           ordering = ['date']
           db_table = 'Event'

class Consultation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    message = models.TextField(blank=True)
    number_of_guests = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)
    status = models.CharField(max_length=20,
                              choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')],
                              default='PENDING')

    def __str__(self):
        return f"Consultation for {self.event} - {self.preferred_date}"
    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"
        ordering = ['preferred_date']
        db_table = 'Consultations'

class Payment(models.Model):
        client = models.ForeignKey(User, on_delete=models.CASCADE)
        event = models.ForeignKey(Event, on_delete=models.CASCADE)
        merchant_request_id = models.CharField(max_length=100)
        checkout_request_id = models.CharField(max_length=100)
        code = models.CharField(max_length=40,null=True)
        amount = models.IntegerField()
        status= models.CharField(max_length=40,default='Pending')
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
           verbose_name = "Payment"
           verbose_name_plural = "Payments"
           ordering = ['created_at']
           db_table = 'Payments'

        def __str__(self):
            return f"Payment for {self.event.name} - {self.merchant_request_id}-{self.code}-{self.amount}"

# ALTER DATABASE `event_db` CHARACTER SET utf8;
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver