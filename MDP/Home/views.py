from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import About_User,Breakfast,Lunch,Dinner,DIET_PLAN,Exercises,Event,User_Image
from django import forms
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

class Delete_Event(DeleteView):
    model = Event
    success_url = reverse_lazy('Response_Giver')

class Delete_Exercise(DeleteView):
    model = Exercises
    success_url = reverse_lazy('Response_Giver')

class Delete_Breakfast(DeleteView):
    model = Breakfast
    success_url  = reverse_lazy('Response_Giver')

class Delete_Lunch(DeleteView):
    model = Lunch
    success_url = reverse_lazy('Response_Giver')

class Delete_Dinner(DeleteView):
    model = Dinner
    success_url = reverse_lazy('Response_Giver')

class Delete_Photo(DeleteView):
    model = User_Image
    success_url = reverse_lazy('Response_Giver')

class Profile_Update(UpdateView):
    model = About_User
    fields = ['USER_PROFILE_IMAGE']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('mypage')



def Response_Giver(request):
    return HttpResponse('Successfully Changed')

def Home(request):  
    profiles = About_User.objects.all()
    return render(request,'home.html', {'profiles':profiles})

def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=UserCreationForm()
    return render(request,'registration/Signup.html',{'form':form})

@login_required
def Digital_Portfolio(request):
    return render(request,'temp.html')


@login_required
def mypage(request,user_id):
    if request.method == "GET":
        try:
            DEFAULT = About_User.objects.get(USER_PROFILE_NUMBER = 1)
            DATA = About_User()
            Datas = About_User.objects.all()
            DATA.USER_PROFILE_NUMBER = len(Datas)+1
            DATA.USER_NAME = DEFAULT.USER_NAME
            DATA.USER_PHONE_NUMBER = DEFAULT.USER_PHONE_NUMBER
            DATA.USER_EMAIL = DEFAULT.USER_EMAIL
            DATA.USER_DESCRIPTION = DEFAULT.USER_DESCRIPTION
            DATA.USER_MOTIVATION_LINE = DEFAULT.USER_MOTIVATION_LINE
            DATA.USER_PROFILE_IMAGE = DEFAULT.USER_PROFILE_IMAGE
            DATA.USER = User.objects.get(id = user_id)
        except Exception as e:
            return HttpResponse('ERROR')
        DATA.save()
        
        return render(request,'mypage.html',{'DATA':DATA})

def create_portfolio(request,pk):
    
    DATA = About_User.objects.get(USER_PROFILE_NUMBER = pk)
    Breakfasts = Breakfast.objects.filter(ABOUT_USER = pk)
    Lunches = Lunch.objects.filter(ABOUT_USER = pk)
    Dinners  = Dinner.objects.filter(ABOUT_USER = pk)
    Exercise = Exercises.objects.filter(ABOUT_USER = pk)
    Events = Event.objects.filter(ABOUT_USER = pk)
    User_Images = User_Image.objects.filter(ABOUT_USER = pk)
    return render(request,'mypage.html',{'DATA':DATA,'Breakfasts':Breakfasts,'Lunches':Lunches,'Dinner':Dinners,'Events':Events,'Exercises':Exercise,'User_Images':User_Images})


def update(request):
    pn = request.GET['Profile_Number']
    img = request.FILES['backgroundimage'] 
    user = About_User.objects.get(USER_PROFILE_NUMBER = pn)
    user.USER_PROFILE_IMAGE = img
    user.save()
    return redirect('mypage')


def Add_Diet(request):
    pn = request.POST['Profile_Number']
    user = About_User.objects.get(USER_PROFILE_NUMBER = pn)
    br = Breakfast()
    br.FOOD = request.POST['b_Food']
    br.DESCRIPTION = request.POST['b_Description']
    br.CARBOHYDRATE = request.POST['b_Carbohydrates']
    br.PROTIEN = request.POST['b_Protiens']
    br.FATS= request.POST['b_Fats']
    br.IMAGE = request.FILES['b_photo']
    br.ABOUT_USER = user
    br.save()

    lh = Lunch()
    lh.FOOD = request.POST['l_Food']
    lh.DESCRIPTION = request.POST['l_Description']
    lh.CARBOHYDRATE = request.POST['l_Carbohydrates']
    lh.PROTIEN = request.POST['l_Protiens']
    lh.FATS= request.POST['l_Fats']
    lh.IMAGE = request.FILES['l_photo']
    lh.ABOUT_USER = user
    lh.save()

    dn = Dinner()
    dn.FOOD= request.POST['d_Food']
    dn.DESCRIPTION = request.POST['d_Description']
    dn.CARBOHYDRATE = request.POST['d_Carbohydrates']
    dn.PROTIEN = request.POST['d_Protiens']
    dn.FATS =request.POST['d_Fats']
    dn.IMAGE = request.FILES['d_photo']
    dn.ABOUT_USER = user
    dn.save()
    return redirect('mypage',pn,permanent  = False)

def Add_Exercise(request):
    pn = request.POST['Profile_Number']
    user = About_User.objects.get(USER_PROFILE_NUMBER = pn)
    ex = Exercises()
    ex.EXERCISE_NAME= request.POST['exercise_name']
    ex.DESCRIPTION = request.POST['exercise_description']
    ex.IMAGE = request.FILES['photo']
    ex.ABOUT_USER = user
    ex.save()
    return redirect('mypage',pn,permanent  = False)
    #return redirect('create_portfolio',pk = pn)

def Add_Event(request):
    pn = request.POST['Profile_Number']
    user = About_User.objects.get(USER_PROFILE_NUMBER = pn)
    e = Event()
    e.EVENT_NAME = request.POST['event_name']
    e.EVENT_DATE = request.POST['event_date']
    e.EVENT_START_TIME = request.POST['event_start']
    e.EVENT_END_TIME = request.POST['event_end']
    e.EVENT_DESCRIPTION = request.POST['event_description']
    e.ABOUT_USER = user
    e.save()
    return redirect('mypage',pn,permanent  = False)
    # return redirect('create_portfolio',pk = pn)

def Add_Photo(request):
    i = User_Image()
    pn = request.POST['Profile_Number']
    user = About_User.objects.get(USER_PROFILE_NUMBER = pn)
    i.IMAGE = request.FILES['photo']
    i.CAPTION_IMAGE = request.POST['Caption']
    i.ABOUT_USER = user
    i.save()
    return redirect('mypage',pn,permanent  = False)

def Save_Profile(request):
    pn = int(request.GET['USER_PROFILE_NUMBER'])
    user = About_User.objects.get(USER_PROFILE_NUMBER = pn) 
    user.USER_NAME = request.GET['USER_NAME']
    user.USER_PHONE_NUMBER = request.GET['USER_PHONE_NUMBER']
    user.USER_EMAIL = request.GET['USER_EMAIL']
    user.USER_DESCRIPTION = request.GET['USER_DESCRIPTION']
    user.USER_MOTIVATION_LINE = request.GET['USER_MOTIVATION_LINE']
    user.save()
    return redirect('mypage',pn,permanent  = False)


def Preview(request,pk):
    DATA = About_User.objects.get(USER_PROFILE_NUMBER = pk)
    Breakfasts = Breakfast.objects.filter(ABOUT_USER = pk)
    Lunches = Lunch.objects.filter(ABOUT_USER = pk)
    Dinners  = Dinner.objects.filter(ABOUT_USER = pk)
    Exercise = Exercises.objects.filter(ABOUT_USER = pk)
    Events = Event.objects.filter(ABOUT_USER = pk)
    User_Images = User_Image.objects.filter(ABOUT_USER = pk)
    return render(request,'template2.html',{'DATA':DATA,'Breakfasts':Breakfasts,'Lunches':Lunches,'Dinner':Dinners,'Events':Events,'Exercises':Exercise,'User_Images':User_Images})
