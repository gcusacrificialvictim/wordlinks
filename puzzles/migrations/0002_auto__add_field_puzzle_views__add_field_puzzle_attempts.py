# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Puzzle.views'
        db.add_column(u'puzzles_puzzle', 'views',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Puzzle.attempts'
        db.add_column(u'puzzles_puzzle', 'attempts',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Puzzle.views'
        db.delete_column(u'puzzles_puzzle', 'views')

        # Deleting field 'Puzzle.attempts'
        db.delete_column(u'puzzles_puzzle', 'attempts')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'puzzles.answer': {
            'Meta': {'unique_together': "(('puzzle', 'answer'),)", 'object_name': 'Answer'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['words.Word']"}),
            'attempts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'puzzle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['puzzles.Puzzle']"})
        },
        u'puzzles.puzzle': {
            'Meta': {'unique_together': "(('left', 'right'),)", 'object_name': 'Puzzle'},
            'attempts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'left+'", 'to': u"orm['words.Word']"}),
            'right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'right+'", 'to': u"orm['words.Word']"}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
            'Meta': {'ordering': "['predecessor']", 'object_name': 'WordLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'predecessor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forward_links'", 'to': u"orm['words.Word']"}),
            'successor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backward_links'", 'to': u"orm['words.Word']"})
        }
    }

    complete_apps = ['puzzles']