from django.urls import path
from session.views import SessionCreateView

from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "session"

urlpatterns = [
    path('', views.session_list, name='list'),
    path('create', SessionCreateView.as_view(), name='session-create' ),
    path('lobby/', views.lobby, name='lobby'),
    path('lobby/room/', views.room, name='room'),
    path('lobby/get_token/', views.getToken, name='get-token'),

    path('lobby/room/create_member/', views.createMember, name='create-member'),
    path('lobby/room/get_member/', views.getMember),
    path('lobby/room/delete_member/', views.deleteMember),

]


urlpatterns += staticfiles_urlpatterns()
