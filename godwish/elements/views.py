from django.shortcuts import render
from django.template.context_processors import request
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from .forms import UpPicture, UpDocument, UpComponent
from .models import Picture, Document


# Create your views here.
# Посмотреть работу с классом, одним классом загружать и васё остальное


def complite(request):
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
    model = Document
    template_name = 'doclist.html'
    context_object_name = 'docs'
    queryset = Document.objects.all()


class GaleryView(View):
    '''Класс просмотра галереи'''

    def get(self, request):
        galeryList = Picture.objects.all()
        content = {'pictures': galeryList}
        return render(request, template_name='galery_pic.html', context=content)


class CompCreate(View):
    form = UpComponent
    def get(self, request):
        content = {"form": self.form}
        return render(request, template_name='component/createComp.html', context=content)

    def post(self, request):
        # Забираем свои аргументы
        name=request.POST.get('name')
        comment=request.POST.get('comment')
        contract = request.POST.get('contract')
        print(name)
        print(comment)
        if contract == 'on':
            contract=True
        else:
            contract=False
        print(contract)
        # Забираем картинки
        uploaded_images = request.FILES.getlist('images')
        # Забираем документы
        uploaded_docs = request.FILES.getlist('docs')
        return render(request, template_name='loaded.html')


class CompShow(View):
    def get(self):
        # Чтобы показать элемент, необходимо поднять несколько таблиц
        return render(request, template_name='showComp.html')
