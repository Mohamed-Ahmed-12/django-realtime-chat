from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
# Register your models here.

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display = ("username","is_superuser","is_online")
    def save_model(self, request, obj, form, change):
        obj.password = make_password(request.POST['password'])
        obj.save()

admin.site.register(User,UserAdmin)