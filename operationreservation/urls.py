from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'operationreservation'

urlpatterns = [

    #path(r'ops/', views.IndexView.as_view(), name='index'),
    #path(r'ops/<int:pk>/', views.DetailView.as_view(), name='operation'),
    #path(r'op/add/', views.OperationCreate.as_view(), name='operation-add'),
    path(r'ops/get/', views.OperationsList.as_view()),
    path(r'op/post/', views.OperationsList.as_view()),
    path(r'deps/get/', views.DepartmentsList.as_view()),
    path(r'dep/post/', views.DepartmentsList.as_view()),
    path(r'oprooms/get/', views.OpRoomsList.as_view()),
    path(r'oproom/post/', views.OpRoomsList.as_view()),
    path(r'ops/<int:pk>/', views.OperationDetial.as_view(), name='get-operation'),
    path(r'ops/<int:pk>/delete/', views.OperationDetial.as_view(), name='delete-operation'),

]

#urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
