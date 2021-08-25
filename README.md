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

Create a new virtual environment (python <3.8) if needed. Then, install all the required dependencies.
The dependencies are compiled by [pip-tools](https://github.com/jazzband/pip-tools), which
compiles `requirements.txt` ensuring compatibility between packages.

    pip install pip-tools
    pip-sync

There is more information on how `pip-tools` work below.

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

	python -m pytest

Or if you want coverage reports:

	python -m pytest --cov


For a coverage report with information about missing lines, run this:

	python -m pytest --cov-report term-missing --cov


### Static files

We're using a [Stylus](http://learnboost.github.io/stylus/) as our CSS pre-processor. [Get styling with Stylus](http://learnboost.github.io/stylus/#get-styling-with-stylus).

This means you shouldn't change any css files, but `.styl` files. They're in /static/source/css/ directory.

Autocompiling of `.styl` files to `.css`:

    npx gulp watch

We're also using gulp for our static files builds (see [below](#gulp-tasks)). To build static files for production, run this:

    npx gulp build

For local development:

    npx gulp local

#### Gulp Tasks

Static files are generated and maintained using [gulp.js](https://gulpjs.com/). To use, you'll need Node.js [installed](https://nodejs.org/en/download/). Then, run `npm install`. You can now use `npx gulp` (note that it's `np**x**`), followed by one of the following commands:

* `gulp local` - run a one-off local build of css & js
* `gulp watch` - compile and watch static assets for changes
* `gulp build` - run a one-off production build, which involves minifying code and asset revision markers
* `gulp clean` - remove the results of any of the above commands

Running `gulp` on its own runs `watch` by default.

#### Developing Gulp Tasks

Each gulp task is a single function, which are combined using the `series` operator so they run as a workflow. Each are commented with what they do and why they're important. 

The biggest gotcha is [async completion](https://gulpjs.com/docs/en/getting-started/async-completion#signal-task-completion). Each task much signal to gulp when it has finished. The easiest way to do this is using an `aysnc` function, **but** if your functionality uses gulp streams (most native gulp functionality does), then you should **not** use an `async` function. Instead, return the gulp stream from the function and it will be handled correctly.

```js
// WRONG - uses gulp's streams in an async function; subsequent tasks won't wait for completion correctly:
const copyFiles = async () => {
    return gulp.src(...).pipe(gulp.dest(...))
}

// RIGHT - either returns a gulp stream _or_ uses an `async` function:
const copyFiles = () => {
    return gulp.src(...).pipe(gulp.dest(...))
}
const deleteFiles = async () => {
    await del(...)
}
```

### Hosting on PythonAnywhere

Key bits of config and secrets are stored in environment variables in two places:

* in the WSGI file (linked from the Web Tab)
* in the virtualenv postactivate at ~/.virtualenvs/djangogirls.com/bin/postactivate


### Google Apps API integration

We're using Google Apps Admin SDK for creating email accounts in djangogirls.org domain automatically.

Several things were needed to get this working:

1. Create an app in Developer Console
2. Create a service account to enable 2 legged oauth (https://developers.google.com/identity/protocols/OAuth2ServiceAccount)
3. Enable delegation of domain-wide authority for the service account.
4. Enable Admin SDK for the domain.
5. Give the service account permission to access admin.directory.users service (https://admin.google.com/AdminHome?chromeless=1#OGX:ManageOauthClients).


### Using pip-tools

The packages required by the project are in `requirements.in` which looks like a regular requirements file. Specific versions of packages can be
specified, or left without a version in which case the latest version which is compatible with the other packages will be used.

If you are working on a feature which requires a new package, add it to `requirements.in`, specifying a version if necessary.
It's dependencies will be included in `requirements.txt` by the compile process. 

The only time a dependency of a third party package needs adding to `requirements.in` is when a version has to be pinned.

By running `pip-compile` the requirements are compiled into `requirements.txt`.

Periodically requirements should be updated to ensure that new versions, most importantly security patches, are used. 
This is done using the `-U` flag.

Once requirements are compiled, `pip-sync` will install the requirements, but also remove any packages not required.
This helps to ensure you have the packages required, but also that there isn't something installed that's missed 
from `requirements.txt`.

For example:

    pip-compile -U

    pip-sync


### Handling environment variables

The `requirements.txt` installs [python-dotenv](https://pypi.org/project/python-dotenv/) which provides the option for
developers to load environment variables via a single file.

You'll see `.environment-example` in the project root. This contains environment variables used by the project so that
you can create your own copy of this and load it with values relevant to your development environment.

To make use of this feature, create a copy of the example file and call it `.environment`. This file will be ignored by
version control, but loaded by `manage.py`. So when you run django commands like `manage.py runserver` during development
`python-dotenv` will load the environment variables from your `.environment` file so that they are available to the application.

This is an optional feature. If you do not have a `.environment` file then it won't impact on the application at all.

## Submitting a Pull Request
We have two major issues we are trying to resolve in our project:
1. [Website internationalization/translations](https://github.com/DjangoGirls/djangogirls/issues/571) 
so that non-English speakers can view the website based on their locale ([571](https://github.com/DjangoGirls/djangogirls/issues/571)).
2. [Migrate from Django Suit which is pinning us on Django version 2.0](https://github.com/DjangoGirls/djangogirls/issues/628) 
so that we can upgrade the version of Django to supported versions ([628](https://github.com/DjangoGirls/djangogirls/issues/628)).

Since these are major changes to the website, pull requests related for each of this cannot be submitted to the `main` 
branch. 

To contribute to [Issue 571- Website internationalization/translations ](https://github.com/DjangoGirls/djangogirls/issues/571), 
submit the pull request to the `translations` branch.

To contribute to [Issue 628 - Migrate from Django Suit which is pinning us on Django version 2.0](https://github.com/DjangoGirls/djangogirls/issues/628),
submit the pull request to the `dev` branch. 
