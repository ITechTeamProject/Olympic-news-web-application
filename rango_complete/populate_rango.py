import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rango_complete.settings') 
import django
django.setup()
from rango.models import Category, Page, Team

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    archery_pages = [
        {'title': 'Tokyo 2020 archery day 8: KANG and Kumari shoot for gold in women\'s individual final',
        'url':'https://olympics.com/tokyo-2020/en/news/tokyo-2020-archery-day-8-kang-and-kumari-shoot-for-gold-in-women-s-individual-fi',
        'views':100},
        {'title':'Tokyo 2020 archery - Republic of Korea favourites for women\'s team title on Day 3',
        'url':'https://olympics.com/tokyo-2020/en/news/tokyo-2020-day-3-women-s-team-archery-final',
        'views':50},
        {'title':'Republic of Korea wins archery women\'s team gold for ninth straight Games',
        'url':'https://olympics.com/tokyo-2020/en/news/republic-of-korea-wins-archery-women-s-team-gold-for-ninth-straight-games',
        'views':30} ]

    athletics_pages = [
        {'title':'Athletes to watch: Noah Lyles',
        'url':'https://olympics.com/tokyo-2020/en/news/athletes-to-watch-noah-lyles',
        'views':110},
        {'title':'Selemon Barega wins men\'s 10,000m in first athletics final of Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/selemon-barega-wins-men-s-10-000m-in-first-athletics-final-of-tokyo-2020',
        'views':60},
        {'title':'How to watch and follow athletics competition for Friday, 30th July at Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/watch-follow-athletics-competition-olympics-tokyo-2020-friday-29-july',
        'views':40} ]

    badminton_pages = [
        {'title':'Tokyo 2020 Badminton day 9: Women\'s singles gold, men\'s singles semi-finals',
        'url':'http://bottlepy.org/docs/dev/',
        'views':120},
        {'title':'Tokyo 2020 Badminton day 8: Men\'s doubles set to reach exciting conclusion',
        'url':'http://flask.pocoo.org',
        'views':70} ]

    baseball_pages = [
        {'title':'Israel’s baseball team: From dreamers to Olympians',
        'url':'https://olympics.com/tokyo-2020/en/news/israels-baseball-team-from-dreamers-to-olympians',
        'views':34},
        {'title':'Japan name their Olympic Baseball squad for Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/japan-name-their-olympic-baseball-squad-for-tokyo-2020',
        'views':70} ]
    
    basketball_pages = [
        {'title':'Matisse Thybulle: Australian basketball star, artistic defender and vlogging sensation',
        'url':'https://olympics.com/tokyo-2020/en/news/matisse-thybulle-australian-basketball-star-artistic-defender-and-vlogging-sensa',
        'views':105},
        {'title':'Basketball: NBA winners Jrue Holiday and Khris Middleton en route to Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/basketball-nba-winners-jrue-holiday-khris-middleton-route-tokyo-2020',
        'views':23} ]
    
    diving_pages = [
        {'title':'Jennifer Abel and Melissa Citrini-Beaulieu react after winning synchro diving silver for Canada',
        'url':'https://olympics.com/tokyo-2020/en/news/jennifer-abel-melissa-citrini-beaulieu-canada-synchro-silver-react-tokyo',
        'views':111},
        {'title':'Exceptional People\'s Republic of China win diving gold in synchronised 3m springboard',
        'url':'https://olympics.com/tokyo-2020/en/news/exceptional-china-win-diving-gold-in-synchronised-3m-springboard',
        'views':7} ]

    archery_teams = [
         {'country':'Canada',
          'likes':1125},
         {'country':'Janpan',
          'likes':225},
         {'country':'People\'s Republic of China',
          'likes':5217}
    ]

    cats = {'Archery': {'pages': archery_pages, 'teams': archery_teams, 'views': 128, 'likes': 64},
            'Athletics': {'pages': athletics_pages, 'teams': archery_teams,'views': 64, 'likes': 32}, 
            'Badminton': {'pages': badminton_pages, 'teams': archery_teams,'views': 32, 'likes': 16},
            'Baseball': {'pages': baseball_pages, 'teams': archery_teams,'views': 32, 'likes': 16},
            'Basketball': {'pages': basketball_pages, 'teams': archery_teams,'views': 30, 'likes': 18},
            'Diving': {'pages': diving_pages, 'teams': archery_teams,'views': 34, 'likes': 10},}

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
        for t in cat_data['teams']:
            add_team(c, t['country'], t['likes'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
        for t in Team.objects.filter(name=c):
            print(f'- {c}: {t}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_team(cat, country, likes=0):
    t = Team.objects.get_or_create(name=cat, country=country)[0]
    t.likes = likes
    t.save()
    return t

#Start execustion here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

