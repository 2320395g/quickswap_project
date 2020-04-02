import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickswap_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from quickswap.models import Trade, Pictures, Comment, UserProfile
from django.utils import timezone

def populate():

    users = [{'username': 'coolguy',
            'email': 'cool@gmail.com'},
            {'username': 'burksA',
            'email': 'adeleBurks1993@gmail.com'},
            {'username': 'bigNIK',
            'email': 'MolloyNikos113@hotmail.com'},
            {'username': 'Alessia!',
            'email': 'alessia.phelps@gmail.com'},
            {'username': 'TheTradeMaster',
            'email': 'sahar_wilks_11@gmail.com'},
            {'username': 'marksman_markham',
            'email': 'daniellamarkham@hotmail.co.uk'},
            {'username': 'JJL',
            'email': 'Jayden-Joyce-Lovett@gmail.com'},
            ]

    userprofiles = [{'user': 'coolguy',
            'description': 'this is my description',
            'picture': 'population_images/sunglasses_guy.jpg'},
            {'user': 'burksA',
            'description': 'Looking for cool vintage stuff!',
            'picture': 'population_images/womanAB.jpg' },
            {'user': 'bigNIK',
            'description': 'I HAVE TOO MUCH STUFF',
            'picture': 'population_images/big_nik.jpg' },
            {'user': 'Alessia!',
            'description': 'Time to Trade!',
            'picture': 'population_images/alessia.jpg' },
            {'user': 'TheTradeMaster',
            'description': 'Whaddaya tradin?',
            'picture': 'population_images/trade_master.jpg' },
            {'user': 'marksman_markham',
            'description': 'Who needs one?',
            'picture': 'population_images/markham.jpg' },
            {'user': 'JJL',
            'description': 'Looking for love.',
            'picture': 'population_images/JJL.jpg' },
            ]

    trades = [{'user': 'coolguy',
            'name': 'DOQAUS Bluetooth Headphones',
            'category': 'electronics',
            'quality': 'battle-scarred',
            'description': 'very cool item, but no longer needed',
            'suggested_trade': 'another electronic item maybe? not fussed.',
            'location': [-4.409959412520465, 55.84680335579537]},
            {'user': 'burksA',
            'name': 'Bookshelf - Antique?',
            'category': 'furniture',
            'quality': 'new',
            'description': 'Wooden bookshelf, comes with extra shelves, possibly antique.',
            'suggested_trade': 'Will wait for offers in comments.',
            'location': [-4.0275166023889994, 55.851113344513834]},
            {'user': 'bigNIK',
            'name': 'Ride on toy car - Lambo',
            'category': 'toys',
            'quality': 'fair',
            'description': 'Got too big so had to upgrade my ride, decent handling, slightly worn tires.',
            'suggested_trade': 'A real lamborghini, open to negotiation/haggling',
            'location': [-3.132554467686788, 55.95861207791498]},
            {'user': 'Alessia!',
            'name': 'Boat - Botnia Targa',
            'category': 'other',
            'quality': 'good',
            'description': 'Small but powerful bot for daily use, pictures: me getting sick air.',
            'suggested_trade': 'Need a bigger boat, so that would be nice. Looking to give this away ASAP!',
            'location': [-0.8043936123177389, 60.80601010256595]},
            {'user': 'TheTradeMaster',
            'name': 'Old book',
            'category': 'books',
            'quality': 'slightly-damaged',
            'description': 'The choice of an avid book collector! It\'s a nice book, mate!',
            'suggested_trade': 'Another book, any I haven\'t read.',
            'location': [-5.006636820034714, 56.79603346780132]},
            {'user': 'marksman_markham',
            'name': 'Denim selection',
            'category': 'clothes',
            'quality': 'good',
            'description': 'My rarely used denim jacket and jean collection, ask in comments about sizes etc.',
            'suggested_trade': 'Maybe a denim hat?',
            'location': [-2.1117825685776097, 57.16302006896015]},
            {'user': 'TheTradeMaster',
            'name': 'Old computer',
            'category': 'electronics',
            'quality': 'battle-scarred',
            'description': 'Got some rare things for trade traders!',
            'suggested_trade': 'Anyone have an old laptop they want rid of?',
            'location': [-4.821152484460924, 56.06054724540664]},
            {'user': 'JJL',
            'name': 'Beautiful painting',
            'category': 'art',
            'quality': 'new',
            'description': 'Masterful canvas painting displaying extreme technical skill, sad to get rid of it.',
            'suggested_trade': 'Please take it from me, I can\'t even sell it.',
            'location': [-6.577134939593833, 57.43633063612921]},
            ]

    comments = [{'trade': 'DOQAUS Bluetooth Headphones',
            'user': 'coolguy',
            'text': 'please someone trade me'},
            {'trade': 'DOQAUS Bluetooth Headphones',
            'user': 'coolguy',
            'text': 'anyone?'},
            {'trade': 'DOQAUS Bluetooth Headphones',
            'user': 'coolguy',
            'text': 'please?',
            'picture': 'population_images/sad.png'},
            {'trade': 'Ride on toy car - Lambo',
            'user': 'coolguy',
            'text': 'trade for this?',
            'picture': 'population_images/jalopy.jpg'},
            {'trade': 'Boat - Botnia Targa',
            'user': 'bigNIK',
            'text': 'Hmm, its a good deal but quite a distance to get too, meet halfway?'},
            {'trade': 'Boat - Botnia Targa',
            'user': 'Alessia!',
            'text': 'No, sorry, until my new boat arrives I can\'t really get to the mainland.'},
            {'trade': 'Boat - Botnia Targa',
            'user': 'bigNIK',
            'text': 'Ahh, fair enough'},
            {'trade': 'Boat - Botnia Targa',
            'user': 'marksman_markham',
            'text': 'Whats the mpg on this?'},
            {'trade': 'Old book',
            'user': 'JJL',
            'text': 'Very interesting, how about a copy of The Dispossessed? I can come to you!',
            'picture': 'population_images/dipossessed.jpg'},
            {'trade': 'Old book',
            'user': 'TheTradeMaster',
            'text': 'Heheh, thank you! I\'ll take it!'},
            {'trade':'Denim selection',
            'user': 'burksA',
            'text': 'What size are the jackets?'},
            {'trade':'Old computer',
            'user': 'burksA',
            'text': 'Is this laptop ok? Its just gathering dust here',
            'picture': 'population_images/laptop.jpg'},
            {'trade':'Old computer',
            'user': 'coolguy',
            'text': 'i got this if thats cool, little scuffed but it works',
            'picture': 'population_images/laptop_2.jpg'},
            {'trade': 'Beautiful painting',
            'user': 'bigNIK',
            'text': 'What a wonderful painting, what medium is this?'},
            {'trade': 'Beautiful painting',
            'user': 'JJL',
            'text': 'Doesn\'t matter...'},
            ]

    pictures = [{'trade': 'DOQAUS Bluetooth Headphones',
            'picture': 'population_images/headphones.jpg'},
            {'trade': 'DOQAUS Bluetooth Headphones',
            'picture': 'population_images/headphones_2.jpg'},
            {'trade': 'Bookshelf - Antique?',
            'picture': 'population_images/bookshelf.jpg'},
            {'trade': 'Bookshelf - Antique?',
            'picture': 'population_images/bookshelf_2.jpg'},
            {'trade': 'Bookshelf - Antique?',
            'picture': 'population_images/bookshelf_3.jpg'},
            {'trade': 'Bookshelf - Antique?',
            'picture': 'population_images/bookshelf_4.jpg'},
            {'trade': 'Ride on toy car - Lambo',
            'picture': 'population_images/lambo.jpg'},
            {'trade': 'Ride on toy car - Lambo',
            'picture': 'population_images/lambo_2.jpg'},
            {'trade': 'Ride on toy car - Lambo',
            'picture': 'population_images/lambo_3.jpg'},
            {'trade': 'Boat - Botnia Targa',
            'picture': 'population_images/boat.jpg'},
            {'trade': 'Boat - Botnia Targa',
            'picture': 'population_images/boat_2.jpg'},
            {'trade': 'Old book',
            'picture': 'population_images/book.jpg'},
            {'trade': 'Denim selection',
            'picture': 'population_images/denim.jpg'},
            {'trade': 'Denim selection',
            'picture': 'population_images/denim_2.jpg'},
            {'trade': 'Old computer',
            'picture': 'population_images/computer.jpg'},
            {'trade': 'Beautiful painting',
            'picture': 'population_images/painting.jpg'},
            ]


    print('Populating Users...')
    for u in users:
        add_user(u['username'], u['email'])

    print('Populating UserProfiles...')
    for up in userprofiles:
        add_userprofile(up['user'], up['description'], up['picture'])

    print('Populating Trades...')
    for t in trades:
        add_trade(t['user'],t['name'],t['category'],t['quality'],
                t['description'],t['suggested_trade'], t['location'])

    print('Populating Pictures...')
    for p in pictures:
        add_picture(p['trade'], p['picture'])

    print('Populating Comments...')
    for c in comments:
        if len(c) == 4:
            add_comment_pic(c['trade'],c['user'],c['text'], c['picture'])
        else:
            add_comment_nopic(c['trade'],c['user'],c['text'])

def add_user(username, email):
    u = User.objects.get_or_create(username = username, email = email, last_login = timezone.now())
    return u

def add_userprofile(user, description, picture):
    up = UserProfile.objects.get_or_create(user = User.objects.get(username = user), description = description,
                picture = picture)
    return up

def add_trade(user, name, category, quality, description, suggested_trade, location):
    t = Trade.objects.get_or_create(user = User.objects.get(username = user),name = name, category = category,
                quality = quality, description = description, suggested_trade = suggested_trade,location = location )
    return t

def add_picture(trade, picture):
    p = Pictures.objects.get_or_create(trade = Trade.objects.get(name = trade), picture = picture)
    return p

def add_comment_pic(trade, user, text, picture):
    c = Comment.objects.get_or_create(trade = Trade.objects.get(name = trade), user = User.objects.get(username = user),
                text = text, picture = picture)
    return c

def add_comment_nopic(trade, user, text):
    c = Comment.objects.get_or_create(trade = Trade.objects.get(name = trade), user = User.objects.get(username = user),
                text = text)
    return c


# Start execution here!
if __name__ == '__main__':
    print('Starting quickswap population script...')
    populate()
    print('Done!')
