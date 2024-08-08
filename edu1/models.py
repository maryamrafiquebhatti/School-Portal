from django.db import models
from django.contrib.auth.models import User

# Define User roles
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('student', 'Student'),
    ('teacher', 'Teacher'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class Cohort(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.name

class Question(models.Model):
    TYPE_CHOICES = [
        ('truefalse', 'True/False'),
        ('mcqs', 'Multiple Choice'),
        ('fillintheblanks', 'Fill in the Blanks'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    statement = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.statement

class QuestionTrueFalse(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='truefalse')
    answer = models.BooleanField()

class QuestionMCQS(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='mcqs')
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    answer = models.CharField(max_length=1)  # Store 'a', 'b', 'c', or 'd'

class QuestionFillInBlank(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='fillintheblanks')
    answer = models.CharField(max_length=255)

class AssignCohort(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.userprofile.role == 'student':
            raise ValueError('User must be a student to be assigned to a cohort.')
        super().save(*args, **kwargs)

class Score(models.Model):
    marks = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name} - {self.marks}"
