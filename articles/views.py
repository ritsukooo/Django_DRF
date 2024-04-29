from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from articles.models import Article,Comment
from articles.serializers import CommentSerializer
from rest_framework.decorators import api_view
from .serializers import ArticleSerializer, ArticleDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)

    def post(self, request):
            serializer = ArticleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
     
    def get(self, request, article_pk):
            article = get_object_or_404(Article, pk=article_pk)    
            serializer = ArticleDetailSerializer(article)
            return Response(serializer.data)
            
    def put(self, request, article_pk):
            article = get_object_or_404(Article, pk=article_pk)    
            serializer = ArticleSerializer(article, data = request.data, partial = True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
            
    def delete(self, request, article_pk):
            article = get_object_or_404(Article, pk=article_pk)
            article.delete()
            return Response(status=status.HTTP_200_OK)


            
class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
     
    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
     
     
    def delete(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        data = {"pk": f"{comment_pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)
    
    
    def put(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = CommentSerializer(comment, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        