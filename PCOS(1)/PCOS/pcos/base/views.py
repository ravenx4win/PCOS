from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
global scaler

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def getPredictions(Age,Weight,BloodGroup,Hb,MarraigeStatus,Pregnant,RR,RBS,Weightgain,Skindarkening,Hairloss,Pimples,Endometrium):
    model = pickle.load(open('DT.pkl', 'rb'))
    prediction = model.predict(np.array([[Age,Weight,BloodGroup,Hb,MarraigeStatus,Pregnant,RR,RBS,Weightgain,Skindarkening,Hairloss,Pimples,Endometrium]]))
    return (prediction)

def result(request):
    Age = float(request.GET['Age (yrs)'])
    Weight = float(request.GET[ 'Weight (Kg)'])
    BloodGroup = float(request.GET[ 'Blood Group'])
    Hb = float(request.GET[ 'Hb(g/dl)'])
    MarraigeStatus = float(request.GET[ 'Marraige Status (Yrs)'])
    Pregnant = float(request.GET[ 'Pregnant(Y/N)'])
    RR = float(request.GET[ 'RR (breaths/min)'])
    RBS = float(request.GET[ 'RBS(mg/dl)'])
    Weightgain= float(request.GET[ 'Weight gain(Y/N)'])
    Skindarkening = float(request.GET[ 'Skin darkening (Y/N)'])
    Hairloss = float(request.GET[ 'Hair loss(Y/N)'])
    Pimples = float(request.GET[ 'Pimples(Y/N)'])
    Endometrium = float(request.GET[ 'Endometrium (mm)'])
    
    result = getPredictions(Age,Weight,BloodGroup,Hb,MarraigeStatus,Pregnant,RR,RBS,Weightgain,Skindarkening,Hairloss,Pimples,Endometrium)
    if result[0]==0:
        res= 'YOU ARE AFFECTED BY POLYCYSTIC OVARY SYNDROME(PCOS) DISEASE'
    else:
        res='YOU ARE A HEALTHY PERSON'
    return render(request, 'result.html', {'result': res})

