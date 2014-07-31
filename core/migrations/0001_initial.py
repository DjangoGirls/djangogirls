# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'core_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'core_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'core.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'core_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'core.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'Event'
        db.create_table(u'core_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('main_organizer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_organizer', null=True, to=orm['core.User'])),
        ))
        db.send_create_signal(u'core', ['Event'])

        # Adding M2M table for field team on 'Event'
        m2m_table_name = db.shorten_name(u'core_event_team')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'core.event'], null=False)),
            ('user', models.ForeignKey(orm[u'core.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'user_id'])

        # Adding model 'EventPage'
        db.create_table(u'core_eventpage', (
            ('event', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Event'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='Django Girls is a one-day workshop about programming in Python and Django tailored for women.', null=True, blank=True)),
            ('main_color', self.gf('django.db.models.fields.CharField')(default='FF9400', max_length=6, null=True, blank=True)),
            ('custom_css', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('is_live', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['EventPage'])

        # Adding model 'EventPageContent'
        db.create_table(u'core_eventpagecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.EventPage'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('background', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['EventPageContent'])

        # Adding model 'EventPageMenu'
        db.create_table(u'core_eventpagemenu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.EventPage'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['EventPageMenu'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'core_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'core_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'core_user_user_permissions'))

        # Deleting model 'Event'
        db.delete_table(u'core_event')

        # Removing M2M table for field team on 'Event'
        db.delete_table(db.shorten_name(u'core_event_team'))

        # Deleting model 'EventPage'
        db.delete_table(u'core_eventpage')

        # Deleting model 'EventPageContent'
        db.delete_table(u'core_eventpagecontent')

        # Deleting model 'EventPageMenu'
        db.delete_table(u'core_eventpagemenu')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.event': {
            'Meta': {'object_name': 'Event'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_organizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_organizer'", 'null': 'True', 'to': u"orm['core.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'team': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.User']", 'null': 'True', 'blank': 'True'})
        },
        u'core.eventpage': {
            'Meta': {'object_name': 'EventPage'},
            'custom_css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'Django Girls is a one-day workshop about programming in Python and Django tailored for women.'", 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_color': ('django.db.models.fields.CharField', [], {'default': "'FF9400'", 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.eventpagecontent': {
            'Meta': {'ordering': "('position',)", 'object_name': 'EventPageContent'},
            'background': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.EventPage']"}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.eventpagemenu': {
            'Meta': {'ordering': "('position',)", 'object_name': 'EventPageMenu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.EventPage']"}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['core']