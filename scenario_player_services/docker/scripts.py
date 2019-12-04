import subprocess
import argparse
from importlib import resources

parser = argparse.ArgumentParser(
    description="Start or stop all available SPaaS services on this machine. "
                "Services are run on port 5100 by default.",
)
parser.add_argument("command", choices=["up", "down"])


def manage_services():
    args = parser.parse_args()
    data_module = "scenario_player_services.docker"
    with resources.path(data_module, "docker-compose.yml") as compose_fpath:
        docker_command = ["docker-compose", "-f", str(compose_fpath), args.command]
        if args.command == "up":
            # Bring services up in the background
            docker_command.append("-d")
        subprocess.run(docker_command, check=True)
