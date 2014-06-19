from django.contrib import admin
from puzzles.models import Puzzle, Answer

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'puzzle', 'answer', 'is_verified')

admin.site.register(Puzzle)
admin.site.register(Answer, AnswerAdmin)