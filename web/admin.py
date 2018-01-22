from django.contrib import admin

# Register your models here.
from  web.models import Jpider_response
from  web.models import Jpider_memory
admin.site.register(Jpider_response)
admin.site.register(Jpider_memory)