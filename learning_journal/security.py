"""Builds authorization and authentication policies."""


import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.security import Allow, Authenticated

from passlib.apps import custom_app_context as pwd_context

# sessions
from pyramid.session import SignedCookieSessionFactory


class NewRoot(object):
    """Builds a root for security policy."""

    def __init__(self, request):
        """Initialize with the request."""
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'cleared')
    ]


def check_credentials(username, password):
    """Check if password and username are correct."""
    if username and password:
        if username == os.environ['AUTH_USERNAME']:
            return pwd_context.verify(password, os.environ['AUTH_PASSWORD'])
    return False


def includeme(config):
    """Configure security."""
    auth_secret = os.environ.get("AUTH_SECRET", "secret_words")
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(NewRoot)
    session_secret = os.environ['SESSION_SECRET']
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
