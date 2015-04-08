import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetravelproject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from wetravel.models import  *


def populate():
    r = addd_region(country="US", state="Texas", city="Houston")

    place1 = add_place(address ="302 Maze Street", place_type="History", region=r)
    place2 = add_place(address ="61243 Angee Ave", place_type="Nature", region=r)
    place3 = add_place(address ="451 Miop Street", place_type="Nature", region=r)

    user1 = add_user(username="user1")
    user2 = add_user(username="user2")
    user3 = add_user(username="user3")
    user4 = add_user(username="user4")
    user5 = add_user(username="user5")
    user6 = add_user(username="user6")

    profile1 = add_profile(user1)
    profile2 = add_profile(user2)
    profile3 = add_profile(user3)
    profile4 = add_profile(user4)
    profile5 = add_profile(user5)
    profile6 = add_profile(user6)

    profile1.friends.add(profile2, profile3, profile4)
    profile1.to_visit.add(place1)
    profile1.visited.add(place2)
    profile1.save()


    profile2.friends.add(profile5, profile6)
    profile2.to_visit.add(place1)
    profile2.visited.add(place2)
    profile2.save()

    profile3.to_visit.add(place1)
    profile3.visited.add(place3)
    profile3.save()

    profile4.to_visit.add(place2)
    profile4.visited.add(place1)
    profile4.save()

    profile5.to_visit.add(place1)
    profile5.visited.add(place3)
    profile5.save()

    profile6.to_visit.add(place3)
    profile6.visited.add(place1)
    profile6.save()

def addd_region(country, state, city):
    r= Region.objects.get_or_create(country=country, state=state, city=city)[0]
    r.save()
    return r

def add_place(address, place_type, region):
    p = Place.objects.get_or_create(address=address)[0]
    p.place_type = place_type
    p.region = region
    p.save()
    return p

def add_user(username):
    u = User.objects.get_or_create(username=username)[0]
    u.save()
    return u

def add_profile(user):
    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.save()
    return profile
# Start execution here!
if __name__ == '__main__':
    print "Starting wetravelproject population script..."
    populate()