# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Hearing.start_datetime'
        db.alter_column('committees_hearing', 'start_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 2, 8, 12, 22, 51, 760285)))

        # Adding unique constraint on 'Hearing', fields ['slug']
        db.create_unique('committees_hearing', ['slug'])

        # Adding unique constraint on 'Committee', fields ['slug']
        db.create_unique('committees_committee', ['slug'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Committee', fields ['slug']
        db.delete_unique('committees_committee', ['slug'])

        # Removing unique constraint on 'Hearing', fields ['slug']
        db.delete_unique('committees_hearing', ['slug'])

        # Changing field 'Hearing.start_datetime'
        db.alter_column('committees_hearing', 'start_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True))


    models = {
        'committees.committee': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Committee'},
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'committees.hearing': {
            'Meta': {'ordering': "('-start_datetime',)", 'object_name': 'Hearing'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hearings'", 'to': "orm['committees.Committee']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['committees']
