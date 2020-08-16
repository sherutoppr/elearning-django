from django.shortcuts import render

# for student registration
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


# for enrolment
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm

# for student course list
from django.views.generic.list import ListView
from courses.models import Course

# to see actually enrolled course content
from django.views.generic.detail import DetailView

# Create your views here.


# for  enrolled course detail view
class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):    # override it to limit the base qs to courses that are enrolled
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):   # override it to set a course module in the context if module_id is given
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context


# for student enrolled courses list
class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):      # to retrieve only those course that a student enrolled in
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


# to enroll the student to the course and redirect to student course detail
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']   # get the course
        self.course.students.add(self.request.user)  # add this user to the enrolled course
        return super().form_valid(form)

    def get_success_url(self):  # if form is successful, then user will redirect to this url
        return reverse_lazy('student_course_detail', args=[self.course.id])


# to register the student and redirect to student course list
class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result