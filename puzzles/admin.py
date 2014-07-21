from django.contrib import admin
from puzzles.models import Puzzle, Answer

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'puzzle', 'answer', 'is_verified')
    actions = ['verify']

    def verify(self, request, queryset):
        for answer in queryset:
            answer.verify();
    verify.short_description = "Approve selected answers"

admin.site.register(Puzzle)
admin.site.register(Answer, AnswerAdmin)