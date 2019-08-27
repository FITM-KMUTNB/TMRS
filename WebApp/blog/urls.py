from django.conf.urls import url
from blog.views import HomeView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='blog'),
    
]

urlpatterns += staticfiles_urlpatterns()