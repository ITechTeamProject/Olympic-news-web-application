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
        'views':30}, 
        {'title': 'Tokyo 2020 archery day 4: India set to challenge \'unstoppable\' Republic of Korea in men\'s team event',
        'url':'https://olympics.com/tokyo-2020/en/news/tokyo-2020-archery-day-4-india-set-to-challenge-unstoppable-republic-of-korea-in',
        'views':80},]

    athletics_pages = [
        {'title':'Athletes to watch: Noah Lyles',
        'url':'https://olympics.com/tokyo-2020/en/news/athletes-to-watch-noah-lyles',
        'views':110},
        {'title':'Selemon Barega wins men\'s 10,000m in first athletics final of Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/selemon-barega-wins-men-s-10-000m-in-first-athletics-final-of-tokyo-2020',
        'views':60},
        {'title':'How to watch and follow athletics competition for Friday, 30th July at Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/watch-follow-athletics-competition-olympics-tokyo-2020-friday-29-july',
        'views':40},
        {'title':'Canada’s Andre de Grasse gets hands on 200m gold medal adding to Rio 2016 silver',
        'url':'https://olympics.com/tokyo-2020/en/news/canada-s-andre-de-grasse-wins-200m-gold',
        'views':98},
        {'title':'Sydney McLaughlin smashes world record to win gold in women\'s 400m hurdles final',
        'url':'https://olympics.com/tokyo-2020/en/news/sydney-mclaughlin-smashes-world-record-to-win-gold-in-women-s-400m-hurdles-final',
        'views':75} ]

    badminton_pages = [
        {'title':'Tokyo 2020 Olympic badminton draw revealed',
        'url':'https://olympics.com/tokyo-2020/en/news/tokyo-2020-olympic-badminton-draw-revealed',
        'views':120},
        {'title':'Tokyo 2020 Badminton day 10: Men\'s singles and women\'s doubles gold medals at stake',
        'url':'https://olympics.com/tokyo-2020/en/news/tokyo-2020-badminton-day10-finals',
        'views':70}, 
        {'title':'Carolina Marin: Olympic badminton champion to miss Tokyo 2020 with torn ACL',
        'url':'https://olympics.com/tokyo-2020/en/news/carolina-marin-to-miss-tokyo-2020-through-injury',
        'views':90},
        {'title':'JIndonesia\'s Anthony Ginting three wins away from making history',
        'url':'https://olympics.com/tokyo-2020/en/news/indonesia-anthony-ginting-three-wins-away-from-making-history',
        'views':62} ]

    baseball_pages = [
        {'title':'Israel’s baseball team: From dreamers to Olympians',
        'url':'https://olympics.com/tokyo-2020/en/news/israels-baseball-team-from-dreamers-to-olympians',
        'views':34},
        {'title':'Japan name their Olympic Baseball squad for Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/japan-name-their-olympic-baseball-squad-for-tokyo-2020',
        'views':70},
        {'title':'Japan beat Republic of Korea to reach Olympic final ',
        'url':'https://olympics.com/tokyo-2020/en/news/olympics-baseball-japan-south-korea',
        'views':62} ]
    
    basketball_pages = [
        {'title':'Matisse Thybulle: Australian basketball star, artistic defender and vlogging sensation',
        'url':'https://olympics.com/tokyo-2020/en/news/matisse-thybulle-australian-basketball-star-artistic-defender-and-vlogging-sensa',
        'views':75},
        {'title':'Basketball: NBA winners Jrue Holiday and Khris Middleton en route to Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/basketball-nba-winners-jrue-holiday-khris-middleton-route-tokyo-2020',
        'views':53},
        {'title':'Tokyo 2020: When do Kevin Durant and the USA men\'s basketball team play next?',
        'url':'https://olympics.com/tokyo-2020/en/news/usa-basketball-men-kevin-durant-semi-final-next-australia-preview-watch',
        'views':105} ]
    
    diving_pages = [
        {'title':'Jennifer Abel and Melissa Citrini-Beaulieu react after winning synchro diving silver for Canada',
        'url':'https://olympics.com/tokyo-2020/en/news/jennifer-abel-melissa-citrini-beaulieu-canada-synchro-silver-react-tokyo',
        'views':111},
        {'title':'Exceptional People\'s Republic of China win diving gold in synchronised 3m springboard',
        'url':'https://olympics.com/tokyo-2020/en/news/exceptional-china-win-diving-gold-in-synchronised-3m-springboard',
        'views':7} ]

    fencing_pages = [
        {'title':'ROC win women\'s team foil fencing',
        'url':'https://olympics.com/tokyo-2020/en/news/roc-win-women-s-team-foil-fencing',
        'views':65},
        {'title':'Chinese fencer SUN Yiwen wins gold in épée',
        'url':'https://olympics.com/tokyo-2020/en/news/china-sun-yiwen-wins-gold-in-womens-epee-individual-fencing',
        'views':265} ]

    football_pages = [
        {'title':'Women\'s football bronze on the line for Team USA and Australia',
        'url':'https://olympics.com/tokyo-2020/en/news/women-s-football-bronze-on-the-line-for-team-usa-and-australia',
        'views':75},
        {'title':'Brazil rejoices as Marta and Formiga break Olympic football records',
        'url':'https://olympics.com/tokyo-2020/en/news/football-brazil-rejoices-marta-formiga-pele-olympic-records',
        'views':34} ]

    rowing_pages = [
        {'title':'Tokyo 2020 rowing: First women\'s four Olympic champions to be crowned since Barcelona 1992',
        'url':'https://olympics.com/tokyo-2020/en/news/preview-rowing-28-july-tokyo-2020-rowing-day-6-finals',
        'views':21},
        {'title':'Croatia\'s Martin and Valent Sinkovic win men’s pairs gold',
        'url':'https://olympics.com/tokyo-2020/en/news/croatia-martin-and-valent-sinkovic-win-men-pairs-gold',
        'views':26} ]

    shooting_pages = [
        {'title':'Tokyo Olympics: First gold of Games goes to China\'s Yang Qian in shooting',
        'url':'https://www.bbc.co.uk/sport/olympics/57952436',
        'views':593},
        {'title':'Shooting-Zhang sets rifle 3P world record, Quiquampoix wins rapid gold',
        'url':'https://www.reuters.com/world/china/shooting-reitz-primed-title-defence-25m-rapid-fire-pistol-2021-08-02/',
        'views':109} ]

    skateboarding_pages = [
        {'title':'Skateboarding fashion steals the show at Tokyo 2020',
        'url':'https://olympics.com/tokyo-2020/en/news/skateboarding-fashion-steals-the-show-tokyo-2020',
        'views':6},
        {'title':'Tokyo 2020 men\'s street skateboarding final: History on the line in hunt for first-ever skateboarding gold',
        'url':'https://olympics.com/tokyo-2020/en/news/tokyo-2020-men-s-street-skateboarding-final-history-on-the-line-in-hunt-for-firs',
        'views':12} ]

    table_tennis_pages = [
        {'title':'ISHIKAWA Kasumi plans to shake up table tennis table with newfound skills',
        'url':'https://olympics.com/tokyo-2020/en/news/ishikawa-kasumi-plans-to-shake-up-table-tennis-table-with-newfound-skills',
        'views':54},
        {'title':'Ma Long wins 2nd Olympic gold in men’s table tennis',
        'url':'https://apnews.com/article/2020-tokyo-olympics-sports-mens-table-tennis-ma-long-china-olympic-team-b5a29ee5b068fba5c7f3746587372eee',
        'views':372} ]
        

    archery_teams = [
        {'country':'Canada', 'likes':1125 },
        {'country':'Japan',  'likes':2052 },
        {'country':'People\'s Republic of China', 'likes':5242 },
        {'country':'Australia',  'likes': 3224  },
        {'country':'France',   'likes': 642  },
        {'country':'Germany',  'likes':1723 },
        {'country':'United States',  'likes':3407 },
        {'country':'Great Britain',  'likes':2727 },
        {'country':'Ukraine', 'likes':37 },
        {'country':'Netherlands', 'likes':1732 },
        {'country':'Switzerland', 'likes':234  }
    ]
    athletics_teams = [
        {'country':'Finland',  'likes':1241     },
        {'country':'Brazil',    'likes':234     },
        {'country':'People\'s Republic of China',     'likes':4772    },
        {'country':'Australia',      'likes': 2341    },
        {'country':'France',    'likes': 2323    },
        {'country':'ROC',      'likes':3231    },
        {'country':'United States',      'likes':4407      },
        {'country':'Great Britain',      'likes':2727      },
        {'country':'Jamaica',      'likes':2722      },
        {'country':'Poland',      'likes':732      },
        {'country':'Denmark', 'likes':1122},
        {'country':'Sweden', 'likes': 875}
    ]
    badminton_teams = [
        {'country':'Canada', 'likes':112 },
        {'country':'Japan',  'likes':202 },
        {'country':'People\'s Republic of China', 'likes':3242 },
        {'country':'Australia',  'likes': 1234  },
        {'country':'France',   'likes': 623  },
        {'country':'Germany',  'likes':1734 },
        {'country':'United States',  'likes':3107 },
        {'country':'Great Britain',  'likes':2727 },
        {'country':'Denmark', 'likes':231 },
        {'country':'ROC', 'likes':1732 },
        {'country':'Republic of Korea', 'likes':234  }
    ]
    baseball_teams = [
        {'country':'Canada', 'likes':1121 },
        {'country':'Japan',  'likes':2022},
        {'country':'Australia',  'likes': 1254  },
        {'country':'France',   'likes': 823  },
        {'country':'Germany',  'likes':1734 },
        {'country':'United States',  'likes':3107 },
        {'country':'Great Britain',  'likes':2747 },
        {'country':'Denmark', 'likes':576 },
        {'country':'ROC', 'likes':1732 },
        {'country':'Republic of Korea', 'likes':214  }
    ]
    basketball_teams = [
        {'country':'Canada', 'likes':1122 },
        {'country':'United States',  'likes':2024 },
        {'country':'People\'s Republic of China', 'likes':1562 },
        {'country':'Australia',  'likes': 1234  },
        {'country':'France',   'likes': 623  },
        {'country':'Germany',  'likes':1734 },
        {'country':'Poland',      'likes':732      },
        {'country':'Denmark', 'likes':1122},
        {'country':'Sweden', 'likes': 875}
    ]
    diving_teams = [
        {'country':'United States',  'likes':2307 },
        {'country':'Great Britain',  'likes':1747 },
        {'country':'Denmark', 'likes':763 },
        {'country':'ROC', 'likes':1532 },
        {'country':'Republic of Korea', 'likes':814  },
        {'country':'People\'s Republic of China', 'likes':1962 },
        {'country':'Australia',  'likes': 1934  },
        {'country':'Netherlands', 'likes':132 },
        {'country':'Switzerland', 'likes':234  }
    ]
    fencing_teams = [
        {'country':'United States',  'likes':2307 },
        {'country':'Great Britain',  'likes':1747 },
        {'country':'Denmark', 'likes':763 },
        {'country':'ROC', 'likes':1532 },
        {'country':'Republic of Korea', 'likes':814  },
        {'country':'People\'s Republic of China', 'likes':1962 },
        {'country':'Australia',  'likes': 1934  },
        {'country':'Netherlands', 'likes':132 },
        {'country':'Switzerland', 'likes':234  }
    ]
    football_teams = [
        {'country':'United States',  'likes':2307 },
        {'country':'Great Britain',  'likes':1747 },
        {'country':'Denmark', 'likes':763 },
        {'country':'ROC', 'likes':1532 },
        {'country':'Republic of Korea', 'likes':814  },
        {'country':'People\'s Republic of China', 'likes':1962 },
        {'country':'Australia',  'likes': 1934  },
        {'country':'Netherlands', 'likes':132 },
        {'country':'Switzerland', 'likes':234  }
    ]
    rowing_teams = [
        {'country':'United States',  'likes':2307 },
        {'country':'Great Britain',  'likes':1747 },
        {'country':'Denmark', 'likes':763 },
        {'country':'ROC', 'likes':1532 },
        {'country':'Republic of Korea', 'likes':814  },
        {'country':'People\'s Republic of China', 'likes':1962 },
        {'country':'Australia',  'likes': 1934  },
        {'country':'Netherlands', 'likes':132 },
        {'country':'Switzerland', 'likes':234  }
    ]
    shooting_teams = [
        {'country':'United States',  'likes':2307 },
        {'country':'Great Britain',  'likes':1747 },
        {'country':'Denmark', 'likes':763 },
        {'country':'ROC', 'likes':1532 },
        {'country':'Republic of Korea', 'likes':814  },
        {'country':'People\'s Republic of China', 'likes':1962 },
        {'country':'Australia',  'likes': 1934  },
        {'country':'Netherlands', 'likes':132 },
        {'country':'Switzerland', 'likes':234  }
    ]
    skateboarding_teams = [
        {'country':'United States',  'likes':2307 },
        {'country':'Great Britain',  'likes':1747 },
        {'country':'Denmark', 'likes':763 },
        {'country':'ROC', 'likes':1532 },
        {'country':'Republic of Korea', 'likes':814  },
        {'country':'People\'s Republic of China', 'likes':1962 },
        {'country':'Australia',  'likes': 1934  },
        {'country':'Netherlands', 'likes':132 },
        {'country':'Switzerland', 'likes':234  }
    ]
    table_tennis_teams = [
        {'country':'United States',  'likes':2307 },
        {'country':'Great Britain',  'likes':1747 },
        {'country':'Japan', 'likes':2353 },
        {'country':'ROC', 'likes':1532 },
        {'country':'Germany', 'likes':3732  },
        {'country':'People\'s Republic of China', 'likes':7362 },
        {'country':'Australia',  'likes': 1934  },
        {'country':'Netherlands', 'likes':132 },
        {'country':'Switzerland', 'likes':234  }
    ]

    cats = {'Archery': {'pages': archery_pages, 'teams': archery_teams, 'views': 1281, 'likes': 64},
            'Athletics': {'pages': athletics_pages, 'teams': athletics_teams,'views': 5056, 'likes': 32}, 
            'Badminton': {'pages': badminton_pages, 'teams': badminton_teams,'views': 3242, 'likes': 16},
            'Baseball': {'pages': baseball_pages, 'teams': baseball_teams,'views': 323, 'likes': 16},
            'Basketball': {'pages': basketball_pages, 'teams': basketball_teams,'views': 2224, 'likes': 18},
            'Diving': {'pages': diving_pages, 'teams': diving_teams,'views': 1723, 'likes': 10},
            'Fencing': {'pages': fencing_pages, 'teams': fencing_teams,'views': 1532, 'likes': 13},
            'Football': {'pages': football_pages, 'teams': football_teams,'views': 1713, 'likes': 43},
            'Rowing': {'pages': rowing_pages, 'teams': rowing_teams,'views': 226, 'likes': 54},
            'Shooting': {'pages': shooting_pages, 'teams': shooting_teams,'views': 1584, 'likes': 64},
            'Skateboarding': {'pages': skateboarding_pages, 'teams': skateboarding_teams,'views': 174, 'likes': 10},
            'Table Tennis': {'pages': table_tennis_pages, 'teams': table_tennis_teams,'views': 3622, 'likes': 36},}

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

    # Print out the sports and teams we have added.
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