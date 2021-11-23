"""tMinusMbta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from users.views import user_logout, dashboard
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^accounts/logout/', user_logout, name='logout'),
    url(r'^accounts/', include("django.contrib.auth.urls")),
    path(r'timer/', include('timer.urls')),
    url(r'^', include("users.urls")),
    url(r'^', dashboard),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
