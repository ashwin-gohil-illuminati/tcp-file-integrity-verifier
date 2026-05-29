from operator import contains
from django import template
from ..models import UserProfile
from ..forms import UserForm
import json

register = template.Library()

gmessage = []


def fetchavatar(jwt):

    myavatar = UserProfile.objects.filter(jwtToken=jwt).first()
    return myavatar.avatar.url


def getname(jwt):
    obj = UserProfile.objects.filter(jwtToken=jwt).first()
    if obj:
        emailfield = str(getattr(obj, 'email'))
        name = emailfield.split("@")
        return name[0]


def changeAvatar(request):
    myjwt = request.COOKIES.get('JWT')
    user = UserProfile.objects.get(jwtToken=myjwt) # this is important the get
    avatar = str(getattr(user, 'avatar'))
    data = [{"avatar":avatar}] # list was important
     
    # request.POST = form # special it worked rendered too
    json_object = json.dumps(data, indent=1) # this would'nt be required
    return json.loads(json_object)



register.filter('fetchavatar', fetchavatar)
register.filter('getname', getname)
register.filter('changeAvatar',changeAvatar)
