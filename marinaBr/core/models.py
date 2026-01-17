from django.db import models
# from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
    
def product_image_path(instance, fileName):
    return f'product_images/{instance.slug}/{fileName}'

def ready_solution_image_path(instance, fileName):
    return f'ready_solutions/{instance.slug}/{fileName}'

class Product(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True, verbose_name='URL')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Цена')
    priceAdditional = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0, verbose_name='Цена за 120г')
    priceFor = models.BooleanField(default=False, verbose_name='Цена за одну штуку')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    ingredients = models.TextField(blank=True, null=True, verbose_name='Состав')
    ingredientsList = models.TextField(blank=True, null=True, help_text="Разделяйте ингредиенты через ';'", verbose_name='Состав списком')
    availableFrom = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0, verbose_name='Отпуск от (шт)')
    imageMain = models.ImageField(upload_to=product_image_path, blank=True, null=True, verbose_name='Главное изображение')
    imageSecond = models.ImageField(upload_to=product_image_path, blank=True, null=True, verbose_name='Дополнительное изображение')
    imageThird = models.ImageField(upload_to=product_image_path, blank=True, null=True, verbose_name='Дополнительное изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория')
    is_bundle = models.BooleanField(default=False, verbose_name='Готовое решение (содержит другие товары)')
    
    # Для готовых решений - количество персон (10, 15 и т.д.)
    persons_count = models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество персон', help_text='Только для готовых решений')

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title
    
    def get_ingredients_list(self):
        if self.ingredientsList:
            return [ingredient.strip() for ingredient in self.ingredientsList.split(';')]
        return []
    
    def get_bundle_items(self):
        """Получить компоненты готового решения"""
        if self.is_bundle:
            return self.bundle_items.all().order_by('order', 'product__title')
        return []


class ProductBundleItem(models.Model):
    """Компоненты готового решения"""
    bundle = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='bundle_items',
        verbose_name='Готовое решение',
        limit_choices_to={'is_bundle': True}
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='in_bundles',
        verbose_name='Товар в составе',
        limit_choices_to={'is_bundle': False}
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    
    class Meta:
        db_table = 'product_bundle_item'
        verbose_name = 'Товар в готовом решении'
        verbose_name_plural = 'Товары в готовых решениях'
        ordering = ['order', 'product__title']
        unique_together = ['bundle', 'product']
    
    def __str__(self):
        return f'{self.bundle.title} → {self.product.title} x{self.quantity}'


class ReadySolution(models.Model):
    """Готовые решения (меню на N человек)"""
    PERSONS_COUNT_CHOICES = [
        (10, '10 человек'),
        (15, '15 человек'),
    ]
    
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='URL')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Цена')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image_main = models.ImageField(upload_to=ready_solution_image_path, blank=True, null=True, verbose_name='Главное изображение')
    persons_count = models.PositiveIntegerField(
        choices=PERSONS_COUNT_CHOICES,
        verbose_name='Количество персон',
        help_text='Выберите количество персон: 10 или 15'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    products = models.ManyToManyField(
        Product,
        through='ReadySolutionItem',
        related_name='ready_solutions',
        verbose_name='Товары в составе',
        limit_choices_to={'is_bundle': False}
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        db_table = 'ready_solution'
        verbose_name = 'Готовое решение'
        verbose_name_plural = 'Готовые решения'
        ordering = ['persons_count', 'title']
        unique_together = [('title', 'persons_count'), ('slug', 'persons_count')]
    
    def __str__(self):
        return f'{self.title} ({self.persons_count} чел.)'
    
    def get_items(self):
        """Получить компоненты готового решения"""
        return self.items.all().order_by('order', 'product__title')


class ReadySolutionItem(models.Model):
    """Товары в составе готового решения"""
    ready_solution = models.ForeignKey(
        ReadySolution,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Готовое решение'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='in_ready_solutions',
        verbose_name='Товар в составе',
        limit_choices_to={'is_bundle': False}
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    
    class Meta:
        db_table = 'ready_solution_item'
        verbose_name = 'Товар в готовом решении'
        verbose_name_plural = 'Товары в готовых решениях'
        ordering = ['order', 'product__title']
        unique_together = ['ready_solution', 'product']
    
    def __str__(self):
        return f'{self.ready_solution.title} → {self.product.title} x{self.quantity}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    customer_name = models.CharField(max_length=255, verbose_name='Имя клиента')
    customer_phone = models.CharField(max_length=20, verbose_name='Телефон')
    order_date = models.DateField(verbose_name='Дата заказа')
    order_time = models.TimeField(verbose_name='Время заказа')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Общая сумма')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Заказ #{self.id} от {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    
    class Meta:
        db_table = 'order_item'
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
    
    def __str__(self):
        return f'{self.product.title} x{self.quantity}'