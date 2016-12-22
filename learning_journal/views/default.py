from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home_page(request):
    try:
        query = request.dbsession.query(MyModel)
        entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': entries}


# view_config(route_name="home", renderer="../templates/list.jinja2")
# def home_page(request):
#     """View the home page."""
#     return {"entries": ENTRIES}


# # This is from class, the rest are just copied
# @view_config(route_name="create",
#     renderer="../templates/form.jinja2")
# def create_view(request):
#     # import pdb; pdb.set_trace()
#     if request.method == "POST":
#         #get the form stuff
#         return {}
#     return {}


# @view_config(route_name="detail", renderer="../templates/detail.jinja2")
# def detail_page(request):
#     """View the detail page."""
#     entry_id = int(request.matchdict[0])
#     # entry_id = int(request.matchdict['id'])
#     return {"entries": ENTRIES[entry_id - 1]}


# @view_config(route_name="edit", renderer="../templates/edit.jinja2")
# def edit_page(request):
#     """View the edit page."""
#     entry_id = int(request.matchdict[0])
#     # entry_id = int(request.matchdict['id'])
#     return {"entries": ENTRIES[entry_id - 1]}


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
