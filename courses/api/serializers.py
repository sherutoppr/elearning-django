from rest_framework import serializers
from ..models import Subject, Course, Module, Content


class ItemRelatedField(serializers.RelatedField):    # created custom field
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):   # content serializer
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):   # module with content serializer created above
    contents = ContentSerializer(many=True)         # nested serializer

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):  # course with module serializer created above
    modules = ModuleWithContentsSerializer(many=True)  # nested serializer

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']


class ModuleSerializer(serializers.ModelSerializer):    # module model serializer
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):    # course model serializer
    modules = ModuleSerializer(many=True, read_only=True)       # nested serializer

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']


class SubjectSerializer(serializers.ModelSerializer):   # subject model serializer
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']