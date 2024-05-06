from django.dispatch import receiver
from django.db.models.signals import pre_save

from quiz.models import UserQuizStatistic


@receiver(pre_save, sender=UserQuizStatistic)
def update_quiz_statistic(sender, instance, **kwargs):
    correct_answers = 0
    wrong_answers = 0

    for answer in instance.user_answers.all():
        correct_answers += 1 if answer.is_correct else 0
        wrong_answers += 1 if not answer.is_correct else 0

    instance.correct_answers = correct_answers
    instance.wrong_answers = wrong_answers

    return instance
