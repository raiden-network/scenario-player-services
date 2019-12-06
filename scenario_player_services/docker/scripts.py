import argparse
import pathlib
import subprocess
from importlib import resources
from typing import List

#: Tag of the container which is built by `scenario-player-services build`.
CONTAINER_TAG = "raidennetwork/scenario-player-services:local"

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="commands", dest="command")

#: Parser for the `scenario-player-services services` command.
services_parser = subparsers.add_parser(
    "services",
    description="Start or Stop SP Services in a docker-compose pod. "
    "Any options given and not listed here will be passed "
    "on to `docker-compose`",
)
services_parser.add_argument(
    "state",
    choices=["up", "down"],
    help="Bring the composes services up or down. When specifying `up`, the '-d' "
    "flag is implied and cannot be unset.",
)

#: Parser for the `scenario-player-services build` command.
build_parser = subparsers.add_parser(
    "build",
    description=f"Build a container tagged {CONTAINER_TAG}, which is executable "
    "and starts the scenario player services as a single flask app "
    "via `waitress-serve`. Any options given and not listed here will"
    "be passed on to `docker build`; passing `-t` and `-f` will"
    "result in an error, as we already pass those flags. Finally, "
    "the build context will always be the current directory, so make"
    "sure you are in a valid scnear-player-services git repository.",
)

#: Parser for the `scenario-player-services show` command.
files_parser = subparsers.add_parser(
    "show", description="Print the full file paths to the specified data file."
)
files_parser.add_argument(
    "option",
    choices=["services", "build"],
    help="Specify the cli option you'd like to see the fpath of the related file for.",
)


def return_fpath_for_docker_file(fname: str) -> pathlib.Path:
    """Return the path of the specified file to be found in :mod:`scneario_player_services.docker`.

    If the file does not exist, this will throw an exception.
    """
    data_module = "scenario_player_services.docker"
    with resources.path(data_module, fname) as fpath:
        return fpath


def compose_command(cli_args: argparse.Namespace, docker_args: List[str]) -> List[str]:
    """Construct the underlying command of `scenario-player-services up|down`.

    `docker_args` is a list of strings parsed from the argument parser (but not
    known to it) and is treated as a list of additional options to be appended
    to the final command list.

    Returns a list which can be passed to :func:`subprocess.run`.
    """
    compose_file = str(return_fpath_for_docker_file("docker-compose.yml"))
    command_list = ["docker-compose", "-f", compose_file, cli_args.state]
    if cli_args.state == "up":
        command_list.append("-d")
    return command_list + docker_args


def build_command(cli_args: argparse.Namespace, docker_args: List[str]) -> List[str]:
    """Construct the underlying command of `scenario-player-services build`.

    `docker_args` is a list of strings parsed from the argument parser (but not
    known to it) and is treated as a list of additional options to be appended
    to the final command list.

    Returns a list which can be passed to :func:`subprocess.run`.
    """
    dockerfile = str(return_fpath_for_docker_file("Dockerfile"))
    command_list = ["docker", "build", "-f", dockerfile, "-t", CONTAINER_TAG] + docker_args + ["."]
    return command_list


def manage_services():
    args, docker_args = parser.parse_known_args()

    if args.command == "show":
        if args.option == "services":
            print(return_fpath_for_docker_file("docker-compose.yml").resolve())
        else:
            print(return_fpath_for_docker_file("Dockerfile").resolve())
        exit(0)

    if args.command == "services":
        command_list = compose_command(args, docker_args)
    else:
        command_list = build_command(args, docker_args)
    subprocess.run(command_list, check=True)
