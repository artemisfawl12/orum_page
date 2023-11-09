from django.core.mail.backends import console
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed
from rest_framework.response import Response
import os
from .settings import MEDIA_ROOT
from uuid import uuid4
from user.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

class Main(APIView):
    def get(self,request):
        feed_list = Feed.objects.all().order_by('-id')
        if 'email' in request.session:
            print('로그인여부'+str(request.session['loginCheck']))
            print('로그인한 사용자:' +str(request.session['email']))
            email=request.session['email']
            user=User.objects.filter(email=email).first()
        else:
            print("로그인 하지 않은 사용자")
            request.session['loginCheck']=False
            return render(request, 'jinstagram/main.html', context=dict(feed_list=feed_list))
        return render(request,'jinstagram/main.html', context=dict(feed_list=feed_list, user=user))

    def get_session_data(request):
        try:
            print("getsessiondata launched")
            session_data={
                'loginCheck':request.session['loginCheck']
            }
            return JsonResponse(session_data)
        except Exception as e:
            return JsonResponse({'error: '+str(e)})

    def user_logout(request):
        logout(request)
        return redirect(reverse('main'))


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')
        image = uuid_name
        profile_image = request.data.get('profile_image')
        user_id = request.data.get('user_id')

        Feed.objects.create(content=content, image=image, profile_image=profile_image, user_id=user_id, like_count=0)

        return Response(status=200)

class AboutUs(APIView):
    def get(self,request):
        if 'email' in request.session:
            print('로그인여부'+str(request.session['loginCheck']))
            print('로그인한 사용자:' +str(request.session['email']))
            email=request.session['email']
            user=User.objects.filter(email=email).first()
        else:
            print("로그인 하지 않은 사용자")
            request.session['loginCheck']=False
            return render(request, 'jinstagram/aboutus.html')
        return render(request,'jinstagram/aboutus.html', context=dict(user=user))

    def get_session_data(request):
        try:
            print("getsessiondata launched")
            session_data={
                'loginCheck':request.session['loginCheck']
            }
            return JsonResponse(session_data)
        except Exception as e:
            return JsonResponse({'error: '+str(e)})

    def user_logout(request):
        logout(request)
        return redirect(reverse('aboutus'))