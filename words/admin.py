from django.contrib import admin
from words.models import Word, WordLink

class LinkInline(admin.TabularInline):
    model = WordLink
    fk_name = 'successor'
    extra = 1
    verbose_name = 'link from a preceding word'

class LinkBackInline(admin.TabularInline):
    model = WordLink
    fk_name = 'predecessor'
    extra = 1
    verbose_name = 'link to a following word'

class WordAdmin(admin.ModelAdmin):
    actions = [ 'verify', 'unverify', 'reject', 'junk', 'offensive', 'obscene', ]
    search_fields = ['word']
    inlines = [ LinkInline, LinkBackInline ]
    exclude = ('successor', )

    list_display = ('word', 'is_verified', 'is_obscenity', 'is_offensive', 'is_junk', 'is_rejected')
    list_filter = ('tags', )

    ordering = ('word', ) 

    def verify(self, request, queryset):
        for word in queryset:
            word.verify()
    verify.short_description = "Approve"

    def unverify(self, request, queryset):
        for word in queryset:
            word.unverify()
    unverify.short_description = "Unapprove"
    
    def reject(self, request, queryset):
        for word in queryset:
            word.reject()
    reject.short_description = "Reject"

    def junk(self, request, queryset):
        for word in queryset:
            word.junk()
    junk.short_description = "Reject as junk / spam"

    def offensive(self, request, queryset):
        for word in queryset:
            word.offensive()
    offensive.short_description = "Mark offensive"

    def obscene(self, request, queryset):
        for word in queryset:
            word.obscene()
    obscene.short_description = "Mark obscene"

class WordLinkAdmin(admin.ModelAdmin):
    actions = [ 'verify', 'unverify', 'reject', 'junk', 'offensive', 'obscene', ]
    search_fields = ['predecessor', 'successor']

    list_display = ('__unicode__', 'is_verified', 'is_obscenity', 'is_offensive', 'is_junk', 'is_rejected')
    list_filter = ('tags', )

    def verify(self, request, queryset):
        for word in queryset:
            word.verify()
    verify.short_description = "Approve"

    def unverify(self, request, queryset):
        for word in queryset:
            word.unverify()
    unverify.short_description = "Unapprove"
    
    def reject(self, request, queryset):
        for word in queryset:
            word.reject()
    reject.short_description = "Reject"

    def junk(self, request, queryset):
        for word in queryset:
            word.junk()
    junk.short_description = "Reject as junk / spam"

    def offensive(self, request, queryset):
        for word in queryset:
            word.offensive()
    offensive.short_description = "Mark offensive"

    def obscene(self, request, queryset):
        for word in queryset:
            word.obscene()
    obscene.short_description = "Mark obscene"

admin.site.register(Word, WordAdmin, )
admin.site.register(WordLink, WordLinkAdmin)