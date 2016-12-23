"""Test the learning journal."""

import pytest
import transaction

from pyramid import testing

from .models import MyModel
from .models.meta import Base

import datetime
import faker


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a configurator instance,
    builds a testing database, and tears it down. Thank you Nick."""
    settings = {
        'sqlalchemy.url': 'sqlite://:memory:'}
    config = testing.setUp(setting=settings)
    config.include('.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def database_session(configuration, request):
    """Create a session to interact with the testing database."""
    SessonFactory = configuration.registry['dbsession_factory']
    session = SessonFactory()
    egine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def dummy_request(database_session):
    """Instantiate a HTTP request with database session for each new request."""


@pytest.fixture()
def add_models(dummy_request):
    """Add the generated model to the database."""
    dummy_request.dbsession.add_all(POSTS)

Fake = faker.Faker()

POSTS = [MyModel(
    title=Fake.text(3),
    id=i,
    body=Fake.text(30),
    creation_date=datetime.datetime.now(),
) for i in range(20)]



def test_add_post(database_session):
    """Test if database entries are added."""
    database_session.add_all(POSTS)
    assert len(database_session.query(POSTS).all()) == len(POSTS)


def test_empty_list_return(dummy_request, add_models):
    from .views.default import list_view
    view = list_view(dummy_request)
    assert len(view["title"])





# def dummy_request(dbsession):
#     return testing.DummyRequest(dbsession=dbsession)


# class BaseTest(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp(settings={
#             'sqlalchemy.url': 'sqlite:///:memory:'
#         })
#         self.config.include('.models')
#         settings = self.config.get_settings()

#         from .models import (
#             get_engine,
#             get_session_factory,
#             get_tm_session,
#             )

#         self.engine = get_engine(settings)
#         session_factory = get_session_factory(self.engine)

#         self.session = get_tm_session(session_factory, transaction.manager)

#     def init_database(self):
#         from .models.meta import Base
#         Base.metadata.create_all(self.engine)

#     def tearDown(self):
#         from .models.meta import Base

#         testing.tearDown()
#         transaction.abort()
#         Base.metadata.drop_all(self.engine)


# class TestMyViewSuccessCondition(BaseTest):

#     def setUp(self):
#         super(TestMyViewSuccessCondition, self).setUp()
#         self.init_database()

#         from .models import MyModel

#         model = MyModel(name='one', value=55)
#         self.session.add(model)

#     def test_passing_view(self):
#         from .views.default import my_view
#         info = my_view(dummy_request(self.session))
#         self.assertEqual(info['one'].name, 'one')
#         self.assertEqual(info['project'], 'learning_journal')


# class TestMyViewFailureCondition(BaseTest):

#     def test_failing_view(self):
#         from .views.default import my_view
#         info = my_view(dummy_request(self.session))
#         self.assertEqual(info.status_int, 500)
