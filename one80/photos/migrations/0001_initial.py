# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Photo'
        db.create_table('photos_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hearing', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['committees.Hearing'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('photos', ['Photo'])

        # Adding model 'Size'
        db.create_table('photos_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sizes', to=orm['photos.Photo'])),
            ('width', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('is_original', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('photos', ['Size'])

        # Adding model 'Annotation'
        db.create_table('photos_annotation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='annotations', to=orm['photos.Photo'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='annotations', to=orm['auth.User'])),
            ('x_pct', self.gf('django.db.models.fields.FloatField')()),
            ('y_pct', self.gf('django.db.models.fields.FloatField')()),
            ('width_pct', self.gf('django.db.models.fields.FloatField')()),
            ('height_pct', self.gf('django.db.models.fields.FloatField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal('photos', ['Annotation'])


    def backwards(self, orm):
        
        # Deleting model 'Photo'
        db.delete_table('photos_photo')

        # Deleting model 'Size'
        db.delete_table('photos_size')

        # Deleting model 'Annotation'
        db.delete_table('photos_annotation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'committees.committee': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Committee'},
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'committees.hearing': {
            'Meta': {'ordering': "('-start_datetime',)", 'object_name': 'Hearing'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hearings'", 'to': "orm['committees.Committee']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'photos.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'annotations'", 'to': "orm['auth.User']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'height_pct': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'annotations'", 'to': "orm['photos.Photo']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'width_pct': ('django.db.models.fields.FloatField', [], {}),
            'x_pct': ('django.db.models.fields.FloatField', [], {}),
            'y_pct': ('django.db.models.fields.FloatField', [], {})
        },
        'photos.photo': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Photo'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'hearing': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['committees.Hearing']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'photos.size': {
            'Meta': {'object_name': 'Size'},
            'height': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_original': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sizes'", 'to': "orm['photos.Photo']"}),
            'width': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['photos']
