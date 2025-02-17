from django.contrib import admin
from .models import StockCompany, StockRating


class StockRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'user', 'rating', 'created_at']
    list_filter = ['company', 'user']
    search_fields = ['user__username', 'company__name']


class StockCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'industry',
                    'market_cap', 'average_rating', 'created_at']
    search_fields = ['name', 'industry']
    list_filter = ['industry']


admin.site.register(StockCompany, StockCompanyAdmin)
admin.site.register(StockRating, StockRatingAdmin)
