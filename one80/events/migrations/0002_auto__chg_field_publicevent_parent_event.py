# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PublicEvent.parent_event'
        db.alter_column('events_event', 'parent_event_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['events.PublicEvent']))

    def backwards(self, orm):

        # Changing field 'PublicEvent.parent_event'
        db.alter_column('events_event', 'parent_event_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['events.PublicEvent']))

    models = {
        'events.publicevent': {
            'Meta': {'ordering': "('-start_datetime',)", 'object_name': 'PublicEvent', 'db_table': "'events_event'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'parent_event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_event'", 'null': 'True', 'to': "orm['events.PublicEvent']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['events']