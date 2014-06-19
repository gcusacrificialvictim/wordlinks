from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from words.models import Word

def index(request):
        word_list = Word.objects.verified_clean
        paginator = Paginator(word_list, 50)
        
        page = request.GET.get('page')
        try:
            words = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            words = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            words = paginator.page(paginator.num_pages)
        
        return render_to_response('words/index.html', { 'word_list': words });

def detail_id(request, word_id):
        word = get_object_or_404(Word, pk=word_id)
        return render(request, 'words/detail.html', {'word': word});

def detail_string(request, word_string):
        word = get_object_or_404(Word, word__exact=word_string)
        return render(request, 'words/detail.html', {'word': word});