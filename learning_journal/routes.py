"""Route for learning journal app."""


def includeme(config):
    """Add routes to include in our pyramid app."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('new', '/journal/new-entry')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('edit', '/journal/{id:\d+}/edit-entry')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
