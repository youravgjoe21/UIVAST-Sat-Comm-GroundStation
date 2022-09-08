# UI VAST Sat-Comm Ground Station
This repository contains the code required to run VAST's Raspberry Pi based ground station written in Python 3.10. It uses a Dash-based web interface to display information to the user, and has a postgresql backend to store received data. We use Iridium modules to communicate with our payload.

## Dependencies
- [Dash] - allows for easy, powerful web app creation
	- dash_bootstrap_components - a bunch of pre-made components that nicely drop into a Dash application 
- [Psycopg] - Python framework that allows Python to interact with a postgresql database

## Setup
Run the command below to get the required dependencies.
`pip install dash dash_bootstrap_components psycopg`
Clone the repository into a folder of your choice.

## How to use
Run `main.py` to start the program. You can access the web interface at [127.0.0.1:8050](127.0.0.1:8050)

[//]: Links
[Dash]: <https://plotly.com/dash/>

[dash_bootstrap_components]:<https://dash-bootstrap-components.opensource.faculty.ai/>

[Psycopg]: <https://www.psycopg.org/>
