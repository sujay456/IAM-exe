from django.contrib import admin

from .models import Organization,IsRoot,PartOf,Permissions,UserPermissions,LoginHistory,RegisterHistory
# Register your models here.

admin.site.register(Organization)
admin.site.register(IsRoot)
admin.site.register(PartOf)
admin.site.register(Permissions)
admin.site.register(UserPermissions)
admin.site.register(LoginHistory)

admin.site.register(RegisterHistory)
