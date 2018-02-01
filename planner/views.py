from itertools import groupby
from datetime import date, datetime
from calendar import monthrange

from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect

from .models import User, Note
from .forms import CreateNoteForm, DeleteNoteForm


class UserSelectView(generic.ListView):
    template_name = 'planner/userselect.html'
    context_object_name = 'user_list'
    def get_queryset(self):
        return User.objects.all()


class ProfileView(generic.DetailView):
    model = User
    template_name = 'planner/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = timezone.now().year
        context['month'] = timezone.now().month
        return context

class NoteDetailView(generic.DetailView):
    model = Note
    template_name = 'planner/note_detail.html'
    context_object_name = 'note'


def del_note(request, pk, **kwargs):
    note_to_delete = get_object_or_404(Note, id=pk)
    # todo - check user and note_id
    if request.method == 'POST':
        form = DeleteNoteForm(request.POST, instance=note_to_delete)
        if form.is_valid(): # check csrf
            note_to_delete.delete()
            return HttpResponseRedirect("../..") # where to go
    else:
        form = DeleteNoteForm(instance=note_to_delete)
    template_vars = {'form': form, 'note': note_to_delete}
    return render(request, 'planner/del_note.html', template_vars)


def get_note(request, slug, **kwargs):
    # Must ensure slug uniqueness
    usr = User.objects.get(slug=slug)
    if request.method == 'POST':
        form = CreateNoteForm(request.POST)
        if form.is_valid():
            n = form.save(commit=False)
            n.user = usr
            n.save()
            return HttpResponseRedirect('..')
    else:
        form = CreateNoteForm()

    return render(request, 'planner/note.html', {'form': form})


def month_name(pMonthNumber):
    """
    Return the name of the month, given the number.
    """
    return date(1900, pMonthNumber, 1).strftime("%B")


def this_month(request):
    """
    Show calendar of notes this month.
    """
    today = datetime.now()
    return calendar(request, today.year, today.month)


def calendar(request, slug, pYear, pMonth, pNoteType=None, **kwargs):
    """
    Show calendar of notes for a given month of a given year.
    pNoteType denotes type of note to display
    """

    lYear = int(pYear)
    lMonth = int(pMonth)
    calendar_from_month = datetime(pYear, pMonth, 1)
    calendar_to_month = datetime(pYear, pMonth, monthrange(pYear, pMonth)[1])
    this_user = User.objects.get(slug=slug) # retrieves only notes for user
    lNoteEvents = Note.objects.filter(user=this_user)
    lNoteEvents = lNoteEvents.filter(expr_date__gte=calendar_from_month)
    lNoteEvents = lNoteEvents.filter(expr_date__lte=calendar_to_month)
    # Note types are not implemented yet
    if pNoteType is not None:
        lNoteEvents = lNoteEvents.filter(type=pNoteType)

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousYear = lYear - 1
        lPreviousMonth = 12
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextYear = lYear + 1
        lNextMonth = 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1
    return render(request,"planner/calendar.html", {
            'note_list': lNoteEvents,
            'month': lMonth,
            'month_name': month_name(lMonth),
            'year': lYear,
            'prev_month_name': month_name(lPreviousMonth),
            'prev_month': lPreviousMonth,
            'prev_year': lPreviousYear,
            'next_month': lNextMonth,
            'next_month_name': month_name(lNextMonth),
            'next_year': lNextYear,
            'year_before_this': lYearBeforeThis,
            'year_after_this': lYearAfterThis,
            'slug':slug
    })
