"""Render our views from jinja2 templates."""

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel

import datetime
from pyramid.httpexceptions import HTTPFound

@view_config(route_name='home', renderer='../templates/list.jinja2')
def home_page(request):
    """Render the home page."""
    try:
        query = request.dbsession.query(MyModel)
        entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': entries}


@view_config(route_name="detail", renderer="../templates/detail.jinja2")
def detail_page(request):
    """View the detail page."""
    entry_id = int(request.matchdict['id'])
    query = request.dbsession.query(MyModel)
    entries = query.get(entry_id)
    return {"entries": entries}


@view_config(route_name="edit", renderer="../templates/edit.jinja2")
def edit_page(request):
    """View the edit page."""
    entry_id = int(request.matchdict['id'])
    query = request.dbsession.query(MyModel)
    entries = query.get(entry_id)
    return {"entries": entries}


@view_config(route_name="new", renderer="../templates/new.jinja2")
def new_page(request):
    """View the edit page."""
    if request.method == "POST":
            new_model = MyModel(title=request.POST['title'],
                                body=request.POST['body'],
                                creation_date=datetime.date.today()
                                )
            request.dbsession.add(new_model)
            return HTTPFound(location=request.route_url('home'))
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
