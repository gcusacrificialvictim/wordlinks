from puzzles.models import Puzzle
from words.models import Word

class PuzzleFactoryException(Exception):
        pass

def generate_puzzle():
    i = 0
    w = Word.objects.verified.order_by('?')[0]
    
    while w.is_terminus and i < 30:
        i = i + 1
        w = Word.objects.verified.order_by('?')[0]

    try:
        puzzle = generate_puzzle_for(w)
    except PuzzleFactoryException:
        return Puzzle.objects.all().order_by('?')[:1].get();

    return puzzle

def generate_puzzle_for(answer):
    if answer.is_terminus:
        raise PuzzleFactoryException("Can't generate puzzles on terminal word '%s'." % answer.word )

    left_word = answer.predecessor.verified.order_by('?')[0]
    right_word = left_word
    i = 0
    while left_word == right_word and i < 10:
        right_word = answer.successor.verified.order_by('?')[0]
        i = i + 1

    if left_word == right_word:
        raise PuzzleFactoryException("Word selection for '%s' too limited." % answer.word )

    p, created = Puzzle.objects.get_or_create(left = left_word, right = right_word)

    return p

def generate_false_puzzle(candidate):
    # the idea here is that we may learn something from these false 'puzzles'
    # (they may even turn out to be perfectly valid!)
    
    random_word = Word.objects.verified.order_by('?')[0]

    w1 = candidate
    w2 = random_word

    if candidate.has_predecessors or (not candidate.is_terminus and random.choice([0, 1])):
        w1 = random_word
        w2 = candidate

    p, created = Puzzle.objects.get_or_create(left = w1, right = w2)
    return p
