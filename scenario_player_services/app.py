from typing import Mapping

from spaas_core.utils import construct_flask_app
from spaas_rpc.app import spaas_rpc_service


def scenario_player_services(
    db_name: str = "default",
    test_config: Mapping = None,
    secret: str = "dev",
    config_file: str = "config.py",
):
    """Create a Scenario Player Services Flask app, runnable by a uwsgi framework."""
    app = construct_flask_app(db_name=db_name, test_config=test_config, secret=secret, config_file=config_file)
    app = spaas_rpc_service(app)
    return app
