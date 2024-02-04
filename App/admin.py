from django.contrib import admin
from .models import *    

# Register your models here.

admin.site.register(Client)
admin.site.register(personnel)
admin.site.register(service)
admin.site.register(projet)
admin.site.register(equipe)
admin.site.register(detail)
admin.site.register(about)
admin.site.register(ServiceDemand)
admin.site.register(AcceptedCommand)
admin.site.register(CompletedCommand)

