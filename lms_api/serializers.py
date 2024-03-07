from rest_framework import serializers
from .import models

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['id' ,'full_name','detail','email','password','qualification','mobile_no','address','teacher_courses' ,'address_list']
        depth=1
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id' , 'title' , 'description']        
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'category','teacher','title','description','featured_img','techs' ,'course_chapters' ,'related_vidios' ,'tech_list' ,'total_enrolled_students']
        depth=1
        
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['id' , 'course' ,'title' , 'description' ,'vidio', 'remarks']

class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['id' , 'course' ,'title' , 'description' ,'vidio', 'remarks']     
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['id' , 'full_name' ,'email','password','username','interested_categories']
        
class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentCourseEnrollment
        fields= ['id','course' ,'student' ,'enrolled_time']  
        depth = 1
        
class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseRating
        fields = ['id','course','student','rating','reviews','review_time']
        depth = 1           
        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields=[
            'id',
            'teacher',
            'title',
            'detail',
            'add_time',
        ]       
    def __init__(self ,*args ,**kwargs):
        super(QuizSerializer,self).__init__(*args,**kwargs)
        request =self.context.get('request')
        self.Meta.depth = 0
        if request and request.method =='GET':
            self.Meta.depth = 2   
                   
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizQuestions
        fields =['id','quiz','questions','ans1','ans2','ans3','ans4','right_ans']
        
    def __init__(self ,*args,**kwargs):
        super(QuestionSerializer ,self).__init__(*args , **kwargs)
        request =self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1                       