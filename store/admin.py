from django.contrib import admin
from .models import Author, Book, Customer, Order, OrderItem

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'published_date')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'author__name')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'total_amount')
    list_filter = ('order_date',)
    search_fields = ('customer__first_name', 'customer__last_name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price')
    list_filter = ('order',)
    search_fields = ('book__title',)