from django.contrib.auth.password_validation import validate_password
from api import models as api_models

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userauths.models import Profile, User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        try:
            token['teacher_id'] = user.teacher.id
        except:
            token['teacher_id'] = 0


        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attr
    
    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email']            
        )

        email_username, _ = user.email.split("@")
        user.username = email_username        
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'image', 'slug', 'course_count']
        model = api_models.Category

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [ "user", "image", "full_name", "bio", "facebook", "twitter", "linkedin", "about", "country", "students", "courses", "review",]
        model = api_models.Teacher

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [ "user", "image", "full_name", "bio", "evtel", "istel", "ceptel", "email", "facebook", "twitter", "linkedin", "about","country","city","active"]
        model = api_models.Agent
    
            
class HafizBilgiSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Hafizbilgileri 
   
            
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Job  
              
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.City  

class ProjeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Proje 

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Designation 
        
class OrganizationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.OrganizationMember  
           
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.District 
        
    def __init__(self, *args, **kwargs):
        super(DistrictSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3      
                               
class VariantItemSerializer(serializers.ModelSerializer):        
    class Meta:
        fields = '__all__'
        model = api_models.VariantItem
    
    def __init__(self, *args, **kwargs):
        super(VariantItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class VariantItemOdevSerializer(serializers.ModelSerializer):        
    class Meta:
        fields = '__all__'
        model = api_models.VariantOdevItem
    
    def __init__(self, *args, **kwargs):
        super(VariantItemOdevSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3   
            
class VariantItemKitapTahliliSerializer(serializers.ModelSerializer):        
    class Meta:
        fields = '__all__'
        model = api_models.VariantKitapTahliliItem
    
    def __init__(self, *args, **kwargs):
        super(VariantItemKitapTahliliSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3   

class VariantItemDersSonuRaporuSerializer(serializers.ModelSerializer):        
    class Meta:
        fields = '__all__'
        model = api_models.VariantDersSonuRaporuItem
    
    def __init__(self, *args, **kwargs):
        super(VariantItemDersSonuRaporuSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3 
                  
class VariantOdevItemSerializer(serializers.ModelSerializer):        
    class Meta:
        fields = '__all__'
        model = api_models.VariantOdevItem
    
    def __init__(self, *args, **kwargs):
        super(VariantOdevItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class VariantKitapTahliliItemSerializer(serializers.ModelSerializer):        
    class Meta:
        fields = '__all__'
        model = api_models.VariantKitapTahliliItem
    
    def __init__(self, *args, **kwargs):
        super(VariantKitapTahliliItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class VariantDersSonuRaporuItemSerializer(serializers.ModelSerializer):        
    class Meta:
        fields = '__all__'
        model = api_models.VariantDersSonuRaporuItem
    
    def __init__(self, *args, **kwargs):
        super(VariantDersSonuRaporuItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class VariantSerializer(serializers.ModelSerializer):
    variant_items = VariantItemSerializer(many=True)
    items = VariantItemSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = api_models.Variant


    def __init__(self, *args, **kwargs):
        super(VariantSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class VariantOdevSerializer(serializers.ModelSerializer):
    variant_items = VariantOdevItemSerializer(many=True)
    items = VariantOdevItemSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = api_models.VariantOdev


    def __init__(self, *args, **kwargs):
        super(VariantOdevSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class VariantKitapTahliliSerializer(serializers.ModelSerializer):
    variant_items = VariantKitapTahliliItemSerializer(many=True)
    items = VariantKitapTahliliItemSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = api_models.VariantKitapTahlili


    def __init__(self, *args, **kwargs):
        super(VariantKitapTahliliSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class VariantDersSonuRaporuSerializer(serializers.ModelSerializer):
    variant_items = VariantDersSonuRaporuItemSerializer(many=True)
    items = VariantDersSonuRaporuItemSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = api_models.VariantDersSonuRaporu


    def __init__(self, *args, **kwargs):
        super(VariantDersSonuRaporuSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class Question_Answer_MessageSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.Question_Answer_Message

class Question_Answer_MessageOdevSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.Question_Answer_MessageOdev

class Question_Answer_MessageKitapTahliliSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.Question_Answer_MessageKitapTahlili
        
class Question_Answer_MessageDersSonuRaporuSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.Question_Answer_MessageDersSonuRaporu

class Question_AnswerSerializer(serializers.ModelSerializer):
    messages = Question_Answer_MessageSerializer(many=True)
    profile = ProfileSerializer(many=False)
    
    class Meta:
        fields = '__all__'
        model = api_models.Question_Answer
        


class Question_AnswerOdevSerializer(serializers.ModelSerializer):
    messages = Question_Answer_MessageOdevSerializer(many=True)
    profile = ProfileSerializer(many=False)
    
    class Meta:
        fields = '__all__'
        model = api_models.Question_AnswerOdev
        
class Question_AnswerKitapTahliliSerializer(serializers.ModelSerializer):
    messages = Question_Answer_MessageKitapTahliliSerializer(many=True)
    profile = ProfileSerializer(many=False)
    
    class Meta:
        fields = '__all__'
        model = api_models.Question_AnswerKitapTahlili

class Question_AnswerDersSonuRaporuSerializer(serializers.ModelSerializer):
    messages = Question_Answer_MessageDersSonuRaporuSerializer(many=True)
    profile = ProfileSerializer(many=False)
    
    class Meta:
        fields = '__all__'
        model = api_models.Question_AnswerDersSonuRaporu


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.Cart

    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.CartOrderItem

    def __init__(self, *args, **kwargs):
        super(CartOrderItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartOrderSerializer(serializers.ModelSerializer):
    order_items = CartOrderItemSerializer(many=True)
    
    class Meta:
        fields = '__all__'
        model = api_models.CartOrder


    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.Certificate



class CompletedLessonSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.CompletedLesson


    def __init__(self, *args, **kwargs):
        super(CompletedLessonSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class CompletedOdevSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.CompletedOdev


    def __init__(self, *args, **kwargs):
        super(CompletedOdevSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Note

class NoteOdevSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.NoteOdev
        
class NoteKitapTahliliSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.NoteKitapTahlili

class NoteDersSonuRaporuSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.NoteDersSonuRaporu
      
class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.Review

    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class ReviewOdevSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.ReviewOdev

    def __init__(self, *args, **kwargs):
        super(ReviewOdevSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class ReviewKitapTahliliSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.ReviewKitapTahlili

    def __init__(self, *args, **kwargs):
        super(ReviewKitapTahliliSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class ReviewDersSonuRaporuSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.ReviewDersSonuRaporu

    def __init__(self, *args, **kwargs):
        super(ReviewDersSonuRaporuSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Notification


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.Coupon


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.Wishlist

    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_models.Country




class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = VariantItemSerializer(many=True, read_only=True)
    completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum =  VariantSerializer(many=True, read_only=True)
    note = NoteSerializer(many=True, read_only=True)
    question_answer = Question_AnswerSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = api_models.EnrolledCourse

    def __init__(self, *args, **kwargs):
        super(EnrolledCourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class EnrolledOdevSerializer(serializers.ModelSerializer):
    lectures = VariantItemOdevSerializer(many=True, read_only=True)
    # completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum =  VariantOdevSerializer(many=True, read_only=True)
    note = NoteOdevSerializer(many=True, read_only=True)
    question_answer = Question_AnswerOdevSerializer(many=True, read_only=True)
    review = ReviewOdevSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = api_models.EnrolledOdev

    def __init__(self, *args, **kwargs):
        super(EnrolledOdevSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class EnrolledKitapTahliliSerializer(serializers.ModelSerializer):
    lectures = VariantItemKitapTahliliSerializer(many=True, read_only=True)
    # completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum =  VariantKitapTahliliSerializer(many=True, read_only=True)
    note = NoteKitapTahliliSerializer(many=True, read_only=True)
    question_answer = Question_AnswerKitapTahliliSerializer(many=True, read_only=True)
    review = ReviewKitapTahliliSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = api_models.EnrolledKitapTahlili

    def __init__(self, *args, **kwargs):
        super(EnrolledKitapTahliliSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class EnrolledDersSonuRaporuSerializer(serializers.ModelSerializer):
    lectures = VariantItemDersSonuRaporuSerializer(many=True, read_only=True)
    # completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum =  VariantDersSonuRaporuSerializer(many=True, read_only=True)
    note = NoteDersSonuRaporuSerializer(many=True, read_only=True)
    question_answer = Question_AnswerDersSonuRaporuSerializer(many=True, read_only=True)
    review = ReviewDersSonuRaporuSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = api_models.EnrolledDersSonuRaporu

    def __init__(self, *args, **kwargs):
        super(EnrolledDersSonuRaporuSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class InstructorOdevSerializer(serializers.ModelSerializer):
    lectures = VariantOdevItemSerializer(many=True, read_only=True)
    # completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum =  VariantOdevSerializer(many=True, read_only=True)
    note = NoteOdevSerializer(many=True, read_only=True)
    question_answer = Question_AnswerOdevSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = api_models.EnrolledOdev

    def __init__(self, *args, **kwargs):
        super(InstructorOdevSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class AttendHafizSerializer(serializers.ModelSerializer):
    hafizs = HafizBilgiSerializer(many=True, read_only=True)    

    class Meta:
        fields = '__all__'
        model = api_models.Hafizbilgileri

    def __init__(self, *args, **kwargs):
        super(AttendHafizSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CourseSerializer(serializers.ModelSerializer):
    students = EnrolledCourseSerializer(many=True, required=False, read_only=True,)
    curriculum = VariantSerializer(many=True, required=False, read_only=True,)
    lectures = VariantItemSerializer(many=True, required=False, read_only=True,)
    reviews = ReviewSerializer(many=True, read_only=True, required=False)
    class Meta:
        fields = ["id", "category", "teacher", "file", "image", "title", "description", "language", "level", "platform_status", "teacher_course_status", "featured", "course_id", "slug", "date", "students", "curriculum", "lectures", "average_rating", "rating_count", "reviews",]
        model = api_models.Course

    def __init__(self, *args, **kwargs):
        super(CourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class OdevSerializer(serializers.ModelSerializer):
    # students = EnrolledCourseSerializer(many=True, required=False, read_only=True,)
    curriculum = VariantSerializer(many=True, required=False, read_only=True,)
    lectures = VariantItemSerializer(many=True, required=False, read_only=True,)
    # reviews = ReviewSerializer(many=True, read_only=True, required=False)
    class Meta:
        fields = ["id", "category", "teacher", "file", "image", "title", "description", "language", "level", "platform_status", "teacher_odev_status", "featured",  "curriculum", "lectures","stajer" ]
        model = api_models.Odev

    def __init__(self, *args, **kwargs):
        super(OdevSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            

class StudentSummarySerializer(serializers.Serializer):
    total_courses = serializers.IntegerField(default=0)
    completed_lessons = serializers.IntegerField(default=0)
    achieved_certificates = serializers.IntegerField(default=0)
    
class ESKEPStudentSummarySerializer(serializers.Serializer):
    total_odevs = serializers.IntegerField(default=0)
    completed_lessons = serializers.IntegerField(default=0)
    achieved_certificates = serializers.IntegerField(default=0)

class AgentSummarySerializer(serializers.Serializer):
    total_courses = serializers.IntegerField(default=0)
    completed_lessons = serializers.IntegerField(default=0)
    achieved_certificates = serializers.IntegerField(default=0)
    total_hafizs = serializers.IntegerField(default=0)

class TeacherSummarySerializer(serializers.Serializer):
    total_courses = serializers.IntegerField(default=0)
    total_students = serializers.IntegerField(default=0)
    total_revenue = serializers.IntegerField(default=0)
    monthly_revenue = serializers.IntegerField(default=0)
    
