"""Test the learning journal."""


import pytest
import transaction

from pyramid import testing

from learning_journal.models import MyModel, get_tm_session
from learning_journal.models.meta import Base

import datetime
import faker


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a configurator instance.
    builds a testing database, and tears it down. Thank you Nick.
    """
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:'}
    config = testing.setUp(settings=settings)
    config.include('learning_journal.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def database_session(configuration, request):
    """Create a session to interact with the testing database."""
    SessonFactory = configuration.registry['dbsession_factory']
    session = SessonFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def dummy_request(database_session):
    """Instantiate a HTTP request with database session for each new request."""
    return testing.DummyRequest(dbsession=database_session)


@pytest.fixture()
def add_models(dummy_request):
    """Add the generated model to the database."""
    dummy_request.dbsession.add_all(POSTS)

Fake = faker.Faker()

POSTS = [MyModel(
    title=Fake.text(20),
    # id=i,
    body=Fake.text(100),
    creation_date=datetime.datetime.now(),
) for i in range(20)]


# Unit Tests

def test_add_post(database_session):
    """Test if database entries are added."""
    database_session.add_all(POSTS)
    query = database_session.query(MyModel).all()
    print('database contents: ', database_session.query(MyModel).all())
    assert len(query) == len(POSTS)


def test_list_return(dummy_request, add_models):
    """Test that the list view returns 20 entries."""
    from learning_journal.views.default import home_page
    view = home_page(dummy_request)
    assert len(view["entries"]) == 20


def test_empty_list(dummy_request):
    """Test that the list view is empty when no entries are added."""
    from learning_journal.views.default import home_page
    view = home_page(dummy_request)
    assert len(view["entries"]) == 0


def test_correct_entries(database_session, dummy_request, add_models):
    """Test entries are added in the right order with expected content."""
    from learning_journal.views.default import home_page
    home_page(dummy_request)
    query = database_session.query(MyModel).all()
    assert query[0].title == POSTS[0].title


def test_detail_view_content(database_session, dummy_request, add_models):
    """Test that database ids match main list ids."""
    from learning_journal.views.default import detail_page
    dummy_request.matchdict['id'] = 1
    detail_page(dummy_request)
    query = database_session.query(MyModel).all()
    assert query[0].title == POSTS[0].title


def test_edit(database_session, dummy_request, add_models):
    """Test database items can be edited."""
    query = database_session.query(MyModel).first()
    query.title = 'edited title'
    assert query.title == 'edited title'



# Functional tests
@pytest.fixture
def testapp():
    """Create basic symbols to support tests."""
    from webtest import TestApp

    import os
    from pyramid.config import Configurator


    def main(global_config, **settings):
        """ This function returns a Pyramid WSGI application.
        """
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.models')
        config.include('learning_journal.routes')
        config.include('learning_journal.security')
        config.scan()
        return config.make_wsgi_app()


    app = main({}, **{'sqlalchemy.url': 'sqlite:///:memory:'})
    testapp = TestApp(app)

    SessonFactory = app.registry['dbsession_factory']
    engine = SessonFactory().bind
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture()
def fill_the_db(testapp):
    """Fill the database with some model instances."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(POSTS)


def test_empty_db(testapp):
    """Test the home page doesn't have articles if the database is empty."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("article")) == 0


def test_home_route_with_data_has_filled_table(testapp, fill_the_db):
    """When there's data in the database, the home page has rows."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("article")) == 20


def test_detail_data(testapp, fill_the_db):
    """Test that detail shows a database entry."""
    response = testapp.get('/journal/1', status=200)
    html = response.html
    assert html.find_all('article')


def test_new_fields(testapp, fill_the_db):
    """Test that new shows the right fields."""
    response = testapp.get('/journal/1', status=200)
    html = response.html
    assert html.find_all('button')
