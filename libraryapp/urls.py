from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('book-details/', views.book_details, name='book_details'),
    path('book-summary/<int:book_id>/', views.book_summary, name='book_summary'),
    path('add-book/', views.add_book, name='add_book'),
    path('add-student/', views.add_student, name='add_student'),
    path('student-details/', views.student_details, name='student_details'),
    path('logout/', views.logout_view, name='logout'),
]