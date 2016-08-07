from datetime import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission

from core.tests.test_views import BaseCoreTestCase
from core.admin import EventAdmin
from core.models import Event, User


class EventAdminTestCase(BaseCoreTestCase):
    
    def setUp(self):
        super(EventAdminTestCase, self).setUp()
        # Reset superadmin's password
        self.ola.set_password('')
        self.ola.save()
        # Reset organizer's password, add permissions
        self.peter.set_password('')
        self.peter.user_permissions = [
            Permission.objects.get(codename='add_event'), 
            Permission.objects.get(codename='change_event')
        ]
        self.peter.save()
        self.event_1.team.add(self.peter)
        self.event_1.save()
        self.event_2.team.add(self.peter)
        self.event_2.save()
        # Login as superadmin
        self.client.login(username=self.ola.email, password='')

    def test_get_queryset_for_superuser(self):
        resp = self.client.get(reverse('admin:core_event_changelist'))
        assert len(resp.context['results']) == 4
        
    def test_get_queryset_for_organizer(self):
        self.client.login(username=self.peter.email, password='')
        resp = self.client.get(reverse('admin:core_event_changelist'))
        assert len(resp.context['results']) == 2
        results = ''.join(sum(resp.context['results'], [])) # flattens the list of lists
        assert all([x.name in results for x in [self.event_1, self.event_2]])
        
    def test_manage_organizers_view_for_superuser(self):
        resp = self.client.get(reverse('admin:core_event_manage_organizers'))
        
        # Only upcoming events are listed
        expected_events = Event.objects.filter(
            date__gte=datetime.now().strftime('%Y-%m-%d')).order_by('name')
        assert len(resp.context['all_events']) == expected_events.count()
        assert all([x.is_upcoming() for x in resp.context['all_events']])
        
        # First event is selected automatically
        assert resp.context['event'] == expected_events[0]
        
    def test_manage_organizers_view_for_organizers(self):
        expected_events = Event.objects.filter(
            date__gte=datetime.now().strftime('%Y-%m-%d'),
            team=self.peter)
        self.client.login(username=self.peter.email, password='')
        resp = self.client.get(reverse('admin:core_event_manage_organizers'))
        assert len(resp.context['all_events']) == expected_events.count()
        assert all([x.is_upcoming() for x in resp.context['all_events']])
        
    def test_adding_organizer_as_superuser(self):
        resp = self.client.get(reverse('admin:core_event_add_organizers'))
        total_count = User.objects.filter(is_staff=True).count()
        team_count = self.event_1.team.count()
        data = {
            'event': self.event_1.pk,
            'name': 'New organizer',
            'email': 'new@organizer.com'
        }
        resp = self.client.post(reverse('admin:core_event_add_organizers'), data)
        assert resp.status_code == 302
        assert User.objects.filter(is_staff=True).count() == (total_count + 1)
        assert self.event_1.team.count() == (team_count + 1)
        
        # Adding already existing organizer
        team_count = self.event_3.team.count()
        data['event'] = self.event_3.pk
        resp = self.client.post(reverse('admin:core_event_add_organizers'), data)
        assert resp.status_code == 302
        assert User.objects.filter(is_staff=True).count() == (total_count + 1)
        assert self.event_2.team.count() == (team_count + 1)
        
    def test_organizer_can_only_add_to_their_event(self):
        self.client.login(username=self.peter.email, password='')
        data = {
            'event': self.event_3.pk,
            'name': 'New organizer',
            'email': 'new@organizer.com'
        }
        resp = self.client.post(reverse('admin:core_event_add_organizers'), data)
        assert resp.status_code == 200
        assert len(resp.context['form'].errors) == 1
        
        data = {
            'event': self.event_1.pk,
            'name': 'New organizer',
            'email': 'new@organizer.com'
        }
        resp = self.client.post(reverse('admin:core_event_add_organizers'), data)
        assert resp.status_code == 302
        
    def test_remove_organizer_as_superuser(self):
        self.event_1.team.add(self.peter)
        self.event_1.save()
        assert self.event_1.team.count() == 2
        
        data = {
            'event_id': self.event_1.pk,
            'remove': self.peter.pk,
        }
        resp = self.client.get(reverse('admin:core_event_manage_organizers'), data)
        assert resp.status_code == 302
        assert self.event_1.team.count() == 1
        
    def test_organizers_can_only_remove_from_their_events(self):
        self.client.login(username=self.peter.email, password='')
        data = {
            'event_id': self.event_3.pk,
            'remove': self.ola.pk,
        }
        assert self.event_3.team.count() == 1
        resp = self.client.get(reverse('admin:core_event_manage_organizers'), data)
        assert resp.status_code == 200
        assert self.event_3.team.count() == 1
        
        self.client.login(username=self.peter.email, password='')
        data = {
            'event_id': self.event_1.pk,
            'remove': self.tinker.pk,
        }
        assert self.event_1.team.count() == 2
        resp = self.client.get(reverse('admin:core_event_manage_organizers'), data)
        assert resp.status_code == 302
        assert self.event_1.team.count() == 1
        
    def test_organizers_cannot_remove_themselves(self):
        self.client.login(username=self.peter.email, password='')
        data = {
            'event_id': self.event_1.pk,
            'remove': self.peter.pk,
        }
        assert self.event_1.team.count() == 2
        resp = self.client.get(reverse('admin:core_event_manage_organizers'), data)
        assert resp.status_code == 200
        assert self.event_1.team.count() == 2
        
        self.client.login(username=self.peter.email, password='')
        data = {
            'event_id': self.event_1.pk,
            'remove': self.tinker.pk,
        }
        assert self.event_1.team.count() == 2
        resp = self.client.get(reverse('admin:core_event_manage_organizers'), data)
        assert resp.status_code == 302
        assert self.event_1.team.count() == 1
        
