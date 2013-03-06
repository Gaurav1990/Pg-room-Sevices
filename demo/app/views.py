# Create your views here.
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import admin
from app.models import Pg , Ad , UserProfile , Rating , Reviews
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
from django.core.mail import send_mail
from sendsms import api
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.conf import settings
from django.contrib.formtools.wizard.views import SessionWizardView


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
    #print area_name
    all_place = []
    d = Ad.objects.filter(area = area_name)
    #print d
    for i in d :
        #print i
        a = {"id": i.id, "posted_by":i.posted_by,"phn_no": i.phn_no,"area": i.area, "monthly_rent": i.monthly_rent, "sharing": i.sharing, "cuisine": i.cuisine}
        rev_list = Reviews.objects.filter(rev  = i)
        #print rev_list
        if not rev_list :
            print "inside if"
            a['voteup'] = 0
            a['votedown'] = 0
        else :
            print "inside else" 
            a['voteup'] = rev_list[0].voteup
            a['votedown'] = rev_list[0].votedown            
        all_place.append(a)
    print all_place
    
    return render_to_response('result.html',locals())

@csrf_exempt
def paste(request):
    #print "1"
    if request.method == 'POST':
        #print "2"        
        form = article(request.POST)
        if form.is_valid():
            #print "3"
            user = Ad.objects.create( posted_by = request.user.username,
                               phn_no = form.cleaned_data['phn_no'],
                               area = form.cleaned_data['area'],
                               monthly_rent = form.cleaned_data['monthly_rent'],
                               sharing = form.cleaned_data['sharing'],
                               cuisine = form.cleaned_data['cuisine']
            )
            #print "4"            
            user.save()
            #print "5"
            return render_to_response('paste-now.html',locals())
        else:
            reg_form = form
            return render_to_response('ad.html',locals())
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
    check_user = User.objects.all()
    if request.method == 'POST':
        form = reg(request.POST)
        if form.is_valid():
            for user_name in check_user:
                if user_name.username == form.cleaned_data['username'] :
                    state = "This Username is already existed. Plz take any other name"
                    return render_to_response('registration.html',locals())
            usert = User.objects.create(
                username = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
                #re-password = form.cleaned_data['re-password'],

            )
            usert.re_password = form.cleaned_data['re_password']
            
            usert.save()

            
            #print "send mail"
            if usert.password != usert.re_password :
                state = "Your passwords do not match"
                return render_to_response('registration.html',locals())

            
            usert.set_password(str(form.cleaned_data['password']))
            usert.save()
            user = UserProfile.objects.create(
                user = usert,
                address = form.cleaned_data['address'],
                user_type = form.cleaned_data['user_type'],
                password2 = form.cleaned_data['password'],
  
              )
            user.save()
            print user.user.email
            send_mail('Registered User Confirmation', 'Welcome to Pg/Room Services', 'pgroomservices@gmail.com', [user.user.email])
            
            #send_sms("This is demo","09632120841" ,"09017060099")
            #api.send_sms(body='This is demo', from_phone='+919632120841', to=['+919017060099'])

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

def del_rating(request):
    return render_to_response("rating-del.html",locals())

@csrf_exempt
def delete_rating(request):
    if request.method == "POST":
        del_name = request.POST.get('del_name')
        if del_name is not None:
            Rating.objects.filter(posted_by = del_name).delete()
            #user_data = UserProfile.objects.get(id = u_id)  
            #UserProfile.objects.filter( user.username = del_name).delete()
        feedback = Rating.objects.all()
    return render_to_response('rating_admin.html',locals())

def vote_up(request,area_name,v_id):
    s = Ad.objects.get(id= v_id)
    print s
    r = Reviews.objects.filter(rev = s)
    
    for i in r :
        print i.voteup, i.votedown
    
    if not r:
        new_r = Reviews(rev=s , voteup = 1, votedown = 0)
        new_r.save()
    else :
        print r[0].voteup
        r[0].voteup = r[0].voteup+1
        r[0].save()
        print r[0].voteup
    return HttpResponseRedirect(reverse('app.views.showdata', kwargs={"area_name":area_name}))


def vote_down(request,area_name,d_id):
    s = Ad.objects.get(id= d_id)
    print s
    r = Reviews.objects.filter(rev = s)
    
    for i in r :
        print i.voteup, i.votedown
    
    if not r:
        new_r = Reviews(rev=s , voteup = 0, votedown = 1)
        new_r.save()
    else :
        print r[0].votedown
        r[0].votedown = r[0].votedown+1
        r[0].save()
        print r[0].votedown
    return HttpResponseRedirect(reverse('app.views.showdata', kwargs={"area_name":area_name}))



@csrf_exempt
def forgot(request):
    return render_to_response('forgot_user.html',locals())


@csrf_exempt
def send_pass(request):
    
    user_data = UserProfile.objects.all()
      
    username = request.POST.get('username')
    '''    
    send_mail('Forgot Password', 'Welcome to Pg/Room Services.Your Password is {% for post in user_data %}{% if post.username == username %}{{ post.password }}{%endif %}{% endfor %}','gauravnagpal2002@gmail.com', [email])
    '''
    data_dict = []
    email_id = []    
    for post in user_data:
        if post.user.username == username:
            data_dict = post.password2
            email_id = post.user.email
    if data_dict == [] and email_id == [] :
        state = "This user name is not exist in database. Plese check again"
        return render_to_response('forgot_user.html',locals())  


    tt = loader.get_template('email.txt')
    c = Context({'data_dict':data_dict , 'username' : username})
    
    e = EmailMultiAlternatives('Forgot Password', tt.render(c), 'pgroomservices@gmail.com', [email_id])
    
    try:
        ht = loader.get_template('email.html')
        e.attach_alternative(ht.render(c), 'text/html')
    except:
        pass
    
    e.send()
    return render_to_response('sended.html',locals())
                             

