from django.contrib import admin

from quiz.models import Quiz, Question, Answer, UserQuizStatistic


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "author")
    list_display_links = ("id", "title", "category")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "title", "is_correct")
    list_display_links = (
        "id",
        "title",
    )

    ordering = ("question",)


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "quiz")
    list_display_links = (
        "id",
        "title",
    )

    inlines = (AnswerInline,)


@admin.register(UserQuizStatistic)
class UserQuizStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "quiz", "correct_answers", "wrong_answers")
    list_display_links = ("id", "user", "quiz")
