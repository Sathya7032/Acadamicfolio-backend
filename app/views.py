from rest_framework.response import Response
from rest_framework import generics, status
from .models import TutorialTopic
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

class TutorialTopicDetailView(generics.RetrieveAPIView):
    serializer_class = TutorialTopicDetailSerializer
    lookup_field = 'url'  # We will filter based on the 'url' of the tutorial topic

    def get_queryset(self):
        # Return an empty queryset as we are handling the object retrieval in the get() method
        return TutorialTopic.objects.none()

    def get(self, request, url, *args, **kwargs):
        try:
            # Fetch the single tutorial topic by its URL
            tutorial_topic = TutorialTopic.objects.get(url=url)
            topic_serializer = self.get_serializer(tutorial_topic)

            # Fetch all text, image, and code snippets related to this tutorial topic and order them by the 'order' field
            text_blocks = TutorialTextBlock.objects.filter(tutorial_topic=tutorial_topic).order_by('order')
            image_blocks = TutorialImageBlock.objects.filter(tutorial_topic=tutorial_topic).order_by('order')
            code_snippets = TutorialCodeSnippet.objects.filter(tutorial_topic=tutorial_topic).order_by('order')

            # Create a combined list of all blocks with their type and order
            content_blocks = []
            for block in text_blocks:
                content_blocks.append({
                    'type': 'text',
                    'content': block.text_block.content,
                    'order': block.order
                })
            for block in image_blocks:
                content_blocks.append({
                    'type': 'image',
                    'content': block.image_block.image_url.url,  # Assuming you want the URL of the image
                    'order': block.order
                })
            for block in code_snippets:
                content_blocks.append({
                    'type': 'code',
                    'content': block.code_snippet.code,
                    'language': block.code_snippet.language,
                    'order': block.order
                })

            # Sort the combined blocks by their order field
            content_blocks = sorted(content_blocks, key=lambda x: x['order'])

            # Fetch all other tutorials in the same category
            related_topics = TutorialTopic.objects.filter(category=tutorial_topic.category).exclude(id=tutorial_topic.id)
            related_serializer = TutorialTopicListSerializer(related_topics, many=True)

            # Return both the single tutorial, combined content blocks, and the related list in the same category
            return Response({
                'topic': topic_serializer.data,
                'content_blocks': content_blocks,
                'related_topics': related_serializer.data
            }, status=status.HTTP_200_OK)

        except TutorialTopic.DoesNotExist:
            return Response({"error": "Tutorial Topic not found."}, status=status.HTTP_404_NOT_FOUND)





@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()  # Retrieve all categories
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryTutorialListView(generics.ListCreateAPIView):
    serializer_class = TutorialTopicListSerializer

    def get(self, request, category_url, *args, **kwargs):
        try:
            # Fetch the category by its URL
            category = Category.objects.get(url=category_url)
            
            # Get all the tutorial topics associated with the category
            topics = TutorialTopic.objects.filter(category=category)
            
            # Serialize the topics
            serializer = self.get_serializer(topics, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
        
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    
from rest_framework.views import APIView

class QuizDetailView(APIView):
    def get(self, request, url):
        quiz = get_object_or_404(Quiz, url=url)  # Fetch quiz using the url field
        questions = quiz.questions.all()
        return Response({
            'quiz': {
                'title': quiz.title,
                'url': quiz.url,
            },
            'questions': [
                {
                    'question_text': question.question_text,
                    'options': [
                        {'id': option.id, 'text': option.option_text, 'is_correct': option.is_correct}
                        for option in question.options.all()
                    ]
                }
                for question in questions
            ]
        })
        
class CheckAnswersView(APIView):
    def post(self, request, url):
        quiz = get_object_or_404(Quiz, url=url)
        submitted_answers = request.data.get('answers', {})

        results = []
        for question in quiz.questions.all():
            selected_option_id = submitted_answers.get(str(question.id))
            correct_option = question.options.filter(is_correct=True).first()
            is_correct = correct_option.id == selected_option_id if correct_option else False
            results.append({
                'question_text': question.question_text,
                'selected_option': selected_option_id,
                'correct_option': correct_option.id if correct_option else None,
                'is_correct': is_correct
            })

        return Response({
            'results': results
        })

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q

@require_GET
def search_view(request):
    query = request.GET.get('q', '')  # Get the query parameter from the URL
    if query:
        # Search in TutorialTopic title and Quiz title
        tutorial_results = TutorialTopic.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
        quiz_results = Quiz.objects.filter(title__icontains=query)
        
        # Create the response data
        tutorial_data = [
            {'id': tutorial.id, 'title': tutorial.title, 'category': tutorial.category.name, 'url': tutorial.url} 
            for tutorial in tutorial_results
        ]
        quiz_data = [
            {'id': quiz.id, 'title': quiz.title, 'url': quiz.url} 
            for quiz in quiz_results
        ]

        response_data = {
            'tutorials': tutorial_data,
            'quizzes': quiz_data,
        }
    else:
        response_data = {
            'tutorials': [],
            'quizzes': []
        }
    
    return JsonResponse(response_data)


class TopicsView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        lang_url = self.kwargs['url']
        language = generics.get_object_or_404(Category, url=lang_url)
        topics = Topics.objects.filter(language=language)
        return topics


class CodeView(generics.ListCreateAPIView):
    serializer_class = CodeSerializer

    def get_queryset(self):
        url = self.kwargs['url']
        topic = generics.get_object_or_404(Topics, url=url)
        return Codes.objects.filter(topic=topic)

#single code view
class CodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Codes.objects.all()
    serializer_class = CodeSerializer
    lookup_field = 'url'