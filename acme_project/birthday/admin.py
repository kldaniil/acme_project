from django.contrib import admin

from .models import Birthday, Tag


# admin.site.register(Birthday)

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
