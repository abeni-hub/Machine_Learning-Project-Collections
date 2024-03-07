from django.db import models
from django.core import serializers

# Create your models here.
class Teacher(models.Model):
    full_name = models.CharField(max_length = 100)
    detail = models.TextField(null = True)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length = 100)
    mobile_no = models.CharField(max_length = 20)
    address = models.TextField()
    
    class Meta:
        verbose_name_plural = "1. Teachers"
        
    def address_list(self):
        address_list = self.address.split(',')
        return address_list    
    
class CourseCategory(models.Model):
    title = models.CharField(max_length = 150)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "2. Course Categories"
    
    
class Course(models.Model):
    category = models.ForeignKey( CourseCategory , on_delete = models.CASCADE)
    teacher = models.ForeignKey(Teacher ,on_delete = models.CASCADE , related_name = 'teacher_courses')
    title = models.CharField(max_length = 150)
    description = models.TextField()
    featured_img = models.ImageField(upload_to ='courses_imgs/', null=True)
    techs = models.TextField(null=True)
    
    class Meta:
        verbose_name_plural = "3. Course"
        
    def related_vidios(self):
        related_vidios = Course.objects.filter(techs= self.techs)
        return serializers.serialize('json',related_vidios)  
    
    def tech_list(self):
        tech_list = self.techs.split(',')
        return tech_list  
    
    def total_enrolled_students(self):
        total_enrolled_students = StudentCourseEnrollment.objects.filter(course=self).count()
        return total_enrolled_students
    
    def __str__(self):
        return self.title
    
class Chapter(models.Model):
    course = models.ForeignKey( Course , on_delete = models.CASCADE , related_name = 'course_chapters')
    title = models.CharField(max_length = 150)
    description = models.TextField()
    vidio = models.FileField(upload_to = 'chapter_videos/' , null=True)
    remarks = models.TextField(null = True)
    
    class Meta:
        verbose_name_plural = " 4. Chapter" 
        
    def chapter_duration(self):
        seconds =0
        import cv2
        cap = cv2.VideoCapture(self.vidio.path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count =int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
        if frame_count:
            duration = frame_count/fps
            print('fps =' + str(fps))
            print('number of frames =' + str(frame_count))
            print('duration (S) =' + str(duration))
            minutes = int(round(duration /60))
            seconds = duration%60
            print('duration (M:S) =' + str(minutes) + ':' + str(seconds))
        return seconds    
            
           
    
class Student(models.Model):
    full_name = models.CharField( max_length = 100 )
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length = 100)
    interested_categories = models.TextField()
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural = "5. Student" 
        
class StudentCourseEnrollment(models.Model):
    course = models.ForeignKey(Course , on_delete = models.CASCADE , related_name='enrolled_courses')
    student = models.ForeignKey(Student,on_delete = models.CASCADE,related_name ='enrolled_student') 
    enrolled_time = models.DateTimeField(auto_now_add =True)
    
    class Meta:
        verbose_name_plural ="6. StudentCourseEnrollment"  
        
    def __str__(self):
        return f"{self.course}-{self.student}"  
    
class CourseRating(models.Model):
    course = models.ForeignKey( Course ,on_delete =models.CASCADE)
    student = models.ForeignKey( Student ,on_delete =models.CASCADE)
    rating = models.PositiveBigIntegerField(default =0)
    reviews = models.TextField(null=True)
    review_time = models.DateTimeField(auto_now_add = True)          
    
    def __str__(self):
        return f"{self.course}-{self.student}-{self.rating}" 
     
    class Meta:
        verbose_name_plural ="7. CourseRating"   
    
class Quiz(models.Model):
    teacher =models.ForeignKey(Teacher ,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    detail = models.TextField()
    add_time = models.DateField(auto_now_add = True) 
    
    class Meta:
        verbose_name_plural ="8. Quiz"
                 
class QuizQuestions(models.Model):
    quiz = models.ForeignKey(Quiz , on_delete =models.CASCADE ,null=True)
    questions = models.CharField(max_length = 200)
    ans1 =models.CharField(max_length =200)
    ans2 =models.CharField(max_length =200)
    ans3=models.CharField(max_length =200)
    ans4 =models.CharField(max_length =200)
    right_ans=models.CharField(max_length=200)
    add_time =models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name_plural ="9. Quiz Questions"    
        
class CourseQuiz(models.Model):
    course = models.ForeignKey(Course ,on_delete=models.CASCADE,null=True)
    quiz = models.ForeignKey(Quiz ,on_delete =models.CASCADE ,null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="10. Course Quiz"                