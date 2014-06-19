# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'WordLink', fields ['predecessor', 'successor']
        db.create_unique(u'words_wordlink', ['predecessor_id', 'successor_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'WordLink', fields ['predecessor', 'successor']
        db.delete_unique(u'words_wordlink', ['predecessor_id', 'successor_id'])


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        },
        u'words.word': {
            'Meta': {'ordering': "['word']", 'object_name': 'Word'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'successor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'predecessor'", 'blank': 'True', 'through': u"orm['words.WordLink']", 'to': u"orm['words.Word']"}),
            'word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'words.wordlink': {
            'Meta': {'ordering': "['predecessor']", 'unique_together': "(('predecessor', 'successor'),)", 'object_name': 'WordLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'predecessor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forward_links'", 'to': u"orm['words.Word']"}),
            'successor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backward_links'", 'to': u"orm['words.Word']"})
        }
    }

    complete_apps = ['words']