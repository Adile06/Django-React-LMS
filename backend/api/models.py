from datetime import datetime
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from userauths.models import User, Profile
from shortuuid.django_fields import ShortUUIDField
from moviepy.editor import VideoFileClip
import math

YEAR =set()
yearNow =int(datetime.strftime(datetime.now(),"%Y"))
for x in range(1930, yearNow):
  YEAR.add((str(x),str(x)))
  
LANGUAGE = (
    ("Turkce", "Türkçe"),
    ("Ingilizce", "İngilizce"),
    ("Arapca", "Arapça"),
)

GENDER_CHOICES =(
    ('Erkek','Erkek'),
    ('Kadın','Kadın')    
)

ONAY_CHOICES =(
    ('Onaylandı','Onaylandı'),
    ('Onaylanmadı','Onaylanmadı')    
)

ISMARRIED_CHOICES =(
    ('Evli','Evli'),
    ('Bekar','Bekar')    
)
OS_CHOICES =[
    ('android','Android'),
    ('ios','ios'),
    ('windows','Windows')        
]
LEVEL = (
    ("Başlangic", "Başlangıç"),
    ("Orta", "Orta"),
    ("Ileri Seviye", "İleri Seviye"),
)


TEACHER_STATUS = (
    ("Taslak", "Taslak"),
    ("Pasif", "Pasif"),
    ("Yayinlanmis", "Yayınlanmış"),
)

STATUS = (
    ("İncelemede", "İncelemede"),
    ("Pasif", "Pasif"),
    ("Reddedilmiş", "Reddedilmiş"),
    ("Taslak", "Taslak"),  
    ("Teslim Edildi", "Teslim Edildi")
)

KOORDINATOR_STATUS = (
    ("Incelemede", "Incelemede"),    
    ("Geri Gönderildi", "Geri Gönderildi"),
    ("Not Verildi", "Not Verildi"),
)

PAYMENT_STATUS = (
    ("Ödendi", "Paid"),
    ("İşleniyor", "İşleniyor"),
    ("Arizali", "Arızalı"),
)


PLATFORM_STATUS = (
    ("İncelemede", "İncelemede"),
    ("Pasif", "Pasif"),
    ("Reddedilmiş", "Reddedilmiş"),
    ("Taslak", "Taslak"),
    ("Yayinlanmis", "Yayınlanmış"),
)

RATING = (
    (1, "1 Yıldız"),
    (2, "2 Yıldız"),
    (3, "3 Yıldız"),
    (4, "4 Yıldız"),
    (5, "5 Yıldız"),
)

NOTI_TYPE = (
    ("New Order", "New Order"),
    ("New Review", "New Review"),
    ("New Course Question", "New Course Question"),
    ("Draft", "Draft"),
    ("Course Published", "Course Published"),
    ("Course Enrollment Completed", "Course Enrollment Completed"),
)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="course-file", blank=True, null=True, default="default.jpg")
    full_name = models.CharField(max_length=100)
    roles = models.ManyToManyField('TeacherRole', verbose_name="Roller")  
    bio = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.full_name
    
    def students(self):
        return CartOrderItem.objects.filter(teacher=self)
    
    def hafizs(self):
        return self.hafiz_ogrencileri.all()

    def courses(self):
        return Course.objects.filter(teacher=self)
    
    def review(self):
        return Course.objects.filter(teacher=self).count()
    
    class Meta:
        verbose_name = "Eğitmen"
        verbose_name_plural = "Eğitmenler"
        
Teacher._meta.get_field('user').verbose_name = "Kullanıcı" 
Teacher._meta.get_field('image').verbose_name = "Eğitmen Profil Resmi"
Teacher._meta.get_field('full_name').verbose_name = "Adı Soyadı"
Teacher._meta.get_field('bio').verbose_name = "Eğitmen Biyografi"
Teacher._meta.get_field('about').verbose_name = "Eğitmen Hakkında Bilgi"
Teacher._meta.get_field('country').verbose_name = "Ülke"

class TeacherStudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="students")

    class Meta:
        unique_together = ("user", "instructor")

    def __str__(self):
        return f"{self.instructor.full_name} ↔ {self.user.username}"

class TeacherRole(models.Model):
    name = models.CharField(
        max_length=50,
        choices=[
          ("AkademiEgitmen", "AkademiEgitmen"),
          ("ESKEPEgitmen", "ESKEPEgitmen"),
          ("HBSEgitmen", "HBSEgitmen"),
          ("HDMEgitmen", "HDMEgitmen")  
        ],
        unique=True
    )
    def __str__(self):
        return self.get_name_display()

class StajerRole(models.Model):
    name = models.CharField(
        max_length=50,
        choices=[          
          ("ESKEPStajer", "ESKEPStajer")           
        ],
        unique=True
    )
    def __str__(self):
        return self.get_name_display()  
    
class AgentRole(models.Model):
    name = models.CharField(
        max_length=50,
        choices=[          
          ("HBSTemsilci", "HBSTemsilci")           
        ],
        unique=True
    )
    def __str__(self):
        return self.get_name_display()  
     
class OgrenciRole(models.Model):
    name = models.CharField(
        max_length=50,
        choices=[          
          ("AkademiOgrenci", "AkademiOgrenci"),
          ("HBSOgrenci", "HBSOgrenci"),
          ("HDMOgrenci", "HDMOgrenci")         
        ],
        unique=True
    )
    def __str__(self):
        return self.get_name_display() 

class HafizRole(models.Model):
    name = models.CharField(
        max_length=50,
        choices=[
          ("HBSHafiz", "HBSHafiz"),
          ("HDMHafiz", "HDMHafiz")       
        ],
        unique=True
    )
    def __str__(self):
        return self.get_name_display() 

class KoordinatorRole(models.Model):
    name = models.CharField(
        max_length=50,
        choices=[
            ("Ogrenci", "Ogrenci"),
            ("Stajer", "Stajer"),
            ("Genel", "Genel"),
            ("AkademiKoordinator", "AkademiKoordinator"),
            ("HBSKoordinator", "HBSKoordinator"),
            ("HDMKoordinator", "HDMKoordinator"),
        ],
        unique=True
    )

    def __str__(self):
        return self.get_name_display()

class Koordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="course-file", blank=True, null=True, default="default.jpg")
    full_name = models.CharField(max_length=100)
    roles = models.ManyToManyField(KoordinatorRole, verbose_name="Roller")   
    bio = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    
    def ogrencis(self):
        return Ogrenci.objects.filter(koordinator=self)
    
    # def courses(self):
    #     return Course.objects.filter(koordinator=self)    
    
    def stajers(self):
        return Stajer.objects.filter(koordinator=self)
    
    # def review(self):
    #     return Course.objects.filter(koordinator=self).count()
    
    class Meta:
        verbose_name = "Koordinator"
        verbose_name_plural = "Koordinatorler"
        
Koordinator._meta.get_field('user').verbose_name = "Kullanıcı" 
Koordinator._meta.get_field('image').verbose_name = "Koordinator Profil Resmi"
Koordinator._meta.get_field('full_name').verbose_name = "Adı Soyadı"
Koordinator._meta.get_field('bio').verbose_name = "Koordinator Biyografi"
Koordinator._meta.get_field('about').verbose_name = "Koordinator Hakkında Bilgi"
Koordinator._meta.get_field('country').verbose_name = "Ülke"
Koordinator._meta.get_field('active').verbose_name = "Aktif/Pasif"

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="course-file", default="category.jpg", null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Category"
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def course_count(self):
        return Course.objects.filter(category=self).count()
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) 
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        
Category._meta.get_field('title').verbose_name = "Başlık" 
Category._meta.get_field('image').verbose_name = "Kategori Resmi"
Category._meta.get_field('active').verbose_name = "Aktf/Pasif"
Category._meta.get_field('slug').verbose_name = "Etiket"
           
class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField(upload_to="course-file", blank=True, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE, default="Turkce", max_length=100)
    level = models.CharField(choices=LEVEL, default="Baslangic", max_length=100)
    platform_status = models.CharField(choices=PLATFORM_STATUS, default="Yayinlanmis", max_length=100)
    teacher_course_status = models.CharField(choices=TEACHER_STATUS, default="Yayinlanmis", max_length=100)
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + str(self.pk)
        super(Course, self).save(*args, **kwargs)

    def students(self):
        return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return Variant.objects.filter(course=self)
    
    def lectures(self):
        return VariantItem.objects.filter(variant__course=self)
    
    def average_rating(self):
        average_rating = Review.objects.filter(course=self, active=True).aggregate(avg_rating=models.Avg('rating'))
        return average_rating['avg_rating']
    
    def rating_count(self):
        return Review.objects.filter(course=self, active=True).count()
    
    def reviews(self):
        return Review.objects.filter(course=self, active=True)
    
    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        
Course._meta.get_field('category').verbose_name = "Kategori" 
Course._meta.get_field('teacher').verbose_name = "Kurs Öğretmeni"
Course._meta.get_field('image').verbose_name = "Kurs Resmi"
Course._meta.get_field('file').verbose_name = "Kurs Dosyası"
Course._meta.get_field('title').verbose_name = "Kurs Başlığı" 
Course._meta.get_field('language').verbose_name = "Kurs Dili"
Course._meta.get_field('description').verbose_name = "Kurs Açıklaması"
Course._meta.get_field('level').verbose_name = "Kurs Seviyesi"
Course._meta.get_field('platform_status').verbose_name = "Uygulamadaki Durumu" 
Course._meta.get_field('teacher_course_status').verbose_name = "Eğitmenin Sistemindeki Durumu"
Course._meta.get_field('featured').verbose_name = "Öne Çıksın Mı?"
Course._meta.get_field('course_id').verbose_name = "Kurs Numarası"
Course._meta.get_field('slug').verbose_name = "Etiket"
Course._meta.get_field('date').verbose_name = "Kurs Eklenme Tarihi"

class Odev(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL,null=True, blank=True)
    hazirlayan = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    file = models.FileField(upload_to="course-file", blank=True, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)    
    language = models.CharField(choices=LANGUAGE, default="Turkce", max_length=100)
    level = models.CharField(choices=LEVEL, default="Baslangic", max_length=100)
    # platform_status = models.CharField(choices=PLATFORM_STATUS, default="Yayinlanmis", max_length=100)
    odev_status = models.CharField(choices=STATUS, default="Taslak", max_length=100)
    koordinator_odev_status = models.CharField(choices=KOORDINATOR_STATUS, max_length=100,blank=True, null=True)
    # featured = models.BooleanField(default=False)    
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # if self.slug == "" or self.slug == None:
        #     self.slug = slugify(self.title) + str(self.pk)
        super(Odev, self).save(*args, **kwargs)

    # def students(self):
    #     return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return VariantOdev.objects.filter(odev=self)
    
    def lectures(self):
        return VariantOdevItem.objects.filter(variant__odev=self)
    
    # def average_rating(self):
    #     average_rating = Review.objects.filter(odev=self, active=True).aggregate(avg_rating=models.Avg('rating'))
    #     return average_rating['avg_rating']
    
    # def rating_count(self):
    #     return Review.objects.filter(odev=self, active=True).count()
    
    # def reviews(self):
    #     return Review.objects.filter(odev=self, active=True)
    
    class Meta:
        verbose_name = "Ödev"
        verbose_name_plural = "Ödevler"
        
Odev._meta.get_field('category').verbose_name = "Kategori" 
Odev._meta.get_field('koordinator').verbose_name = "Ödev Koordinatorü"
Odev._meta.get_field('image').verbose_name = "Ödev Resmi"
Odev._meta.get_field('hazirlayan').verbose_name = "Ödevi Hazırlayan"
Odev._meta.get_field('file').verbose_name = "Ödev Dosyası"
Odev._meta.get_field('title').verbose_name = "Ödev Başlığı" 
Odev._meta.get_field('language').verbose_name = "Ödev Dili"
Odev._meta.get_field('description').verbose_name = "Ödev Açıklaması"
Odev._meta.get_field('level').verbose_name = "Ödev Seviyesi"
Odev._meta.get_field('odev_status').verbose_name = "Ödevin Durumu" 
Odev._meta.get_field('koordinator_odev_status').verbose_name = "Koordinatorün Sistemindeki Durumu"
# Odev._meta.get_field('featured').verbose_name = "Öne Çıksın Mı?"
# Odev._meta.get_field('course_id').verbose_name = "Ödev Numarası"
# Odev._meta.get_field('slug').verbose_name = "Etiket"
# Odev._meta.get_field('date').verbose_name = "Ödev Eklenme Tarihi"

class VariantOdev(models.Model):
    odev = models.ForeignKey(Odev, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    variant_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def variant_items(self):
        return VariantOdevItem.objects.filter(variant=self)
    
    def items(self):
        return VariantOdevItem.objects.filter(variant=self)
    class Meta:
        verbose_name = "Odev Müfredat"
        verbose_name_plural = "Odev Müfredat Bölümleri"   
VariantOdev._meta.get_field('odev').verbose_name = "Odev" 
VariantOdev._meta.get_field('title').verbose_name = "Odev Başlığı"
VariantOdev._meta.get_field('variant_id').verbose_name = "Odev Numarası"
VariantOdev._meta.get_field('date').verbose_name = "Odev Eklenme Tarihi"   

class VariantOdevItem(models.Model):
    variant = models.ForeignKey(VariantOdev, on_delete=models.CASCADE, related_name="variantOdev_items")
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if self.file:
        #     clip = VideoFileClip(self.file.path)
        #     duration_seconds = clip.duration

        #     minutes, remainder = divmod(duration_seconds, 60)  

        #     minutes = math.floor(minutes)
        #     seconds = math.floor(remainder)

        #     duration_text = f"{minutes}m {seconds}s"
        #     self.content_duration = duration_text
        #     super().save(update_fields=['content_duration'])
    class Meta:
        verbose_name = "Ödev Bölüm"
        verbose_name_plural = "Ödev Bölümler" 

class DersSonuRaporu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL,null=True, blank=True)
    hazirlayan = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    file = models.FileField(upload_to="course-file", blank=True, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE, default="Turkce", max_length=100)
    level = models.CharField(choices=LEVEL, default="Baslangic", max_length=100)
    derssonuraporu_status = models.CharField(choices=STATUS, default="Taslak", max_length=100)
    koordinator_derssonuraporu_status = models.CharField(choices=KOORDINATOR_STATUS, max_length=100,blank=True, null=True)
    # featured = models.BooleanField(default=False)
    # course_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    # slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # if self.slug == "" or self.slug == None:
        #     self.slug = slugify(self.title) + str(self.pk)
        super(DersSonuRaporu, self).save(*args, **kwargs)

    # def students(self):
    #     return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return VariantDersSonuRaporu.objects.filter(derssonuraporu=self)
    
    def lectures(self):
        return VariantDersSonuRaporuItem.objects.filter(variant__derssonuraporu=self)
    
    # def average_rating(self):
    #     average_rating = Review.objects.filter(odev=self, active=True).aggregate(avg_rating=models.Avg('rating'))
    #     return average_rating['avg_rating']
    
    # def rating_count(self):
    #     return Review.objects.filter(odev=self, active=True).count()
    
    # def reviews(self):
    #     return Review.objects.filter(odev=self, active=True)
    
    class Meta:
        verbose_name = "Ders Sonu Raporu"
        verbose_name_plural = "Ders Sonu Raporuler"
        
DersSonuRaporu._meta.get_field('category').verbose_name = "Kategori" 
DersSonuRaporu._meta.get_field('koordinator').verbose_name = "Ders Sonu Raporu Koordinatörü"
DersSonuRaporu._meta.get_field('image').verbose_name = "Ders Sonu Raporu Resmi"
DersSonuRaporu._meta.get_field('file').verbose_name = "Ders Sonu Raporu Dosyası"
DersSonuRaporu._meta.get_field('hazirlayan').verbose_name = "Ders Sonunu Hazırlayan"
DersSonuRaporu._meta.get_field('title').verbose_name = "Ders Sonu Raporu Başlığı" 
DersSonuRaporu._meta.get_field('language').verbose_name = "Ders Sonu Raporu Dili"
DersSonuRaporu._meta.get_field('description').verbose_name = "Ders Sonu Raporu Açıklaması"
DersSonuRaporu._meta.get_field('level').verbose_name = "Ders Sonu Raporu Seviyesi"
DersSonuRaporu._meta.get_field('derssonuraporu_status').verbose_name = "Ders Sonu Raporunun Durumu" 
DersSonuRaporu._meta.get_field('koordinator_derssonuraporu_status').verbose_name = "Koordinatorün Sistemindeki Durumu"
# DersSonuRaporu._meta.get_field('featured').verbose_name = "Öne Çıksın Mı?"
# Odev._meta.get_field('course_id').verbose_name = "Ödev Numarası"
# Odev._meta.get_field('slug').verbose_name = "Etiket"
# Odev._meta.get_field('date').verbose_name = "Ödev Eklenme Tarihi"
class VariantDersSonuRaporu(models.Model):
    derssonuraporu = models.ForeignKey(DersSonuRaporu, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    variant_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def variant_items(self):
        return VariantDersSonuRaporuItem.objects.filter(variant=self)
    
    def items(self):
        return VariantDersSonuRaporuItem.objects.filter(variant=self)
    
    class Meta:
        verbose_name = "Ders Sonu Raporu Müfredat"
        verbose_name_plural = "Ders Sonu Raporu Müfredat Bölümleri"   
VariantDersSonuRaporu._meta.get_field('derssonuraporu').verbose_name = "Ders Sonu Raporu" 
VariantDersSonuRaporu._meta.get_field('title').verbose_name = "Ders Sonu Raporu Başlığı"
VariantDersSonuRaporu._meta.get_field('variant_id').verbose_name = "Ders Sonu Raporu Numarası"
VariantDersSonuRaporu._meta.get_field('date').verbose_name = "Ders Sonu Raporu Eklenme Tarihi"   

class VariantDersSonuRaporuItem(models.Model):
    variant = models.ForeignKey(VariantDersSonuRaporu, on_delete=models.CASCADE, related_name="variantDersSonuRaporu_items")
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if self.file:
        #     clip = VideoFileClip(self.file.path)
        #     duration_seconds = clip.duration

        #     minutes, remainder = divmod(duration_seconds, 60)  

        #     minutes = math.floor(minutes)
        #     seconds = math.floor(remainder)

        #     duration_text = f"{minutes}m {seconds}s"
        #     self.content_duration = duration_text
        #     super().save(update_fields=['content_duration'])
    class Meta:
        verbose_name = "Ders Sonu Raporu Bölüm"
        verbose_name_plural = "Ders Sonu Raporu Bölümler" 

class KitapTahlili(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    hazirlayan = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True, related_name='koordinated_kitaplar')
    file = models.FileField(upload_to="course-file", blank=True, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE, default="Turkce", max_length=100)
    level = models.CharField(choices=LEVEL, default="Baslangic", max_length=100)
    kitaptahlili_status = models.CharField(choices=STATUS, default="Taslak", max_length=100)
    koordinator_kitaptahlili_status = models.CharField(choices=KOORDINATOR_STATUS, max_length=100,blank=True, null=True)
    # featured = models.BooleanField(default=False)
    # course_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    # slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # if self.slug == "" or self.slug == None:
        #     self.slug = slugify(self.title) + str(self.pk)
        super(KitapTahlili, self).save(*args, **kwargs)

    # def students(self):
    #     return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return VariantKitapTahlili.objects.filter(kitaptahlili=self)
    
    def lectures(self):
        return VariantKitapTahliliItem.objects.filter(variant__kitaptahlili=self)
    
    # def average_rating(self):
    #     average_rating = Review.objects.filter(odev=self, active=True).aggregate(avg_rating=models.Avg('rating'))
    #     return average_rating['avg_rating']
    
    # def rating_count(self):
    #     return Review.objects.filter(odev=self, active=True).count()
    
    # def reviews(self):
    #     return Review.objects.filter(odev=self, active=True)
    
    class Meta:
        verbose_name = "Kitap Tahlili"
        verbose_name_plural = "Kitap Tahlilleri"
        
KitapTahlili._meta.get_field('category').verbose_name = "Kategori" 
KitapTahlili._meta.get_field('koordinator').verbose_name = "Kitap Tahlili Koordinator"
KitapTahlili._meta.get_field('image').verbose_name = "Kitap Tahlili Kapak Resmi"
KitapTahlili._meta.get_field('file').verbose_name = "Kitap Tahlili Dosyası"
KitapTahlili._meta.get_field('hazirlayan').verbose_name = "Kitap Tahlilini Hazırlayan"
KitapTahlili._meta.get_field('title').verbose_name = "Kitap Tahlili Başlığı" 
KitapTahlili._meta.get_field('language').verbose_name = "Kitap Tahlili Dili"
KitapTahlili._meta.get_field('description').verbose_name = "Kitap Tahlili Açıklaması"
KitapTahlili._meta.get_field('level').verbose_name = "Kitap Tahlili Seviyesi"
KitapTahlili._meta.get_field('kitaptahlili_status').verbose_name = "Kitap Tahlili Durumu" 
KitapTahlili._meta.get_field('koordinator_kitaptahlili_status').verbose_name = "Kitap Tahlilinin Koordinatorun Sistemindeki Durumu"
# KitapTahlili._meta.get_field('featured').verbose_name = "Öne Çıksın Mı?"
# Odev._meta.get_field('course_id').verbose_name = "Ödev Numarası"
# Odev._meta.get_field('slug').verbose_name = "Etiket"
# Odev._meta.get_field('date').verbose_name = "Ödev Eklenme Tarihi"
class VariantKitapTahlili(models.Model):
    kitaptahlili = models.ForeignKey(KitapTahlili, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    variant_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def variant_items(self):
        return VariantKitapTahliliItem.objects.filter(variant=self)
    
    def items(self):
        return VariantKitapTahliliItem.objects.filter(variant=self)
    
    class Meta:
        verbose_name = "Kitap Tahlili Müfredat"
        verbose_name_plural = "Kitap Tahlili Müfredat Bölümleri" 
          
VariantKitapTahlili._meta.get_field('kitaptahlili').verbose_name = "Kitap Tahlili" 
VariantKitapTahlili._meta.get_field('title').verbose_name = "Kitap Tahlili Başlığı"
VariantKitapTahlili._meta.get_field('variant_id').verbose_name = "Kitap Tahlili Numarası"
VariantKitapTahlili._meta.get_field('date').verbose_name = "Kitap Tahlili Eklenme Tarihi"   

class VariantKitapTahliliItem(models.Model):
    variant = models.ForeignKey(VariantKitapTahlili, on_delete=models.CASCADE, related_name="variantKitapTahlili_items")
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if self.file:
        #     clip = VideoFileClip(self.file.path)
        #     duration_seconds = clip.duration

        #     minutes, remainder = divmod(duration_seconds, 60)  

        #     minutes = math.floor(minutes)
        #     seconds = math.floor(remainder)

        #     duration_text = f"{minutes}m {seconds}s"
        #     self.content_duration = duration_text
        #     super().save(update_fields=['content_duration'])
    class Meta:
        verbose_name = "Kitap Tahlili Bölüm"
        verbose_name_plural = "Kitap Tahlili Bölümler" 

class EskepProje(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL,null=True, blank=True)
    hazirlayan = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    file = models.FileField(upload_to="course-file", blank=True, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE, default="Turkce", max_length=100)
    level = models.CharField(choices=LEVEL, default="Baslangic", max_length=100)
    eskepProje_status = models.CharField(choices=STATUS, default="Taslak", max_length=100)
    koordinator_eskepProje_status = models.CharField(choices=KOORDINATOR_STATUS, max_length=100,blank=True, null=True)
    # featured = models.BooleanField(default=False)
    # course_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    # slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # if self.slug == "" or self.slug == None:
        #     self.slug = slugify(self.title) + str(self.pk)
        super(EskepProje, self).save(*args, **kwargs)

    # def students(self):
    #     return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return VariantEskepProje.objects.filter(eskepProje=self)
    
    def lectures(self):
        return VariantEskepProjeItem.objects.filter(variant__eskepProje=self)
    
    # def average_rating(self):
    #     average_rating = Review.objects.filter(odev=self, active=True).aggregate(avg_rating=models.Avg('rating'))
    #     return average_rating['avg_rating']
    
    # def rating_count(self):
    #     return Review.objects.filter(odev=self, active=True).count()
    
    # def reviews(self):
    #     return Review.objects.filter(odev=self, active=True)
    
    class Meta:
        verbose_name = "Eskep Proje"
        verbose_name_plural = "Eskep Projeleri"
        
EskepProje._meta.get_field('category').verbose_name = "Kategori" 
EskepProje._meta.get_field('koordinator').verbose_name = "Proje Koordinatörü"
EskepProje._meta.get_field('image').verbose_name = "Proje Kapak Resmi"
EskepProje._meta.get_field('file').verbose_name = "Proje Dosyası"
EskepProje._meta.get_field('hazirlayan').verbose_name = "Projeyi Hazırlayan"
EskepProje._meta.get_field('title').verbose_name = "Proje Başlığı" 
EskepProje._meta.get_field('language').verbose_name = "Proje Dili"
EskepProje._meta.get_field('description').verbose_name = "Proje Açıklaması"
EskepProje._meta.get_field('level').verbose_name = "Proje Seviyesi"
EskepProje._meta.get_field('eskepProje_status').verbose_name = "Proje Durumu" 
EskepProje._meta.get_field('koordinator_eskepProje_status').verbose_name = "Projenin Koordinatörün Sistemindeki Durumu"
# KitapTahlili._meta.get_field('featured').verbose_name = "Öne Çıksın Mı?"
# Odev._meta.get_field('course_id').verbose_name = "Ödev Numarası"
# Odev._meta.get_field('slug').verbose_name = "Etiket"
# Odev._meta.get_field('date').verbose_name = "Ödev Eklenme Tarihi"
class VariantEskepProje(models.Model):
    eskepProje = models.ForeignKey(EskepProje, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    variant_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def variant_items(self):
        return VariantEskepProjeItem.objects.filter(variant=self)
    
    def items(self):
        return VariantEskepProjeItem.objects.filter(variant=self)
    
    class Meta:
        verbose_name = "Eskep Proje Müfredat"
        verbose_name_plural = "Eskep Proje Müfredat Bölümleri" 
          
VariantEskepProje._meta.get_field('eskepProje').verbose_name = "Proje" 
VariantEskepProje._meta.get_field('title').verbose_name = "Proje Başlığı"
VariantEskepProje._meta.get_field('variant_id').verbose_name = "Proje Numarası"
VariantEskepProje._meta.get_field('date').verbose_name = "Proje Eklenme Tarihi"   

class VariantEskepProjeItem(models.Model):
    variant = models.ForeignKey(VariantEskepProje, on_delete=models.CASCADE, related_name="variantEskepProje_items")
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if self.file:
        #     clip = VideoFileClip(self.file.path)
        #     duration_seconds = clip.duration

        #     minutes, remainder = divmod(duration_seconds, 60)  

        #     minutes = math.floor(minutes)
        #     seconds = math.floor(remainder)

        #     duration_text = f"{minutes}m {seconds}s"
        #     self.content_duration = duration_text
        #     super().save(update_fields=['content_duration'])
    class Meta:
        verbose_name = "Eskep Proje Bölüm"
        verbose_name_plural = "Eskep Proje Bölümler" 
    
class Variant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    variant_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def variant_items(self):
        return VariantItem.objects.filter(variant=self)

    class Meta:
        verbose_name = "Müfredat"
        verbose_name_plural = "Müfredatlar"   

# Alan isimlerini Türkçeleştirme
Variant._meta.get_field('course').verbose_name = "Ders" 
Variant._meta.get_field('title').verbose_name = "Ders Başlığı"
Variant._meta.get_field('variant_id').verbose_name = "Ders Numarası"
Variant._meta.get_field('date').verbose_name = "Ders Eklenme Tarihi"
  

class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="variant_items")
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file:
            clip = VideoFileClip(self.file.path)
            duration_seconds = clip.duration

            minutes, remainder = divmod(duration_seconds, 60)  

            minutes = math.floor(minutes)
            seconds = math.floor(remainder)

            duration_text = f"{minutes}m {seconds}s"
            self.content_duration = duration_text
            super().save(update_fields=['content_duration'])
    class Meta:
        verbose_name = "Ders"
        verbose_name_plural = "Dersler" 

VariantItem._meta.get_field('variant').verbose_name = "Ders" 
VariantItem._meta.get_field('title').verbose_name = "Ders Başlığı"
VariantItem._meta.get_field('description').verbose_name = "Ders Açıklaması"
VariantItem._meta.get_field('file').verbose_name = "Ders Dosyası"  
VariantItem._meta.get_field('duration').verbose_name = "Ders Süresi" 
VariantItem._meta.get_field('content_duration').verbose_name = "İçerik Süresi"
VariantItem._meta.get_field('preview').verbose_name = "Önizleme"
VariantItem._meta.get_field('variant_item_id').verbose_name = "Ders Numarası"  
VariantItem._meta.get_field('date').verbose_name = "Tarih"  
      
class Question_Answer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    class Meta:
        ordering = ['-date']

    def messages(self):
        return Question_Answer_Message.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Soru Cevap"
        verbose_name_plural = "Soru Cevaplar" 
        
Question_Answer._meta.get_field('course').verbose_name = "Kurs" 
Question_Answer._meta.get_field('title').verbose_name = "Soru Başlığı"
Question_Answer._meta.get_field('user').verbose_name = "Kullanıcı"
Question_Answer._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 

class Question_AnswerOdev(models.Model):
    odev = models.ForeignKey(Odev, related_name="question_answers", on_delete=models.CASCADE)
    mesajiAlan = models.ForeignKey(User, related_name="qao_mesajiAlan", on_delete=models.SET_NULL, null=True, blank=True)
    mesajiGonderen = models.ForeignKey(User, related_name="qao_mesajiGonderen", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        gonderen = self.mesajiGonderen.username if self.mesajiGonderen else "Bilinmeyen Gönderen"
        odev_basligi = self.odev.title if self.odev else "Bilinmeyen Ödev"
        return f"{gonderen} - {odev_basligi}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Ödev Soru Cevap"
        verbose_name_plural = "Ödev Soru Cevaplar"

    def messages(self):
        return Question_Answer_MessageOdev.objects.filter(question=self)

    def profile(self):
        if self.mesajiGonderen is None:
            return None  # veya istersen özel bir profil nesnesi ya da dummy veri döndürebilirsin
        try:
            return Profile.objects.get(user=self.mesajiGonderen)
        except Profile.DoesNotExist:
            return None

class Question_Answer_MessageOdev(models.Model):
    odev = models.ForeignKey(Odev, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_AnswerOdev, on_delete=models.CASCADE)
    mesajiAlan = models.ForeignKey(User, related_name="qam_mesajiAlan", on_delete=models.SET_NULL, null=True, blank=True)
    mesajiGonderen = models.ForeignKey(User, related_name="qam_mesajiGonderen", on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        gonderen = self.mesajiGonderen.username if self.mesajiGonderen else "Bilinmeyen Gönderen"
        odev_basligi = self.odev.title if self.odev else "Bilinmeyen Ödev"
        return f"{gonderen} - {odev_basligi}"

    def profile(self):
        if self.mesajiGonderen is None:
            return None  # veya istersen özel bir profil nesnesi ya da dummy veri döndürebilirsin
        try:
            return Profile.objects.get(user=self.mesajiGonderen)
        except Profile.DoesNotExist:
            return None

    class Meta:
        ordering = ['date']
        verbose_name = "Ödev Soru Cevap Mesaj"
        verbose_name_plural = "Ödev Soru Cevap Mesajlar"



class Question_AnswerDersSonuRaporu(models.Model):
    derssonuraporu = models.ForeignKey(DersSonuRaporu, on_delete=models.CASCADE)
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True) 
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.derssonuraporu.title}"
    
    class Meta:
        ordering = ['-date']

    def messages(self):
        return Question_Answer_MessageDersSonuRaporu.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Ders Sonu Raporu Soru Cevap"
        verbose_name_plural = "Ders Sonu Raporu Soru Cevaplar" 
        
Question_AnswerDersSonuRaporu._meta.get_field('derssonuraporu').verbose_name = "Ders Sonu Raporu" 
Question_AnswerDersSonuRaporu._meta.get_field('title').verbose_name = "Soru Başlığı"
Question_AnswerDersSonuRaporu._meta.get_field('ogrenciStajer').verbose_name = "Öğrenci/Stajer"
Question_AnswerDersSonuRaporu._meta.get_field('koordinator').verbose_name = "Koordinator"
Question_AnswerDersSonuRaporu._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_AnswerDersSonuRaporu._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 

class Question_Answer_MessageDersSonuRaporu(models.Model):
    derssonuraporu = models.ForeignKey(DersSonuRaporu, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_AnswerDersSonuRaporu, on_delete=models.CASCADE)
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True) 
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.derssonuraporu.title}"
    
    class Meta:
        ordering = ['date']

    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Ders Sonu Raporu Soru Cevap Mesaj"
        verbose_name_plural = "Ders Sonu Raporu Soru Cevap Mesajlar" 
        
Question_Answer_MessageDersSonuRaporu._meta.get_field('derssonuraporu').verbose_name = "Ders Sonu Raporu" 
Question_Answer_MessageDersSonuRaporu._meta.get_field('question').verbose_name = "Soru Başlığı"
Question_Answer_MessageDersSonuRaporu._meta.get_field('ogrenciStajer').verbose_name = "Öğrenci/Stajer"
Question_Answer_MessageDersSonuRaporu._meta.get_field('koordinator').verbose_name = "Koordinator"
Question_Answer_MessageDersSonuRaporu._meta.get_field('qam_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_MessageDersSonuRaporu._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_MessageDersSonuRaporu._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 

class Question_AnswerKitapTahlili(models.Model):
    kitaptahlili = models.ForeignKey(KitapTahlili, on_delete=models.CASCADE)
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True) 
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.kitaptahlili.title}"
    
    class Meta:
        ordering = ['-date']

    def messages(self):
        return Question_Answer_MessageKitapTahlili.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Kitap Tahlili Soru Cevap"
        verbose_name_plural = "Kitap Tahlili Soru Cevaplar" 
        
Question_AnswerKitapTahlili._meta.get_field('kitaptahlili').verbose_name = "Kitap Tahlili" 
Question_AnswerKitapTahlili._meta.get_field('title').verbose_name = "Soru Başlığı"
Question_AnswerKitapTahlili._meta.get_field('ogrenciStajer').verbose_name = "Öğrenci/Stajer"
Question_AnswerKitapTahlili._meta.get_field('koordinator').verbose_name = "Koordinator"
Question_AnswerKitapTahlili._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_AnswerKitapTahlili._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 

class Question_Answer_MessageKitapTahlili(models.Model):
    kitaptahlili = models.ForeignKey(KitapTahlili, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_AnswerKitapTahlili, on_delete=models.CASCADE)
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True) 
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.kitaptahlili.title}"
    
    class Meta:
        ordering = ['date']

    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Kitap Tahlili Soru Cevap Mesaj"
        verbose_name_plural = "Kitap Tahlili Soru Cevap Mesajlar" 
        
Question_Answer_MessageKitapTahlili._meta.get_field('kitaptahlili').verbose_name = "Kitap Tahlili" 
Question_Answer_MessageKitapTahlili._meta.get_field('question').verbose_name = "Soru Başlığı"
Question_Answer_MessageKitapTahlili._meta.get_field('ogrenciStajer').verbose_name = "Öğrenci/Stajer"
Question_Answer_MessageKitapTahlili._meta.get_field('koordinator').verbose_name = "Koordinator"
Question_Answer_MessageKitapTahlili._meta.get_field('qam_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_MessageKitapTahlili._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_MessageKitapTahlili._meta.get_field('date').verbose_name = "Soru Sorulan Tarih"

class Question_AnswerEskepProje(models.Model):
    eskepproje = models.ForeignKey(EskepProje, on_delete=models.CASCADE)
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True) 
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ogrenciStajer.username} - {self.eskepproje.title}"
    
    class Meta:
        ordering = ['-date']

    def messages(self):
        return Question_Answer_MessageEskepProje.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Eskep Proje Soru Cevap"
        verbose_name_plural = "Eskep Proje Soru Cevaplar" 
        
Question_AnswerEskepProje._meta.get_field('eskepproje').verbose_name = "Eskep Proje" 
Question_AnswerEskepProje._meta.get_field('title').verbose_name = "Soru Başlığı"
Question_AnswerEskepProje._meta.get_field('ogrenciStajer').verbose_name = "Öğrenci/Stajer"
Question_AnswerEskepProje._meta.get_field('koordinator').verbose_name = "Koordinator"
Question_AnswerEskepProje._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_AnswerEskepProje._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 

class Question_Answer_MessageEskepProje(models.Model):
    eskepproje = models.ForeignKey(EskepProje, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_AnswerDersSonuRaporu, on_delete=models.CASCADE)
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True) 
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.derssonuraporu.title}"
    
    class Meta:
        ordering = ['date']

    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Eskep Proje Soru Cevap Mesaj"
        verbose_name_plural = "Eskep Proje Soru Cevap Mesajlar" 
        
Question_Answer_MessageEskepProje._meta.get_field('eskepproje').verbose_name = "Eskep Proje" 
Question_Answer_MessageEskepProje._meta.get_field('question').verbose_name = "Soru Başlığı"
Question_Answer_MessageEskepProje._meta.get_field('ogrenciStajer').verbose_name = "Öğrenci/Stajer"
Question_Answer_MessageEskepProje._meta.get_field('koordinator').verbose_name = "Koordinator"
Question_Answer_MessageEskepProje._meta.get_field('qam_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_MessageEskepProje._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_MessageEskepProje._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 

class Question_Answer_Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    class Meta:
        ordering = ['date']

    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Soru Cevap Mesaj"
        verbose_name_plural = "Soru Cevap Mesajlar" 
        
Question_Answer_Message._meta.get_field('course').verbose_name = "Kurs" 
Question_Answer_Message._meta.get_field('question').verbose_name = "Soru Başlığı"
Question_Answer_Message._meta.get_field('user').verbose_name = "Kullanıcı"
Question_Answer_Message._meta.get_field('qam_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_Message._meta.get_field('qa_id').verbose_name = "Soru Cevap Numarası"  
Question_Answer_Message._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 

class Cart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    cart_id = ShortUUIDField(length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    class Meta:
        verbose_name = "Talep"
        verbose_name_plural = "Talepler"
        
Cart._meta.get_field('course').verbose_name = "Kurs" 
Cart._meta.get_field('tax_fee').verbose_name = "Kurs Linki"
Cart._meta.get_field('user').verbose_name = "Talep Eden Kullanıcı"
Cart._meta.get_field('total').verbose_name = "Toplam"  
Cart._meta.get_field('country').verbose_name = "Ülke"  
Cart._meta.get_field('date').verbose_name = "Soru Sorulan Tarih" 
       
class CartOrder(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ManyToManyField(Teacher, blank=True)
    #sub_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    #tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    #total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    #initial_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    #saved = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    #payment_status = models.CharField(choices=PAYMENT_STATUS, default="Processing", max_length=100)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    coupons = models.ManyToManyField("api.Coupon", blank=True)
    # stripe_session_id = models.CharField(max_length=1000, null=True, blank=True)
    oid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ['-date']
    
    def order_items(self):
        return CartOrderItem.objects.filter(order=self)
    
    def __str__(self):
        return self.oid
    
    class Meta:
        verbose_name = "Talep Seçenek"
        verbose_name_plural = "Talep Seçenekleri"
    
CartOrder._meta.get_field('student').verbose_name = "Öğrenci Adı" 
CartOrder._meta.get_field('teachers').verbose_name = "Eğitmen Adı"
CartOrder._meta.get_field('full_name').verbose_name = "Adı Soyadı"
CartOrder._meta.get_field('email').verbose_name = "E-Posta"  
CartOrder._meta.get_field('coupons').verbose_name = "Ödül"  
CartOrder._meta.get_field('oid').verbose_name = "Talep Numarası" 
CartOrder._meta.get_field('date').verbose_name = "Talep Tarihi" 
   
class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, related_name="orderitem")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="order_item")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # initial_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # saved = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    coupons = models.ManyToManyField("api.Coupon", blank=True)
    applied_coupon = models.BooleanField(default=False)
    oid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']
    
    def order_id(self):
        return f"Order ID #{self.order.oid}"
    
    def payment_status(self):
        return f"{self.order.payment_status}"
    
    def __str__(self):
        return self.oid
    
    class Meta:
        verbose_name = "Talep İstek Seçenek"
        verbose_name_plural = "Talep İstek Seçenekleri"
        
CartOrderItem._meta.get_field('order').verbose_name = "Talep Numarası"     
CartOrderItem._meta.get_field('course').verbose_name = "Talep Edilen Kurs Numarası" 
CartOrderItem._meta.get_field('teacher').verbose_name = "Eğitmen Adı" 
CartOrderItem._meta.get_field('applied_coupon').verbose_name = "Eklenen Ödül" 
CartOrderItem._meta.get_field('coupons').verbose_name = "Ödül"  
CartOrderItem._meta.get_field('oid').verbose_name = "Talep Numarası" 
CartOrderItem._meta.get_field('date').verbose_name = "Talep Tarihi" 
   
class Certificate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    certificate_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    class Meta:
        verbose_name = "Sertifika"
        verbose_name_plural = "Sertifikalar" 
        
Certificate._meta.get_field('course').verbose_name = "Sertifikası Alınan Kurs"     
Certificate._meta.get_field('user').verbose_name = "Sertifikası Alınan Kurs Numarası" 
Certificate._meta.get_field('certificate_id').verbose_name = "Sertifikası Numarası" 
Certificate._meta.get_field('date').verbose_name = "Sertifika Alınan Tarih" 
   
class CompletedLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    variant_item = models.ForeignKey(VariantItem, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    class Meta:
        verbose_name = "Tamamlanmış Ders"
        verbose_name_plural = "Tamamlanmış Dersler"
         
CompletedLesson._meta.get_field('course').verbose_name = "Tamamlanan Kurs"     
CompletedLesson._meta.get_field('user').verbose_name = "Kurs Eğitmeni" 
CompletedLesson._meta.get_field('variant_item').verbose_name = "Tamamlanan Kurs" 
CompletedLesson._meta.get_field('date').verbose_name = "Kursun Tamamlanma Tarihi" 

class CompletedOdev(models.Model):
    odev = models.ForeignKey(Odev, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    variant_item = models.ForeignKey(VariantItem, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    class Meta:
        verbose_name = "Tamamlanmış Ödev"
        verbose_name_plural = "Tamamlanmış Ödevler"
         
CompletedOdev._meta.get_field('odev').verbose_name = "Tamamlanan Ödev"    
CompletedOdev._meta.get_field('user').verbose_name = "Ödev Eğitmeni" 
CompletedOdev._meta.get_field('variant_item').verbose_name = "Tamamlanan Bölüm" 
CompletedOdev._meta.get_field('date').verbose_name = "Ödevin Tamamlanma Tarihi" 

class CompletedKitapTahlili(models.Model):
    kitaptahlili = models.ForeignKey(KitapTahlili, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    variant_item = models.ForeignKey(VariantItem, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    class Meta:
        verbose_name = "Tamamlanmış Kitap Tahlili"
        verbose_name_plural = "Tamamlanmış Ödevler"
         
CompletedKitapTahlili._meta.get_field('kitaptahlili').verbose_name = "Tamamlanan Kitap Tahlili"    
CompletedKitapTahlili._meta.get_field('user').verbose_name = "Kitap Tahlili Eğitmeni" 
CompletedKitapTahlili._meta.get_field('variant_item').verbose_name = "Tamamlanan Bölüm" 
CompletedKitapTahlili._meta.get_field('date').verbose_name = "Kitap Tahlilinin Tamamlanma Tarihi"

class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    def lectures(self):
        return VariantItem.objects.filter(variant__course=self.course)
    
    def completed_lesson(self):
        return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return Variant.objects.filter(course=self.course)
    
    def note(self):
        return Note.objects.filter(course=self.course, user=self.user)
    
    def question_answer(self):
        return Question_Answer.objects.filter(course=self.course)
    
    def review(self):
        return Review.objects.filter(course=self.course, user=self.user).first()
    
    class Meta:
        verbose_name = "Kaydedilan Kurs"
        verbose_name_plural = "Kaydedilen Kurslar" 
        
EnrolledCourse._meta.get_field('course').verbose_name = "Kayıt Olunan Kurs"     
EnrolledCourse._meta.get_field('user').verbose_name = "Kayıt Olunan Kurs Öğrencisi" 
EnrolledCourse._meta.get_field('teacher').verbose_name = "Kayıt Olunan Kurs Eğitmeni" 
EnrolledCourse._meta.get_field('order_item').verbose_name = "Kayıt Olunan Ders"     
EnrolledCourse._meta.get_field('enrollment_id').verbose_name = "Kayıt Olunan Kurs Numarası" 
EnrolledCourse._meta.get_field('date').verbose_name = "Kurs Kayıt Tarihi" 

class EnrolledOdev(models.Model):
    odev = models.ForeignKey(Odev, on_delete=models.CASCADE)
    hazirlayan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    egitmen = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    # order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.odev.title
    
    def lectures(self):
        return VariantOdevItem.objects.filter(variant__odev=self.odev)
    
    # def completed_lesson(self):
    #     return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return VariantOdev.objects.filter(odev=self.odev)
    
    def note(self):
        return NoteOdev.objects.filter(odev=self.odev, user=self.user)
    
    def question_answer(self):
        return Question_AnswerOdev.objects.filter(odev=self.odev)
    
    def review(self):
        return ReviewOdev.objects.filter(odev=self.odev, user=self.user).first()
    
    class Meta:
        verbose_name = "Eğitmene Gönderilen Ödev"
        verbose_name_plural = "Eğitmene Gönderilen Ödevler" 
        
EnrolledOdev._meta.get_field('odev').verbose_name = "Ödev"     
EnrolledOdev._meta.get_field('hazirlayan').verbose_name = "Ödevi Hazırlayan" 
EnrolledOdev._meta.get_field('egitmen').verbose_name = "Eğitmeni" 
EnrolledOdev._meta.get_field('koordinator').verbose_name = "Koordinator" 
# EnrolledOdev._meta.get_field('order_item').verbose_name = "Kayıt Olunan Ders"     
EnrolledOdev._meta.get_field('enrollment_id').verbose_name = "Ödev Numarası" 
EnrolledOdev._meta.get_field('date').verbose_name = "Ödev Kayıt Tarihi" 

class EnrolledKitapTahlili(models.Model):
    kitaptahlili = models.ForeignKey(KitapTahlili, on_delete=models.CASCADE)
    hazirlayan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    egitmen = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    # order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.kitaptahlili.title
    
    def lectures(self):
        return VariantKitapTahliliItem.objects.filter(variant__kitaptahlili=self.kitaptahlili)
    
    # def completed_lesson(self):
    #     return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return VariantKitapTahlili.objects.filter(kitaptahlili=self.kitaptahlili)
    
    def note(self):
        return NoteKitapTahlili.objects.filter(kitaptahlili=self.kitaptahlili, user=self.user)
    
    def question_answer(self):
        return Question_AnswerKitapTahlili.objects.filter(kitaptahlili=self.kitaptahlili)
    
    def review(self):
        return ReviewKitapTahlili.objects.filter(kitaptahlili=self.kitaptahlili, user=self.user).first()
    
    class Meta:
        verbose_name = "Eğitmene Gönderilen Kitap Tahlili"
        verbose_name_plural = "Eğitmene Gönderilen Kitap Tahlilleri" 
        
EnrolledKitapTahlili._meta.get_field('kitaptahlili').verbose_name = "Kitap Tahlili"     
EnrolledKitapTahlili._meta.get_field('hazirlayan').verbose_name = "Kitap Tahlilini Hazırlayan" 
EnrolledKitapTahlili._meta.get_field('egitmen').verbose_name = "Eğitmeni" 
EnrolledKitapTahlili._meta.get_field('koordinator').verbose_name = "Koordinatörü" 
# EnrolledKitapTahlili._meta.get_field('order_item').verbose_name = "Kayıt Olunan Ders"     
EnrolledKitapTahlili._meta.get_field('enrollment_id').verbose_name = "Kitap Tahlili Numarası" 
EnrolledKitapTahlili._meta.get_field('date').verbose_name = "Kitap Tahlili Kayıt Tarihi" 

class EnrolledDersSonuRaporu(models.Model):
    derssonuraporu = models.ForeignKey(DersSonuRaporu, on_delete=models.CASCADE)
    hazirlayan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    egitmen = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    # order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.derssonuraporu.title
    
    def lectures(self):
        return VariantDersSonuRaporuItem.objects.filter(variant__derssonuraporu=self.derssonuraporu)
    
    # def completed_lesson(self):
    #     return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return VariantDersSonuRaporu.objects.filter(derssonuraporu=self.derssonuraporu)
    
    def note(self):
        return NoteDersSonuRaporu.objects.filter(derssonuraporu=self.derssonuraporu, user=self.user)
    
    def question_answer(self):
        return Question_AnswerDersSonuRaporu.objects.filter(derssonuraporu=self.derssonuraporu)
    
    def review(self):
        return ReviewDersSonuRaporu.objects.filter(derssonuraporu=self.derssonuraporu, user=self.user).first()
    
    class Meta:
        verbose_name = "Eğitmene Gönderilen Ders Sonu Raporu"
        verbose_name_plural = "Eğitmene Gönderilen Ders Sonu Raporları" 
        
EnrolledDersSonuRaporu._meta.get_field('derssonuraporu').verbose_name = "Ders Sonu Raporu"     
EnrolledDersSonuRaporu._meta.get_field('hazirlayan').verbose_name = "Ders Sonu Raporunu Hazırlayan" 
EnrolledDersSonuRaporu._meta.get_field('egitmen').verbose_name = "Eğitmeni" 
EnrolledDersSonuRaporu._meta.get_field('koordinator').verbose_name = "Koordinator"     
EnrolledDersSonuRaporu._meta.get_field('enrollment_id').verbose_name = "Ders Sonu Raporu Numarası" 
EnrolledDersSonuRaporu._meta.get_field('date').verbose_name = "Ders Sonu Raporu Kayıt Tarihi" 

class EnrolledEskepProje(models.Model):
    eskepproje = models.ForeignKey(EskepProje, on_delete=models.CASCADE)
    hazirlayan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    egitmen = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    # order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.eskepproje.title
    
    def lectures(self):
        return VariantEskepProjeItem.objects.filter(variant__eskepproje=self.eskepproje)
    
    # def completed_lesson(self):
    #     return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return VariantEskepProje.objects.filter(eskepproje=self.eskepproje)
    
    def note(self):
        return NoteEskepProje.objects.filter(eskepproje=self.eskepproje, user=self.user)
    
    def question_answer(self):
        return Question_AnswerEskepProje.objects.filter(eskepproje=self.eskepproje)
    
    def review(self):
        return ReviewEskepProje.objects.filter(eskepproje=self.eskepproje, user=self.user).first()
    
    class Meta:
        verbose_name = "Koordinatore Gönderilen Proje"
        verbose_name_plural = "Koordinatore Gönderilen Projeler" 
        
EnrolledEskepProje._meta.get_field('eskepproje').verbose_name = "Ders Sonu Raporu"     
EnrolledEskepProje._meta.get_field('hazirlayan').verbose_name = "Ders Sonu Raporunu Hazırlayan" 
EnrolledEskepProje._meta.get_field('egitmen').verbose_name = "Eğitmeni" 
EnrolledEskepProje._meta.get_field('koordinator').verbose_name = "Koordinator"     
EnrolledEskepProje._meta.get_field('enrollment_id').verbose_name = "Ders Sonu Raporu Numarası" 
EnrolledEskepProje._meta.get_field('date').verbose_name = "Ders Sonu Raporu Kayıt Tarihi" 
  
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Not"
        verbose_name_plural = "Notlar"

class NoteOdev(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    odev = models.ForeignKey(Odev, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Ödev Not"
        verbose_name_plural = "Ödev Notları"
        
class NoteKitapTahlili(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    kitaptahlili = models.ForeignKey(KitapTahlili, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Kitap Tahlili Not"
        verbose_name_plural = "Kitap Tahlili Notları"
        
class NoteProje(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    proje = models.ForeignKey(EskepProje, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Proje Not"
        verbose_name_plural = "Proje Notları"
        
class NoteDersSonuRaporu(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    derssonuraporu = models.ForeignKey(DersSonuRaporu, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Ders Sonu Raporu Not"
        verbose_name_plural = "Ders Sonu Raporu Notları"
        
class NoteEskepProje(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    eskepproje = models.ForeignKey(DersSonuRaporu, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Eskep Proje Not"
        verbose_name_plural = "Eskep Proje Notları"
        
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.course.title
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        
class ReviewOdev(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    odev = models.ForeignKey(Odev, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.odev.title
    
    def profile(self):
        return Profile.objects.get(ogrenciStajer=self.ogrenciStajer)
    
    class Meta:
        verbose_name = "Ödev Notu"
        verbose_name_plural = "Ödev Notları"
        
class ReviewKitapTahlili(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    kitaptahlili = models.ForeignKey(KitapTahlili, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.kitaptahlili.title
    
    def profile(self):
        return Profile.objects.get(ogrenciStajer=self.ogrenciStajer)
    
    class Meta:
        verbose_name = "Kitap Tahlili Notu"
        verbose_name_plural = "Kitap Tahlili Notları"
        
class ReviewDersSonuRaporu(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    derssonuraporu = models.ForeignKey(DersSonuRaporu, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.derssonuraporu.title
    
    def profile(self):
        return Profile.objects.get(ogrenciStajer=self.ogrenciStajer)
    
    class Meta:
        verbose_name = "Ders Sonu Raporu Notu"
        verbose_name_plural = "Ders Sonu Raporu Notları"

class ReviewEskepProje(models.Model):
    ogrenciStajer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    koordinator = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    eskepproje = models.ForeignKey(EskepProje, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return self.eskepproje.title
    
    def profile(self):
        return Profile.objects.get(ogrenciStajer=self.ogrenciStajer)
    
    class Meta:
        verbose_name = "Eskep Proje Notu"
        verbose_name_plural = "Eskep Proje Notları"
       
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100, choices=NOTI_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"

class Coupon(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    used_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=50)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)   
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Ödül"
        verbose_name_plural = "Ödüller"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.course.title)
    
    class Meta:
        verbose_name = "İstek"
        verbose_name_plural = "İstekler"

class WishlistOdev(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    odev = models.ForeignKey(Odev, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.odev.title)
    
    class Meta:
        verbose_name = "Ödev İstek"
        verbose_name_plural = "Ödev İstekler"
         
class Country(models.Model):
    name = models.CharField(max_length=100)
    tax_rate = models.IntegerField(default=5)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ülke"
        verbose_name_plural = "Ülkeler"
        
Country._meta.get_field('name').verbose_name = "Ülke" 
Country._meta.get_field('active').verbose_name = "Aktif/Pasif"
       
class Job(models.Model):
    name = models.CharField(max_length=100)   
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Meslek"
        verbose_name_plural = "Meslekler"  
             
Job._meta.get_field('name').verbose_name = "Meslek" 
Job._meta.get_field('active').verbose_name = "Aktif/Pasif" 

class Hafiz(models.Model):    
    full_name = models.CharField(max_length=100,default="")
    babaadi = models.CharField(max_length=150,default="",null=True, blank=True)
    tcno = models.CharField(max_length=150,default="",null=True, blank=True)
    adres = models.CharField(max_length=150, default="",null=True, blank=True)
    adresIl = models.ForeignKey("City",related_name="AdresIl", null=True, blank=True, on_delete=models.SET_NULL)
    adresIlce = models.ForeignKey("District", null=True, blank=True, on_delete=models.SET_NULL)
    roles = models.ManyToManyField(HafizRole, verbose_name="Roller")
    hafizlikbitirmeyili = models.CharField(max_length=8, choices=tuple(sorted(YEAR))  ,default="")
    evtel = models.CharField(max_length=150, default="",null=True, blank=True)
    istel = models.CharField(max_length=150, default="",null=True, blank=True)
    ceptel = models.CharField(max_length=150, default="", unique=True)
    isMarried = models.CharField(max_length=150, choices=ISMARRIED_CHOICES,default="",null=True, blank=True)
    email = models.CharField(max_length=150, default="", unique=True)
    hafizlikyaptigikursadi = models.CharField(max_length=150, default="")
    hafizlikyaptigikursili = models.ForeignKey("City",related_name="KursIlı", null=True, blank=True, on_delete=models.SET_NULL)
    gorev = models.CharField(max_length=150, default="",null=True, blank=True)
    hafizlikhocaadi = models.CharField(max_length=150, default="",null=True, blank=True,)
    hafizlikhocasoyadi = models.CharField(max_length=150, default="",null=True, blank=True)
    hafizlikhocaceptel = models.CharField(max_length=150, default="",null=True, blank=True)
    hafizlikarkadasadi = models.CharField(max_length=150, default="",null=True, blank=True)
    hafizlikarkadasoyad = models.CharField(max_length=150, default="",null=True, blank=True)
    hafizlikarkadasceptel = models.CharField(max_length=150, default="",null=True, blank=True)
    referanstcno = models.CharField(max_length=150, default="",null=True, blank=True)
    onaydurumu = models.CharField(max_length=150,choices=ONAY_CHOICES,default="Onaylanmadı")    
    description = models.TextField(blank=True,null=True)    
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES,default="")    
    job = models.ForeignKey("Job", null=True, blank=True, on_delete=models.SET_NULL)
    yas = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)    
    country = models.ForeignKey("Country", null=True, blank=True, on_delete=models.SET_NULL)
    hdm_egitmen = models.ForeignKey("Teacher",on_delete=models.SET_NULL,null=True,blank=True,verbose_name="HDM Eğitmeni",related_name="hafiz_ogrencileri")

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Hafız Bilgi"
        verbose_name_plural = "Hafız Bilgileri"   

Hafiz._meta.get_field('full_name').verbose_name = "Adı Soyadı" 
Hafiz._meta.get_field('babaadi').verbose_name = "Baba Adı" 
Hafiz._meta.get_field('tcno').verbose_name = "TC Kimlik NO"     
Hafiz._meta.get_field('adres').verbose_name = "Adres" 
Hafiz._meta.get_field('adresIl').verbose_name = "İl" 
Hafiz._meta.get_field('adresIlce').verbose_name = "İlçe"     
Hafiz._meta.get_field('hafizlikbitirmeyili').verbose_name = "Hafızlık Bitirme Yılı" 
Hafiz._meta.get_field('evtel').verbose_name = "Ev Telefonu" 
Hafiz._meta.get_field('istel').verbose_name = "İş Telefonu"     
Hafiz._meta.get_field('ceptel').verbose_name = "Cep Telefonu" 
Hafiz._meta.get_field('isMarried').verbose_name = "Medeni Hali" 
Hafiz._meta.get_field('email').verbose_name = "E-Posta Adresi" 
Hafiz._meta.get_field('hafizlikyaptigikursadi').verbose_name = "Hafızlık Yaptığı Kurs Adı" 
Hafiz._meta.get_field('hafizlikyaptigikursili').verbose_name = "Hafızlık Yaptığı Kurs İli" 
Hafiz._meta.get_field('gorev').verbose_name = "Görevi" 
Hafiz._meta.get_field('hafizlikhocaadi').verbose_name = "Hoca Adı" 
Hafiz._meta.get_field('hafizlikhocasoyadi').verbose_name = "Hoca Soyadı" 
Hafiz._meta.get_field('hafizlikhocaceptel').verbose_name = "Hoca Cep Telefonu" 
Hafiz._meta.get_field('hafizlikarkadasadi').verbose_name = "Hafız Arkadaş Adı" 
Hafiz._meta.get_field('hafizlikarkadasoyad').verbose_name = "Hafız Arkadaş Soyadı" 
Hafiz._meta.get_field('hafizlikarkadasceptel').verbose_name = "Hafız Arkadaş Cep Telefonu" 
Hafiz._meta.get_field('referanstcno').verbose_name = "Referanst TC Kimlik NO" 
Hafiz._meta.get_field('onaydurumu').verbose_name = "Onay Durumu" 
Hafiz._meta.get_field('description').verbose_name = "Hakkında" 
Hafiz._meta.get_field('gender').verbose_name = "Cinsiyet" 
Hafiz._meta.get_field('job').verbose_name = "Meslek" 
Hafiz._meta.get_field('yas').verbose_name = "Yaş" 
Hafiz._meta.get_field('active').verbose_name = "Aktif/Pasif" 
Hafiz._meta.get_field('agent').verbose_name = "İl Temsilcisi" 
Hafiz._meta.get_field('country').verbose_name = "Ülke" 

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="course-file", blank=True, null=True, default="default.jpg")
    roles = models.ManyToManyField(AgentRole, verbose_name="Roller")
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    evtel = models.CharField(max_length=150, default="")
    istel = models.CharField(max_length=150, default="")
    ceptel = models.CharField(max_length=150, default="", unique=True)
    email = models.CharField(max_length=150, default="", unique=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.ForeignKey("Country", related_name="Ülkeler", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("City", related_name="Sehirler", null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES,default="")   
    
    def __str__(self):
        return self.full_name 
    
    def Hafizs(self):
        return Hafiz.objects.filter(agent=self)   
    
    class Meta:
        verbose_name = "Temsilci"
        verbose_name_plural = "Temsilciler"

Agent._meta.get_field('user').verbose_name = "Temsilci"     
Agent._meta.get_field('image').verbose_name = "Profil Resmi" 
Agent._meta.get_field('full_name').verbose_name = "Adı Soyadı" 
Agent._meta.get_field('bio').verbose_name = "Biografi"     
Agent._meta.get_field('evtel').verbose_name = "Ev Telefonu" 
Agent._meta.get_field('istel').verbose_name = "İş Telefonu" 
Agent._meta.get_field('ceptel').verbose_name = "Cep Telefonu"     
Agent._meta.get_field('email').verbose_name = "E-posta Adresi"     
Agent._meta.get_field('facebook').verbose_name = "Facebook" 
Agent._meta.get_field('twitter').verbose_name = "Twitter" 
Agent._meta.get_field('linkedin').verbose_name = "Linkedin"     
Agent._meta.get_field('about').verbose_name = "Hakkında" 
Agent._meta.get_field('country').verbose_name = "Ülke" 
Agent._meta.get_field('city').verbose_name = "Şehir" 
Agent._meta.get_field('active').verbose_name = "Aktif/Pasif" 
Agent._meta.get_field('gender').verbose_name = "Cinsiyet" 

class City(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Şehir"
        verbose_name_plural = "Şehirler"
        
City._meta.get_field('name').verbose_name = "Şehir" 
City._meta.get_field('active').verbose_name = "Aktif/Pasif" 

     
class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey("City", related_name="Cities", null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "İlçe"
        verbose_name_plural = "İlçeler"
        
District._meta.get_field('name').verbose_name = "İlçe"    
District._meta.get_field('city').verbose_name = "Şehir" 
District._meta.get_field('active').verbose_name = "Aktif/Pasif" 

class OrganizationMember(models.Model):
    Name = models.CharField(max_length=100)    
    Designation = models.ForeignKey("Designation", null=True, blank=True, on_delete=models.SET_NULL)
    ImageUrl = models.FileField(upload_to="course-file", blank=True, null=True, default="default.jpg")
    IsExpand = models.BooleanField()
    active = models.BooleanField()
    email = models.EmailField(default="")
    phone = models.CharField(max_length=15,default="")
    
    def __str__(self):
        return self.Name
    
    class Meta:
        verbose_name = "Organizasyon Üyesi"
        verbose_name_plural = "Organizasyon Üyeleri"
        
OrganizationMember._meta.get_field('Name').verbose_name = "Üye Adı Soyadı"    
OrganizationMember._meta.get_field('Designation').verbose_name = "Görevi" 
OrganizationMember._meta.get_field('ImageUrl').verbose_name = "Üye Resmi" 
OrganizationMember._meta.get_field('IsExpand').verbose_name = "Expand" 
OrganizationMember._meta.get_field('active').verbose_name = "Aktif/Pasif" 
OrganizationMember._meta.get_field('email').verbose_name = "E Posta" 
OrganizationMember._meta.get_field('phone').verbose_name = "Telefon" 

class Designation(models.Model):
    name = models.CharField(max_length=100)
    ustBirim = models.IntegerField(default=0) 
    birimNumarasi = models.IntegerField(default=0)
    active = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Üye Görevi"
        verbose_name_plural = "Üye Görevleri"
        
Designation._meta.get_field('name').verbose_name = "Üye Görevi" 
Designation._meta.get_field('active').verbose_name = "Aktif/Pasif" 
Designation._meta.get_field('ustBirim').verbose_name = "Üst Birim" 
Designation._meta.get_field('birimNumarasi').verbose_name = "Birim Numarası" 

class Proje(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    image = models.FileField(upload_to="proje-file", default="HBS.png", null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Proje Adı"
        verbose_name_plural = "Projeler"
        
Proje._meta.get_field('name').verbose_name = "Proje Adı" 
Proje._meta.get_field('active').verbose_name = "Aktif/Pasif" 
Proje._meta.get_field('image').verbose_name = "Proje Resmi" 


class Stajer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True, default="default.jpg")    
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    evtel = models.CharField(max_length=150, default="")
    istel = models.CharField(max_length=150, default="")
    ceptel = models.CharField(max_length=150, default="", unique=True)
    roles = models.ManyToManyField('StajerRole', verbose_name="Roller")  
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("City", null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES,default="")   
    
    def __str__(self):
        return self.full_name    
    
    class Meta:
        verbose_name = "Stajer"
        verbose_name_plural = "Stajerler"

Stajer._meta.get_field('user').verbose_name = "Stajer"     
Stajer._meta.get_field('instructor').verbose_name = "Koordinator"     
Stajer._meta.get_field('image').verbose_name = "Profil Resmi" 
Stajer._meta.get_field('full_name').verbose_name = "Adı Soyadı" 
Stajer._meta.get_field('bio').verbose_name = "Biografi"     
Stajer._meta.get_field('evtel').verbose_name = "Ev Telefonu" 
Stajer._meta.get_field('istel').verbose_name = "İş Telefonu" 
Stajer._meta.get_field('ceptel').verbose_name = "Cep Telefonu"     
# Stajer._meta.get_field('email').verbose_name = "E-posta Adresi"     
Stajer._meta.get_field('facebook').verbose_name = "Facebook" 
Stajer._meta.get_field('twitter').verbose_name = "Twitter" 
Stajer._meta.get_field('linkedin').verbose_name = "Linkedin"     
Stajer._meta.get_field('about').verbose_name = "Hakkında" 
Stajer._meta.get_field('country').verbose_name = "Ülke" 
Stajer._meta.get_field('city').verbose_name = "Şehir" 
Stajer._meta.get_field('active').verbose_name = "Aktif/Pasif" 
Stajer._meta.get_field('gender').verbose_name = "Cinsiyet" 

class Ogrenci(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Koordinator, on_delete=models.SET_NULL, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True, default="default.jpg")
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    evtel = models.CharField(max_length=150, default="")
    istel = models.CharField(max_length=150, default="")
    ceptel = models.CharField(max_length=150, default="", unique=True)
    roles = models.ManyToManyField('OgrenciRole', verbose_name="Roller")    
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("City", null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES,default="")   
    
    def __str__(self):
        return self.full_name    
    
    class Meta:
        verbose_name = "Öğrenci"
        verbose_name_plural = "Öğrenciler"

Ogrenci._meta.get_field('user').verbose_name = "Öğrenci"     
Ogrenci._meta.get_field('image').verbose_name = "Profil Resmi" 
Ogrenci._meta.get_field('full_name').verbose_name = "Adı Soyadı" 
Ogrenci._meta.get_field('bio').verbose_name = "Biografi"     
Ogrenci._meta.get_field('evtel').verbose_name = "Ev Telefonu" 
Ogrenci._meta.get_field('istel').verbose_name = "İş Telefonu" 
Ogrenci._meta.get_field('ceptel').verbose_name = "Cep Telefonu"     
# Ogrenci._meta.get_field('email').verbose_name = "E-posta Adresi"     
Ogrenci._meta.get_field('facebook').verbose_name = "Facebook" 
Ogrenci._meta.get_field('twitter').verbose_name = "Twitter" 
Ogrenci._meta.get_field('linkedin').verbose_name = "Linkedin"     
Ogrenci._meta.get_field('about').verbose_name = "Hakkında" 
Ogrenci._meta.get_field('country').verbose_name = "Ülke" 
Ogrenci._meta.get_field('city').verbose_name = "Şehir" 
Ogrenci._meta.get_field('active').verbose_name = "Aktif/Pasif" 
Ogrenci._meta.get_field('gender').verbose_name = "Cinsiyet"

class QuranAnnotation(models.Model):
    SHAPE_CHOICES = [
        ('line', 'Line'),
        ('circle', 'Circle'),
    ]
    shape_type = models.CharField(max_length=10, choices=SHAPE_CHOICES)
    coordinates = models.JSONField()  # {"x1": .., "y1": .., "x2": .., "y2": ..} veya {"cx":..,"cy":..,"r":..}
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class ESKEPEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    background_color = models.CharField(max_length=20, default="#007bff")
    border_color = models.CharField(max_length=20, default="#0056b3")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.date})"
    

# class HDMEgitmen(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=100)
#     photo = models.ImageField(upload_to='instructors/', null=True, blank=True)
    
#     def __str__(self):
#         return self.full_name

# class HDMHafiz(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     egitmen = models.ForeignKey(HDMEgitmen, on_delete=models.CASCADE, related_name="hafizlar")
#     full_name = models.CharField(max_length=100)
#     photo = models.ImageField(upload_to='hafizlar/', null=True, blank=True)

#     def __str__(self):
#         return self.full_name

class DersAtamasi(models.Model):
    hafiz = models.ForeignKey(Hafiz, on_delete=models.CASCADE, related_name="dersler")
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateTimeField(default=timezone.now)
    time = models.TimeField(default=timezone.now)  # yeni eklenen alan
    aciklama = models.TextField(blank=True, null=True)
    topic = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.hafiz.full_name} - {self.date.date()} {self.time}"
    
class Ders(models.Model):
    hafiz = models.ForeignKey(Hafiz, on_delete=models.CASCADE)
    Instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=255,default="")

    def __str__(self):
        return f"{self.hafiz.full_name} - {self.date}"
    
class HataNotu(models.Model):
    hafiz = models.ForeignKey(Hafiz, on_delete=models.CASCADE, related_name="hatalar")
    lesson = models.ForeignKey(Ders, on_delete=models.SET_NULL, null=True, blank=True)
    sayfa = models.IntegerField()    
    tarih = models.DateField(auto_now_add=True)    
    shape_type = models.CharField(max_length=20,null=True, blank=True)
    coordinates = models.JSONField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    hata_turu = models.CharField(max_length=50,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"{self.hafiz.full_name} - Sayfa {self.page_number}"
    


class PeerID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peer_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.peer_id}"


class QuranPage(models.Model):
    page_number = models.PositiveIntegerField(unique=True)
    image = models.ImageField(upload_to='quran_pages/')

    def __str__(self):
        return f"Page {self.page_number}"


class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    page = models.ForeignKey(QuranPage, on_delete=models.CASCADE)
    shape_type = models.CharField(max_length=10, choices=[('line', 'Line'), ('circle', 'Circle')])
    x1 = models.FloatField(default=0.0)
    y1 = models.FloatField(default=0.0)
    x2 = models.FloatField(default=0.0)
    y2 = models.FloatField(default=0.0)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - Page {self.page.page_number} - {self.shape_type}"