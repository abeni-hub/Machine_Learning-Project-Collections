from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import generics , permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import TeacherSerializer ,CategorySerializer , CourseSerializer , ChapterSerializer ,CourseChapterSerializer ,StudentSerializer , StudentCourseEnrollSerializer ,CourseRatingSerializer ,QuizSerializer ,QuestionSerializer
from .import models
# Create your views here.

class TeacherList(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer  
    #permission_classes = [permissions.IsAuthenticated]
    
def teacher_login(request):
    email = request.POST['email']
    password = request.POST['password'] 
    
    teacherData = models.Teacher.objects.get(email=email , password=password)
    if teacherData:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})      

class CategoryList(generics.ListCreateAPIView):
    queryset = models.CourseCategory.objects.all()
    serializer_class = CategorySerializer    
    
class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer   
    
    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs = models.Course.objects.all().order_by('-id')[:4]
        
        return qs    
 
class CourseDetailView(generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer    
    # specific teacher course
class TeacherCourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = models.Teacher.objects.get(pk = teacher_id)
        return models.Course.objects.filter(teacher = teacher) 
class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all() 
    serializer_class = CourseSerializer    
    
# Course
class ChapterList(generics.ListCreateAPIView):
    queryset = models.Chapter.objects.all()
    serializer_class = ChapterSerializer       
       
class CourseChapterList(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = models.Course.objects.get(pk=course_id)
        return models.Chapter.objects.filter(course = course) 
    
    # Update the Course chapter
class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Chapter.objects.all()
    serializer_class = ChapterSerializer                       
    
    # Student Data
class StudentList(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer    
    
@csrf_exempt   
def student_login(request):
    email = request.POST['email']
    password = request.POST['password'] 
    try:
        studentData = models.Student.objects.get(email=email , password=password)
    except models.Student.DoesNotExist:
        studentData = None    
    
    if studentData:
        return JsonResponse({'bool':True,'student_id':studentData.id})
    else:
        return JsonResponse({'bool':False})     
    

class StudentCourseEnrollList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer 
    
@csrf_exempt   
def fetch_enroll_status(request ,student_id ,course_id):
   student =models.Student.objects.filter(id =student_id).first()
   course = models.Course.objects.filter(id=course_id).first()
   enrollStatus = models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()
   
   if enrollStatus:
       return JsonResponse({'bool':True})
   else:
       return JsonResponse({'bool':False})     
 
class EnrollStudentList(generics.ListAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer
    
    def  get_queryset(self):
        course_id = self.kwargs['course_id']
        course = models.Course.objects.get(pk =course_id)
        return models.StudentCourseEnrollment.objects.filter(course=course)
    
class CourseRatingList(generics.ListCreateAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = CourseRatingSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = models.Course.objects.get(pk = course_id)
        return models.CourseRating.objects.filter(course=course)
    
class QuizList(generics.ListCreateAPIView):
    queryset =models.Quiz.objects.all()
    serializer_class =QuizSerializer    
               
#student change_password
@csrf_exempt
def student_change_password(request,student_id):
    password = request.POST('password')
    try:
        studentData = models.Student.objects.get(id =student_id)
    except models.Teacher.DoesNotExist:
        studentData =None
    if studentData:
        models.Student.objects.filter(id=student_id).update(password =password)
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})        
    
class QuizQuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        quiz_id =self.kwargs['quiz_id']
        quiz =models.Quiz.objects.get(pk=quiz_id)
        return models.QuizQuestions.objects.filter(quiz=quiz)  