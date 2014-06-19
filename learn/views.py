from django import forms
from django.shortcuts import render, get_object_or_404
from django.forms import widgets
from words.models import Word, WordLink, validate_word

WORD_ORDER_CHOICES = (
    (0, 'Before'), #  BLANK some_word
    (1, 'After'),  #  some_word BLANK
)

class LearnForm(forms.Form):
    word = forms.CharField(widget = widgets.HiddenInput, max_length=100, \
        min_length=3, required=True, validators = [validate_word] )
    submission = forms.CharField(max_length=100, min_length=3, required=True, \
        label='', validators = [validate_word])
    word_order = forms.ChoiceField(choices = WORD_ORDER_CHOICES, \
        widget = widgets.HiddenInput)
    
def learn_word(request, word):
    from django.shortcuts import redirect
    context = {}
    if request.method == 'POST':
        form = LearnForm(request.POST)
        if form.is_valid():
            # process form.cleaned_data
            word_order = form.cleaned_data['word_order']
            f_root_word = form.cleaned_data['word']
            f_submission = form.cleaned_data['submission']
            
            root_word = Word.objects.get(word=f_root_word)
            submission, created = Word.objects.get_or_create(word=f_submission)

            new_link = False
            link = ""
            if word_order == '0':
                link = submission.word + " " + root_word.word
                if not root_word.predecessor.filter(word=submission).exists():
                    link, new_link = WordLink.objects.get_or_create(
                        predecessor = submission, successor = root_word)
            else:
                link = root_word.word + " " + submission.word
                if not root_word.successor.filter(word=submission).exists():
                    link, new_link = WordLink.objects.get_or_create(
                        predecessor = root_word, successor = submission)

            # drop through here to set up another learning opportunity
            # TODO: I'm sure this is the wrong way to do things!
            context['learned'] = True
            context['link'] = link
            context['last_order'] = word_order
            context['last_word'] = root_word
            context['last_submission'] = submission
            context['link_created'] = new_link
            context['word_created'] = created
        else:
            # form was invalid, so redisplay with errors.
            return render(request, 'learn/index.html',
                {'form': form })

    import random
    order = str(random.randint(0, 1))
    form = LearnForm( initial = { 'word': word, 'word_order': order } )
    context['form'] = form

    return render(request, 'learn/index.html',
        context )


def index(request):
    from django.shortcuts import redirect
    w = Word.objects.verified.order_by('?')[0]
    return redirect('learn:learn_word', word = w.word)
