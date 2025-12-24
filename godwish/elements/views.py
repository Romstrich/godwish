from django.shortcuts import render
from django.template.context_processors import request
from django.views import View
from django.http import HttpResponseRedirect


from .forms import UpPicture
from .models import Picture
# Create your views here.
# Посмотреть работу с классом, одним классом загружать и васё остальное



def complite(request):
    return render(request,template_name='loaded.html')

class PictureWorkView(View):
    '''Класс загрузки изображений'''
    def get(self,request):
        form = UpPicture
        content={'form':form}
        return render(request,context=content,template_name='picture_upload.html')
    def post(self,request):
        # form=UpPicture(request.POST,request.FILES)
        # if form.is_valid():
        #     #for img in request.FILES.getlist('images')
        #     form.save()
        #     img_obj=form.instance
        #Получим картинки
        uploaded_images = request.FILES.getlist('picture')
        #'_post': <QueryDict: {'csrfmiddlewaretoken': ['JQkGZHdbEzr0OSFybtm4k6fJ4bTp6Ycb4drfVc4Rip4Eamz63cDZZifiNdeW3prO'], 'name': ['sdfasdf'], 'comment': ['asdfasdf'], 'picture': ['']}>, '_files': <MultiValueDict: {}>
        #Получим комментарий и имя
        commentPic=request.POST['comment']
        namePic=comment=request.POST['name']
        upImageLen=len(uploaded_images)
        for image in uploaded_images:
            print(image._name)
            #Сохраним картинку
            #Если картинка одна и есть name из формы:
            if upImageLen == 1:
                if namePic:
                    Picture.objects.create(name=namePic, comment=commentPic, picture=image)
                else:
                    Picture.objects.create(name=image._name, comment=commentPic, picture=image)
            else:
                Picture.objects.create(name=image._name,comment=commentPic,picture=image)

        return render(request,template_name='picture_upload.html')

class GaleryView(View):
    '''Класс просмотра галереи'''
    def get(self,request):
        galeryList=Picture.objects.all()
        content={'pictures':galeryList}
        return render(request,template_name='galery_pic.html',context=content)