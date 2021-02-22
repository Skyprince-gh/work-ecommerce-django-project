from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import PhoneOTP

admin.site.register(PhoneOTP)


class UserAdmin(BaseUserAdmin):
    # Forms to add or change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used to display the user model
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('name', 'phone', 'admin')
    list_filter = ('staff', 'active', 'admin')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'address', 'street_name')}),
        ('Permisions', {'fields': ('admin', 'staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute.
    # UserAdmin overrides get_fieldsetsto use this attribute when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('Wide',),
            'fields': ('phone', 'password1', 'password2')
        }),
    )

    search_fields = ('phone', 'name')
    ordering = ('phone', 'name')
    filter_horizontal = ()


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)

# Remove Group model from admin
admin.site.unregister(Group)