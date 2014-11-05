# Register your models here.
from django.contrib.auth import get_user_model
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from server.models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'region', 'cadastral_code')
    list_filter = ['province', 'region']
    search_fields = ['id', 'name', 'province', 'cadastral_code']


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'is_active', 'is_admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    add_form = UserCreationForm


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': (('email', 'username'), 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Hours', {'fields': (('available_hours', 'worked_hours', 'requested_hours', 'used_hours'),)}),
        (None, {'fields': ('address', 'city',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {'fields': (('email', 'username'), ('password1', 'password2'))}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Hours', {'fields': (('available_hours', 'worked_hours', 'requested_hours', 'used_hours'),)}),
        (None, {'fields': ('address', 'city',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ListingAdmin(admin.ModelAdmin):
    def get_owner_name(self, obj):
        return obj.owner.username

    def get_applicant_name(self, obj):
        if obj.applicant is not None:
            return obj.applicant.username
        else:
            return None

    def get_description_preview(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100]
        else:
            return obj.description

    get_owner_name.short_description = 'Owner'

    get_owner_name.admin_order_field = 'owner__username'

    get_applicant_name.short_description = 'Applicant'

    get_applicant_name.admin_order_field = 'applicant__username'

    get_description_preview.short_description = 'Description'

    get_description_preview.order_field = 'listing__description'

    list_display = (
        'id', 'get_description_preview', 'get_owner_name', 'get_applicant_name', 'creation_date', 'requested')

    fieldsets = [
        (None, {'fields': [
            ('description', 'creation_date', 'category')
        ]}),
        ("Owner & Applicant", {'fields': [
            ('owner', 'applicant'), 'requested'
        ]})
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'name']
    search_fields = ['name']


admin.site.unregister(Group)
admin.site.register(City, CityAdmin)
admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
