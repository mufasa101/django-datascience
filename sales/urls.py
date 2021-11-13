from django.urls import path
from . import views
app_name = "sales"

urlpatterns = [
    path('', views.index, name="index"),
    path('sales/',views.SalesListView.as_view(),name="list"),
    path('sales/<pk>',views.SalesDetilView.as_view(),name="detail"),
    path('csv/',views.UploadTemplateView.as_view(),name="csv"),
    path('upload/', views.csv_upload_view, name='upload'),

]