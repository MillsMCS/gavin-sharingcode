from django.contrib import admin

from .models import Script, Coder, Problem, Review
admin.site.register(Script)
admin.site.register(Coder)
admin.site.register(Problem)
admin.site.register(Review)

# Register your models here.
