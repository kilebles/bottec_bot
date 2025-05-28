from django.db import models


class Broadcast(models.Model):
    message = models.TextField('Текст сообщения')
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'Рассылка #{self.pk}'


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)  # Telegram ID
    username = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'users'
        managed = False
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username or str(self.id)


class TelegramResource(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    tg_id = models.BigIntegerField()

    class Meta:
        db_table = 'telegram_resources'
        managed = False
        verbose_name = 'Обязательное сообщество'
        verbose_name_plural = 'Обязательные сообщества'

    def __str__(self):
        return self.name


class FAQ(models.Model):
    key = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        db_table = 'faqs'
        managed = False
        verbose_name = 'Частый вопрос'
        verbose_name_plural = 'Частые вопросы'

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'
        managed = False
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        db_table = 'subcategories'
        managed = False
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

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
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user_id = models.BigIntegerField()
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'cart_items'
        managed = False
        verbose_name = 'Позиция в корзине'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.quantity} × {self.product.title}'


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('pending', 'Ожидает'),
        ('paid', 'Оплачен'),
        ('failed', 'Ошибка'),
    ]

    user_id = models.BigIntegerField()
    address = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='pending')

    class Meta:
        db_table = 'orders'
        managed = False
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} — {self.payment_status}'
