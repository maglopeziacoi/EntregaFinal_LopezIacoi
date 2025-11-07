from django.urls import path
from . import views


urlpatterns = [
    path('', views.PageListView.as_view(), name='page_list'),
    path('search/', views.search_pages, name='page_search'),
    path('create/', views.PageCreateView.as_view(), name='page_create'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    path('<slug:slug>/edit/', views.PageUpdateView.as_view(), name='page_update'),
    path('<slug:slug>/delete/', views.PageDeleteView.as_view(), name='page_delete'),
]