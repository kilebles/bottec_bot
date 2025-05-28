from django.contrib import admin

from app.bottec_bot.services.broadcast import send_broadcast_message

from .models import (
    Broadcast,
    Category,
    Subcategory,
    Product,
    FAQ,
    TelegramResource,
    CartItem,
    Order,
    User,
)


@admin.action(description='Отправить выбранные рассылки всем пользователям')
def send_broadcasts(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.is_sent:
            send_broadcast_message(obj.id)
            obj.is_sent = True
            obj.save()


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'is_sent', 'created_at')
    actions = [send_broadcasts]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subcategory', 'price')
    search_fields = ('title',)
    list_filter = ('subcategory',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'title')
    search_fields = ('key', 'title')


@admin.register(TelegramResource)
class TelegramResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'tg_id')
    search_fields = ('name', 'tg_id')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product', 'quantity')
    list_filter = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'address', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('user_id', 'address')
