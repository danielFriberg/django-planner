from calendar import HTMLCalendar
from django import template
from datetime import date
from itertools import groupby
import logging

from django.utils.html import conditional_escape as esc

register = template.Library()
logger = logging.getLogger(__name__)

def do_note_calendar(parser, token):
    """
    The template tag's syntax is { % note_calendar year month note_list %}
    """

    try:
        tag_name, year, month, note_list = token.split_contents()
    except ValueError:
        pass#raise template.TemplateSyntaxError,     "%r tag requires three arguments" % token.contents.split()[0]
    return NoteCalendarNode(year, month, note_list)


class NoteCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, note_list):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.note_list = template.Variable(note_list)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            my_note_list = self.note_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            cal = NoteCalendar(my_note_list)
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return
        except template.VariableDoesNotExist:
            return


class NoteCalendar(HTMLCalendar):

    def __init__(self, pNote):
        super(NoteCalendar, self).__init__()
        self.notes = self.group_by_day(pNote)
        logger.error(self.notes)

    def formatday(self, day, weekday):
        if day != 0:
            #logger.info(day)
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.notes:
                cssclass += ' filled'
                body = ['<ul>']
                for note in self.notes[day]:
                    logger.error(note)
                    body.append('<li>')
                    body.append(esc(note.title))
                    body.append('</li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '<span class="dayNumber">%d</span> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<span class="dayNumberNoReadings">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(NoteCalendar, self).formatmonth(year, month)

    def group_by_day(self, notes):
        field = lambda note: note.expr_date.date().day
        # return dict(
        #         [(day, list(items)) for day, items in groupby(notes, field)]
        # )
        return dict(
            [(day, list(items)) for day, items in groupby(notes, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

register.tag("note_calendar", do_note_calendar)
