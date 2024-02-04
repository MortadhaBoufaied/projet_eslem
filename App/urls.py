from django.urls import path

from . import views
from App.views import *
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views 

urlpatterns = [
    #path('index/', views.home, name='home'),
    path('', index, name='index'),
    path('login/', views.LoginView, name='login'),
    path('signup/', views.SignupView, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('profile/', views.Profile, name='profile'),
    path('get_services/', views.get_services, name='get_services'),
    path('contact/', views.contact, name='contact'),
    
    path('comand_list/', views.ComandList, name='comand_list'),
    path('accept_command/<int:command_id>/', views.accept_command, name='accept_command'),
    path('delete_command/<int:command_id>/', views.delete_command, name='delete_command'),

    path('accepted_commands/', accepted_commands_list, name='accepted_commands_list'),
    path('complete_accepted_command/<int:accepted_command_id>/', complete_accepted_command, name='complete_accepted_command'),

    path('completed_commands/', completed_command_list, name='completed_command_list'),

    #reset password ursls
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    path('get_command_details/<int:command_id>/', views.get_command_details, name='get_command_details'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

