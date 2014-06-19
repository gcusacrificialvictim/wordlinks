from django import forms
from django.forms import widgets
from django.shortcuts import render, redirect, get_object_or_404
from puzzles.models import Puzzle, Answer, WrongAnswerException
from words.models import Word

# Create your views here.

# TODO: remove most of these views. keep puzzle_get as entrypoint

def index(request):
    puzzles = Puzzle.objects.all().order_by('?')[:10]
    return render(request, 'puzzles/index.html', {'puzzles': puzzles})

def puzzle_show(request, puzzle):
    form = PuzzleForm();
    return render(request, 'puzzles/puzzle.html',
        {'puzzle': puzzle, 'form': form })

def puzzle_id(request, puzzle_id):
    puzzle = get_object_or_404(Puzzle, pk=puzzle_id)
    return puzzle_show(request, puzzle)

def puzzle_by_words(request, left, right):
    w1 = get_object_or_404(Word, word=left)
    w2 = get_object_or_404(Word, word=right)
    puzzle = get_object_or_404(Puzzle, left=w1, right=w2)
    return puzzle_show(request, puzzle)

def puzzle_random(request):
    puzzle = Puzzle.objects.all().order_by('?')[:1].get()
    return puzzle_show(request, puzzle)


def puzzle_get(request):
    from puzzles.factory import PuzzleFactoryException, generate_puzzle
    try:
        p = generate_puzzle()
        return redirect(p)
    except PuzzleFactoryException:
        pass
    return render(request, 'puzzles/generate_error.html' )


# answer form

class PuzzleForm(forms.Form):
    answer = forms.CharField(max_length=100, min_length=3,
        required=True, label='')

def answer(request, puzzle_id):
    from django.shortcuts import redirect
    puzzle = get_object_or_404(Puzzle, pk=puzzle_id)
    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        if form.is_valid():
            # process form.cleaned_data
            w = form.cleaned_data['answer']
            word, created = Word.objects.get_or_create(word=w)
            answer = puzzle.answer(word);
            link1, link2 = answer.get_links()
            template_args = {'puzzle': puzzle, 'answer': answer,
                'left_link': link1, 'right_link': link2}
            if answer.is_verified:
                return render(request, 'puzzles/answer.html', template_args)
            elif answer.is_rejected: 
                return render(request, 'puzzles/rejected.html', template_args)
            else:
                return render(request, 'puzzles/unverified.html', template_args)
        else: # redisplay form with error notification:
            return render(request, 'puzzles/puzzle.html',
                        {'puzzle': puzzle, 'form': form })

    return redirect(puzzle)

# creation action

def puzzle_create(request, word):
    w = get_object_or_404(Word, word=word)
    if request.method == 'POST':
        f_left  = request.POST['left']
        f_right = request.POST['right']
        # TODO: all this could go wrong and exceptions need to be caught!
        w_left  = Word.objects.get(word = f_left)
        w_right = Word.objects.get(word = f_right)
        p = Puzzle.objects.create(left = w_left, right = w_right)
        a = Answer.objects.create(puzzle = p, answer = w)
        return render(request, 'puzzles/create.html', { 'word': w, 'puzzle': p, 'answer': a } )
    return render(request, 'puzzles/create.html', { 'word': w } )

