from typing import Mapping

import flask
from spaas_core.plugins import get_plugin_manager


def scenario_player_services(
    db_name: str = "default",
    test_config: Mapping = None,
    secret: str = "dev",
    config_file: str = "config.py",
):
    """Create a Scenario Player Services Flask app, runnable by a uwsgi framework."""
    app = flask.Flask("Scenario-Player-Services", instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secret, DATABASE=db_name)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(config_file, silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    plugins = get_plugin_manager()
    recipes = plugins.hook.service_recipe()
    for recipe in recipes:
        app = recipe(app)
    return app
