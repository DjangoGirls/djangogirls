# Contributing to Django Girls website

The website is hosted on Heroku and is available here: http://djangogirls.org/

We have an auto-deploy thing going on, so everything commited to master is automatically deployed to our Heroku. 

## Setting up a development environment

First, clone the repository:

    git clone git@github.com:DjangoGirls/djangogirls.git
  
Step into newly created `djangogirls` directory:

    cd djangogirls
  
Then, install all the required dependencies:

    pip install -r requirements.txt
  
After that, you need to do is create a `djangogirls/local_settings.py` file. Create a file called `local_settings.py` in `djangogirls` directory, next to `settings.py`. The content of the file:

```
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATIC_URL = '/static/'
MEDIA_ROOT = 'static/media'

STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

SECRET_KEY = 'hello'
```

Create your database:

    ./manage.py migrate
  
Add a sample event

    ./manage.py new_event
  
Run your local server:

     ./manage.py runserver
  
:tada: You're done.

### CSS processing

We're using a [Stylus](http://learnboost.github.io/stylus/) as our CSS pre-processor. [Get styling with Stylus](http://learnboost.github.io/stylus/#get-styling-with-stylus).

This means you shouldn't change any css files, but `.styl` files. They're in /static/css/ directory.

Install stylus:

    npm install stylus -g
  
Autocompiling of `.styl` files to `.css`:

    stylus -w static/css

## Contribution process


## How you can help?

### Issues

### Projects

