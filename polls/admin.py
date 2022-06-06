from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsest = [
        (None, {'fields': ['question_text']}),
        ('Date info', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'get_value')
    list_filter = ('pub_date',)
    search_fields = ['question_text']

    def get_queryset(self, request):
        return super().get_queryset(request).do_annotation()

    def get_value(self, obj):
        return obj.was_published_recently

    get_value.admin_order_field = "was_published_recently"
    get_value.short_description = "was published recently"


admin.site.register(Question, QuestionAdmin)
