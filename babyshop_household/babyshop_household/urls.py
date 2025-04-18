from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('baby/', include('baby_shop.urls', namespace='baby_shop')),
    path('household/', include('household.urls', namespace='household')),
    path('cart/', include('cart.urls', namespace='cart')),
    
    # Password reset views (override allauth)
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='account/password_reset.html'
         ), 
         name='account_reset_password'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ), 
         name='account_reset_password_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'
         ), 
         name='account_reset_password_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ), 
         name='account_reset_password_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)