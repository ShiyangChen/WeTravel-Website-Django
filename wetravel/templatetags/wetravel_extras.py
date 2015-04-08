from django import template

from wetravel.models import UserProfile
from django.contrib.auth.models import User

register= template.Library()

@register.inclusion_tag('wetravel/recommend.html')
#recommend to you among your friends who share the same to_visit places
def recommend(user):
  for friend in user.userprofile.fiends.all:
    if friend.to_visit.all & user.userprofile.to_visit.all:
      candidates.append(friend)
	return {'candidates': candidates}