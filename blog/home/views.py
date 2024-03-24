from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

class PublicView(APIView):
    def get(self,request):
        try:
            blogs=Blog.objects.all().order_by('?')
            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains=search)|Q(blog_text__icontains=search))
        
            page_number=request.GET.get('page',1)
            paginator=Paginator(blogs,4)
            serializer=BlogSerializer(paginator.page(page_number),many=True)



            return Response({
                "data":serializer.data,
                "message":"blog fecheted successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "data":{},
                "message":"invalid page number"
            })




class BlogView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get(self,request):
        try:
            blogs=Blog.objects.filter(user=request.user)
            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains=search)|Q(blog_text__icontains=search))
            serializer=BlogSerializer(blogs,many=True)



            return Response({
                "data":serializer.data,
                "message":"blog fecheted successfully"
            },status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "data":{},
                "message":"something wrong"
            })

    def post(self,request):
        try:
            data=request.data
            data['user']=request.user.id
            serializer=BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':"invalid credentials"
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data':serializer.data,
                'message':"successfully created"

            },status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                    "data":{},
                    "message":'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        try:
           data=request.data
           blogs=Blog.objects.filter(uid=data.get('uid'))
           if not blogs.exists():
               return Response({
                   "data":{},
                   "message":"invalid uid"
               },status=status.HTTP_400_BAD_REQUEST)
           if request.user != blogs[0].user:
               return Response({
                   "data":{},
                   "message":"invalid user"
               },status=status.HTTP_400_BAD_REQUEST)
           serializer=BlogSerializer(blogs[0],data=data,partial=True)
           if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':"invalid credentials"
                },status=status.HTTP_400_BAD_REQUEST)
           serializer.save()
           return Response({
                'data':serializer.data,
                'message':"successfully created"

            },status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                    "data":{},
                    "message":'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        try:
           data=request.data
           blogs=Blog.objects.filter(uid=data.get("uid")) 
           if not blogs.exists():
               return Response({
                   "message":"invalid uid"
               },status=status.HTTP_400_BAD_REQUEST)
           if request.user != blogs[0].user:
               return Response({
                   "message":"invalid user"
               },status=status.HTTP_400_BAD_REQUEST)
           blogs.delete()
           return Response({
               "message":"blog deleted"
           },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message":"something wrong!"
            },status=status.HTTP_400_BAD_REQUEST)   




               
                    

            
