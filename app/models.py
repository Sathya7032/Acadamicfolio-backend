from django.db import models
from tinymce.models import HTMLField
from django_summernote.fields import SummernoteTextField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content =  models.TextField()
    image = models.ImageField(upload_to='tutorial-images')
    url = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


class TextBlock(models.Model):
    content = SummernoteTextField()

    def __str__(self):
        return f"Text Block {self.id}"


class ImageBlock(models.Model):
    image_url = models.ImageField(upload_to='Tutorial-Topics')

    def __str__(self):
        return f"Image Block {self.id}"


class CodeSnippet(models.Model):
    language = models.CharField(max_length=50)
    code = models.TextField()

    def __str__(self):
        return f"Code Snippet {self.id} - {self.language}"


# Intermediary models for ordering
class TutorialTextBlock(models.Model):
    tutorial_topic = models.ForeignKey('TutorialTopic', on_delete=models.CASCADE)
    text_block = models.ForeignKey(TextBlock, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class TutorialImageBlock(models.Model):
    tutorial_topic = models.ForeignKey('TutorialTopic', on_delete=models.CASCADE)
    image_block = models.ForeignKey(ImageBlock, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class TutorialCodeSnippet(models.Model):
    tutorial_topic = models.ForeignKey('TutorialTopic', on_delete=models.CASCADE)
    code_snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        



# Updated TutorialTopic model
class TutorialTopic(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=100)
    video_web = models.URLField(default=1)
    video_mobile = models.CharField(max_length=1000, default=1)

    # Category relation
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tutorials')

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=1000, default=1)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)  # Indicate if this option is the correct answer

    def __str__(self):
        return self.option_text


class Topics(models.Model):
    topic = models.CharField(max_length=100)
    language = models.ForeignKey(Category,on_delete=models.CASCADE)
    url = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.topic

class Codes(models.Model):
    code_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    code = models.TextField()
    content = models.TextField()
    topic = models.ForeignKey(Topics,on_delete= models.CASCADE)
    url = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.title