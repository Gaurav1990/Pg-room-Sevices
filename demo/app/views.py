# Create your views here.
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import admin
from app.models import Pg , Ad , UserProfile , Rating
from app.forms import article , reg , rate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.functional import SimpleLazyObject
from django.db.models import Avg
from django import forms

@csrf_exempt
#@login_required
def home(request):
    try:
        request_user = UserProfile.objects.get(user = request.user)
    except Exception:
        pass
    rate = Rating.objects.all().aggregate(Avg('rating'))
    rating_avg = rate.get('rating__avg')
    if rating_avg is None:
        rating_avg = 0.0
    return render_to_response("base.html",locals())

def page(request):
    #aa = Ad.objects.all()
    query = Ad.objects.all().query
    query.group_by = ['area']
    aa = QuerySet(query = query, model = Ad)
    
    return render_to_response("one.html",locals())

def showdata(request,area_name):
    d = Ad.objects.filter(area = area_name)
    return render_to_response('result.html',locals())

@csrf_exempt
def post_ad(request):
    ad = article()
    return render_to_response('ad.html',locals())

@csrf_exempt
def paste(request):
    print "1"
    if request.method == 'POST':
        print "2"        
        form = article(request.POST)
        if form.is_valid():
            print "3"
            user = Ad.objects.create( posted_by = request.user.username,
                               phn_no = form.cleaned_data['phn_no'],
                               area = form.cleaned_data['area'],
                               monthly_rent = form.cleaned_data['monthly_rent'],
                               sharing = form.cleaned_data['sharing'],
                               cuisine = form.cleaned_data['cuisine']
            )
            print "4"            
            user.save()
            print "5"
            return render_to_response('paste-now.html',locals())
    else:
        form = article()
    return render_to_response('ad.html',locals())

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print "post request"
        user = authenticate(username=username, password=password)
        if user is not None:
            #print "authenticated"
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('app.views.home'))
        else:
            state = "Username or Password is not correct please check"
    return render_to_response('login.html',locals())


@csrf_exempt
def register(request):
    form = reg()
    return render_to_response('registration.html',locals())

@csrf_exempt
def savedata(request):
    if request.method == 'POST':
        form = reg(request.POST)
        if form.is_valid():
            usert = User.objects.create(
                username = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            #    re-password = form.cleaned_data['re-password'],

            )
            usert.re_password = form.cleaned_data['re_password']
            usert.save()
            if usert.password != usert.re_password :
                state = "Your passwords do not match"
                return render_to_response('registration.html',locals())

            
            usert.set_password(str(form.cleaned_data['password']))
            usert.save()
            user = UserProfile.objects.create(
                user = usert,
                address = form.cleaned_data['address'],
                user_type = form.cleaned_data['user_type'],
  
              )
            user.save()

            return render_to_response('savedata.html',locals())
        else:
            return render_to_response('registration.html',locals())
    else:
        print "not working "
        form = reg()
        return render_to_response('registration.html',locals())

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('app.views.home'))

def error(request):
    return render_to_response("error.html",locals())

def data(request):
    user_data = User.objects.all()
    return render_to_response('show.html',locals())

def showingdata(request,u_id):
    #user_data = User.objects.get(id = u_id )
    user_data = UserProfile.objects.get(user__id = u_id)     
    return render_to_response('showdata.html',locals())

@csrf_exempt
def delete(request):
    return render_to_response('delete.html',locals())

@csrf_exempt
def delete_admin(request):
    if request.method == "POST":
        del_name = request.POST.get('del_name')
        if del_name is not None:
            User.objects.filter(username = del_name).delete()
            #user_data = UserProfile.objects.get(id = u_id)  
            #UserProfile.objects.filter( user.username = del_name).delete()
        user_data = User.objects.all()
    return render_to_response('show.html',locals())

@csrf_exempt
def user_rating(request):
    rating = rate()
    return render_to_response('rate.html',locals())

@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        print "2"        
        feed = rate(request.POST)
        if feed.is_valid():
            user_feed = Rating.objects.create( 
                               posted_by = request.user.username,
                               rating = feed.cleaned_data['rating'],
                               suggesion = feed.cleaned_data['suggesion'],
            )            
            user_feed.save()
            return render_to_response('feed.html',locals())
    else:
        feed = rate()
    return render_to_response('rate.html',locals())


@csrf_exempt
def all_rating(request):
    feedback = Rating.objects.all()
    return render_to_response('rating_admin.html',locals())
def about(request):
    return render_to_response('about.html',locals())
