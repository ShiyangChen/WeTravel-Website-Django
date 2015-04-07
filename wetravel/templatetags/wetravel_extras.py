from django import template

from wetravel.models import UserProfile
from django.contrib.auth.models import User

register= template.Library()

@register.inclusion_tag('wetravel/recommend.html')
#recommend to you among your friends who share the same to_visit places
def recommend(user):
	for future_place in user.userprofile.to_visit.all:
		if future_place:
			for friend in user.userprofile.friends.all:
				if friend:
					for friend_future_place in friend.to_visit.all:
						if friend_future_place:
							if friend_future_place == future_place:
								candidates.append(friend)


	return {'candidates': candidates}