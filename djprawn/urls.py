from django.conf import settings

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djprawn.views.home', name='home'),
    # url(r'^djprawn/', include('djprawn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', TemplateView.as_view(template_name='static/index.html')),
    url(r'^rtube/', include('rtube.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', 'papi.views.open_api'),
)

# if settings.DEBUG:
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
