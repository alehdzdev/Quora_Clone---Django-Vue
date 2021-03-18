from django.contrib import admin
from django.urls import include, path, re_path
from django_registration.backends.one_step.views import RegistrationView

from core.views import IndexTemplateView
from users.forms import CustomUserForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path("accounts/register/",
         RegistrationView.as_view(
             form_class=CustomUserForm,
             success_url="/",
             ), name="django_registration_register"),

    path('accounts/', include('django_registration.backends.one_step.urls')),

    path('accounts/', include('django.contrib.auth.urls')),

    path('api/', include("users.api.urls")),
    
    path('api/', include("questions.api.urls")),

    path('api-auth/', include("rest_framework.urls")),

    path('api/rest-auth/', include("rest_auth.urls")),

    path('api/rest-auth/registration/', include("rest_auth.registration.urls")),

    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")
]
