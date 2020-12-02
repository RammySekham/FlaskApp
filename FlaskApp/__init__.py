import flask


def init_ser():
    app = flask.Flask(__name__)
    return app


def init_app():
    app = init_ser()
    """Construct core Flask application with embedded Dash app."""
    with app.app_context():
        # Import parts of our core Flask app
        from . import views
        # Import Dash application
        from .dashapp import dashboard
        app = dashboard.init_dashboard(app)
        return app
