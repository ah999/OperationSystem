from django.contrib import admin
from .models import OpRoom, Operation, Department


# Register your models here.
admin.site.register(OpRoom)
admin.site.register(Department)
admin.site.register(Operation)
