import os
import uuid
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError
from socialmedia.models import User


class File(models.Model):
    def get_upload_file_url(self, file_name):
        _, ext = os.path.splitext(file_name)
        now = datetime.now()
        return 'polls/files/{}/{}/{}/'.format(now.year, now.month, now.day) + str(self.id) + ext

    def validate_file_size(value):
        limit = 30 * 1024 * 1024
        if value.size > limit:
            raise ValidationError('Maximum size limit exceeded.')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    file = models.FileField(upload_to=get_upload_file_url, blank=True, null=True, max_length=200,
                            validators=[validate_file_size])


class Image(models.Model):
    def get_upload_file_url(self, image_name):
        _, ext = os.path.splitext(image_name)
        now = datetime.now()
        return 'polls/images/{}/{}/{}/'.format(now.year, now.month, now.day) + str(self.id) + ext

    def validate_image_size(value):
        limit = 10 * 1024 * 1024
        if value.size > limit:
            raise ValidationError('Maximum size limit exceeded.')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.ImageField(upload_to=get_upload_file_url, blank=True, null=True, max_length=200,
                              validators=[validate_image_size])


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('order',)

    def __str__(self):
        return 'Category = name: {}, id: {}, parent_id: {}'.format(self.name, self.id,
                                                                   '{}' if self.parent is None else self.parent.id)

    def get_sub_categories(self):
        return self.sub_categories.all()


class Poll(models.Model):
    class PollVisibilityStatus(models.TextChoices):
        VISIBLE = 'VI', 'visible'
        VISIBLE_AFTER_VOTE = 'VA', 'visible_after_vote'
        HIDDEN = 'HI', 'hidden'

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_commentable = models.BooleanField(default=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, related_name='polls', null=True)
    file = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='polls', null=True)
    max_choice_can_vote = models.PositiveSmallIntegerField(default=1,
                                                           validators=[MinValueValidator(1), MaxValueValidator(10)])
    min_choice_can_vote = models.PositiveSmallIntegerField(default=1,
                                                           validators=[MinValueValidator(1), MaxValueValidator(10)])
    attached_http_link = models.URLField(blank=True)
    is_vote_retractable = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    visibility_status = models.CharField(max_length=2, choices=PollVisibilityStatus.choices,
                                         default=PollVisibilityStatus.VISIBLE_AFTER_VOTE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='polls', null=True)

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


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField("content", max_length=2000)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        username = self.creator.username
        _content = self.content[:20]
        if not self.parent:
            return f'{self.id}) comment by {username} on poll {self.poll.id}: {_content}'
        else:
            return f'{self.id}) reply by {username} on comment {self.parent.id}: {_content}'

    likes = models.ManyToManyField(User, related_name='liked_comment')
    dislikes = models.ManyToManyField(User, related_name='disliked_comment')
