from django.db import models

from users.models import User
from utils.models import CreateUpdateTracker


class Quiz(CreateUpdateTracker):
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.title


class Question(CreateUpdateTracker):
    title = models.CharField(max_length=255)

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title


class Answer(CreateUpdateTracker):
    title = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.title


class UserQuizStatistic(CreateUpdateTracker):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_quiz_statistic')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_quiz_statistic')
    correct_answers = models.ManyToManyField(Answer, related_name='user_quiz_statistic', blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.quiz_id}"