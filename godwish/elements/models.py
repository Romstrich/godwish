from django.db import models

# Create your models here.
'''
Здесь будут создаваться модели элементов, таких как:
    -Картинки
    -Документы
    -Компоненты
    -Заказы
    -ПО'''

class Picture(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(verbose_name="Название изображения",max_length=128,null=True)
    comment=models.CharField(verbose_name="Комментарий к изображению", max_length=256,null=True)
    picture=models.ImageField(verbose_name="Изображение",null=False,upload_to='galery/',blank=True)
    update=models.DateTimeField(verbose_name="Время загрузки",auto_now_add=True)
    #Включить автора загрузки
    #Включить "хозяина" Картинки