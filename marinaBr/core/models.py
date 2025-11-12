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

class ReadySolution(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='Цена')
    # disheFirst = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='Блюдо №1')
    # disheSecond = models.ManyToManyField(to=Product, unique=True, blank=True, on_delete=models.PROTECT, verbose_name='Блюдо №2')
    # disheThird = models.ManyToManyField(to=Product, unique=True, blank=True, on_delete=models.PROTECT, verbose_name='Блюдо №3')
    # disheFourth = models.ManyToManyField(to=Product, unique=True, blank=True, on_delete=models.PROTECT, verbose_name='Блюдо №4')
    # disheFifth = models.ManyToManyField(to=Product, unique=True, blank=True, on_delete=models.PROTECT, verbose_name='Блюдо №5')
    # disheSixth = models.ManyToManyField(to=Product, unique=True, blank=True, on_delete=models.PROTECT, verbose_name='Блюдо №6')
    # disheSeventh = models.ManyToManyField(to=Product, unique=True, blank=True, on_delete=models.PROTECT, verbose_name='Блюдо №7')
    # disheEighth = models.ManyToManyField(to=Product, unique=True, blank=True, on_delete=models.PROTECT, verbose_name='Блюдо №8')