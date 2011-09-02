# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('people_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('extra', self.gf('jsonfield.fields.JSONField')(default='{}', blank=True)),
        ))
        db.send_create_signal('people', ['Person'])


    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('people_person')


    models = {
        'people.person': {
            'Meta': {'object_name': 'Person'},
            'extra': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['people']
