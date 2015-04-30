import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetravelproject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from wetravel.models import  *


def populate():

    #add region
    r1 = addd_region(country="US", state="Texas", city="Houston")
    r2 = addd_region(country="US", state="Texas", city="Dallas")
    r3 = addd_region(country="US", state="California", city="San Jose")
    
    #add place
    place1 = add_place(address ="302 Maze Street", place_type="City", region=r1)
    place2 = add_place(address ="61243 Angee Ave", place_type="Nature", region=r1)
    place3 = add_place(address ="451 Miop Street", place_type="City", region=r1)
    place4 = add_place(address ="7th Street", place_type="History", region=r2)
    place5 = add_place(address ="132 Bug Ave", place_type="Nature", region=r2)
    place6 = add_place(address ="8922 Jweaz Street", place_type="Nature", region=r2)
    place7 = add_place(address ="392 Moon Street", place_type="History", region=r3)
    place8 = add_place(address ="441 Logse Ave", place_type="City", region=r3)
    place9 = add_place(address ="502 Gooqq Street", place_type="Nature", region=r3)

    #add user
    users = []
    user_profiles = []
    user_names = ["jack1", "moon_walk", "java_leaner", "blair", "clair", "cycy", "jackson", "smile", "sunshine", "grace", "xila", "cece", "melon", "waterrr", "car_dr", "seattle_live", "sheep", "lamp_222", "leaf", "grass", "gezi"]
    user_emails = ["jfoe@gmail.com", "jfoxxx1@hotmail.com", "ojijie@yahoo.com", "ojiafe@126.com", "areoq@gmail.com", "ureauo@hotmail.com", "jcijo@tamu.edu", "pjaifepa@yahoo.com", "jpavvv@amazon.com", "pqjife@ucb.edu", "jppaaaa@jk.com", "ncccccnn@gmail.com", "pp1111@hotmail.com", "zvmi@yahho.com", "vnoivovue@tamu.edu", "joppaa@zz.com", "rearfa@qun.com", "pjifpe@yahhoo.com", "feqww@gmai.com", "qqcc@pp.com", "qvpea@gmail.com"]

    for user_name in user_names:
        user = add_user(username=user_name)
        set_password(user)
        profile = add_profile(user)
        users.append(user)
        user_profiles.append(profile)

    #add email
    for i in range(len(user_names)):
        users[i].email = user_emails[i]
        users[i].save()
    # add friends relationship
    user_profiles[1].friends.add(user_profiles[2],user_profiles[3],user_profiles[4],user_profiles[5],user_profiles[6],user_profiles[7],user_profiles[13],user_profiles[14],user_profiles[15])
    user_profiles[2].friends.add(user_profiles[8],user_profiles[9])
    user_profiles[3].friends.add(user_profiles[9],user_profiles[10])
    user_profiles[4].friends.add(user_profiles[9],user_profiles[11])
    user_profiles[5].friends.add(user_profiles[10],user_profiles[18])
    user_profiles[6].friends.add(user_profiles[12])
    user_profiles[7].friends.add(user_profiles[12],user_profiles[17],user_profiles[19])
    user_profiles[13].friends.add(user_profiles[17],user_profiles[18],user_profiles[19])
    user_profiles[14].friends.add(user_profiles[19])
    user_profiles[15].friends.add(user_profiles[20])

    #add to_visit
    user_profiles[1].to_visit = place1

    #friends
    user_profiles[2].to_visit = place1
    user_profiles[5].to_visit = place2
    user_profiles[13].to_visit = place3
    user_profiles[15].to_visit = place1

    #second-level friends
    user_profiles[8].to_visit = place1
    user_profiles[11].to_visit = place2
    user_profiles[17].to_visit = place3
    user_profiles[20].to_visit = place1
    
    #add visit
    user_profiles[1].visited.add(place4, place6)

    user_profiles[2].visited.add(place4, place6)
    user_profiles[3].visited.add(place4, place5, place3)
    user_profiles[4].visited.add(place1, place2)
    user_profiles[5].visited.add(place6, place7)
    user_profiles[6].visited.add(place1, place4)
    user_profiles[7].visited.add(place6)
    user_profiles[8].visited.add(place2)
    user_profiles[9].visited.add(place3)
    user_profiles[10].visited.add(place7)
    user_profiles[11].visited.add(place9)
    user_profiles[12].visited.add(place9)
    user_profiles[13].visited.add(place9)
    user_profiles[14].visited.add(place2)
    user_profiles[15].visited.add(place7)
    user_profiles[16].visited.add(place2)
    user_profiles[17].visited.add(place1)
    user_profiles[18].visited.add(place2)
    user_profiles[19].visited.add(place4)
    user_profiles[20].visited.add(place7)


    user_profiles[0].avatar = "/images/fry.jpg"
    user_profiles[1].avatar = "/images/1.jpg"
    user_profiles[2].avatar = "/images/2.jpg"
    user_profiles[3].avatar = "/images/3.jpg"
    user_profiles[4].avatar = "/images/4.jpg"
    user_profiles[5].avatar = "/images/5.jpg"
    user_profiles[6].avatar = "/images/6.jpg"
    user_profiles[7].avatar = "/images/7.png"
    user_profiles[8].avatar = "/images/8.jpg"
    user_profiles[9].avatar = "/images/9.jpeg"
    user_profiles[10].avatar = "/images/10.png"
    user_profiles[11].avatar = "/images/11.jpg"
    user_profiles[12].avatar = "/images/12.jpg"
    user_profiles[13].avatar = "/images/13.jpg"
    user_profiles[14].avatar = "/images/14.jpg"
    user_profiles[15].avatar = "/images/15.jpeg"
    user_profiles[16].avatar = "/images/16.jpg"
    user_profiles[17].avatar = "/images/17.jpg"
    user_profiles[18].avatar = "/images/18.jpg"
    user_profiles[19].avatar = "/images/19.jpg"
    user_profiles[20].avatar = "/images/20.jpg"
    
    for user_profile in user_profiles:
        user_profile.save()

    #Add Posts:
    posts = []
    contents = ["Weather ruined plans. Can you help?",
                'Can anyone help me set up a tentative itinerary from scratch? We have 3 boys aged 8, 6, and 3.',
                'When I bought my backpack the trip became real. At 54 I was going to hike Torres del Paine National Park in Patagonia, Chile',
                'Buying it was rejuvenating. Carrying it was even better.',
                'Fantastic cruise and land trip in Alaska',
                'What comes to mind when you think about our largest state: unique world class vistas? ',
                'You can choose your own pace from intense to leisurely, continuing for a longer time or cutting things short.',
                'There is loads to eat- like cattle at feedlots amounts and the quality is good but in no way sensational. ',
                'Two words about equipment provided by Backroads: barely adequate. ',
                'A sidebar note here. Our guides were very good at their jobs. Beyond their technical competence, they were ever patient, attentive, and responsive. ',
                'Where to go in spring break?',
                ' had a lovely house in Christchurch out by the airport (It survived all the earthquakes in one piece because the damage was elsewhere).',
                'I did take the Tranzscenic railroad to the West Coast. Traveling off season (August is winter in NZ). I did not have to reserve seats on the train. I went all the way to Greymouth.',
                'Instead of the expensive helicopter ride, I took a hike to a glacier. It was very slippery over some glacial moraine, but, with the help of some hiking poles',
                'Jaw dropping viewing of wildlife in habitat? Abandon 90% of your hope, all ye who journey here.',
                'I actually was sorry for them after a while though, as they felt the constant need to inflate modest mom.',
                'I made it! I ended up looking down on a glacial lake with lots of icebergs.',
                'Before going to NZ I had arranged a flight to Queenstown so I could do the day tour to Milford Sound. I got very sick the last week of my trip.',
                ' NZ has a lot of work to do to recover from the multiple disasters. It will take years.',
                'Yes, I am glad I did it. Would I do it again? No.',
                'Roma, Roma, Roma',
                ' After a grueling 20 hours of cars, trams, and airplanes we finally made it to Roma, it was beautiful to behold even from the air.',
                'We went to a delightful restaurant close to the Pantheon called "angolette Romano" where we had an amazing and delicious dinner including antipasti, pasta, lemon Veal, wine, and a trio of desserts which completely hit the spot.',
                'The prices were very reasonable and the food was excellent.',
                'We walked from our hotel to the king of Baroque churches called St. Ignacio, the Romans call this the 3D church because the artist Pozzo painted a fake dome which looks very much like a dome if you are standing in the proper place to see it.',
                'Next we head to the Ghetto area to visit the ancient Synagogue and Jewish museum, which is right on the Tiber close to Ponte Fabrizio. ',
                'The Synagogue and Museum are very interesting, we learn that Romes Jews are some of the oldest Romans around; they came here long before the birth of Christ!',
                'The walk back to the hotel is quick, and we see many Romans out for their nightly walk, and people are gathering in squares all over the city.',
                'We hit the pharmacy because I am getting my travel bug, this time it feels like a bad sinus infection with a productive cough!',
                'Transfer to the Port',
                'We all adore Fabrizio; he even brings our friend who is sick on the ship some wine to help her get better. What a guy!',
                'his world-class museum always seems to be under renovation, but most of its collections can still be viewed in its nearly 80 galleries.',
                'Highlights are 18 paintings from the two years when Van Gogh lived in the south of France.',
                'The mountains were shrouded in clouds; we could not see the peaks.',
                'Incredible describes looking out over a vast landscape and seeing herd after herd of majestic elk.',
                'Our hotel did not disappoint, upon entering the lobby you notice a huge moose antler chandelier that hangs over the wooden registration desk carved with an elk and dall sheep.',
                'We chose the Cowboy Steakhouse for supper and was not disappointed, elk sausage appetizer, filet mignon',
                'Saturday\'s excursion is a sunset sled ride to supper, so we chose to check out Teton Village in the morning.',
                'The top had several directions to ski but every one required nerves of steel...what appeared to be straight down.',
                'For southern kids this was a treat. The trip down was a private tour...we were the only two riders with the tram operator.',
                'Saturday we had our planned snowmobile excursion in Yellowstone.',
                'Our guide was a seasoned Wyoming resident, who owns a ranch west of Jackson.',
                'We rode to Old Faithful, parked the snowmobiles. Lunch was served in canvas structures called a Yurt.',
                'Our last excursion was the sled ride at the National Elk Refuge. Jackson Hole Town was built on the winter migration route of elk.',
                'Monday was travel home day. Waiting at the Jackson Hole terminal was so nice, as the Tetons were in full view out the windows.',
                'I remember as a child driving by the abandoned Marineland of the Pacific, an animal seaside theme park. ',
                'The views from every angle are exquisite, offering 270-degree views of the rocky coastline, secluded coves and Catalina Island to the west.',
                'Our day began with a short stroll to The Links at Terranea.',
                ' During the winter-spring seasons, this area is the migration route of the California Gray Whale.',
                'For romantic dinners, the resort offers the Tide Pool Adventure Club from 6 to 10 pm for ages 4 to 12. ',
                'The fresh herbs and produce used each evening are grown in tidy little gardens behind the restaurant. ',
                'Be sure to attend the sunset ritual in the evening on the Lobby Terrace. ',
                'To signify the end of the day a member from Concierge brings out a sacred crystal-singing bowl.',
                'The pure sounds of the crystals resonate to bring harmony and well-being to all who hear the beautiful sound. ',
                ' It\'s a wonderful way to end the day and enjoy an evening at Terranea.',
                'The writer of the most useful, detailed and engaging trip review',
                'HAWAII is beautiful and nothing can take that away, it is paradise.',
                ' have cruised almost every line including some foreign ones and I will be very honest. ',
                'I did not meet one person that thought this cruise was great except for the itinerary. ',
                ' I would suggest pre-renting a car in each port and seeing the islands at your leisure or if you do not want to drive, hire a taxi at each port and ask for a tour of the island.',
                'They are great and they know all the special places to see.',
                ' Be prepared however, they are not what you are used to with other cruises with foreign staff.',
                'Beware and be warned if you book this cruise, I certainly wish I had. ',
                'The city\'s history is epic, with human fossil records dating back more than 230,000 years and evidence of cities in the vicinity of modern-day Beijing as early as the first millennium B.C.',
                'So to make it digestible, let\'s focus on the Beijing now',
                'City buses are shockingly inexpensive, but to ride them successfully you will need to be at least adept in deciphering Chinese pictographs'

                ]
    for user_profile in user_profiles:
            post1 = create_post(user_profile=user_profile)
            post2 = create_post(user_profile=user_profile)
            post3 = create_post(user_profile=user_profile)
            posts.append(post1)
            posts.append(post2)
            posts.append(post3)

    #Add contents to posts:
    for i in range(len(posts)):
        posts[i].text = contents[i]
        posts[i].save()


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

def set_password(user):
    user.set_password("111111")
    user.save()

def add_profile(user):
    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.save()
    return profile

def create_post(user_profile):
    post = Post(publisher=user_profile)
    post.save()
    return post


# Start execution here!
if __name__ == '__main__':
    print "Starting wetravelproject population script..."
    populate()