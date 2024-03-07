from django.urls import path
from .import views

urlpatterns = [
    path('teacher/',views.TeacherList.as_view()),
    path('teacher/<int:pk>', views.TeacherDetail.as_view()),
    path('teacher-login',views.teacher_login),
    path('category/' , views.CategoryList.as_view()),
    path('course/' , views.CourseList.as_view()),
    path('chapter/<int:pk>' , views.ChapterDetailView.as_view()),
    path('course-chapters/<int:course_id>' , views.CourseChapterList.as_view()),
    path('teacher-courses/<int:teacher_id>', views.TeacherCourseList.as_view()),
    path('teacher-course-detail/<int:pk>', views.TeacherCourseDetail.as_view()),
    # Student
    path('student/',views.StudentList.as_view()),
    path('student-login',views.student_login),
    path('student-enroll-course/',views.StudentCourseEnrollList.as_view()),
    path('fetch-enroll-status/<int:student_id>/<int:course_id>', views.fetch_enroll_status),
    path('fetch-enroll-students/<int:course_id>', views.EnrollStudentList.as_view()),
    path('course-rating/<int:course_id>',views.CourseRatingList.as_view()),
   #Quiz Start
   path('quiz/',views.QuizList.as_view()),
   path('quiz-questions/<int:quiz_id>',views.QuizQuestionList.as_view()),

]
