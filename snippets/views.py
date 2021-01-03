from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins, generics, renderers, permissions, status, viewsets
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework.reverse import reverse


'''
@csrf_exempt
def snippet_list(request):
    if request.method=='GET':
        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method=='POST':
        data=JSONParser().parse(request)
        serializer=SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
'''

'''
@api_view(['GET','POST'])
def snippet_list(request,format=None):
    if request.method=='GET':
        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


'''
@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method=='GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer=SnippetSerializer(snippet,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif  request.method =='DELETE':
        snippet.delete()
        return HttpResponse(status=204)
'''

'''
@api_view(['GET','PUT','DELETE'])
def snippet_detail(request,pk, format=None):
    try:
        snippet=Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer=SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=SnippetSerializer(snippet,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

'''
class SnippetList(generics.ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes=[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
'''

'''
class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
'''


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


'''
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes=[renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet=self.get_object()
        return Response(snippet.highlight)
'''


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highligt(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highliht)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
