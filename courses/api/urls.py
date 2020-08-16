from django.urls import path, include
from . import views
from django.views.decorators.cache import cache_page

# routers used for both list() or retrieval of single objects
from rest_framework import routers

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
    path('subjects/', (cache_page(60*5))(views.SubjectListView.as_view()) , name='subject_list'),
    path('subjects/<pk>/', (cache_page(60*5))(views.SubjectDetailView.as_view()) , name='subject_detail'),
    # path('courses/<pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
]