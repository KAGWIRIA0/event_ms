from django.contrib import admin

from events.models import Client, Consultation, Event, Payment

# Register your models here.
admin.site.site_header = 'Event Management System'
admin.site.site_title = 'Manage Events'


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number']
    search_fields =  ['name', 'email', 'phone_number']
    list_per_page = 30

class EventAdmin(admin.ModelAdmin):
    list_display = ['event_name','client','status','date','cost','number_of_guests']
    search_fields = ['event_name','client','status','date','cost','number_of_guests']
    list_per_page = 35

class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['client', 'preferred_date','number_of_guests']
    search_fields = ['client','preferred_date','number_of_guests']
    list_per_page = 25

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['client','event','code','status','amount','created_at']
    search_fields= ['client','event','code','status','amount','created_at']
    list_per_page = 25

admin.site.register(Client,ClientAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Consultation,ConsultationAdmin)
admin.site.register(Payment,PaymentAdmin)