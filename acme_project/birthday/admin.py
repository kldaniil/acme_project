from django.contrib import admin

from .models import Birthday


# admin.site.register(Birthday)

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    pass
