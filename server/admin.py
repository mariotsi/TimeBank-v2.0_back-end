from django.contrib import admin

# Register your models here.
from server.models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'region', 'cadastral_code')
    list_filter = ['province', 'region']
    search_fields = ['id', 'name', 'province', 'cadastral_code']


class UserAdmin(admin.ModelAdmin):
    def get_province(self, obj):
        return obj.city.province

    def get_cap(self, obj):
        return obj.city.cap

    get_province.short_description = 'Province'

    get_province.admin_order_field = 'city__province'

    get_cap.short_description = 'CAP'

    get_cap.admin_order_field = 'city__cap'

    # comma after ...'used_hours') make the magic happen, fields on the same row
    fieldsets = [
        (None, {'fields': [
            ('username', 'admin'), 'email', 'address', 'city'
        ]}),
        ('Hours', {'fields': (
            ('available_hours', 'worked_hours', 'requested_hours', 'used_hours'),
        ), 'classes': [
            'collapse']}
        )
    ]
    list_display = (
        'username', 'email', 'admin', 'address', 'get_cap', 'city', 'get_province', 'available_hours', 'worked_hours',
        'requested_hours', 'used_hours'
    )

    list_filter = ['city__province']
    search_fields = ['username', 'email', 'city__name', 'city__cap']


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

# admin.site.register(City, CityAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
