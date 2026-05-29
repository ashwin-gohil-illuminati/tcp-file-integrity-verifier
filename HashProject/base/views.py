

import mimetypes
from multiprocessing import context
from urllib import response
from wsgiref import headers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from .models import UserProfile
import requests
from .forms import UserForm
from django.utils.timesince import timesince

import os
from django.conf import settings
from django.http import Http404








# Create your views here.

apiURL = 'http://127.0.0.1:5000/'



def alreadyloggedin(func):
    def inner(request):
        myjwt = request.COOKIES.get('JWT')
        jwtUser = UserProfile.objects.filter(jwtToken = myjwt).first()
        if jwtUser:
            return render(request, 'base/home.html')
        return func(request)
    return inner

# In use
"""
def checkExpiryToken(func):
    def inner(request):
        myjwt = request.COOKIES.get('JWT')
        if not myjwt:
            return redirect('logout')
        elif myjwt:
            jwtUser = UserProfile.objects.filter(jwtToken = myjwt).first()
            if not jwtUser:
                return redirect('logout')
        return func(request)
    return inner
"""

def checkExpiryToken(func):
    def inner(request):
        myjwt = request.COOKIES.get('JWT')
        if not myjwt:
            return redirect('logout')
        elif myjwt:
            jwtUser = UserProfile.objects.filter(jwtToken = myjwt).first()
            if not jwtUser:
                return redirect('logout')
            elif jwtUser:
                is_pc = request.user_agent.is_pc
                is_mobile = request.user_agent.is_mobile
                is_tablet = request.user_agent.is_tablet
                is_touch_capable = request.user_agent.is_touch_capable
                is_bot = request.user_agent.is_bot
                browser_family = request.user_agent.browser.family
                browser_version = request.user_agent.browser.version
                browser_versionstring = request.user_agent.browser.version_string
                os = request.user_agent.os
                osversion = request.user_agent.os.version
                devicefamily = request.user_agent.device.family
                http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ipaddress = request.META.get('REMOTE_ADDR')
                http_user_agent = request.META.get('HTTP_USER_AGENT')
                                
                if is_pc != getattr(jwtUser, 'ispc') or is_mobile != getattr(jwtUser, 'ismobile')\
                            or is_tablet != getattr(jwtUser, 'istablet') \
                            or is_touch_capable != getattr(jwtUser, 'istouchcapable') \
                            or is_bot != getattr(jwtUser, 'isbot') \
                            or str(browser_family) != str(getattr(jwtUser, 'browserfamily')) \
                            or str(browser_version) != str(getattr(jwtUser, 'browserversion')) \
                            or str(browser_versionstring) != str(getattr(jwtUser, 'browserversionstring')) \
                            or str(os) != str(getattr(jwtUser, 'os')) \
                            or str(osversion) != str(getattr(jwtUser, 'osversion')) \
                            or str(devicefamily) != str(getattr(jwtUser, 'devicefamily')) \
                            or str(ipaddress) != str(getattr(jwtUser, 'ipaddress')) \
                            or str(http_user_agent) != str(getattr(jwtUser, 'useragent')):
                            
                                
                    print('redirecting here')

                    print(is_pc,is_mobile,is_tablet,is_touch_capable,is_bot,browser_family,browser_version,browser_versionstring,
                            os,osversion,devicefamily,http_x_forwarded_for,ipaddress,http_user_agent)
                    #or http_x_forwarded_for != getattr(jwtUser, 'http_xforwarded_for') \
                    return redirect('logout')
                
                else:    
                   time = (timesince(jwtUser.updated))
                   minutes = time.find('minutes')
                   day = time.find('day')
                   days = time.find('days')
                   
                   if day != -1:
                       return redirect('logout')
                   elif days != -1:
                       return redirect('logout')
                   elif minutes >= 0:
                       value = int(time[0])
                       if value >= 28:
                           return redirect('logout')
                                               
        return func(request)
    return inner



def updatelogininfo(request, email, jwt, founduser = None):

    ispc = request.user_agent.is_pc
    ismobile = request.user_agent.is_mobile
    istablet = request.user_agent.is_tablet
    istouchcapable = request.user_agent.is_touch_capable
    isbot = request.user_agent.is_bot
    browserfamily = request.user_agent.browser.family
    browserversion = request.user_agent.browser.version
    browserversionstring = request.user_agent.browser.version_string
    os = request.user_agent.os
    osversion = request.user_agent.os.version
    devicefamily = request.user_agent.device.family
    http_xforwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ipaddress = request.META.get('REMOTE_ADDR')
    useragent = request.META.get('HTTP_USER_AGENT')

    if founduser:
        record = UserProfile.objects.get(email = email)
        record.jwtToken = jwt
        record.ispc = ispc
        record.ismobile = ismobile
        record.istablet = istablet
        record.istouchcapable = istouchcapable
        record.isbot = isbot
        record.browserfamily = browserfamily
        record.browserversion = browserversion
        record.browserversionstring = browserversionstring
        record.os = os
        record.osversion = osversion
        record.devicefamily = devicefamily
        record.http_xforwarded_for = http_xforwarded_for
        record.ipaddress = ipaddress
        record.useragent = useragent
        record.save()
    else:
        UserProfile.objects.create(
                    email = email,
                    jwtToken = jwt,
                    ispc = ispc,
                    ismobile = ismobile,
                    istablet = istablet,
                    istouchcapable = istouchcapable,
                    isbot = isbot,
                    browserfamily = browserfamily,
                    browserversion = browserversion,
                    browserversionstring = browserversionstring,
                    os = os,
                    osversion = osversion,
                    devicefamily = devicefamily,
                    http_xforwarded_for = http_xforwarded_for,
                    ipaddress = ipaddress,
                    useragent = useragent
                )



@alreadyloggedin
def loginPage(request):
    print('LOGIN')
    page = 'login'
    context = {'page': page} 

    if request.method != 'POST':
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        header = {
            "Content-Type":"application/x-www-form-urlencoded"
        }

        payload = {'username':username,'password':password}

        result = requests.post(apiURL+'login', headers=header, data=payload)

        print('status code', result.status_code)
        if result.status_code == 403:
            messages.error(request, 'Invalid credentials')
            return render(request, 'main.html')
        elif result.status_code == 200:
            data = result.json()
            jwt = data['access_token']
            email = username

            founduser = UserProfile.objects.filter(email = email)
            if founduser:
                updatelogininfo(request, email, jwt, founduser)
            else:
                updatelogininfo(request, email, jwt)

            response = redirect('home')
            #response = render(request, 'base/home.html', context)
            response.set_cookie(key='JWT', value=jwt, max_age=28*60, domain=None, httponly=True)
            return response

    # return render(request, 'base/login_register.html', context)
    return render(request, 'base/home.html', context)



def logoutUser(request):
    jwtfound = request.COOKIES.get('JWT')
    if not jwtfound:
        return redirect('home')
    elif jwtfound:
        response = redirect('home')
        response.delete_cookie('JWT')
        return response


@alreadyloggedin
def registerPage(request):

    if request.method != 'POST':
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
      
        if password1 != password2:
            messages.error(request, 'Passwords did not match')
            return render(request, 'main.html')
        else:
            header = {
                "Content-Type":"application/json"
            }

            payload = {'email':username,'password':password1}

            result = requests.post(apiURL+'user', headers=header, json=payload)
            if result.status_code == 201:
                header = {
                        "Content-Type":"application/x-www-form-urlencoded"
                     }
                payload = {'username':username,'password':password1}

                result = requests.post(apiURL+'login', headers=header, data=payload)
                if result.status_code == 200:
                    data = result.json()
                    jwt = data['access_token']
                    email = username
                    updatelogininfo(request, email, jwt)
    
                    response = redirect('home')
                    response.set_cookie(key='JWT', value=jwt, max_age=28*60, domain=None, httponly=True)
                    return response
            elif result.status_code == 409:
                messages.error(request, 'User already exists')
                return render(request, 'main.html')
                
    #return render(request, 'base/login_register.html')
    return render(request, 'base/home.html')


@checkExpiryToken
def updateUser(request):
    myjwt = request.COOKIES.get('JWT')
    user = UserProfile.objects.get(jwtToken=myjwt) # this is important the get
    form = UserForm()
    form = UserForm(instance=user)
    
    context = {'form': form}
   
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/home.html', context)
    
 

def home(request):
    print('IN home function')
    myjwt = request.COOKIES.get('JWT')
    if not myjwt:
        return render(request, 'base/intro.html')
    
    jwtUser = UserProfile.objects.filter(jwtToken = myjwt).first()
    if jwtUser:
        return render(request, 'base/home.html')
    else:
        return render(request, 'base/intro.html')


@checkExpiryToken
def getscanjobs(request):
    context = {}
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}"
        }
    
    result = requests.get(apiURL+'hash/scanjobs', headers=header)
    if result.status_code == 200:
        data = result.json()    
        context = {'data': data}
    elif result.status_code == 404:
        messages.error(request, 'No Scan submitted by user')

    return render(request, 'base/scanjobs.html', context)


@checkExpiryToken
def getlastscan(request):
    context = {}
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}"
        }
    
    result = requests.get(apiURL+'hash/lastscan', headers=header)
    if result.status_code == 200:
        data = result.json()    
        context = {'data': data}
    elif result.status_code == 404:
        messages.error(request, 'No Scan submitted by user')

    return render(request, 'base/lastscan.html', context)


@checkExpiryToken
def getlastrescan(request):
    context = {}
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}"
        }

    result = requests.get(apiURL+'hash/lastrescan', headers=header)
    if result.status_code == 200:
        data = result.json()    
        context = {'data': data}
    elif result.status_code == 404:
        messages.error(request, 'No ReScan done by user')

    return render(request, 'base/lastrescan.html', context)


@checkExpiryToken
def getscanByJob(request):
    context = {}
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}"
        }  
    if request.method == 'POST':
        val = request.POST.get('JobID')
        if val:
            result = requests.get(apiURL+'hash/scans/'+val, headers=header)
            if result.status_code == 200:
                data = result.json()
                context = {'data': data}
            elif result.status_code == 404:
                 messages.error(request, 'No Scan Job by JobID')
   
    return render(request, 'base/getscan.html', context)


@checkExpiryToken
def getrescanByJob(request):
    context = {}
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}"
        }
    if request.method == 'POST':
        val = request.POST.get('JobID')
        if val:
            result = requests.get(apiURL+'hash/rescans/'+val, headers=header)
            if result.status_code == 200:
                data = result.json()
                context = {'data': data}
            elif result.status_code == 404:
                 messages.error(request, 'No ReScan Job by JobID') 

    return render(request, 'base/getrescan.html', context)


@checkExpiryToken
def connectinfo(request):
    context = {}
    payload = {}
    jwt = request.COOKIES.get('JWT')
    if request.method == 'POST':
        jobdescription = request.POST.get('jobdescription')
        jobid = int(request.POST.get('JobID'))
        print('jobid',jobid)
        if jobid == 0:
            payload = {'jobdescription':jobdescription}
        else:
            payload = {'jobdescription':jobdescription, 'jobid':jobid}

        header = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json"
        }

        result = requests.post(apiURL+'hash/connection', headers=header, json=payload)
        if result.status_code == 403:
            messages.error(request, 'Previous job in process. Wait for sometime to start with new connection info')
        elif result.status_code == 226:
            messages.error(request, 'All ports are in use. Please try after sometime')
        elif result.status_code == 200:
            data = result.json()
            context = {'data': data}
    else:
        context = {'data': None}
        
    return render(request, 'base/connectinfo.html', context)


checkExpiryToken
def deletescanjob(request):
    context = {}
    payload = []
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json"
        }
    if request.method == 'POST':
        listofoptions = request.POST.getlist('inputs')
        if listofoptions:
            for option in listofoptions:
                tempdic = {"jobid": f"{option}"}
                payload.append(tempdic)
            result = requests.delete(apiURL+'hash/deletescanjobs', headers=header, json=payload)
            if result.status_code == 204:
                context = {'message': 'Selected ScanJobs and associated rescans have been removed'}
    
    return render(request, 'base/deletescanjob.html', context)


@checkExpiryToken
def deleterescanjob(request):
    context = {}
    payload = []
    jwt = request.COOKIES.get('JWT')
    header = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json"
        }
    if request.method == 'POST':
        listofoptions = request.POST.getlist('inputs')
        if listofoptions:
            for option in listofoptions:
                tempdic = {"jobid": f"{option}"}
                payload.append(tempdic)
            result = requests.delete(apiURL+'hash/deleterescanjobs', headers=header, json=payload)
            if result.status_code == 204:
                context = {'message': 'Selected ReScan Jobs have been removed'}

    return render(request, 'base/deleterescanjob.html', context)


@checkExpiryToken
def send_file(request):

    dir = settings.BASE_DIR
    filename = 'HashProjectClient.py'    
    # basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # this was working
    #filepath = basedir+ f'/{filename}' # this line and above worked well for filepath
    filepath = os.path.join(dir,filename)    
    path = open(filepath, 'rb')
    #mime_type, _ = mimetypes.guess_type(filepath) # content_type = mime_type below it was
    response = HttpResponse(path, content_type = "application/octet-stream")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
 

