from django.urls import path
from . import views
urlpatterns = [

    # for Course model CRUD function
    path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),  # <app>/manage/<model>/list.html G
    path('create/', views.CourseCreateView.as_view(), name='course_create'),  # <app>/manage/<model>/form.html
    path('<pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),  # <app>/manage/<model>/form.html
    path('<pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),  # <app>/manage/<model>/delete.html G

    # for Content model CRUD function
    path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),        # <app>/manage/<model=content>/form.html create (Given)
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCreateUpdateView.as_view(),         # <app>/manage/<model=content>/form.html update (Given)
         name='module_content_update'),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),  # no html
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),  # list Given

    # for Module model CRUD function
    path('<pk>/module/',
         views.CourseModuleUpdateView.as_view(),        # <app>/manage/<model=module>/formset.html update (Given)
         name='course_module_update'),


    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),

    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_subject'),  # all course Given
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),     # course detail  Given
]