from django.urls import path, include
from snippets import views
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


snippet_list=SnippetViewSet.as_view({
    'get':'list',
    'post':'create'
})

snippet_detail=SnippetViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy'
})

snippet_highlight=SnippetViewSet.as_view({
    'get':'highliht'
},renderer_classes=[renderers.StaticHTMLRenderer])

user_list=UserViewSet.as_view({
    'get':'list'
})

user_detail=UserViewSet.as_view({
    'get':'retrieve'
})

urlpatterns = [
    path('snippets/',snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/',snippet_detail, name='snippet-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/',user_detail, name='user-detail'),
    path('api-auth/', include('rest_framework.urls')),
    path('',views.api_root),
    path('snippets/<int:pk>/highligt/', snippet_highlight, name='snippet-highlight'),
]

urlpatterns=format_suffix_patterns(urlpatterns)

