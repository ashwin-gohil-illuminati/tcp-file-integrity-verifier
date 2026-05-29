from django import template
from ..models import UserProfile

register = template.Library()


def tokenAuthentication(jwt):
    jwtUser = UserProfile.objects.filter(jwtToken = jwt).first()
    if jwtUser:
        return True
    else:
        return False


def getuser(jwt):
    jwtUser = UserProfile.objects.filter(jwtToken = jwt).first()

    if jwtUser:
        return jwtUser.email


register.filter('tokenAuthentication', tokenAuthentication)
register.filter('getuser', getuser)