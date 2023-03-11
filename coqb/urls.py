from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('facultydashboard', views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('co', views.course_outline, name='co'),
    path('add-co', views.add_course_outline, name='add-co'),
    path('add-co/<int:co_id>', views.edit_course_outline),
    path('qb', views.question_bank, name='qb'),
    path('add-qb', views.add_question_bank, name='add-qb'),
    path('add-qb/edit-qb/<int:qb_id>', views.edit_qb_view, name='add-qb'),
    path('add-qb/<int:section_id>', views.question_bank_qlist),
    path('edit-qb', views.edit_qb_action, name='edit-qb'),
    path('co-pdf', views.generate_co_pdf, name='co-pdf'),
    path('qb-pdf', views.generate_qb_pdf, name='qb-pdf'),
]