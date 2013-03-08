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
    url(r'^ad$','app.views.paste'),
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
    url(r'^notification/$','app.views.notification'),
    url(r'^noti/$','app.views.noti'),
    url(r'^remove_noti/$','app.views.remove_noti'),
    url(r'^notification_admin/$','app.views.notification_all'),
    url(r'^notification_admin/(?P<d_id>\d+)$','app.views.delete_noti_admin'),
    url(r'^forgot/$','app.views.forgot'),
    url(r'^send_pass/$','app.views.send_pass'),
    url(r'^deleted/$','app.views.delete_rating'),
    url(r'^changed_password/$','app.views.password_change'),
    url(r'^del_rating/$','app.views.del_rating'),
    url(r'^change_pass/$','app.views.change_pass'),
    url(r'^page/(?P<area_name>\w+)/(?P<v_id>\d+)$','app.views.vote_up'),
    url(r'^page/down/(?P<area_name>\w+)/(?P<d_id>\d+)$','app.views.vote_down'),
   
    #url(r'^admin/', include(admin.site.urls)),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
