from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('rtube.views',
    # Examples:
    # url(r'^$', 'djprawn.views.home', name='home'),
    # url(r'^djprawn/', include('djprawn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'index'),
    url(r'^details/(?P<video_id>\d+)/$', 'details'),
    url(r'^random/$', 'random'),
    url(r'^p/(?P<category>[-\w]+)/$', 'p'),
)
