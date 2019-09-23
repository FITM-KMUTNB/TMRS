from django.conf.urls import url
from blog.views import HomeView
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^document/$', views.document, name='document'),
    url(r'^neighbor/$', views.neighbor, name='neighbor'),
    
    
]

urlpatterns += staticfiles_urlpatterns()