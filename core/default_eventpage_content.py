# -*- encoding: utf-8 -*-
import random

from django.conf import settings
from django.core.files import File


DEFAULT_BACKGROUND_PHOTOS = {
    'about': [
        settings.STATICFILES_DIRS[0]+'/img/photos/about1.jpg',
        settings.STATICFILES_DIRS[0]+'/img/photos/about2.jpg'
    ],
    'apply': [
        settings.STATICFILES_DIRS[0]+'/img/photos/apply.jpg'
    ],
    'coach': [
        settings.STATICFILES_DIRS[0]+'/img/photos/coach1.jpg',
        settings.STATICFILES_DIRS[0]+'/img/photos/coach2.jpg'
    ],
    'footer': [
        settings.STATICFILES_DIRS[0]+'/img/photos/footer1.jpg',
        settings.STATICFILES_DIRS[0]+'/img/photos/footer2.jpg'
    ]
}

def get_random_photo(section):
    if section in DEFAULT_BACKGROUND_PHOTOS:
        photos = DEFAULT_BACKGROUND_PHOTOS[section]
        return File(open(photos[random.randint(0, len(photos)-1)], 'rb'))
    return None


def get_default_eventpage_data():
    return [
        {
            'name': 'about',
            'is_public': True,
            'background': get_random_photo('about'),
            'content': '<div style="text-align: center;"><h1>Free programming workshop for women</h1><h2>Build your first website at EuroPython 2014 in Berlin!</h2><a class="btn" href="#value">Learn more »</a></div>'
        },
        {
            'name': 'values',
            'is_public': True,
            'content': '<div class="row">      <div class="col-md-6">          <h3>Django Girls</h3>          <p>If you are a female and you want to learn how to make websites,          we have good news for you! We are holding a one-day workshop for beginners!</p>        <p>It will take place on <strong>21st of July</strong> in <strong>Berlin</strong>,        on the first day of a big IT conference:        <a href="http://europython.eu/">EuroPython</a>, which gathers a lot of talented programmers from all over the world.</p>        <p>We believe that IT industry will greatly benefit from bringing more women        into technology. We want to give you an opportunity to learn how to program        and become one of us - female programmers!</p>        <p>Workshops are free of charge and if you can’t afford coming to Berlin,        but you are very motivated to learn and then share your knowledge with others,        we have some funds to help you out        with your travel costs and accommodation. Don’t wait too long -        you can apply for a pass only until <strong>30th of June</strong>!</p>      </div>      <div class="col-md-6">          <h3>Apply for a pass!</h3>          <p>If you are a woman, you know English and have a laptop - you can apply          for a pass! You don’t need to know any technical stuff - workshops          are for people who are new to programming.</p>        <p>As a workshop attendee you will:        <ul>            <li>attend one-day Django workshops during which you will            create your first website</li>            <li>get a free EuroPython ticket (which normally costs 400 €!),            where you can meet people from the industry and learn more about programming</li>            <li>be fed by us - during workshops and EuroPython food is provided</li>        </ul>        </p>        <p>We have space only for 40 people, so make sure to fill the form very carefully!</p>      </div>  </div>'
        },
        {
            'name': 'apply',
            'is_public': True,
            'background': get_random_photo('apply'),
            'content': '<div class="row"><div class="col-md-7 col-md-offset-5"><h2>Applications are now open!</h2><p>Application process closes on July 23rd and you\'ll be informedabout acceptance or rejection by July 28th (or sooner)!.</p><a class="btn" href="http://t.co/YvvAFiUvKN">Register</a><p></p></div></div>'
        },
        {
            'name': 'faq',
            'is_public': True,
            'content': '<div class="row"><div class="col-md-4"><p><b>Do I need to know anything about websites or programming?</b></p><p>No! Workshops are for beginners. You don’t need to know anything about it.However, if you have a little bit of technical knowledge(i.e. you know what HTML or CSS are) you still can apply!</p></div><div class="col-md-4"><p><b>I am not living in Germany, can I attend?</b></p><p>Of course! Workshops will be in English, so if you have notroubles with speaking and understanding English - you should apply.If you need financial aid to get toBerlin or you need assistance with booking flights or hotel in Berlin -let us know. We are willing to help you!</p></div><div class="col-md-4"><p><b>Should I bring my own laptop?</b></p><p>Yes. We have no hardware, so we expect you to bring your computer with you.It is also important for us that you will take home everything you’llwrite and create during workshops. </p></div></div><div class="row" style="margin-top: 30px"><div class="col-md-4"><p><b>Do I need to have something installed on my laptop? </b></p><p>It would be helpful to have Django installed before workshops, but wouldn\'t expect you to install anything on your own.We will make sure that one of our coaches will helpyou out with this task. </p></div><div class="col-md-4"><p><b>Is EuroPython conference good for a total beginner?</b></p><p>As a workshop attendee you will get a free ticket to EuroPython -conference for Python programmers. Even though you are new to programming,conference is a good place to meet many interestingpeople in the industry and find inspiration.</p></div><div class="col-md-4"><p><b>Is food provided? </b></p><p>Yes. Thanks to EuroPython, snacks and lunch will be served during workshops. </p></div></div>'
        },
        {
            'name': 'coach',
            'is_public': True,
            'background': get_random_photo('coach'),
            'content': '<div class="row"><div class="col-md-6"><h2>Be a Mentor!</h2><p>We would be delighted if you would like to join us as a mentor! Fill in the form  <a href="http://t.co/YvvAFiUvKN">here</a>, but select the option to be a mentor.</p><p>We will contact you :)</p></div><div class="col-md-6"><h2>Django Girls</h2><p>Django Girls Australia is a part of bigger initiative: <a href="http://djangogirls.org/">Django Girls</a>.  It is a non-profit organization and events are organized by volunteersin different places of the world.  </p><p>To see the source for the program find us on gihub: <a href="https://github.com/DjangoGirls/">github.com/DjangoGirls</a>.</p><p>If you want to bring Django Girls to your city, drop us a line: <a href="mailto:hello@djangogirls.org">hello@djangogirls.org</a>.</p></div></div>'
        },
        {
            'name': 'partners',
            'is_public': True,
            'content': '<h3>Sponsors</h3><p>We couldn\'t be here without the support from amazing people and organizations who donated money, knowledge and time to help us make this a reality. If you want to contribute and support our goal, please get in touch: <a href="mailto:hello@djangogirls.org">hello@djangogirls.org</a></p>'
        },
        {
            'name': 'footer',
            'is_public': True,
            'background': get_random_photo('footer'),
            'content': '<div class="row social"><div class="col-md-4"><div class="facebook"><div class="fb-page" data-href="https://www.facebook.com/djangogirls" data-small-header="true" data-adapt-container-width="true" data-hide-cover="true" data-show-facepile="false" data-show-posts="false"><div class="fb-xfbml-parse-ignore"><blockquote cite="https://www.facebook.com/djangogirls"><a href="https://www.facebook.com/djangogirls">Django Girls</a></blockquote></div></div></div></div><div class="col-md-4"><div class="twitter"> <a href="https://twitter.com/djangogirls" class="twitter-follow-button" data-show-count="false" data-size="large">Follow @djangogirls</a></div> </div><div class="col-md-4">Get in touch: <br> <a href="mailto:hello@djangogirls.org">hello@djangogirls.org</a><br><br></div></div><div class="row credits"><div class="col-md-12">♥ Django Girls Europe is organized by <a href="http://twitter.com/olasitarska">Ola Sitarska</a> and <a href="http://twitter.com/asednecka">Ola Sendecka</a> with the support from <a href="http://europython.eu/">EuroPython 2014</a>.<br>Django Girls Europe is a part of <a href="/">Django Girls</a>.<br>Every participant needs to follow the <a href="/pages/coc/">Code of Conduct</a>.</div></div>'
        },
    ]


def get_default_menu():
    return [
        {'title': 'About', 'url': '#values'},
        {'title': 'Apply for a pass!', 'url': '#apply'},
        {'title': 'FAQ', 'url': '#faq'},
        {'title': 'Become a coach', 'url': '#coach'},
        {'title': 'Partners', 'url': '#partners'},
    ]
