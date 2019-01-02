from django.contrib import admin

from . import models


admin.site.register(models.Location)
admin.site.register(models.Category)
admin.site.register(models.Detail)
admin.site.register(models.List)
admin.site.register(models.ListInventory)
admin.site.register(models.UserInventory)
admin.site.register(models.Item)
admin.site.register(models.Transaction)
