from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from boards import views as boards_views

urlpatterns = [
    url(r'^$', boards_views.home, name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^boards/(?P<pk>\d+)/$', boards_views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', boards_views.new_topic, name='new_topic'),
    url(r'^admin/', admin.site.urls),
]
