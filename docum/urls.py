from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('tai-lieu/', views.document_list, name='documents'),
    path('labs-thuc-hanh/', views.lab_list, name='labs'),
    url(r'^tai-lieu/(?P<slug>[\w-]+)/$', views.document_detail, name='doc-detail'),
    url(r'^mua-san-pham/(?P<slug>[\w-]+)/$', views.buy_item, name='buy-item'),
    url(r'^danh-muc/(?P<slug>[\w-]+)/$', views.catago_list, name='catago-list'),
    path('chi-tiet-mua/', views.buy_detail, name='buy-detail'),
    # path('comment/<int:id>/delete', views.delete_comment, name='delete-comment'),
    url('comment/delete', views.delete_comment, name='delete-comment'),
    url('comment/create', views.create_comment, name='create-comment'),
    path('export/', views.export_csv, name='export'),
]

    