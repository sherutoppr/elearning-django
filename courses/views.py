from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet

# add content to the module
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content

# reordering
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

# display courses
from django.db.models import Count


# display a single course overview
from django.views.generic.detail import DetailView

# to enroll a student to the course
from students.forms import CourseEnrollForm

# for cache
from django.core.cache import cache
from .models import Course, Subject
# Create your views here.


# display a single course overview and enrollment button
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context


# list of all available courses , filter by subject (doing 2 work simultaneously)
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        # subjects = Subject.objects.annotate(total_courses=Count('courses'))  # retrieve all subjects
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)

        all_courses = Course.objects.annotate(total_modules=Count('modules'))    # retrieve all courses with modules

        if subject:   # if a subject given, we retrieve that subject with courses, not modules
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get('key')
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'subjects': subjects, 'subject': subject, 'courses': courses})


# to reorder the module of an course
class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


# to reorder the content of an module
class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


# to list all module of a course and their content
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


# to delete the content of an module
class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


# to create and update the content of an module of an course
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    # used to get available content type model by model name -text, video, image , file
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    # create dynamic form for content type and dont include excluded fields
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    # first func to be called and save data then, call get or post method based on request type
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:             # when u update , id already generated so use this content to update
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    # executed when a GET request is received by dispatch method
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)     # create model form based on content type
        return self.render_to_response({'form': form, 'object': self.obj})

    # executed when a POST  request is received by dispatch method
    def post(self, request, module_id, model_name, id=None):
        # build the model form with received data and files
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)   # create the new object
            obj.owner = request.user
            obj.save()
            if not id:      # creation time, id is not generated so create new object
                Content.objects.create(module=self.module, item=obj)   # new content
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


# to create and update the module of an course
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    # method to avoid repeating the code to build the formset
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    # first function to retrieve the request and course id
    # for both GET and POST requests and sent request to get or post functions
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    # Executed for GET requests
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()          # build the formset and render it to template with course object
        return self.render_to_response({'course': self.course, 'formset': formset})

    # Executed for POST requests
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)     # build the formset
        if formset.is_valid():       # validate all forms
            formset.save()                            # if all forms are valid then,
            return redirect('manage_course_list')     # save it and redirect to course list
        return self.render_to_response({'course': self.course, 'formset': formset})


# to check is the current user is owner or not
class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


# to save the courses  into database if the form(create or update) is valid and set owner = current user
class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# setting the data for child class like model, fields and success_url if form(create or update)  is valid
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


# only owner can edit the course
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


# to watch the list of all courses by an instructor
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


# to create the courses
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


# to update the courses
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


# to delete the course
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class ManagarCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

