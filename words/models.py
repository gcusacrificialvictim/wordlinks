from django.db import models
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager
import re

## Ugh, there's a lot of junk in here for managing tags. It's pretty ugly and
# unreadable and unmaintainable. The idea was that it's be easier and more
# flexible to model approval / rejection of words with a tag system, but I'm
# not sure that's the way its turned out at all.
#
# So what to do about it?
#
# Well, er, probably just having some flag columns in the DB would be ok.
#

class WordManager(models.Manager):
    def _get_available(self):
        return self.get_query_set().exclude(tags__name__in=['rejected'])
        
    def _get_verified(self):
        return self._get_available().filter(tags__name__in=['verified'])
        
    def _get_verified_clean(self):
        return self._get_clean().filter(tags__name__in=['verified'])

    def _get_unverified(self):
        return self._get_available().filter(tags__name__in=['unverified'])

    def _get_clean(self):
        return self._get_available().exclude(tags__name__in=['obscene', 'offensive'])
        
    def _get_rejected(self):
        return self.get_query_set().filter(tags__name__in=['rejected'])

    available = property(_get_available)
    clean = property(_get_clean)
    verified = property(_get_verified)
    verified_clean = property(_get_verified_clean)
    unverified = property(_get_unverified)
    rejected = property(_get_rejected)

word_re = re.compile(r'^[a-zA-Z]+$')
validate_word = RegexValidator(word_re, "Words should contain plain alphabetic characters only.", 'invalid')

class Word(models.Model):
    objects = WordManager()
    
    word = models.CharField(max_length=100, unique=True, validators=[validate_word]) 
    successor = models.ManyToManyField("self", symmetrical=False,
        blank=True, through='WordLink', related_name='predecessor') 
    
    tags = TaggableManager(blank=True)

    def _get_has_predecessors(self):
        # read 'there is an available [not deleted] word which comes *before*
        # this word to form a viable compound.'
        return Word.objects.available.filter(successor = self).exists()

    def _get_has_successors(self):
        # read 'there is an available [not deleted] word which comes *after*
        # this word to form a viable compound.'
        return Word.objects.available.filter(predecessor = self).exists()
    
    def _get_is_orphan(self):
        return not (self.has_predecessors or self.has_successors)

    def _get_is_terminus(self):
        return not self.has_predecessors or not self.has_successors

    has_predecessors = property(_get_has_predecessors)
    has_successors = property(_get_has_successors)
    is_orphan = property(_get_is_orphan)
    is_terminus = property(_get_is_terminus)

    def _get_is_verified(self):
        return self.tags.filter(name='verified').exists()

    def _get_is_unverified(self):
        return self.tags.filter(name='unverified').exists()

    def _get_is_rejected(self):
        return self.tags.filter(name='rejected').exists()

    def _get_is_obscene(self):
        return self.tags.filter(name='obscene').exists()

    def _get_is_offensive(self):
        return self.tags.filter(name='offensive').exists()

    def _get_is_junk(self):
        return self.tags.filter(name='junk').exists()

    is_verified = property(_get_is_verified)
    is_unverified = property(_get_is_unverified)
    is_rejected = property(_get_is_rejected)
    is_obscenity = property(_get_is_obscene)
    is_offensive = property(_get_is_offensive)
    is_junk = property(_get_is_junk)

    def mark(self, *args):
        self.tags.add(*args)

    def unmark(self, *args):
        self.tags.remove(*args)

    def verify(self):
        self.mark('verified')
        self.unmark('unverified', 'junk', 'rejected')
    def unverify(self):
        self.mark('unverified')
        self.unmark('verified')

    def reject(self):
        self.mark('rejected')
        self.unmark('unverified', 'verified')
    def unreject(self):
        self.unmark('rejected', 'junk')
        self.mark('verified')

    def obscene(self):
        self.mark('obscene')
    def unobscene(self):
        self.unmark('obscene')

    def offensive(self):
        self.mark('offensive')
    def unoffensive(self):
        self.unmark('offensive')

    def junk(self):
        self.tags.add('junk', 'rejected')
        self.tags.remove('verified', 'unverified')
    def unjunk(self):
        self.tags.remove('junk', 'rejected')
        self.tags.add('verified')

    def __unicode__(self):
        return self.word

    def save(self, *args, **kwargs):
        super(Word, self).save(*args, **kwargs) # Call the "real" save() method.
        if (not self.is_verified) and (not self.is_rejected):
            self.unverify()

    def clean(self):
        self.word = self.word.lower()

    class Meta:
        ordering = ['word']

class WordLinkManager(models.Manager):
    def _get_available(self):
        return self.get_query_set().exclude(tags__name__in=['rejected'])
    
    def _get_verified(self):
        return self._get_available().filter(tags__name__in=['verified'])
        
    def _get_verified_clean(self):
        return self._get_clean().filter(tags__name__in=['verified'])

    def _get_clean(self):
        return self._get_available().exclude(tags__name__in=['obscene', 'offensive'])
        
    def _get_rejected(self):
        return self.get_query_set().filter(tags__name__in=['rejected'])

    available = property(_get_available)
    clean = property(_get_clean)
    verified = property(_get_verified)
    verified_clean = property(_get_verified_clean)
    rejected = property(_get_rejected)
                
class WordLink(models.Model):
    objects = WordLinkManager()
    
    id = models.AutoField(primary_key=True)
    predecessor = models.ForeignKey(Word, related_name='forward_links')
    successor = models.ForeignKey(Word, related_name='backward_links')
    annotation = models.TextField(blank = True)

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.predecessor.word + ' ' + self.successor.word

    def _get_is_verified(self):
        return self.tags.filter(name='verified').exists()

    def _get_is_unverified(self):
        return self.tags.filter(name='unverified').exists()

    def _get_is_rejected(self):
        return self.tags.filter(name='rejected').exists()

    def _get_is_obscene(self):
        return self.tags.filter(name='obscene').exists()

    def _get_is_offensive(self):
        return self.tags.filter(name='offensive').exists()

    def _get_is_junk(self):
        return self.tags.filter(name='junk').exists()

    is_verified = property(_get_is_verified)
    is_unverified = property(_get_is_unverified)
    is_rejected = property(_get_is_rejected)
    is_obscenity = property(_get_is_obscene)
    is_offensive = property(_get_is_offensive)
    is_junk = property(_get_is_junk)

    def mark(self, *args):
        self.tags.add(*args)

    def unmark(self, *args):
        self.tags.remove(*args)

    def verify(self):
        self.mark('verified')
        self.unmark('unverified', 'junk', 'rejected')
        self.predecessor.verify()
        self.successor.verify()
    def unverify(self):
        self.mark('unverified')
        self.unmark('verified', 'junk', 'rejected')

    def reject(self):
        self.mark('rejected')
        self.unmark('unverified', 'verified')
    def unreject(self):
        self.unmark('rejected', 'junk')
        self.mark('verified')

    def obscene(self):
        self.mark('obscene')
    def unobscene(self):
        self.unmark('obscene')

    def offensive(self):
        self.mark('offensive')
    def unoffensive(self):
        self.unmark('offensive')

    def junk(self):
        self.tags.add('junk', 'rejected')
        self.tags.remove('verified', 'unverified')
    def unjunk(self):
        self.tags.remove('junk', 'rejected')
        self.tags.add('verified')

    def save(self, *args, **kwargs):
        super(WordLink, self).save(*args, **kwargs) # Call the "real" save() method.
        if (not self.is_verified) and (not self.is_rejected):
            self.unverify()

    class Meta:
        ordering = ['predecessor']
        unique_together = ('predecessor', 'successor')
