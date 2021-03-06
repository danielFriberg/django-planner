=====
Planner
=====

Planner is a calendar/note managing app. The intent of this calendar
is to place an emphasis on personal management and goals - self 
improvement type of stuff - rather than scheduling. I could never find
an app suitable for my needs elsewhere, so I decided to work towards one
myself. It will be worked on occasionally, but as of now it is barebones
without any styling whatsoever.  

It makes use of a custom User model instead of the built in Django user 
model for purposes of simplicity. The next step in developement will be
to abandon the custom User model and provide user authentication using
the authentication system provided by Django. 

Asides from personal need, I started the task of creating an app in order
to be comfortable with making use of databases instead of a simple file system,
as well as to familiarize myself with the structure of Python programs. As it
is meant for personal use, I do not think there will be any effort in improving
the aesthetics in the near future. 



Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'planner',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('planner/', include('planner.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user defined by the planner.

5. Visit http://127.0.0.1:8000/planner/ to select a user and begin 
   adding notes.


Notes
---------------
If notes are displayed in the wrong day, you may have not assigned your
timezone properly in the project/database settings