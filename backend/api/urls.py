from api import views as api_views
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Hafız Bilgi
    path("hafizbilgi/create/", api_views.HafizBilgiCreateAPIView.as_view()),   
    path("hafizbilgi/list/", api_views.HafizsListAPIView.as_view()),   
    
    # Meslek    
    path("job/list/", api_views.JobListAPIView.as_view()),
    
    # İl    
    path("city/list/", api_views.CityListAPIView.as_view()),
    
    # Proje   
    path("proje/list/", api_views.ProjeListAPIView.as_view()),
    
    # İlçe    
    path("district/list/", api_views.DistrictListAPIView.as_view()),
    
    # OrganizationChart    
    path("admin/organizationchart/", api_views.OrganizationMemberViewSetAPIVIew.as_view()),
   
    # Authentication Endpoints
    path("user/token/", api_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
    path("user/register/", api_views.RegisterView.as_view()),
    path("user/password-reset/<email>/", api_views.PasswordResetEmailVerifyAPIView.as_view()),
    path("user/password-change/", api_views.PasswordChangeAPIView.as_view()),
    path("user/profile/<user_id>/", api_views.ProfileAPIView.as_view()),
    path("user/change-password/", api_views.ChangePasswordAPIView.as_view()),

    # Core Endpoints
    path("course/category/", api_views.CategoryListAPIView.as_view()),
    path("course/course-list/", api_views.CourseListAPIView.as_view()),
    path("course/search/", api_views.SearchCourseAPIView.as_view()),
    path("course/course-detail/<slug>/", api_views.CourseDetailAPIView.as_view()),
    path("course/cart/", api_views.CartAPIView.as_view()),
    path("course/cart-list/<cart_id>/", api_views.CartListAPIView.as_view()),
    path("cart/stats/<cart_id>/", api_views.CartStatsAPIView.as_view()),
    path("course/cart-item-delete/<cart_id>/<item_id>/", api_views.CartItemDeleteAPIView.as_view()),
    path("order/create-order/", api_views.CreateOrderAPIView.as_view()),
    path("order/checkout/<oid>/", api_views.CheckoutAPIView.as_view()),
    path("order/coupon/", api_views.CouponApplyAPIView.as_view()),
    path("payment/stripe-checkout/<order_oid>/", api_views.StripeCheckoutAPIView.as_view()),
    path("payment/payment-sucess/", api_views.PaymentSuccessAPIView.as_view()),


    # Student API Endpoints
    path("student/summary/<user_id>/", api_views.StudentSummaryAPIView.as_view()),
    path("student/course-list/<user_id>/", api_views.StudentCourseListAPIView.as_view()),
    path("student/course-detail/<user_id>/<enrollment_id>/", api_views.StudentCourseDetailAPIView.as_view()),
    path("student/course-completed/", api_views.StudentCourseCompletedCreateAPIView.as_view()),
    path("student/course-note/<user_id>/<enrollment_id>/", api_views.StudentNoteCreateAPIView.as_view()),
    path("student/course-note-detail/<user_id>/<enrollment_id>/<note_id>/", api_views.StudentNoteDetailAPIView.as_view()),
    path("student/rate-course/", api_views.StudentRateCourseCreateAPIView.as_view()),
    path("student/review-detail/<user_id>/<review_id>/", api_views.StudentRateCourseUpdateAPIView.as_view()),
    path("student/wishlist/<user_id>/", api_views.StudentWishListListCreateAPIView.as_view()),
    path("student/question-answer-list-create/<course_id>/", api_views.QuestionAnswerListCreateAPIView.as_view()),
    path("student/question-answer-message-create/", api_views.QuestionAnswerMessageSendAPIView.as_view()),

    # Agent API Endpoints
    path("agent/summary/<agent_id>/", api_views.AgentSummaryAPIView.as_view()),
    path("agent/course-list/<user_id>/", api_views.StudentCourseListAPIView.as_view()),
    path("agent/hafiz-list/<agent_id>/", api_views.HafizListViewSetAPIVIew.as_view({'get': 'list'})),
    path("agent/<user_id>/", api_views.IsAgent),
    path("agent/hafizbilgi-update/<agent_id>/<hafizbilgi_id>/", api_views.HafizBilgiUpdateAPIView.as_view()),
    path("agent/hafizbilgi-create/", api_views.HafizBilgiCreateAPIView.as_view()),
    
    # Teacher API Endpoints
    path("teacher/summary/<teacher_id>/", api_views.TeacherSummaryAPIView.as_view()),
    path("teacher/course-lists/<teacher_id>/", api_views.TeacherCourseListAPIView.as_view()),
    path("teacher/review-lists/<teacher_id>/", api_views.TeacherReviewListAPIView.as_view()),
    path("teacher/review-detail/<teacher_id>/<review_id>/", api_views.TeacherReviewDetailAPIView.as_view()),
    path("teacher/student-lists/<teacher_id>/", api_views.TeacherStudentsListAPIVIew.as_view({'get': 'list'})),
    path("teacher/all-months-earning/<teacher_id>/", api_views.TeacherAllMonthEarningAPIView),
    path("teacher/best-course-earning/<teacher_id>/", api_views.TeacherBestSellingCourseAPIView.as_view({'get': 'list'})),
    path("teacher/course-order-list/<teacher_id>/", api_views.TeacherCourseOrdersListAPIView.as_view()),
    path("teacher/question-answer-list/<teacher_id>/", api_views.TeacherQuestionAnswerListAPIView.as_view()),
    path("teacher/coupon-list/<teacher_id>/", api_views.TeacherCouponListCreateAPIView.as_view()),
    path("teacher/coupon-detail/<teacher_id>/<coupon_id>/", api_views.TeacherCouponDetailAPIView.as_view()),
    path("teacher/noti-list/<teacher_id>/", api_views.TeacherNotificationListAPIView.as_view()),
    path("teacher/noti-detail/<teacher_id>/<noti_id>", api_views.TeacherNotificationDetailAPIView.as_view()),
    path("teacher/course-create/", api_views.CourseCreateAPIView.as_view()),
    path("teacher/course-update/<teacher_id>/<course_id>/", api_views.CourseUpdateAPIView.as_view()),
    path("teacher/course-detail/<course_id>/", api_views.TeacherCourseDetailAPIView.as_view()),
    path("teacher/course/variant-delete/<variant_id>/<teacher_id>/<course_id>/", api_views.CourseVariantDeleteAPIView.as_view()),
    path("teacher/course/variant-item-delete/<variant_id>/<variant_item_id>/<teacher_id>/<course_id>/", api_views.CourseVariantItemDeleteAPIVIew.as_view()),

    # Stajer API Endpoints
    path("stajer/odev-create/", api_views.OdevCreateAPIView.as_view()),
    path("stajer/odev-list/<stajer_id>/", api_views.StajerOdevListAPIView.as_view()),
    path("stajer/odev-detail/<user_id>/<enrollment_id>/", api_views.StajerOdevDetailAPIView.as_view()),
    # path("stajer/odev-completed/", api_views.StudentCourseCompletedCreateAPIView.as_view()),
    
    # Eğitmen API Endpoints
    # path("instructor/odev-detail/<user_id>/<teacher_id>/", api_views.InstructorOdevDetailAPIView.as_view()),
    # path("instructor/odev-list/<teacher_id>/", api_views.InstructorOdevListAPIView.as_view()),
    path("instructor/odev-completed/", api_views.InstructorOdevCompletedCreateAPIView.as_view()),
    
    path("instructor/summary/<user_id>/", api_views.InstructorSummaryAPIView.as_view()),
    path("instructor/odev-list/<user_id>/", api_views.InstructorOdevListAPIView.as_view()),
    path("instructor/odev-detail/<user_id>/<enrollment_id>/", api_views.InstructorOdevDetailAPIView.as_view()),
    path("instructor/odev-completed/", api_views.InstructorOdevCompletedCreateAPIView.as_view()),
    path("instructor/odev-note/<user_id>/<enrollment_id>/", api_views.InstructorNoteCreateAPIView.as_view()),
    path("instructor/odev-note-detail/<user_id>/<enrollment_id>/<note_id>/", api_views.InstructorNoteDetailAPIView.as_view()),
    path("instructor/rate-odev/", api_views.InstructorRateCourseCreateAPIView.as_view()),
    path("instructor/review-detail/<user_id>/<review_id>/", api_views.InstructorRateCourseUpdateAPIView.as_view()),
    path("instructor/wishlist/<user_id>/", api_views.InstructorWishListListCreateAPIView.as_view()),
    path("instructor/question-answer-list-create/<odev_id>/", api_views.OdevQuestionAnswerListCreateAPIView.as_view()),
    path("instructor/question-answer-message-create/", api_views.OdevQuestionAnswerMessageSendAPIView.as_view()),
]


