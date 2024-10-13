from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)

urlpatterns = [
     path('api/categories/', category_list, name='category_list'),
     path('api/tutorials/<str:url>/', TutorialTopicDetailView.as_view(), name='tutorial-topic-detail'),
     path('api/category/<str:category_url>/topics/', CategoryTutorialListView.as_view(), name='category-tutorials'),
     path('', include(router.urls)),
     path('quiz/<str:url>/', QuizDetailView.as_view(), name='get_quiz'),
     path('check-answers/', CheckAnswersView.as_view(), name='check_answers'),
     path('search/', search_view, name='search_view'),
     
     path('languages/<str:url>/topics/', TopicsView.as_view(), name='topics-details'),
     path('languages/<str:url>/codes/', CodeView.as_view(), name='code-details'),
     path('languages/codes/<str:url>/', CodeDetail.as_view(), name='code-detailsview'),
]