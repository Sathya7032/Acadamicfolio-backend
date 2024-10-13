from rest_framework import serializers
from .models import *

# Serializer for TextBlock, ImageBlock, CodeSnippet remains the same
class TextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBlock
        fields = ['id', 'content']

class ImageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBlock
        fields = ['id', 'image_url']

class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = ['id', 'language', 'code']

# Serializer for single TutorialTopic with ordered blocks
class TutorialTopicDetailSerializer(serializers.ModelSerializer):
    text_blocks = serializers.SerializerMethodField()
    image_blocks = serializers.SerializerMethodField()
    code_snippets = serializers.SerializerMethodField()

    class Meta:
        model = TutorialTopic
        fields = ['id', 'title', 'created_at', 'url', 'text_blocks', 'image_blocks', 'code_snippets','video_web','video_mobile']

    # Fetch ordered text blocks for the tutorial
    def get_text_blocks(self, obj):
        text_blocks = TutorialTextBlock.objects.filter(tutorial_topic=obj).order_by('order')
        return TextBlockSerializer([tb.text_block for tb in text_blocks], many=True).data

    # Fetch ordered image blocks for the tutorial
    def get_image_blocks(self, obj):
        image_blocks = TutorialImageBlock.objects.filter(tutorial_topic=obj).order_by('order')
        return ImageBlockSerializer([ib.image_block for ib in image_blocks], many=True).data

    # Fetch ordered code snippets for the tutorial
    def get_code_snippets(self, obj):
        code_snippets = TutorialCodeSnippet.objects.filter(tutorial_topic=obj).order_by('order')
        return CodeSnippetSerializer([cs.code_snippet for cs in code_snippets], many=True).data

# Serializer for listing topics in the same category
class TutorialTopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialTopic
        fields = ['id', 'title', 'url', 'created_at']


from rest_framework import serializers
from .models import TutorialTopic, Quiz, Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
        
class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Codes
        fields = ['code_id', 'title', 'code', 'content','url']



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id','topic','url']
