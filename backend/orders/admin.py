from django.contrib import admin
from .models import DefaultOrder, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'email', 'phone', 'total_price')

    fieldsets = (('Личные данные', {'fields': (("name", "email", "phone"),
                                               ("address")),
                                    }
                  ),
                 )

admin.site.register(DefaultOrder, OrderAdmin)
