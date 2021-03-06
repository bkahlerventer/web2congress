#############################################
### FOR ALL ATTENDEES
#############################################

def index():
    redirect(URL("attendees"))
    
@caching
def companies():
    if auth.has_membership(role='manager'): s=db()
    else: s=db(db.auth_user.include_in_delegate_listing==True)
    rows=s.select(db.auth_user.company_name,
                  db.auth_user.company_home_page,
                  orderby=db.auth_user.company_name,distinct=True)
    d = dict(rows=rows)
    return response.render(d)
    
@caching
def attendees():
    import unicodedata
    s=db((db.auth_user.include_in_delegate_listing==True)&(db.auth_user.attendee_type!='non_attending')&(db.auth_user.amount_due==0.0))
    rows=s.select(db.auth_user.ALL,
                  orderby=db.auth_user.first_name|db.auth_user.last_name)
    ret = {}
    # avoid duplicates (remove spaces, acents, etc)
    for row in rows:
        name = ''.join([l.lower() for l in (row.first_name+row.last_name) if l.isalpha()])
        name = unicodedata.normalize('NFD', unicode(name, 'utf8'))
        if name in ret: continue
        ret[name] = row
    d = dict(rows=sorted(ret.values()))
    return response.render(d) 


from misc_utils import COLORS

def barchart(data,width=400,height=15,scale=None,
             label_width=50,values_width=50):
    if not scale:
        try:
            scale=max([m for n,c,m in data])
        except ValueError:
            # empty sequence
            scale=None
    if not scale: return None
    return TABLE(_class='barchart',
           *[TR(TD(n,_width=label_width,_style="text-align: right"),
           TABLE(TR(TD(_width=int(m*width/scale),_height=height,
           _style='background-color:'+c))),TD(m,_width=values_width),
           _style="vertical-alignment: middle") for n,c,m in data])

def colorize(d,sort_key=lambda x:x):
    s=[(m,n) for n,m in d.items()]
    s.sort(key=sort_key)
    s.reverse()
        
    t=[(x[1],COLORS[i % len(COLORS)],x[0]) for i,x in enumerate(s)]
    return barchart(t,label_width=150)   

@caching
def charts():    
    cn=[]
    if auth.has_membership(role='manager'): 
        q = db.activity.id>0
    else:
        q = db.activity.status=='accepted'
        q &= db.activity.type=='talk'
    tutorials = [row.title for row in db(q).select()]    
    if not is_gae:
        for k,item in enumerate(tutorials):
            m=db(db.auth_user.tutorials.like('%%|%s|%%'%item)).count()
            try:
                color = COLORS[k]
            except IndexError:
                color = ""
            cn.append((item,color,m))
    else:        
        cn2={}
        for row in db(db.auth_user.id>0).select(db.auth_user.tutorials):
            for item in tutorials:
                    if not cn2.has_key(item): cn2[item]=0
                    if row.tutorials.find('|%s|'%item)>=0: cn2[item]+=1
        for k,item in enumerate(tutorials):
                cn.append((TUTORIALS[item],COLORS[k],cn2[item]))
                k+=1
    cn.sort(key=lambda x: x[-1], reverse=True) 

    chart_tutorials=barchart(cn,label_width=150)

    country={}
    city={}
    state={}
    food_preference={}
    t_shirt_size={}
    attendee_type={}
    attendee_levels={}
    registration_date={}
    certificates={}
    for row in db().select(db.auth_user.ALL):
        country[row.country]=country.get(row.country,0)+1
        city[row.city.lower()]=city.get(row.city.lower(),0)+1
        state[row.state.lower()]=state.get(row.state.lower(),0)+1
        #food_preference[row.food_preference]=food_preference.get(row.food_preference,0)+1
        #t_shirt_size[row.t_shirt_size]=t_shirt_size.get(row.t_shirt_size,0)+1
        attendee_type[row.attendee_type]=attendee_type.get(row.attendee_type,0)+1
        attendee_levels[row.level]=attendee_levels.get(row.level,0)+1
        registration_date[row.created_on.date()]=registration_date.get(row.created_on.date(),0)+1
        certificates[row.certificate]=certificates.get(row.certificate,0)+1
    chart_country=colorize(country)
    chart_state=colorize(state)
    chart_city=colorize(city)
    chart_food_preference=None #colorize(food_preference)
    chart_t_shirt_size=None #colorize(t_shirt_size)
    chart_attendee_type=colorize(attendee_levels)
    chart_registration_date=colorize(registration_date,sort_key=lambda x: x[1]) #colorize(attendee_type)
    chart_certificates=colorize(certificates) #colorize(attendee_type)

    d = dict(chart_tutorials=chart_tutorials,
                chart_country=chart_country,
                chart_food_preference=chart_food_preference,
                chart_t_shirt_size=chart_t_shirt_size,
                chart_city=chart_city,
                chart_state=chart_state,
                chart_attendee_type=chart_attendee_type,
                chart_registration_date=chart_registration_date,
                chart_certificates=chart_certificates
                )
    return response.render(d)
    
@caching
def brief():    
    cn=[]

    activity_status={}
    activity_types={}
    activity_levels={}
    activity_categories={}
    for row in db().select(db.activity.ALL):
        status = "%s%s" % (row.status, row.confirmed and " (confirmed)" or "")
        activity_status[status]=activity_status.get(status,0)+1
        if not request.args or request.args[0] == row.status:
            activity_types[row.type]=activity_types.get(row.type,0)+1
            activity_levels[row.level]=activity_levels.get(row.level,0)+1
            for category in row.categories:
                activity_categories[category]=activity_categories.get(category,0)+1
    chart_status=colorize(activity_status)
    chart_type=colorize(activity_types)
    chart_level=colorize(activity_levels)
    chart_categories=colorize(activity_categories)

    authors_country={}
    q = db.auth_user.id==db.author.user_id
    q &=db.activity.id==db.author.activity_id
    q &= db.auth_user.country != None
    if request.args and request.args[0] in ("accepted", "rejected", "pending", "declined"): 
        q &=db.activity.status==request.args[0]
    for row in db(q).select(db.auth_user.id, db.auth_user.country, groupby=db.auth_user.id):
        authors_country[row.country]=authors_country.get(row.country,0)+1
    chart_country=colorize(authors_country)

    d = dict(chart_status=chart_status,
                chart_type=chart_type,
                chart_level=chart_level,
                chart_categories=chart_categories,
                chart_country=chart_country,
                )
    return response.render(d)

@caching
def maps():
    rows=db(db.auth_user.id>0).select(
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.auth_user.latitude,
            db.auth_user.longitude,
            db.auth_user.personal_home_page,
            db.auth_user.include_in_delegate_listing)
    x0,y0=CONFERENCE_COORDS
    d = dict(googlemap_key=GOOGLEMAP_KEY,x0=x0,y0=y0,rows=rows)
    return response.render(d)
