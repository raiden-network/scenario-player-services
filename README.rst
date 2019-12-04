Scenario Player Services
========================

A middleware for creating and interacting with raiden test environments.

Installation
------------
Using pip::

    pip install scenario-player-services

Using a docker container, which will run all services as a single flask application, reachable under a single port::

    docker run raidennetwork/scenario-player-services:latest

Using docker-compose, which will create a flask app for each service, each available under a different port::

    git clone https://github.com/raiden-network/scenario-player-services
    cd scenario-player-services
    docker-compose up

Usage
-----
In order to make use of the Scenario Player Services, it's important to spin them
up *before* running scenarios. Unless you've changed the ports used by the
services or do not run them on the local machine, no further configuration is
required on your part::

    ~/scenario-player-service$ docker-compose up
    ~/scenario-player-service$ scenario_player [...] # supply options as necessary

Newer versions of the scenario player may also offer a cli option to automatically
fire up SP services if not already running, and taking care of detecting the port
configurations for you - however, this is only available when the SP services are
run locally::

    # Start Scenario Player Services
    $ scenario_player services up
    # Run a scenario, using the local services
    $ scenario_player run [...]
    # services are not stopped after an SP run and must be stopped manually
    $ scenario_player services down