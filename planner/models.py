import datetime

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField(default=timezone.now)
    motto = models.CharField(max_length=200, default='What is your motto?')
    slug = models.SlugField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # doesnt handle duplicate slugs
    def save(self, *args, **kwargs):
        if not self.id:
            #newly created so set slu
            slug_str = "%s %s" % (self.first_name, self.last_name)
            self.slug = slugify(slug_str)
        super(User, self).save(*args, **kwargs)


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    post_date = models.DateField('date posted',default=timezone.now)
    expr_date = models.DateTimeField('expiration date', default=timezone.now)
    priority = models.IntegerField(default=-1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            #newly created so set slug
            self.slug = slugify(self.title)
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title + ': ' + self.content

    def expired(self):
        now = timezone.now()
        return self.expr_date < now

    def expiring_within_week(self):
        now = timezone.now()
        return (not self.expired()) and (
                now + datetime.timedelta(days=7) >= self.expr_date)
