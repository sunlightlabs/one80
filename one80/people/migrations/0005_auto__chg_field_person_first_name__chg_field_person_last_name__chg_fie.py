# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Person.first_name'
        db.alter_column('people_person', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'Person.last_name'
        db.alter_column('people_person', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'Person.title'
        db.alter_column('people_person', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Person.organization'
        db.alter_column('people_person', 'organization', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Changing field 'Person.slug'
        db.alter_column('people_person', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=64))


    def backwards(self, orm):
        
        # Changing field 'Person.first_name'
        db.alter_column('people_person', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Person.last_name'
        db.alter_column('people_person', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Person.title'
        db.alter_column('people_person', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Person.organization'
        db.alter_column('people_person', 'organization', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Person.slug'
        db.alter_column('people_person', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))


    models = {
        'people.person': {
            'Meta': {'object_name': 'Person'},
            'extra': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['people']
