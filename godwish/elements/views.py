'''

'''
import os.path

from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView
from django.core.files.storage import FileSystemStorage
from PIL import Image

from .forms import UpPicture, UpDocument, UpComponent, OrderAdd
from .models import Picture, Document, Component, img_location
# from godwish import settings


# Create your views here.
# Посмотреть работу с классом, одним классом загружать и васё остальное

def plug(request):
    return HttpResponse('<h1>ЗАГЛУШКА</h1>')

def complite(request):
    '''Страничка успешной загрузки'''
    return render(request, template_name='loaded.html')


class PictureWorkView(View):
    '''Класс загрузки изображений'''
    def get(self, request):
        form = UpPicture
        content = {'form': form}
        return render(request, context=content, template_name='picture_upload.html')

    def post(self, request):
        # Получим картинки
        uploaded_images = request.FILES.getlist('picture')
        # '_post': <QueryDict: {'csrfmiddlewaretoken': ['JQkGZHdbEzr0OSFybtm4k6fJ4bTp6Ycb4drfVc4Rip4Eamz63cDZZifiNdeW3prO'], 'name': ['sdfasdf'], 'comment': ['asdfasdf'], 'picture': ['']}>, '_files': <MultiValueDict: {}>
        # Получим комментарий и имя
        commentPic = request.POST['comment']
        namePic = request.POST['name']
        upImageLen = len(uploaded_images)
        for image in uploaded_images:
            print(image._name)
            # Сохраним картинку
            # Если картинка одна и есть name из формы:
            if upImageLen == 1:
                if namePic:
                    Picture.objects.create(name=namePic, comment=commentPic, picture=image)
                else:
                    Picture.objects.create(name=image._name, comment=commentPic, picture=image)
            else:
                Picture.objects.create(name=image._name, comment=commentPic, picture=image)

        return render(request, template_name='loaded.html')


class DocumentUpload(View):
    '''
    класс загрузки документов
    '''
    def get(self, request):
        form = UpDocument
        content = {'form': form}
        return render(request, context=content, template_name='picture_upload.html')

    def post(self, request):
        print(request.POST.__dict__)
        uploaded_docs = request.FILES.getlist('document')
        commentDoc = request.POST['comment']
        nameDoc = request.POST['name']
        upDocsLen = len(uploaded_docs)
        print(upDocsLen)
        for doc in uploaded_docs:
            print(doc._name)
            if upDocsLen == 1:
                if nameDoc:
                    Document.objects.create(name=nameDoc, comment=commentDoc, document=doc)
                else:
                    Document.objects.create(name=doc._name, comment=commentDoc, document=doc)
            else:
                Document.objects.create(name=doc._name, comment=commentDoc, document=doc)

        return render(request, template_name='loaded.html')


class DocList(ListView):
    '''
    Просмотр всех документов
    '''
    model = Document
    template_name = 'doclist.html'
    context_object_name = 'docs'
    queryset = Document.objects.all()


class GaleryView(View):
    '''
    Класс просмотра всей галереи
    '''
    def get(self, request):
        galeryList = Picture.objects.all()
        content = {'pictures': galeryList}
        return render(request, template_name='galery_pic.html', context=content)


class CompCreate(View):
    '''
    Создание элемента
    '''
    form = UpComponent

    def get(self, request):
        content = {"form": self.form}
        return render(request, template_name='component/createComp.html', context=content)

    def post(self, request):
        # Забираем свои аргументы
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        contract = request.POST.get('contract')
        print(name)
        print(comment)
        if contract == 'on':
            contract = True
        else:
            contract = False
        print(contract)
        comp=Component.objects.create(name=name, comment=comment, contract=contract)
        print(comp)

        # Забираем картинки
        # IMG_LOCATION='new_galery/'
        uploaded_images = request.FILES.getlist('images')
        if len(uploaded_images):
            for image in uploaded_images:
                print(image.name)
                # Сохраним картинку со сменой локации
                fs = FileSystemStorage(location=f'media/{name}')
                img_fname = fs.save(image.name,image)
                img_url= os.path.join(f'/{name}/',img_fname)
                # Если картинка одна и есть name из формы:
                pic=Picture.objects.create(name=image.name, comment=comment,picture=img_url)# picture=image)
                comp.images.add(pic)
                #переложим картинку
        # Забираем документы
        uploaded_docs = request.FILES.getlist('docs')
        if len(uploaded_docs):
            for doc in uploaded_docs:
                print(doc._name)
                #Сохраним документ со сменой локации
                fs = FileSystemStorage(location=f'media/{name}')
                doc_fname = fs.save(doc.name, doc)
                doc_url = os.path.join(f'/{name}/', doc_fname)
                upDoc=Document.objects.create(name=doc._name, comment=comment, document=doc_url)
                comp.docs.add(upDoc)

        return render(request, template_name='loaded.html')


class CompShow(View):
    '''
    Показ элемента (списка)
    '''
    def get(self,request):
        # Чтобы показать элемент, необходимо поднять несколько таблиц
        components=Component.objects.all()
        content={'components':components}
        return render(request,context=content, template_name='component/showComp.html')

class OrdersShow(ListView):
    '''
    Список заказов
    '''
    model = Component
    template_name = 'component/orderList.html'
    context_object_name = 'components'
    extra_context = {'title':'Список заказов'}

    def get_queryset(self):
        '''
        Возмём только компоненты, имеющие флаг заказа
        '''
        return Component.objects.filter(contract=True)
    # def get_context_data(self, *, object_list=None, **kwargs):

    # def get(self,request):
    #     components = Component.objects.all()
    #     content = {'components': components}
    #     return render(request, context=content, template_name='component/showComp.html')

class OrderAdd(CreateView):
    '''
    Создание заказа
    '''
    form_class = OrderAdd
    template_name = 'component/orderAdd.html'
    success_url = reverse_lazy('index')

    # def get_form_kwargs(self):
    #     """
    #     Возвращает словарь аргументов для экземпляра формы
    #     """
    #     # kwargs = {'initial': self.get_initial()}
        # if self.request.method in ('POST', 'PUT'):
        #     kwargs.update({
        #         'data': self.request.POST,
        #         'files': self.request.FILES,
        #     })
        # return kwargs