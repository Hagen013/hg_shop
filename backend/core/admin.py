from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import CategoryPage, ProductPage

MPTT_ADMIN_LEVEL_INDENT = 20

class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 40
    search_fields = ('name', 'slug')
    readonly_fields = ('url',)
    list_display = ('tree_actions', 'indented_title','__str__', 'slug',  'id')
    fieldsets = [
        ('Основное', {
            'fields' :[
                'name',
                'parent',
                'scoring',
                'slug',
                'is_published',
            ],
            }),
        ('SEO информация', {
            'fields': [
                '_meta_title',
                '_meta_keywords',
                '_meta_description',
                ],
            'classes': ['collapse']
            }),
    ]


class ProductPageAdmin(admin.ModelAdmin):
    search_fields = ('vendor_code', 'name', 'slug', 'category__name')
    list_display = ('vendor_code', '__str__',
                    'price', 'is_in_stock', 'category')


#class WatchesProductInline(admin.TabularInline):
#    model = WatchesProductPage
#    fields = ('id', 'slug', 'model', 'vendor', 'price', 'old_price',
#              'is_published', 'is_in_stock', 'is_new_product', 'is_bestseller',
#              'is_yml')



admin.site.register(CategoryPage, CustomMPTTModelAdmin)
admin.site.register(ProductPage, ProductPageAdmin)



