"""Render our views from jinja2 templates."""

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel

import datetime
from pyramid.httpexceptions import HTTPFound
from learning_journal.security import check_credentials
from pyramid.security import remember, forget


@view_config(route_name='home', renderer='../templates/list.jinja2', require_csrf=True)
def home_page(request):
    """Render the home page."""
    try:
        query = request.dbsession.query(MyModel)
        entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=501)
    return {'entries': entries}


@view_config(route_name="detail", renderer="../templates/detail.jinja2", require_csrf=False)
def detail_page(request):
    """View the detail page."""
    entry_id = int(request.matchdict['id'])
    query = request.dbsession.query(MyModel)
    entries = query.get(entry_id)
    return {"entries": entries}


@view_config(route_name="edit", renderer="../templates/edit.jinja2", permission="cleared", require_csrf=False)
def edit_page(request):
    """View the edit page."""
    try:
        data = request.dbsession.query(MyModel).get(request.matchdict['id'])
        if request.method == "POST":
            data.title = request.POST["title"]
            data.body = request.POST["body"]
            request.dbsession.flush()
            return HTTPFound(location=request.route_url('home'))
        return {'entries': data}
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=502)


@view_config(route_name="new", renderer="../templates/new.jinja2", permission="cleared", require_csrf=False)
def new_page(request):
    """View the edit page."""
    print('in new_page')
    try:
        if request.method == "POST":
            # import pdb; pdb.set_trace()
            new_model = MyModel(title=request.POST['title'],
                                body=request.POST['body'],
                                creation_date=datetime.date.today()
                                )
            request.dbsession.add(new_model)
            return HTTPFound(location=request.route_url('home'))
        return {}
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=503)


@view_config(route_name="login", renderer="../templates/login.jinja2", require_csrf=False)
def login_page(request):
    """Log the user in and remembers their credentials."""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=auth_head)
    return {}


@view_config(route_name="logout")
def logout_view(request):
    """Log the user out by forgetting their credentials."""
    auth_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=auth_head)


# @view_config(route_name="api_list", renderer="string")
# def api_list_view(request):
#     expenses = request.dbsession.query(Expense).all()
#     output = [item.to_json() for item in expenses]
#     return output


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
