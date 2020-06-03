from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('documents/', views.document_list, name='documents'),
    path('labs/', views.lab_list, name='labs'),
    url(r'^document/(?P<slug>[\w-]+)/$', views.document_detail, name='doc-detail'),
    url(r'^buy-item/(?P<slug>[\w-]+)/$', views.buy_item, name='buy-item'),
    url(r'^catagories/(?P<slug>[\w-]+)/$', views.catago_list, name='catago-list'),
    path('buy-detail/', views.buy_detail, name='buy-detail'),
    path('comment/<int:id>/delete', views.delete_comment, name='delete-comment'),
    # path('export/', views.export_csv, name='export'),
]

    