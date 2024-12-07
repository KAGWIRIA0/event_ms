"""
URL configuration for event_ms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import redirect

from events import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('', lambda request: redirect('event_dashboard')),  # Redirect root URL to event_dashboard
    path('dashboard/', views.event_dashboard, name='event_dashboard'),
    path('events/', views.events_list, name='events_list'),
    path('booked-events/', views.booked_events, name='booked_events'),
    path('events/<int:event_id>/cancel/', views.cancel_event, name='cancel_event'),
    path('events/<int:event_id>/approve/', views.approve_event, name='approve_event'),
    path('pie-chart/', views.pie_chart, name='pie_chart'),
    path('line-chart/', views.line_chart, name='line_chart'),
    path('bar-chart/', views.bar_chart, name='bar_chart'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls),

]
# path('events/<int:event_id>/', views.event_detail, name='event_detail'),  # Event details
# path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),  # Edit event
# path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),  # Delete event
# path('consultation/book/', views.book_consultation, name='book_consultation'),
# path('consultation/success/', views.consultation_success, name='consultation_success'),