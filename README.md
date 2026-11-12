# Django Girls website

[![Build Status](https://travis-ci.org/DjangoGirls/djangogirls.svg?branch=master)](https://travis-ci.org/DjangoGirls/djangogirls) [![codecov](https://codecov.io/gh/DjangoGirls/djangogirls/branch/master/graph/badge.svg)](https://codecov.io/gh/DjangoGirls/djangogirls)


This repository contains the Django application which powers [DjangoGirls.org](https://djangogirls.org/).

## What's in it?

It's a simple CMS that contains 3 main models:

- __Event__ - a list of events and their website configuration
- __EventPageContent__ - blocks of content that are visible on the website
- __EventPageMenu__ - items of menu of every website

## How to create new event?

Simply go to command line and run this command:

```bash
python ./manage.py new_event
```
And then follow the instructions.

## How to manage your website?

### Event

https://djangogirls.org/admin/core/event/

Here you can change:
- Meta tags - title and description of the website
- Main color - main color on the website in HEX (default is FF9400)
- Custom CSS - customize CSS on the website
- URL - url that goes after the domain (https://djangogirls.org/__url__)
- Is live? - live website is available [on the homepage](https://djangogirls.org/) and can be accessed by anyone

### EventPageContent

https://djangogirls.org/admin/core/eventpagecontent/

Each website comes with some default content that you can adjust to your needs. Each object is a "block" on the website that you can modify in following ways:
- Name - it's also a permalink that you can link to like this: __#name__
- Content - HTML is allowed
- Background - there are two available types of blocks: without background and with background. By uploading image you're choosing the type with background.
- Is public - check this if you want this block to be visible

### EventPageMenu

https://djangogirls.org/admin/core/eventpagemenu/add/

To manage menu available on the website, you can add objects to EventPageMenu. Available options:
- Title
- URL


# Contributing to Django Girls website

The website is hosted on PythonAnywhere and is available here: https://djangogirls.org/

Please note that we use Python 3 only, so make sure that you use correct version when running commands below.

## Setting up a development environment

First, fork and clone the repository:

```bash
git clone git@github.com:your-username/djangogirls.git
```

Step into newly created `djangogirls` directory:

```bash
cd djangogirls
```

Both setups below, Docker and non Docker, read environment variables from a `.environment` file.
Copy `.environment-example` to `.environment`:

```bash
cp .environment-example .environment
```

Then turn on debug mode in `.environment`. Change this line:

```
export DJANGO_DEBUG="FALSE"
```

to:

```
export DJANGO_DEBUG="TRUE"
```

See [Handling environment variables](#handling-environment-variables) for more details.

### Docker

If you have Docker and Docker Compose installed, run `docker compose up --build`.

Docker sets the database variables (`POSTGRES_*`) for you, so you don't need to change them in `.environment`.

If you see this error, you don't have a `.environment` file yet. Create it as explained above:

```
Failed to load .../djangogirls/.environment: open .../djangogirls/.environment: no such file or directory
```

If you see `The SECRET_KEY setting must not be empty.`, check that `DJANGO_DEBUG` is `"TRUE"` in `.environment`.

### Non Docker

Create a new [virtual environment](https://docs.python.org/3/library/venv.html) (with Python 3.12).

In `.environment`, also set the database user and password:

```
export POSTGRES_USER="djangogirls"
export POSTGRES_PASSWORD="<create a password>"
```

Then, install all the required dependencies. The dependencies are compiled by [pip-tools](https://github.com/jazzband/pip-tools), which
compiles `requirements.txt` ensuring compatibility between packages.

```bash
pip install pip-tools
pip-sync
```

> There is more information on how `pip-tools` work below in [Using pip-tools](#using-pip-tools).

Install the [pre-commit](https://github.com/pre-commit/pre-commit) hook. It's useful so we automatically format and lint code before committing any changes.

```bash
pre-commit install
```

Start the [PostgreSQL database server](https://www.postgresql.org/docs/current/static/server-start.html) and enter the `psql` shell (you need to have [PostgreSQL](https://www.postgresql.org/download/) installed).

```bash
psql postgres
```

In the `psql` shell, create a database and a role with the necessary permissions:

```sql
CREATE DATABASE djangogirls;
CREATE USER djangogirls WITH PASSWORD '<use the password you set up earlier in .environment>';
ALTER USER djangogirls CREATEDB;

\connect djangogirls

GRANT ALL privileges ON DATABASE djangogirls TO djangogirls;
ALTER SCHEMA public OWNER TO djangogirls;
```

Exit the `psql` shell:

```bash
\q
```

Run the migration to create database schema:

```bash
./manage.py migrate
```

Load sample data to the database

```bash
./manage.py loaddata sample_db.json
```

Create a user so you can login to the admin:

```bash
./manage.py createsuperuser
```

Install dependencies for static files:

```bash
npm install
```

Compile CSS and JS files and watch for changes:

```bash
npm run watch
```

In a separate terminal window, run your local server:

```bash
./manage.py runserver
```

:tada: You're done.


## Run the tests

You can run the tests like this:

```bash
python -m pytest
```

Or if you want coverage reports:

```bash
python -m pytest --cov
```

For a coverage report with information about missing lines, run this:

```bash
python -m pytest --cov-report term-missing --cov
```

### Static files

We're using [Stylus](https://stylus-lang.com/) as our CSS pre-processor.

This means you shouldn't change any css files, but `.styl` files. They're in `/static/source/css/` directory.

Static files are built by a small Node.js script, [`scripts/build-static.mjs`](scripts/build-static.mjs). You'll need Node.js 20 or newer [installed](https://nodejs.org/en/download/). Then, run `npm install`.

* `npm run watch` - build CSS & JS and rebuild when files in `static/source/` change
* `npm run build:local` - run a one-off local build of CSS & JS into `static/local/`
* `npm run build` - run a one-off production build into `static/build/`: minifies code and adds a content hash to CSS & JS filenames (listed in `static/rev-manifest.json`)
* `npm run clean` - remove the results of any of the above commands


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

```bash
pip-compile -U
pip-sync
```

### Handling environment variables

The `requirements.txt` installs [python-dotenv](https://pypi.org/project/python-dotenv/) which provides the option for
developers to load environment variables via a single file.

You'll see `.environment-example` in the project root. This contains environment variables used by the project so that
you can create your own copy of this and load it with values relevant to your development environment.

To make use of this feature, create a copy of the example file and call it `.environment`. This file will be ignored by
version control, but loaded by `manage.py`. So when you run django commands like `manage.py runserver` during development
`python-dotenv` will load the environment variables from your `.environment` file so that they are available to the application.

With Docker, `docker-compose.yml` also loads `.environment` into the container (`env_file`), so the same file works for both setups.

### Before you Open a Pull Request

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. A lint check runs in CI on every pull request. Before you create a pull request, it's advisable to fix any linting issues locally to avoid failures. In order to have Ruff run on your local machine automatically you can do the following:

1) Run `pip install pre-commit` to install [pre-commit](https://pypi.org/project/pre-commit/). This package helps setting up git hooks.

2) Run `pre-commit install` to install the git hook. After this, whenever you run `git commit` in your local machine, Ruff will lint and format your changes and report any errors that it found.

3) If you've already committed your changes before installing `pre-commit`, you can follow steps 1 and 2 and then run `pre-commit run --all-files` to run Ruff against all of the files.

## Help with translation of the website
Join us on [poeditor.com](https://poeditor.com/join/project?hash=n5I3liMVyj) to help with translation of the website so 
that non-English speakers can view the website based on their locale.

Languages available for translation are;

* French
* German
* Korean
* Persian
* Portuguese
* Portuguese (BR)
* Russian
* Spanish

See [issue 571- Website internationalization/translations ](https://github.com/DjangoGirls/djangogirls/issues/571) for further details. 
Alternatively submit the pull request to the `translations` branch.
