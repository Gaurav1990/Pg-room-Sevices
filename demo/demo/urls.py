from django.conf.urls import patterns, include, url
#from django.contrib import admin
#admin.autodiscover()
#from app import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','app.views.home'),
    url(r'^page$','app.views.page'),
    url(r'^login$','app.views.login_user'),
    url(r'^register$','app.views.register'),
    url(r'page/(?P<area_name>\w+)/$','app.views.showdata'),
    url(r'^ad$','app.views.post_ad'),
    url(r'^data$','app.views.data'),
    url(r'^paste/$','app.views.paste'),
    url(r'^savedata/$','app.views.savedata'),
    url(r'^logout/$','app.views.logout_view'),
    url(r'^delete/$','app.views.delete'),
    url(r'^error/$','app.views.error'),
    url(r'^rating/$','app.views.user_rating'),
    url(r'^delete_admin/$','app.views.delete_admin'),
    url(r'^show/(?P<u_id>\d+)/$','app.views.showingdata'),
    url(r'^feedback/$','app.views.feedback'),
    url(r'^admin/rating$','app.views.all_rating'),
    url(r'^about_us/$','app.views.about'),
    #url(r'^admin/', include(admin.site.urls)),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
