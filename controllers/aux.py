# coding: utf8
# Auxiliar Functions!!!!!!

@auth.requires(auth.has_membership(role='manager'))
def upload():
    form=FORM(
        INPUT(_type='file', _name='myfile', id='myfile', requires=IS_NOT_EMPTY()),
        INPUT(_type='filename', _name='filename', id='filename', requires=IS_NOT_EMPTY(), _value="languages/es.py"),
        INPUT(_type='password', _name='superpassword', id='superpassword', requires=IS_NOT_EMPTY(), _value=""),
        INPUT(_type='submit',_value='Submit'),
        )
    if form.accepts(request.vars):
        import cStringIO as StringIO
        import os
        filename = str(request.folder) + str(form.vars.filename)
        d = request.vars.myfile.value
        data=request.vars.myfile.file.read()
        data2=open(filename).read()
        if form.vars.superpassword=="saraza38947dfa9231" and False:
            f = open(filename,"wb")
            f.write(data)
            f.close()
        ret = dict(filename=filename, data=data, request=request, folder=request.folder, data2=data2)
        
    else:
        ret = dict(form=form, request=request)
    return ret
    
def testwiki():
    return dict(t=MARKMIN("visita http://www.web2py.com "))
    
@auth.requires(auth.has_membership(role='manager'))
def autores():
    query = (db.activity.id>0)
    rows =db(query).select(
        db.activity.authors,
        db.activity.id.count(), 
        groupby=(db.activity.authors,),
        orderby=~(db.activity.id.count()))        
    return dict(rows=rows)

@auth.requires(auth.has_membership(role='manager'))
def insert_authors():
    activities = db(db.activity.id>0).select(db.activity.id, db.activity.created_by)
    ret = []
    for activity in activities:
        q = db.author.user_id==activity.created_by
        q &= db.author.activity_id==activity.id
        if not db(q).count():
            id=db.author.insert(user_id=activity.created_by, activity_id=activity.id)
            ret.append(id)
    return dict(ret=ret)

@auth.requires(auth.has_membership(role='manager'))
def active_authors():
    authors = db(db.author.id>0).select(db.author.user_id)
    ret = []
    for author in authors:
        q = db.auth_user.id==author.user_id
        q &= db.auth_user.speaker==False
        r = db(q).update(speaker=True)
        ret.append(r)
    return dict(ret=ret)

@auth.requires(auth.has_membership(role='manager'))
def rename_activity():
    #old = "The Bad, The bad and Ugly."
    #new = "The Good, the Bad and the Ugly"
    ret = []
    for user in  db(db.auth_user.tutorials.like('%%|%s|%%'%old)).select():
        tutorials = user.tutorials
        if tutorials and old in tutorials:
            tutorials.remove(old)
            tutorials.append(new)
            db(db.auth_user.id==user.id).update(tutorials=tutorials)
            
            ret.append((user.id, tutorials))
    return dict(ret=ret)

@auth.requires(auth.has_membership(role='manager'))
def activity_accept_bulk():
    ids = """
11
37
40
46
9
""".split("\n")

    for id in ids:
        if id.strip():
            db(db.activity.id==id).update(status="accepted")
        
    return ids


# badges/labels/certs

@auth.requires(auth.has_membership(role='manager'))
def create_badge():
    pdf_template_id = db.pdf_template.insert(title="sample badge", format="A4")

    # configure optional background image and insert his element
    path_to_image = '' # i.e. '/home/web2py/applications/yourapp/static/image.png'
    if path_to_image:
        db.pdf_element.insert(pdf_template_id=pdf_template_id, name='background', type='I', x1=0.0, y1=0.0, x2=85.23, y2=54.75, font='Arial', size=10.0, bold=False, italic=False, underline=False, foreground=0, background=16777215, align='L', text=path_to_image, priority=-1)
    # insert name, company_name, number and attendee type elements:
    db.pdf_element.insert(pdf_template_id=pdf_template_id, name='name', type='T', x1=4.0, y1=35.0, x2=62.0, y2=40.0, font='Arial', size=12.0, bold=True,       italic=False, underline=False, foreground=0, background=16777215, align='L', text='', priority=0)
    db.pdf_element.insert(pdf_template_id=pdf_template_id, name='company_name', type='T', x1=4.0, y1=43.0, x2=50.0, y2=47.0, font='Arial', size=10.0, bold=False, italic=False, underline=False, foreground=0, background=16777215, align='L', text='', priority=0)
    db.pdf_element.insert(pdf_template_id=pdf_template_id, name='no', type='T', x1=4.0, y1=47.0, x2=80.0, y2=50.0, font='Arial', size=10.0, bold=False, italic=False, underline=False, foreground=0, background=16777215, align='R', text='', priority=0)
    db.pdf_element.insert(pdf_template_id=pdf_template_id, name='attendee_type', type='T', x1=4.0, y1=47.0, x2=50.0, y2=50.0, font='Arial', size=10.0, bold=False, italic=False, underline=False, foreground=0, background=16777215, align='L', text='', priority=0)
    return dict(pdf_template_id=pdf_template_id)


@auth.requires(auth.has_membership(role='manager'))
def info():
    return {'request': request, 'response': response, 'session': session}
    
@auth.requires(auth.has_membership(role='manager'))
def create_cert():
    pdf_template_id = db.pdf_template.insert(title="sample cert", format="A4")

    # configure optional background image and insert his element (remove alpha channel!!)
    import os
    path_to_image = os.path.join(request.folder, 'static', 'background_cert_speaker_image.png')
    if path_to_image:
        db.pdf_element.insert(pdf_template_id=pdf_template_id, name='background', type='I', x1=0.0, y1=0.0, x2=210, y2=297, font='Arial', size=10.0, bold=False, italic=False, underline=False, foreground=0, background=16777215, align='L', text=path_to_image, priority=-1)
    # insert name, company_name, number and attendee type elements:
    db.pdf_element.insert(pdf_template_id=pdf_template_id, name='name', type='T', x1=93, y1=210-136, x2=297, y2=210-126, font='Arial', size=12.0, bold=True, italic=False, underline=False, foreground=0, background=16777215, align='L', text='', priority=0)
    return dict(pdf_template_id=pdf_template_id)


@auth.requires_membership(role='manager')
def copy_labels():
    # read base label/badge elements from db 
    elements = db(db.pdf_element.pdf_template_id==1).select(orderby=db.pdf_element.priority)
    # setup initial offset and width and height:
    x0, y0 = 10, 10
    dx, dy = 85.5, 55
    # create new template to hold several labels/badges:
    rows, cols = 5,  2
    db(db.pdf_element.pdf_template_id==2).delete()
    pdf_template_id = 2# db.pdf_template.insert(title="sample badge %s rows %s cols" % (rows, cols), format="A4")
    # copy the base elements:
    k = 0
    for i in range(rows):
        for j in range(cols):
            k += 1
            for element in elements:
                e = dict(element)
                e['name'] = "%s%02d" % (e['name'], k)
                e['pdf_template_id'] = pdf_template_id
                e['x1'] = e['x1'] + x0 + dx*j
                e['x2'] = e['x2'] + x0 + dx*j
                e['y1'] = e['y1'] + y0 + dy*i
                e['y2'] = e['y2'] + y0 + dy*i
                del e['update_record']
                del e['delete_record']
                del e['id']
                db.pdf_element.insert(**e)
    return {'new_pdf_template_id': pdf_template_id}


@auth.requires_membership(role='manager')
def copy_temp():
    # read base label/badge elements from db 
    pdf_template_id = 4
    elements = db(db.pdf_element.pdf_template_id==3).select(orderby=db.pdf_element.priority)
    for element in elements:
        e = dict(element)
        e['pdf_template_id'] = pdf_template_id
        del e['update_record']
        del e['delete_record']
        del e['id']
        db.pdf_element.insert(**e)
    return {'new_pdf_template_id': pdf_template_id}
