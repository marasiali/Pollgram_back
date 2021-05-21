import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from socialmedia.models import User


class File(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    file = models.FileField(upload_to='polls/files/%Y/%m/%d/' + str(id), blank=True, null=True)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.ImageField(upload_to='polls/images/%Y/%m/%d/' + str(id), blank=True, null=True)


class Poll(models.Model):
    class PollVisibilityStatus(models.TextChoices):
        VISIBLE = 'VI', 'visible'
        VISIBLE_AFTER_VOTE = 'VA', 'visible_after_vote'
        HIDDEN = 'HI', 'hidden'

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    description = models.TextField()
    is_commentable = models.BooleanField(default=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, related_name='polls', null=True)
    file = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='polls', null=True)
    max_choice_can_vote = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(10)])
    min_choice_can_vote = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    attached_http_link = models.URLField(blank=True)
    is_vote_retractable = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    visibility_status = models.CharField(max_length=2, choices=PollVisibilityStatus.choices,
                                         default=PollVisibilityStatus.VISIBLE_AFTER_VOTE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'Poll = id: {}, creator: {}, question: {}'.format(self.id, self.creator, self.question)


class Choice(models.Model):
    context = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    order = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])

    class Meta:
        indexes = [
            models.Index(fields=['poll', 'order']),
        ]
        unique_together = ['poll', 'order']

    def get_votes(self):
        return self.votes.all()

    def __str__(self):
        return 'Choice = id: {}, context: {}'.format(self.id, self.context)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='votes')
    selected = models.ManyToManyField(Choice, related_name='votes')

    def __str__(self):
        return 'Vote = id: {}, userId: {}, choiceId: {}'.format(self.id, self.user.id, self.selected.id)
