# -*- encoding: utf-8 -*-
import random, string, click
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
from django_date_extensions.fields import ApproximateDate

from core.models import *
from core.utils import get_coordinates_for_city

class Command(BaseCommand):
    help = 'Creates new Django Girls event'

    def prepare_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return ApproximateDate(year=date_obj.year, month=date_obj.month, day=date_obj.day)
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, '%m/%Y')
                return ApproximateDate(year=date_obj.year, month=date_obj.month)
            except ValueError:
                return False

        return False


    def get_basic_info(self):
        click.echo("Hello there! Let's create new Django Girls event! So exciting!")
        click.echo("Let's start with some basics.")
        city = click.prompt("What is the name of the city?")
        country = click.prompt("What is the name of the country?")
        date = self.prepare_date(click.prompt("What is the date of the event? (Format: DD/MM/YYYY or MM/YYYY)"))
        while not date:
            date = self.prepare_date(click.prompt("Wrong format! Provide a date in format: DD/MM/YYYY or MM/YYYY)"))

        url = click.prompt("What should be the URL of website? djangogirls.org/xxxx")
        click.echo(u"Ok, got that! Your new event will happen in {0}, {1} on {2}".format(city, country, date))

        return (city, country, date, url)

    def get_main_organizer(self):
        team = []
        click.echo("Now let's talk about the team. First the main organizer:")
        main_name = click.prompt("First and last name")
        main_email = click.prompt("E-mail address")
        try:
            team.append({'first_name': main_name.split(' ')[0], 'last_name': main_name.split(' ')[1], 'email': main_email})
        except IndexError:
            team.append({'first_name': main_name, 'last_name': '', 'email': main_email})
        click.echo(u"All right, the main organizer is {0} ({1})".format(main_name, main_email))

        return team

    def get_team(self, team):
        add_team = click.prompt("Do you want to add additional team members? y/n")
        i = 1
        while add_team != 'n':
            i += 1
            name = click.prompt("First and last name of #{0} member".format(i))
            email = click.prompt("E-mail address of #{0} member".format(i))
            if len(name) > 0:
                try:
                    team.append({'first_name': name.split(' ')[0], 'last_name': name.split(' ')[1], 'email': email})
                except IndexError:
                    team.append({'first_name': main_name, 'last_name': '', 'email': main_email})
                click.echo(u"All right, the #{0} team member of Django Girls is {1} ({2})".format(i, name, email))
            add_team = click.prompt("Do you want to add additional team members? y/n")

        return team

    def create_users(self, team):
        main_organizer = None
        members = []
        for member in team:
            member['password'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            user = User.objects.create(email=member['email'],
                                        first_name=member['first_name'],
                                        last_name=member['last_name'],
                                        is_active=True,
                                        is_staff=True)
            user.set_password(member['password'])
            user.save()
            user.groups.add(1)

            if not main_organizer:
                main_organizer = user
            members.append(user)
            click.echo(u"{0} - email: {1} password: {2}".format(member['first_name'], member['email'], member['password']))

        return members

    def add_default_content(self, page):
        EventPageContent.objects.create(
            page = page,
            name = 'about',
            position = 1,
            is_public = True,
            background = File(open(settings.STATICFILES_DIRS[0]+'/img/photos/photo1.jpg')),
            content = '<div style="text-align: center;"><h1>Free programming workshop for women</h1><h2>Build your first website at EuroPython 2014 in Berlin!</h2><a class="btn" href="#value">Learn more »</a></div>')

        EventPageContent.objects.create(
            page = page,
            name = 'values',
            position = 10,
            is_public = True,
            content = '<div class="row">      <div class="col-md-6">          <h3>Django Girls</h3>          <p>If you are a female and you want to learn how to make websites,          we have good news for you! We are holding a one-day workshop for beginners!</p>        <p>It will take place on <strong>21st of July</strong> in <strong>Berlin</strong>,        on the first day of a big IT conference:        <a href="http://europython.eu/">EuroPython</a>, which gathers a lot of talented programmers from all over the world.</p>        <p>We believe that IT industry will greatly benefit from bringing more women        into technology. We want to give you an opportunity to learn how to program        and become one of us - female programmers!</p>        <p>Workshops are free of charge and if you can’t afford coming to Berlin,        but you are very motivated to learn and then share your knowledge with others,        we have some funds to help you out        with your travel costs and accommodation. Don’t wait too long -        you can apply for a pass only until <strong>30th of June</strong>!</p>      </div>      <div class="col-md-6">          <h3>Apply for a pass!</h3>          <p>If you are a woman, you know English and have a laptop - you can apply          for a pass! You don’t need to know any technical stuff - workshops          are for people who are new to programming.</p>        <p>As a workshop attendee you will:        <ul>            <li>attend one-day Django workshops during which you will            create your first website</li>            <li>get a free EuroPython ticket (which normally costs 400 €!),            where you can meet people from the industry and learn more about programming</li>            <li>be fed by us - during workshops and EuroPython food is provided</li>        </ul>        </p>        <p>We have space only for 40 people, so make sure to fill the form very carefully!</p>      </div>  </div>')

        EventPageContent.objects.create(
            page = page,
            name = 'apply',
            position = 20,
            is_public = True,
            background = File(open(settings.STATICFILES_DIRS[0]+'/img/photos/photo5.jpg')),
            content = '<div class="row"><div class="col-md-7"><h2>Application are now open!</h2><p>Application process closes on July 23rd and you\'ll be informedabout acceptance or rejection by July 28th (or sooner)!.</p><a class="btn" href="http://t.co/YvvAFiUvKN">Register</a><p></p></div></div>')

        EventPageContent.objects.create(
            page = page,
            name = 'faq',
            position = 30,
            is_public = True,
            content = '<div class="row"><div class="col-md-4"><p><b>Do I need to know anything about websites or programming?</b></p><p>No! Workshops are for beginners. You don’t need to know anything about it.However, if you have a little bit of technical knowledge(i.e. you know what HTML or CSS are) you still can apply!</p></div><div class="col-md-4"><p><b>I am not living in Germany, can I attend?</b></p><p>Of course! Workshops will be in English, so if you have notroubles with speaking and understanding English - you should apply.If you need financial aid to get toBerlin or you need assistance with booking flights or hotel in Berlin -let us know. We are willing to help you!</p></div><div class="col-md-4"><p><b>Should I bring my own laptop?</b></p><p>Yes. We have no hardware, so we expect you to bring your computer with you.It is also important for us that you will take home everything you’llwrite and create during workshops. </p></div></div><div class="row" style="margin-top: 30px"><div class="col-md-4"><p><b>Do I need to have something installed on my laptop? </b></p><p>It would be helpful to have Django installed before workshops, but wouldn\'t expect you to install anything on your own.We will make sure that one of our coaches will helpyou out with this task. </p></div><div class="col-md-4"><p><b>Is EuroPython conference good for a total beginner?</b></p><p>As a workshop attendee you will get a free ticket to EuroPython -conference for Python programmers. Even though you are new to programming,conference is a good place to meet many interestingpeople in the industry and find inspiration.</p></div><div class="col-md-4"><p><b>Is food provided? </b></p><p>Yes. Thanks to EuroPython, snacks and lunch will be served during workshops. </p></div></div>')

        EventPageContent.objects.create(
            page = page,
            name = 'coach',
            position = 40,
            is_public = True,
            background = File(open(settings.STATICFILES_DIRS[0]+'/img/photos/photo0.jpg')),
            content = '<div class="row"><div class="col-md-6"><h2>Be a Mentor!</h2><p>We would be delighted if you would like to join us as a mentor! Fill in the form  <a href="http://t.co/YvvAFiUvKN">here</a>, but select the option to be a mentor.</p><p>We will contact you :)</p></div><div class="col-md-6"><h2>Django Girls</h2><p>Django Girls Australia is a part of bigger initiative: <a href="http://djangogirls.org/">Django Girls</a>.  It is a non-profit organization and events are organized by volunteersin different places of the world.  </p><p>To see the source for the program find us on gihub: <a href="https://github.com/DjangoGirls/">github.com/DjangoGirls</a>.</p><p>If you want to bring Django Girls to your city, drop us a line: <a href="mailto:hello@djangogirls.org">hello@djangogirls.org</a>.</p></div></div>')

        EventPageContent.objects.create(
            page = page,
            name = 'partners',
            position = 50,
            is_public = True,
            content = '<h3>Sponsors</h3><p>We couldn\'t be here without the support from amazing people and organizations who donated money, knowledge and time to help us make this a reality.</p><div class="row" style="margin-top: 30px;"><div class="col-md-4"><a href="http://europython.eu/"><img src="https://djangogirls.s3.amazonaws.com/img/partners/ep.png" /></a></div><div class="col-md-4"><a href="https://www.djangoproject.com/"><img src="https://djangogirls.s3.amazonaws.com/img/partners/django.png" width="50%" /></a></div><div class="col-md-4"><a href="http://www.django-de.org/"><img src="https://djangogirls.s3.amazonaws.com/img/partners/djangode.png" /></a></div></div><div class="row" style="margin-top: 30px;"><div class="col-md-4"><a href="http://www.python.org/"><img src="https://djangogirls.s3.amazonaws.com/img/partners/python.png" /></a></div><div class="col-md-4"><a href="http://github.com/"><img src="https://djangogirls.s3.amazonaws.com/img/partners/github.png" width="50%" /></a></div><div class="col-md-4"><a href="https://p.ota.to/"><img src="https://djangogirls.s3.amazonaws.com/img/partners/potato.png" /></a></div></div><div class="row" style="padding: 30px 0 30px 0;"><div class="col-md-4"><a href="http://stxnext.com/#/en"><img src="https://djangogirls.s3.amazonaws.com/img/partners/stxnext.png" /></a></div></div><p>If you want to contribute and support our goal, please get in touch: <a href="mailto:hello@djangogirls.org">hello@djangogirls.org</a></p>')

        EventPageContent.objects.create(
            page = page,
            name = 'footer',
            position = 60,
            is_public = True,
            content = '<div class="row social"><div class="col-md-7"><div class="facebook"><div class="fb-like-box" data-href="https://www.facebook.com/djangogirls" data-colorscheme="dark" data-show-faces="false" data-header="false" data-stream="false" data-show-border="false"></div></div><div class="twitter"> <a href="https://twitter.com/djangogirls" class="twitter-follow-button" data-show-count="false" data-size="large">Follow @djangogirls</a></div> </div><div class="col-md-5">Get in touch: <br> <a href="mailto:hello@djangogirls.org">hello@djangogirls.org</a><br><br></div></div><div class="row credits"><div class="col-md-12">♥ Django Girls Europe is organized by <a href="http://twitter.com/olasitarska">Ola Sitarska</a> and <a href="http://twitter.com/asednecka">Ola Sendecka</a> with the support from <a href="http://europython.eu/">EuroPython 2014</a>.<br>Django Girls Europe is a part of <a href="/">Django Girls</a>. Whole thing is inspired by wonderful <a target="_blank" href="http://railsgirls.com/">Rails Girls</a>.<br>Every participant needs to follow the <a href="/coc/">Code of Conduct</a>.</div></div>')



    def add_default_menu(self, page):

        EventPageMenu.objects.create(page = page, title = 'About', position = 1, url = '#values')
        EventPageMenu.objects.create(page = page, title = 'Apply for a pass!', position = 10, url = '#apply')
        EventPageMenu.objects.create(page = page, title = 'FAQ', position = 20, url = '#faq')
        EventPageMenu.objects.create(page = page, title = 'Become a coach', position = 30, url = '#coach')
        EventPageMenu.objects.create(page = page, title = 'Partners', position = 40, url = '#partners')



    def handle(self, *args, **options):

        #Basics
        (city, country, date, url) = self.get_basic_info()

        #Main organizer
        team = self.get_main_organizer()

        #Team
        team = self.get_team(team)

        #Create users
        click.echo("OK! That's it. Now I'll create your event.")
        click.echo("Here is an access info for team members:")

        members = self.create_users(team)

        #Event and EventPage objects
        name = u'Django Girls '+city
        latlng = get_coordinates_for_city(city, country)
        event = Event.objects.create(name=name, city=city, country=country, latlng=latlng, main_organizer=members[0], date=date)
        for member in members:
            event.team.add(member)

        page = EventPage.objects.create(event=event, url=url, title=name)

        #Default content
        self.add_default_content(page)
        self.add_default_menu(page)

        click.echo(u"Website is ready here: http://djangogirls.org/{0}".format(url))
        click.echo("Congrats on yet another event!")
