from django.contrib import admin
from .models import *
admin.site.site_header = admin.site.site_title = "Student Information"

admin.site.register(Role)
admin.site.register(Master)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Subject)