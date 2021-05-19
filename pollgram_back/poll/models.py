from django.db import models
from socialmedia.models import User


class Poll(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    description = models.TextField()
    is_commentable = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'Poll = id: {}, creator: {}, question: {}'.format(self.id, self.creator, self.question)


class Choice(models.Model):
    context = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    order = models.IntegerField()

    def get_votes(self):
        return self.votes.all()

    def __str__(self):
        return 'Choice = id: {}, context: {}'.format(self.id, self.context)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='votes')
    selected = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')

    def __str__(self):
        return 'Vote = id: {}, userId: {}, choiceId: {}'.format(self.id, self.user.id, self.selected.id)
