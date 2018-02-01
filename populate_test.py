## Populates database with test data
import datetime

from planner.models import Note, User
from django.utils import timezone

user1 = User(first_name='Daniel', last_name='Friberg',
        birthday=timezone.now(),
        motto = "live and let live")
user2 = User(first_name='Charlie', last_name='Dog',
            birthday=timezone.now(),motto='bark')
user1.save()
user2.save()
user1.note_set.create(
    title='note 1',
    content='finish this',
    post_date=timezone.now(),
    expr_date=timezone.now()+datetime.timedelta(days=3),
    priority=1,
)

user1.note_set.create(
    title='note 2',
    content='This is the second note',
    post_date=timezone.now(),
    expr_date=timezone.now()+datetime.timedelta(days=-43),
    priority=1,
)

user2.note_set.create(
    title='bark'
    content='barkbarkbark'
)
