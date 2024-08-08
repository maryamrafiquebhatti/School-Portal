from django.urls import path
from .views import manage_roles
from .views import create_cohort, view_cohorts, create_lesson, view_lessons, create_question, view_questions, assign_students, view_assignments
from .views import  view_results , attempt_question ,student_signup, student_login

urlpatterns = [
    
    path('signup/', student_signup, name='student_signup'),
    path('login/', student_login, name='student_login'),
    path('manage_roles/', manage_roles, name='manage_roles'),
    path('create_cohort/', create_cohort, name='create_cohort'),
    path('view_cohorts/', view_cohorts, name='view_cohorts'),
    path('create_lesson/', create_lesson, name='create_lesson'),
    path('view_lessons/', view_lessons, name='view_lessons'),
    path('create_question/', create_question, name='create_question'),
    path('view_questions/', view_questions, name='view_questions'),
    path('assign_students/', assign_students, name='assign_students'),
    path('view_assignments/', view_assignments, name='view_assignments'),
    path('view_results/', view_results, name='view_results'),
    path('attempt_question/<int:question_id>/', attempt_question, name='attempt_question'),
 

]
    