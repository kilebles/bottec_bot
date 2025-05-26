from django.db import models

# Create your models here.


class TelegramResource(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    tg_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'telegram_resources'
        managed = False


    def __str__(self):
        return self.name


class FAQ(models.Model):
    key = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    
    class Meta:
        db_table = 'faqs'
        managed = False


    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'categories'
        managed = False

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'subcategories'
        managed = False

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo_url = models.URLField(blank=True)
    price = models.PositiveIntegerField()
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products'
        managed = False


    def __str__(self):
        return self.title


class CartItem(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'cart_items'
        managed = False


    def __str__(self):
        return f'{self.quantity} × {self.product.title}'


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user_id = models.IntegerField()
    address = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='pending')
    
    class Meta:
        db_table = 'orders'
        managed = False


    def __str__(self):
        return f'Order #{self.pk} — {self.payment_status}'
