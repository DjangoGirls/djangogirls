# Django Girls website

This repository contains sources of Django application that powers [DjangoGirls.org](http://djangogirls.org/).

## What's in it?

It's a simple CMS that contains 4 models:

- __Event__ - a list of events
- __EventPage__ - configuration of website
- __EventPageContent__ - blocks of content that are visible on the website
- __EventPageMenu__ - items of menu of every website

## How to create new event?

Simply go to command line and run this command:

    python ./manage.py new_event

And then follow the instructions.

## How to manage your website?

### EventPage

http://djangogirls.org/admin/core/eventpage/

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

The website is hosted on Heroku and is available here: http://djangogirls.org/

We have an auto-deploy thing going on, so everything commited to master is automatically deployed to our Heroku. 

## Setting up a development environment

First, clone the repository:

    git clone git@github.com:DjangoGirls/djangogirls.git
  
Step into newly created `djangogirls` directory:

    cd djangogirls
  
Then, install all the required dependencies:

    pip install -r requirements.txt

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
