from django.contrib import admin
from .models import UserProfile, Cohort, Lesson, Question, QuestionTrueFalse, QuestionMCQS, QuestionFillInBlank, AssignCohort, Score

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'cohort')
    search_fields = ('name',)
    list_filter = ('cohort',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('statement', 'type', 'lesson')
    search_fields = ('statement',)
    list_filter = ('type', 'lesson')

@admin.register(QuestionTrueFalse)
class QuestionTrueFalseAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question__statement',)

@admin.register(QuestionMCQS)
class QuestionMCQSAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer')
    search_fields = ('question__statement',)

@admin.register(QuestionFillInBlank)
class QuestionFillInBlankAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question__statement',)

@admin.register(AssignCohort)
class AssignCohortAdmin(admin.ModelAdmin):
    list_display = ('user', 'cohort')
    search_fields = ('user__username', 'cohort__name')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'question', 'marks')
    search_fields = ('user__username', 'lesson__name', 'question__statement')

