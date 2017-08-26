from django.contrib import admin
from .models import Specialty, Doctors, Schedule, UserProfile

# Register your models here.


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['pub_date', 'specialty', 'doctor', 'client']

    class Meta:
        model=Schedule


admin.site.register(Specialty)
admin.site.register(Doctors)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(UserProfile)
