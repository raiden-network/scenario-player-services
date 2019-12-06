FROM python:3.7
LABEL maintainer=contact@brainbot.li
LABEL org.label-schema.name="Raiden Scenario Player Services"
LABEL org.label-schema.description="A middleware for creating and interacting with Raiden test environments."
LABEL org.label-schema.version="0.2.0"
LABEL org.label-schema.vcs-url="https://github.com/raiden-network/scenario-player-services"
LABEL org.label-schema.vendor="Brainbot Laboratories"

ARG PORT=5100

COPY . /sp
RUN pip install /sp
RUN pip install waitress
ENTRYPOINT waitress-serve --port $PORT --call "scenario_player_services.app:scenario_player_services"