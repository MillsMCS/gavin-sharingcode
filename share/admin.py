from django.contrib import admin

from .models import Script, Coder, Problem
admin.site.register(Script)
admin.site.register(Coder)
admin.site.register(Problem)
# Register your models here.
