"""Church IMS URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

site_name = "StAnds IMS"
admin.site.site_header = f"{site_name} administration"
admin.site.site_title = f"{site_name} admin"
admin_url = settings.ADMIN_URL + "/"

urlpatterns = [
    path(admin_url + "doc/", include("django.contrib.admindocs.urls")),
    path(admin_url, admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("people/", include("people.urls")),
    path("records/", include("records.urls")),
    path("reports/", include("reports.urls")),
    path("", include("core.urls")),
]
