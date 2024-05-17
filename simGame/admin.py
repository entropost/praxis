from django.contrib import admin
from .models import simGame, CommonComponent, Market, Company, UserProfile
# Register your models here.

admin.site.register(simGame)
admin.site.register(Market)
admin.site.register(Company)
admin.site.register(CommonComponent)
admin.site.register(UserProfile)