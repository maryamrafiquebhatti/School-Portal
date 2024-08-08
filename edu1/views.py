from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cohort, Lesson, Question, AssignCohort, UserProfile
from .forms import CohortForm, LessonForm, QuestionForm, AssignCohortForm
from .forms import QuestionForm, QuestionTrueFalseForm, QuestionMCQSForm, QuestionFillInBlankForm
from .models import Question, QuestionTrueFalse, QuestionMCQS, QuestionFillInBlank, Score
from .forms import AttemptQuestionForm
def home(request):
    return render(request, 'edu1/home.html')

def manage_roles(request):
    if not request.user.userprofile.role == 'admin':
        return redirect('home') 

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)

        # Update user role
        profile.role = new_role
        profile.save()
        messages.success(request, f'User role updated to {new_role}')

    users = UserProfile.objects.all()
    return render(request, 'edu1/manage_roles.html', {'users': users})


@login_required
def create_cohort(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')  

    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cohort created successfully.')
            return redirect('view_cohorts')
    else:
        form = CohortForm()
    
    return render(request, 'edu1/create_cohort.html', {'form': form})

@login_required
def view_cohorts(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    cohorts = Cohort.objects.all()
    return render(request, 'edu1/view_cohorts.html', {'cohorts': cohorts})

@login_required
def create_lesson(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson created successfully.')
            return redirect('view_lessons')
    else:
        form = LessonForm()
    
    return render(request, 'edu1/create_lesson.html', {'form': form})

@login_required
def view_lessons(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    lessons = Lesson.objects.all()
    return render(request, 'edu1/view_lessons.html', {'lessons': lessons})

@login_required
def create_question(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            if question.type == 'truefalse':
                tf_form = QuestionTrueFalseForm(request.POST, instance=QuestionTrueFalse(question=question))
                if tf_form.is_valid():
                    tf_form.save()
            elif question.type == 'mcqs':
                mcqs_form = QuestionMCQSForm(request.POST, instance=QuestionMCQS(question=question))
                if mcqs_form.is_valid():
                    mcqs_form.save()
            elif question.type == 'fillintheblanks':
                fill_in_blank_form = QuestionFillInBlankForm(request.POST, instance=QuestionFillInBlank(question=question))
                if fill_in_blank_form.is_valid():
                    fill_in_blank_form.save()
            messages.success(request, 'Question created successfully.')
            return redirect('view_questions')
    else:
        form = QuestionForm()
    
    return render(request, 'edu1/create_question.html', {'form': form})
@login_required
def view_questions(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    questions = Question.objects.all()
    return render(request, 'edu1/view_questions.html', {'questions': questions})

@login_required
def assign_students(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    if request.method == 'POST':
        form = AssignCohortForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Students assigned to cohort successfully.')
            return redirect('view_assignments')
    else:
        form = AssignCohortForm()
    
    return render(request, 'edu1/assign_students.html', {'form': form})

@login_required
def view_assignments(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    assignments = AssignCohort.objects.all()
    return render(request, 'edu1/view_assignments.html', {'assignments': assignments})


@login_required
def view_results(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('home')

    results = Score.objects.all()
    return render(request, 'edu1/view_results.html', {'results': results})


@login_required
def attempt_question(request, question_id):
    question = Question.objects.get(id=question_id)
    
    if request.method == 'POST':
        form = AttemptQuestionForm(request.POST)
        if form.is_valid():
            user = request.user
            score = form.save(commit=False)
            score.user = user
            score.lesson = question.lesson
            
            if question.type == 'truefalse':
                answer = request.POST.get('answer')
                correct_answer = QuestionTrueFalse.objects.get(question=question).answer
                score.marks = 10 if answer == correct_answer else 0
                
            elif question.type == 'mcqs':
                answer = request.POST.get('answer')
                correct_answer = QuestionMCQS.objects.get(question=question).answer
                score.marks = 10 if answer == correct_answer else 0
                
            elif question.type == 'fillintheblanks':
                answer = request.POST.get('answer')
                correct_answer = QuestionFillInBlank.objects.get(question=question).answer
                score.marks = 10 if answer.strip().lower() == correct_answer.strip().lower() else 0
                
            score.question = question
            score.save()
            
            return redirect('home')  

    else:
        form = AttemptQuestionForm()
    
    return render(request, 'edu1/attempt_question.html', {'form': form, 'question': question})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import StudentSignupForm, StudentLoginForm

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user, role='student')
            login(request, user)
            return redirect('home')  
    else:
        form = StudentSignupForm()
    return render(request, 'edu1/student_signup.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = StudentLoginForm()
    return render(request, 'edu1/student_login.html', {'form': form})
