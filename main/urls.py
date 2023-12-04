from django.urls import path
from . import views
app_name='main'
urlpatterns=[
    path('',views.upload_invoice , name='upload_invoice'),
    path('test/',views.style_test , name='test'),
    path('dashboard/',views.dashBoard , name='dashboard'),
    path('t2/',views.t2 , name='t2'),
  
    path('describe_spending/', views.describe_department_spending, name='describe_spending'),
]