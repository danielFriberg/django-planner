import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Note

class NoteModelTests(TestCase):

    def test_expired_expired_note(self):
        time = timezone.now() + datetime.timedelta(days=-4)
        old_note = Note(expr_date=time)
        self.assertIs(old_note.expired(), True)

    def test_expired_non_expired_note(self):
        time = timezone.now() + datetime.timedelta(days=4)
        new_note = Note(expr_date=time)
        self.assertIs(new_note.expired(), False)

    def test_expiring_within_week_within_week_note(self):
        time = timezone.now() + datetime.timedelta(days=4)
        new_note = Note(expr_date=time)
        self.assertIs(new_note.expiring_within_week(), True)

    def test_expiring_within_week_within_month_note(self):
        time = timezone.now() + datetime.timedelta(days=30)
        new_note = Note(expr_date=time)
        self.assertIs(new_note.expiring_within_week(), False)

    def test_expiring_within_week_expired_note_month(self):
        time = timezone.now() + datetime.timedelta(days=-30)
        old_note = Note(expr_date=time)
        self.assertIs(old_note.expiring_within_week(), False)

    def test_expiring_within_week_expired_note_2days(self):
        time = timezone.now() + datetime.timedelta(days=-2)
        old_note = Note(expr_date=time)
        self.assertIs(old_note.expiring_within_week(), False)
