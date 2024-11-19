"""asset_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import asset_manage_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("record", asset_manage_app.views.record_signin, name = "record_signin"),
    path("record_signout", asset_manage_app.views.record_signout, name = "record_signout"),
    path("record_signup", asset_manage_app.views.record_signup, name = "record_signup"),
    path("record_list", asset_manage_app.views.record_list, name = "record_list"),
    path("record/add/", asset_manage_app.views.record_add, name = "record_add"),
    path("record/<int:housekeep_id>/edit", asset_manage_app.views.record_edit, 
          name = "record_edit"),
    path("record/<int:housekeep_id>/delete", asset_manage_app.views.record_delete,
          name = "record_delete")
]
