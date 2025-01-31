from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "user"

urlpatterns = [
    path('show/<int:id>', views.show, name='show'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('', views.user_list, name='list'),

]


urlpatterns += staticfiles_urlpatterns()