from django.urls import path

from . import views

app_name = 'planner'
urlpatterns = [
    path('', views.UserSelectView.as_view(), name='userselect'),
    path('<slug:slug>/', views.ProfileView.as_view(), name='profile'),
    path('<slug:slug>/<int:pk>', views.NoteDetailView.as_view(), name='note_detail'),
    path('<slug:slug>/new_note/', views.get_note, name='new_note'),
    path('<slug:slug>/<int:pk>/delete/', views.del_note, name='del_note'),
    path('<slug:slug>/calendar/<int:pYear>/<int:pMonth>', views.calendar, name ='calendar')
]

"""
<slug:slug> allows you to have a slug field
that contains the url portion in the view field
"""
