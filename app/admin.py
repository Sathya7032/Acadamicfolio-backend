from django.contrib import admin
from .models import (
    Category, TextBlock, ImageBlock, CodeSnippet, 
    TutorialTextBlock, TutorialImageBlock, TutorialCodeSnippet, 
    TutorialTopic, Quiz, Question, Option, Topics, Codes
)

# For managing inline related models in admin
class TextBlockInline(admin.TabularInline):
    model = TutorialTextBlock
    extra = 1

class ImageBlockInline(admin.TabularInline):
    model = TutorialImageBlock
    extra = 1

class CodeSnippetInline(admin.TabularInline):
    model = TutorialCodeSnippet
    extra = 1

# TutorialTopic admin with inlines and filters
@admin.register(TutorialTopic)
class TutorialTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'created_at')
    inlines = [TextBlockInline, ImageBlockInline, CodeSnippetInline]

# Quiz admin with filters
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)

# Question admin with filters
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text')
    list_filter = ('quiz',)

# Category admin with filters
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)
    list_filter = ('name',)

# Topics admin with filters
@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('topic', 'language', 'url')
    search_fields = ('topic', 'language__name')
    list_filter = ('language',)

# Codes admin with filters
@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'url')
    search_fields = ('title', 'topic__topic')
    list_filter = ('topic', 'topic__language')

# Simple registrations with filters for remaining models
@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')
    list_filter = ('id',)

@admin.register(ImageBlock)
class ImageBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url')
    list_filter = ('id',)

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'code')
    list_filter = ('language',)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_text', 'is_correct')
    list_filter = ('question', 'is_correct')
