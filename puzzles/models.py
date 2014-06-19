from django.db import models
from django.db.models import F
from words.models import Word

class WrongAnswerException(Exception):
        pass

class Puzzle(models.Model):
    left = models.ForeignKey(Word, related_name='left+')
    right = models.ForeignKey(Word, related_name='right+')
    views = models.PositiveIntegerField(default=0)
    attempts =  models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.left.word + ' / ' + self.right.word

    def get_absolute_url(self):
        ## from django.core.urlresolvers import reverse
        return "/puzzles/%s/%s/" % (self.left, self.right);
        ## return reverse('puzzles.views.puzzle_by_words',
        ##     args=(self.left.word, self.right.word))

    def answer(self, word):
        self.attempts = self.attempts + 1
        self.save()
        answer, created = Answer.objects.get_or_create(puzzle=self, answer = word)
        answer.make_links()
        answer.attempts = F('attempts') + 1
        answer.save()
        return Answer.objects.get(pk=answer.pk)

    class Meta:
        unique_together = ('left', 'right')

class Answer(models.Model):
    puzzle = models.ForeignKey(Puzzle, related_name='answers')
    answer = models.ForeignKey(Word)
    attempts = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.puzzle.left.word + ' * ' + self.answer.word + ' * ' + self.puzzle.right.word

    @property
    def is_verified(self):
        link1, link2 = self.get_links()
        return (
            self.puzzle.left.is_verified and
            self.puzzle.right.is_verified and 
            self.answer.is_verified and
            link1.is_verified and
            link2.is_verified
        )

    @property
    def is_rejected(self):
        link1, link2 = self.get_links()
        return (
            self.puzzle.left.is_rejected or
            self.puzzle.right.is_rejected or 
            self.answer.is_rejected or
            link1.is_rejected or
            link2.is_rejected
        )

    def make_links(self):
        return self.get_links();

    def get_links(self):
        from words.models import WordLink
        link1, created1 = WordLink.objects.get_or_create(predecessor = self.puzzle.left, successor = self.answer)
        link2, created2 = WordLink.objects.get_or_create(predecessor = self.answer, successor = self.puzzle.right)
        return (link1, link2)

    def verify():
        # approving an answer means first approving the component words if
        # necessary: 
        self.puzzle.left.verify();
        self.puzzle.left.save();
        self.puzzle.right.verify();
        self.puzzle.right.save();
        self.answer.verify();
        self.answer.save();

        ## then the two links A -> B and B -> C need to be created if necessary
        ## and also approved: 
        link1, link2, c1, c2 = self.get_links()
        link1.verify();
        link2.verify();
        link1.save();
        link2.save();
        
        ## the actual answer object (self) doesn't change at all.

    class Meta:
        unique_together = ('puzzle', 'answer')
