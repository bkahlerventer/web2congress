# -*- coding: utf-8 -*-

# set user selected language (default spanish)

if request.vars.lang: session.lang=request.vars.lang
T.force(session.lang or "es")

# Return service unavailable
# for maintenance

SUSPEND_SERVICE = False
# True for accepting user activity votes
ALLOW_VOTE = False
# call for proposals
CFP = True

######################################
### PARAMETERS
######################################
import datetime
try:
    from gluon.contrib.gql import *
except ImportError:
    is_gae=False
else:
    is_gae=True

VERSION=0.5

# Set available languages:
T.current_languages=['es','es-ar','es-es']

# If Developer Test, turn off email verificaiton and recaptcha checks,
#  db-pooling, use GCO sandbox, etc.:
# DEV_TEST=True   # settings suitable for development work
DEV_TEST=True # Deployed settings

if DEV_TEST:
    DBURI='sqlite://development.db'
    DBPOOLS=0
    # to test translations; example:  http://..../function?force_language=es
    if request.vars.force_language: session.language=request.vars.force_language
    if session.language: T.force(session.language)
else:
    # DBURI set in app_setting_private.py (unversioned file)
    DBURI=None
    DBPOOLS=0

TWITTER_HASH = "pyconar"

response.title=T('web2conf')
response.subtitle=''
response.footer=T("""Conference description<b>dates</b> city (organized by <a href="#">users group</a>). <br/>
More info: <a href="#">blog</a>&nbsp; Contact: <a href="#">mail address</a>""")
response.keywords='python, free software'
response.description=T('Powered by web2py')

# Enable or disable dynamic menu
NAVBAR = False


# GOOGLEMAP_KEY set in app_settings_private.py - here just to ensure definition
GOOGLEMAP_KEY=''

# The following GOOGLE items set in app_settings_private.py - here to ensure defaults:
GOOGLE_MERCHANT_ID=''
GOOGLE_MERCHANT_KEY=''
GOOGLE_SANDBOX=DEV_TEST

# Event link in social networks
LINKEDIN_EVENT = ""
FACEBOOK_EVENT = ""

FOOD_PREFERENCES=('normal','vegetarian','vegan','kosher','halal')
FOOD_PREFERENCES_LABELS=(T('normal'),T('vegetarian'),T('vegan'),T('kosher'),T('halal'))

T_SHIRT_SIZES=('', 'S','M','L','XL','XXL','XXXL',)
T_SHIRT_SIZES_LABELS=(T('no, thanks'),    T("small"),T("medium"),T("large"),T("xlarge"),T("xxlarge"), T("xxxlarge"),)

# TODAY_DATE is here so that comparizons w/ cutoff dates
#  will work properly anywhere in web2conf
# NOTE: we add 6 hours since our server is EST, and this will cover Hawaii
#  will want to have these times be session time local in next rev.
TODAY_DATE=datetime.datetime.today()
PROPOSALS_DEADLINE_DATE=datetime.datetime(2013,10,19,23,59,59)
REVIEW_DEADLINE_DATE=datetime.datetime(2013,7,29,23,59,59)
EARLYBIRD_DATE=datetime.datetime(2013,10,12,23,59,0)
PRECONF_DATE=datetime.datetime(2013,11,2,23,59,0)
FACUTOFF_DATE=datetime.datetime(2013,9,30,23,59,0)
REGCLOSE_DATE=datetime.datetime(2013,11,18,23,59,59)
CONFERENCE_DATE=datetime.datetime(2013,10,24,8,00,00)

SIMPLIFIED_REGISTRATION=False # don't ask password on registration

### fix this ...

ATTENDEE_TYPES=(
 ('gratis',T('Gratuito, $0')),
)

# 
ATTENDEE_TYPE_COST=dict(
     professional=dict(general=250, preconf=195, earlybird=175, speaker=125),
     enthusiast=dict(general=150, preconf=130, earlybird=115,  speaker=85),
     novice=dict(general=85, preconf=75, earlybird=65, speaker=75),
     gratis=dict(general=0, preconf=0, earlybird=0, speaker=0),
   )
ATTENDEE_TYPE_COST[None]=dict(general=0, preconf=0, earlybird=0, speaker=0)

ATTENDEE_TYPE_TEXT=dict(
    professional="t-shirt, catering, closing party, pro listing (micro-sponsor: logo in badge and web site), and other extra goodies",
    enthusiast="t-shirt, catering and other extra goodies",
    novice="t-shirt",
    gratis="badge, certificate, program guide, community magazine and special benefits (subject to availability)",
    )

TUTORIALS_LIST=(
)
TUTORIALS=dict(TUTORIALS_LIST) ### do not remove

TUTORIALS_CAPS={
}

COST_FIRST_TUTORIAL=120.0
COST_SECOND_TUTORIAL=80.0

if CFP:
    ACTIVITY_TYPES = ('talk', 'extreme talk')
else:
    # default activities
    ACTIVITY_TYPES= ('keynote', 'panel', 'plenary',
                 'talk', 'extreme talk', 'poster',
                 'tutorial', 'workshop', 'project',
                 'stand', 'summit', 'open space',
                 'social', 'break', 'lightning talk',
                 'sprint', 'paper', 
                 'special')

ACTIVITY_CATEGORIES=sorted(('py3k','gui','web','cli','herramientas',
                             'lenguaje','fomento','core','educación',
                             'ciencia','académico','comunidad','moviles',
                             'caso de estudio','redes','juegos','seguridad',
                             'testing'))

# override other activities
ACTIVITY_COMMON = ["plenary", "lightning talk", "conference break",  "break", "social"]
ACTIVITY_VOTEABLE = ['keynote', 'talk', 'extreme talk', 'tutorial', 'workshop']
ACTIVITY_REVIEWABLE = ACTIVITY_VOTEABLE + ['poster']

ACTIVITY_LEVELS=("Beginner","Intermediate","Advanced")
ACTIVITY_TRACKS=("General", "Science", "Student Works", "Extreme")
ACTIVITY_DURATION={'talk': 40, 'extreme talk': 30, 'tutorial': 120, 'workshop': 0, 'poster': 0, 'project': 0, 'panel': 45, 'plenary': 60, 'keynote': 60}

# TODO: create a room table (id, name, venue)!
ACTIVITY_ROOMS={1: "Auditorium", 2: "Room A", 3: "Room B", 4: "Room C", 7: "Meeting Room", 0: "-"}
ACTIVITY_ROOMS_ADDRESS={1: "", 2: "", 3: "", 4: "", 0: "-"}

# Estimate room sizes (actual size*attendance factor: 0.30 (talks), *1 for workshops, 0.60 for sprints (shared))
ACTIVITY_ROOMS_EST_SIZES={1: 40, 2: 40, 3: 40, 4: 40, 5: 38, 6: 60, 7: 8, 8: 8, 9: 8, 10: 8, 11: 40, 0: "-"}
ACTIVITY_VENUE=SPAN(A("Main Venue \"Downtown\"", _href=URL(c="venue")))

ACTIVITY_SHOW_DESCRIPTION = False # hide desc to public

ACTIVITY_BACKUP_TO = "pyconar2013@gmail.com"

PROPOSALS_DEADLINE_DATE_PER_ACTIVITY_TYPE={
    'talk': datetime.datetime(2013,6,30,23,59,59),
    'extreme talk': datetime.datetime(2013,6,30,23,59,59),
    'tutorial': datetime.datetime(2013,6,30,23,59,59),
    'keynote': datetime.datetime(2013,9,12,0,0,0),
    'plenary': datetime.datetime(2013,9,12,0,0,0),
    'poster': datetime.datetime(2013,10,19,23,59,59),
    'paper': datetime.datetime(2013,9,12,0,0,0),
    'project': datetime.datetime(2013,10,12,0,0,0),
    'stand': datetime.datetime(2013,10,12,0,0,0),
    'sprint': datetime.datetime(2013,10,12,0,0,0),
    }

ON_PROPOSE_EMAIL = "edvm@fedoraproject.org" #email address list, separated by ";"
PROPOSE_NOTIFY_TEXT = str(T("""Your activity proposal %(activity)s has been recorded.
You can access the current activity information at %(link)s
Thank you"""))
PROPOSE_NOTIFY_SUBJECT = str(T("New activity proposal %(activity)s"))
COMMENT_NOTIFY_TEXT = str(T("""Your activity %(activity)s received a comment by %(user)s:
%(comment)s
"""))
COMMENT_NOTIFY_SUBJECT = str(T("The activity %(activity)s received a comment"))
REVIEW_NOTIFY_TEXT = str(T("A review of your activity %(activity)s has been created or updated by %(user)s."))
REVIEW_NOTIFY_SUBJECT = str(T("Activity %(activity)s review"))
CONFIRM_NOTIFY_TEXT = str(T("""Your activity %(activity)s has been confirmed.
You can access the current activity information at %(link)s"""))
CONFIRM_NOTIFY_SUBJECT = str(T("The activity %(activity)s was confirmed"))

SPONSOR_LEVELS=("Organizer", "Gold", "Silver", "Bronx", "Specials Thanks", "Media", "Adherent")

# verify by email, unless running a developer test:
EMAIL_VERIFICATION= not DEV_TEST
EMAIL_SERVER='localhost:25' #or Configure!
EMAIL_AUTH=None # or 'username:password'
EMAIL_SENDER='pyconar2013@gmail.com'

# on production, mail should be sent by a cron job or similar
# (really, avoid timeout issues and problems like google spam filtering)
MAIL_QUEUE = not DEV_TEST


# for FA applications / communication
FA_EMAIL_UPDATES=True
FA_EMAIL_TO=EMAIL_SENDER

# for testing:
#  disable recaptcha by setting DEV_TEST at the top of this file:
DO_RECAPTCHA= not DEV_TEST
# RECAPTCHA public and private keys are set in app_settings_private.py
#  - here to ensure defaults:
RECAPTCHA_PUBLIC_KEY=''
RECAPTCHA_PRIVATE_KEY=''

# enable to use social networks single-sign-on
JANRAIN = False

# modules
ENABLE_TALKS=True
ENABLE_EXPENSES = False
ENABLE_FINANCIAL_AID = True
ENABLE_PAYMENTS = True
ENABLE_BADGE = True

if DEV_TEST:    # for local development
    HOST='localhost:8000'
    HOST_NEXT='localhost:8000'
else:
    HOST=''
    HOST_NEXT=''

HOTELS=('unknown','Hyatt Regency','Crowne Plaza','other','none')

EMAIL_VERIFY_SUBJECT=str(T("%s Registration Confirmation") % response.title)
EMAIL_VERIFY_BODY=str(T("""
Dear Attendee,\n
To proceed with your registration and verify your email, click on the following link:\n
%s\n--\n%s\n""") % (
 "http://%s%s/%%(key)s" % (request.env.http_host, URL(r=request,f='verify')), 
 response.title))

IMAP_URI = None

PASSWORD_RETRIEVE_SUBJECT=str(T("%s Registration Password") % response.title)
PASSWORD_RETRIEVE_BODY=str(T("Your new password is %(password)s"))
INVOICE_HEADER = "This is a Conference Invoice!!!"

CONFERENCE_URL=None
CONFERENCE_COORDS=-20.2597103,-61.4510078 #-31.2597103,-61.4510078

from misc_utils import COUNTRIES, FLAGS

# caching decorator:

def caching(fn):
    "Special cache decorator (do not cache if user is logged in)"
    if DEV_TEST or request.vars or request.args or response.flash or session.flash or auth.is_logged_in():
        return fn
    else:
        session.forget()    # only if no session.flash (allow to clean it!)
        return cache(request.env.path_info,time_expire=60*5,cache_model=cache.ram)(fn)
