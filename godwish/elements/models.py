from django.db import models
from django.db.models import ManyToManyField

# Create your models here.
'''
Здесь будут создаваться модели элементов, таких как:
    -Картинки
    -Документы
    -Компоненты
    -Заказы
    -ПО'''


class Picture(models.Model):
    '''Модель картинки
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название изображения", max_length=128, blank=True)
    comment = models.CharField(verbose_name="Комментарий к изображению", max_length=256, blank=True)
    picture = models.ImageField(verbose_name="Изображение", upload_to='galery/', blank=True, null=True)
    update = models.DateTimeField(verbose_name="Время загрузки", auto_now_add=True)
    # Включить автора загрузки
    # Включить "хозяина" Картинки


class Document(models.Model):
    '''модель документа
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название документу", max_length=128, blank=True)
    comment = models.CharField(verbose_name="Комментарий к документу", max_length=256, blank=True)
    document = models.FileField(verbose_name="Документ", upload_to='documents/', blank=True, null=True)
    update = models.DateTimeField(verbose_name="Время загрузки", auto_now_add=True)


class Component(models.Model):
    '''Constituent (Составная часть)
    модель элемента комплектации
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название", max_length=128, blank=True)
    comment = models.CharField(verbose_name="Комментарий", max_length=256, blank=True)
    # ссылка на изображения
    images = ManyToManyField(Picture,through='CompPic')
        #models.ImageField(verbose_name="Изображение", upload_to='galery/', blank=True, null=True)
    # ссылка на документы
    docs = ManyToManyField(Document,through='CompDoc')
        #models.FileField(verbose_name="Документ", upload_to='documents/', blank=True, null=True))
    # дата
    update = models.DateTimeField(verbose_name="Время загрузки", auto_now_add=True)
    # ометка о том, что является заказом/проектом
    contract=models.BooleanField(null=False,blank=False,default=False,verbose_name="Является заказом")
    # номер контракта/заказа
    # ссылка на родительский компонент
    # ссылка на дочерний компонент
    # ссылка на проект/заказ
    # Рассмотреть вариант "каталога"


class CompPic(models.Model):
    '''Связка компонента и картинок'''
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    # отметка об активности связки


class CompDoc(models.Model):
    '''Связка компонента и документов'''
    dokument = models.ForeignKey(Document, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    # отметка об активности связки


class CompLink(models.Model):
    '''связь компонентов между собой'''
    parentC = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="parentC")
    childC = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='childC')
    # отметка об активности связки
