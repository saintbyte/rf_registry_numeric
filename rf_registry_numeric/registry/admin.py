from django.contrib import admin
from registry.models import Registry


class RegistryAdmin(admin.ModelAdmin):
    search_fields = [
        "code",
        "start",
        "end",
        "operator",
        "region",
        "tax_number",
    ]
    list_display =  [
        "code",
        "start",
        "end",
        "size",
        "operator",
    ]


admin.site.register(Registry, RegistryAdmin)
