# Django_Project_E_Learning_Website_Educa
This is my 7th and biggest project of Django ever. I am very excited about it. Let's start..

1. python manage.py dumpdata courses --indent=2 --output=courses/fixtures/
subjects.json --> to save data from database to json file

2. python manage.py loaddata subjects.json  -> from json file to data base

3. Created models for diverse content using model inheritance

4. created content model and custom model field for relative ordering of module and content

5. Added an authentication system

6. CRUD for course added and ceeate and update have same html and form

7. to access style files , set staticfiles to settings

8. created class-based views and used mixin , work with group and permission of admin-site, restricted the class-based views

9. used formset to create various module for courses and various content for a module.

10. The management form(in the formsets) includes hidden field to control the initial, total, minimum, and maximum number of forms

11. pip install django-braces==1.14.0 it works

12. for enrolment many to many relationship between user and courses

13. for video upload and save - pip install django-embed-video

14. for cached system - > conda install -c anaconda python-memcached, then add it to setting.py

15. to monitor memchached  - > pip install django-memcache-status==2.2 and set sth in admin.py in that app where u want to use it

16. all type of cache done 

17. render means from server to client(response)

18. parse means from client to server(request)

19. installed postman for custom HTTP request 

20. python request package -> pip install requests==2.23 

21. user can enrolled using api done 

22. WSGI can handle only HTTP request and for chat room , we have to use websocket request and websocket request require ASGI.

23. for chat room -> pip install channels==2.4.0

24. for channel layer -> pip install channels-redis==2.4.0

25 When Channels is added to the INSTALLED_APPS setting, it takes control over the
runserver command, replacing the standard Django development server. Besides
handling URL routing to Django views for synchronous requests, the Channels
development server also manages routes to WebSocket consumers.

26->consumer = django views for asynchronous applicaiton that handle message , notification and other things.

27->Unlike Django views, consumers are built for longrunning
communication  

28 routing = url for asynchronous application

29 In order to build communication between consumers, you
have to enable a channel layer. A channel layer is the transport mechanism that allows multiple
consumer instances to communicate with each other and with other parts of Django

30 Channel: You can think of a channel as an inbox where messages can be
sent to or as a task queue. Each channel has a name. Messages are sent
to a channel by anyone who knows the channel name and then given to
consumers listening on that channel.

31 Group: Multiple channels can be grouped into a group. Each group has
a name. A channel can be added or removed from a group by anyone
who knows the group name. Using the group name, you can also send
a message to all channels in the group.

32-> Redis is the preferred option for a channel layer, though Channels has support
for other types of channel layers. Redis works as the communication store for the
channel layer.

33 memcached.exe -vv -> to run cache server from its directory

34 open ubuntu and run redis-server

35 created multiple environment for real-life project

36 local.py for custom settings for your local environment

37 pro.py for custom settings for your production environment

38 open shell and run : export DJANGO_SETTINGS_MODULE=educa.settings.pro  --> this command set the django_settings_module for current settion 

39. or 2nd option - > python manage.py shell --settings=educa.settings.pro 
