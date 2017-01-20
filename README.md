# Django Girls website

[![Build Status](https://travis-ci.org/DjangoGirls/djangogirls.svg?branch=master)](https://travis-ci.org/DjangoGirls/djangogirls) [![codecov](https://codecov.io/gh/DjangoGirls/djangogirls/branch/master/graph/badge.svg)](https://codecov.io/gh/DjangoGirls/djangogirls)


This repository contains sources of Django application that powers [DjangoGirls.org](http://djangogirls.org/).

## What's in it?

It's a simple CMS that contains 4 models:

- __Event__ - a list of events and their website configuration
- __EventPageContent__ - blocks of content that are visible on the website
- __EventPageMenu__ - items of menu of every website

## How to create new event?

Simply go to command line and run this command:

    python ./manage.py new_event

And then follow the instructions.

## How to manage your website?

### Event

http://djangogirls.org/admin/core/event/

Here you can change:
- Meta tags - title and description of the website
- Main color - main color on the website in HEX (default is FF9400)
- Custom CSS - customize CSS on the website
- URL - url that goes after the domain (http://djangogirls.org/__url__)
- Is live? - live website is available [on the homepage](http://djangogirls.org/) and can be accessed by anyone

### EventPageContent

http://djangogirls.org/admin/core/eventpagecontent/

Each website comes with some default content that you can adjust to your needs. Each object is a "block" on the website that you can modify in following ways:
- Name - it's also a permalink that you can link to like this: __#name__
- Content - HTML is allowed
- Background - there are two available types of blocks: without background and with background. By uploading image you're choosing the type with background.
- Is public - check this if you want this block to be visible

### EventPageMenu

http://djangogirls.org/admin/core/eventpagemenu/add/

To manage menu available on the website, you can add objects to EventPageMenu. Available options:
- Title
- URL


# Contributing to Django Girls website

The website is hosted on PythonAnywhere and is available here: http://djangogirls.org/

Please note that we use Python 3 only, so make sure that you use correct version when running commands below.

## Setting up a development environment

First, clone the repository:

    git clone git@github.com:DjangoGirls/djangogirls.git

Step into newly created `djangogirls` directory:

    cd djangogirls

Create a new virtual environment if needed. Then, install all the required dependencies:

    pip install -r requirements.txt

Start the [PostgreSQL database server](http://www.postgresql.org/docs/current/static/server-start.html) and enter the `psql` shell (you need to have [PostgreSQL](http://www.postgresql.org/download/) installed):

    psql

In the `psql` shell, create a database and a role with the necessary permissions:

    CREATE DATABASE djangogirls;
    CREATE ROLE postgres;
    GRANT ALL privileges ON DATABASE djangogirls TO postgres;
    ALTER ROLE postgres WITH LOGIN;

Exit the `psql` shell:

    \q

Run the migration to create database schema:

    ./manage.py migrate

Load sample data to the database

    ./manage.py loaddata sample_db.json

Create a user so you can login to the admin:

    ./manage.py createsuperuser

Install dependencies for static files:

    npm install

Compile CSS and JS files:

    gulp watch

Run your local server:

     ./manage.py runserver

:tada: You're done.


## Run the tests

You can run the tests like this:

	py.test

Or if you want coverage reports:

	py.test --cov


For a coverage report with information about missing lines, run this:

	py.test --cov-report term-missing --cov


## Update requirements.txt

You will need to install `pip-tools`:

    pip install pip-tools

Then compile `requirements.in` into a new list of requirements:

    pip-compile

To try and update a particular dependency:

    pip-compile -P django

You can also tell it to try and update all the dependency versions:

    pip-compile -U

Please note that `pip-compile` will not install or upgrade any packages. You
still need to install them separately.

`pip-tools` also provides a tool that will install all required packages and
uninstall all packages that are not explicitly required. This can prove useful
when removing dependencies to make sure no code tries to import them:

    pip-sync


### Static files

We're using a [Stylus](http://learnboost.github.io/stylus/) as our CSS pre-processor. [Get styling with Stylus](http://learnboost.github.io/stylus/#get-styling-with-stylus).

This means you shouldn't change any css files, but `.styl` files. They're in /static/source/css/ directory.

Autocompiling of `.styl` files to `.css`:

    gulp watch

We're also using gulp for our static files builds. To build static files for production, run this:

    gulp build

For local development:

    gulp local


### Hosting on PythonAnywhere

Key bits of config and secrets are stored in environment variables in two places:

* in the WSGI file (linked from the Web Tab)
* in the virtualenv postactivate at ~/.virtualenvs/djangogirls.com/bin/postactivate
