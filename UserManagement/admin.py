# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from .models import User


# class UserAdmin(BaseUserAdmin):
#     list_display = ('email', 'first_name', 'last_name',
#                     'tc', 'is_staff', 'is_active', 'is_superuser',)

#     search_fields = ('email', 'first_name', 'last_name',)
#     ordering = ('email',)

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('first_name',
#          'last_name', 'tc', 'profile_image')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff',
#          'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {
#          'fields': ('last_login', 'created_at')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'tc', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
#          ),
#     )

#     list_filter = ('is_active', 'is_staff', 'is_superuser',  'groups',)

#     def mark_as_active(self, request, queryset):
#         queryset.update(is_active=True)
#     mark_as_active.short_description = "Mark selected users as active"

#     def mark_as_inactive(self, request, queryset):
#         queryset.update(is_active=False)
#     mark_as_inactive.short_description = "Mark selected users as inactive"

#     def send_email(self, request, queryset):
#         subject = "Important message from our system"
#         message = "Dear user,\n\nWe would like to inform you that..."
#         for user in queryset:
#             user.email_user(subject, message)
#     send_email.short_description = "Send email to selected users"

#     def grant_staff_permission(self, request, queryset):
#         queryset.update(is_staff=True)
#         self.message_user(
#             request, "Staff permission granted to selected users.")
#         # return HttpResponseRedirect(reverse('admin:app_list', args=['UserManagement']))
#     grant_staff_permission.short_description = "Grant staff permission to selected users"

#     def remove_staff_permission(self, request, queryset):
#         queryset.update(is_staff=False)
#         self.message_user(
#             request, "Staff permission removed from selected users.")
#         # return HttpResponseRedirect(reverse('admin:app_list', args=['UserManagement']))
#     remove_staff_permission.short_description = "Remove staff permission from selected users"

#     actions = [mark_as_active, mark_as_inactive,
#                send_email, grant_staff_permission, remove_staff_permission]


# admin.site.register(User, UserAdmin)
from django.contrib import admin
from UserManagement.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'tc', 'is_admin', 'user_slug')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', "last_name", 'tc', 'user_slug', 'profile_image')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'tc', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
