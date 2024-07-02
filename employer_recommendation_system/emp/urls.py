from django.urls import path
from .views import * 
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('student',views.student_homepage,name="student"),
    path('<pk>/profile/<int:job>',views.student_profile_confirm,name='student_profile_confirm'),
    path('<pk>/profile',views.student_profile,name='student_profile'),
    path('add_student_job_status',views.add_student_job_status,name='add_student_job_status'),
    path('student_profile/<int:id>/<int:job>',views.student_profile_details,name='student_profile_details'),
    path('student_profile_spk/<int:id>',views.student_profile_details_spk,name='student_profile_details_spk'),
    path('student-list',StudentListView.as_view(),name='student-list'),
    path('notify-student-profile/',views.notify_student,name='notify-student-profile'),

    
    path('manager',views.manager_homepage,name="manager"),
    path('shortlist_student',views.shortlist_student,name='shortlist_student'),
    ################### company urls : currently only accessible to MANAGER Role : Set conditions via admin
    path('add_company/', CompanyCreate.as_view(), name='add_company'),
    path('<slug:slug>/update-company/', CompanyUpdate.as_view(), name='update-company-detail'),
    path('company_list/', CompanyListView.as_view(), name='company-list'),
    path('company/<slug:slug>/', CompanyDetailView.as_view(), name='company-detail'),
    ################### job urls
    path('add_job/', JobCreate.as_view(), name='add_job'),
    path('<slug:slug>/update-job/', JobUpdate.as_view(), name='update-job-detail'),
    path('job_list/', JobListView.as_view(), name='job-list'),
    path('my_jobs/', views.student_jobs, name='student_jobs'),
    path('job/<slug:slug>/', JobDetailView.as_view(), name='job-detail'),
    path('job_listings/', JobListingView.as_view(), name='job-listing'),
    path('api/jobs/<req_user>/',views.jobs,name='jobs'),
    ################### jobshortlist
    path('job_application_status/', JobAppStatusListView.as_view(), name='job-app-status'),
    path('job_application_status/<int:id>/', views.job_app_details, name='job-app-detail'),
    path('check_mail_status/<int:id>/', views.check_mail_status, name='check_mail_status'),
    path('logout1', views.handlelogout, name='logout'),
    path('<pk>/document', views.document_view, name='document_view'), #resume & cover_letter as 'type' query
    ################### Degree urls : currently only accessible to MANAGER Role : Set conditions via admin
    path('add_degree/', DegreeCreateView.as_view(), name='add_degree'),
    path('<slug:slug>/update-degree/', DegreeUpdateView.as_view(), name='update-degree'),
    ################### Discipline urls : currently only accessible to MANAGER Role : Set conditions via admin
    path('add_discipline/', DisciplineCreateView.as_view(), name='add_discipline'),
    path('<slug:slug>/update-discipline/', DisciplineUpdateView.as_view(), name='update-discipline'),
    # path('discipline/<slug:slug>/', DisciplineDetailView.as_view(), name='discipline-detail'),
    ################### Domain urls : currently only accessible to MANAGER Role : Set conditions via admin
    path('add_domain/', DomainCreateView.as_view(), name='add_domain'),
    path('<slug:slug>/update-domain/', DomainUpdateView.as_view(), name='update-domain'),
    ################### Domain urls : currently only accessible to MANAGER Role : Set conditions via admin
    path('add_job_type/', JobTypeCreateView.as_view(), name='add_job_type'),
    path('<slug:slug>/update_job_type/', JobTypeUpdateView.as_view(), name='update_job_type'),

    ################### ajax
    path('ajax-state-city/', views.ajax_state_city, name='ajax_state_city'),
    path('ajax-institute-list/', views.ajax_institute_list, name='ajax_institute_list'),
    path('ajax-send-mail/', views.ajax_send_mail, name='ajax_send_mail'),
    path('ajax-get-state-city/', views.ajax_get_state_city, name='ajax_get_state_city'),
    path('ajax-contact-form/', views.ajax_contact_form, name='ajax_contact_form'),
    path('update_jobfair_student_status/', views.update_jobfair_student_status, name='update_jobfair_student_status'),


    path('student_filter',views.student_filter,name='student_filter'),

    #landing page
    path('add_image', GalleryImageCreate.as_view(),name='add_image' ),
    path('image-gallery', GalleryImageList.as_view(),name='image_gallery' ),
    # path('image_details/<int:pk>', GalleryImageDetail.as_view(),name='gallery_image_detail' ),
    path('update_image/<int:pk>', GalleryImageUpdate.as_view(),name='update_image' ),
    path('add_testimonial', TestimonialCreate.as_view(),name='add_testimonial' ),
    # path('image_details/<int:pk>', GalleryImageDetail.as_view(),name='gallery_image_detail' ),
    path('update_testimonial/<int:pk>', TestimonialUpdate.as_view(),name='update_testimonial' ),
    path('list_testimonials/', TestimonialsList.as_view(),name='list_testimonials' ),
    

    # path('<slug:slug>/', GalleryImageDetail.as_view(), name='gallery-image-detail'),
    # path('degree/<slug:slug>/', DegreeDetailView.as_view(), name='degree-detail'),
    # path('degree/', CompanyListView.as_view(), name='company-list'),
    # path('degree/<slug:slug>/', CompanyDetailView.as_view(), name='company-detail'),
    
    ################### public urls
    path('companies',CompanyList.as_view(),name='companies-list'),

    #API for registration
    path('api/register/',RegistrationView.as_view(),name='register'),

    #Utils APi
    path('api/utils/cities/',get_cities_from_states,name='get-cities-from-state'),
    
    #API for companies
    # path('api/companies/',CompanyViewSet.as_view({'get': 'list'}),name='company'),
    # path('api/companies/<int:pk>',CompanyViewSet.as_view({'get': 'retrieve'}),name='company-patch'),

    #API for jobs
    path('api/jobs/',JobView.as_view(),name='jobs'),
    path('api/jobs/<int:pk>',JobView.as_view(),name='jobs-patch'),

    #----------------------------------- APIs V2 -----------------------------------#
    path('api/homepage', HomepageView.as_view(), name='homepage'),
    # path('api/companies/',CompanyView.as_view(),name='companies'),
    path('api/students/<int:pk>/dashboard',StudentHomepageView.as_view(),name='companies'),
    path('api/students/<int:pk>/events',StudentJobView.as_view(),name='companies'),
    path('api/students/<int:pk>/profile',StudentProfileView.as_view(),name='companies'),
    path('api/companies/<int:pk>/jobs',CompanyJobView.as_view(),name='companies'),
    path('api/admin/companies',AdminCompanyView.as_view(),name='companies'),
    # path('api/admin/jobs',AdminJobView.as_view(),name='companies'),
    path('api/admin/students',AdminStudentView.as_view(),name='students'), # ToDo Later
    path('api/admin/events',AdminEventsView.as_view(),name='companies'),

    ################### v2 APIs ###################
    
    # path('api/companies/',CompanyRegistrationData.as_view(),name='job-data'), #API to register a new company from public company registration form
    #Final
    path('api/companies/',CompanyView.as_view(),name='job-data'), #API to register a new company from public company registration form
    
    #Final
    path('api/company/manager/jobs/<str:pk>',JobDetailView.as_view(),name='job-detail'), #API to get job detail
    #Final
    path('api/jobs/<str:pk>/change-status/<str:new_status>/',JobStatusChangeView.as_view(),name='job-detail'), #API to change job status
    path('api/dashboard/company',CompanyDashboardView.as_view(),name='job-detail'), #API to get company dashboard data
    # path('api/students/<str:pk>',StudentDetailView.as_view(),name='job-detail'), #API to get job detail
    path('api/jobs/',JobDetailCreateView.as_view(),name='job-detail'), #API to get company dashboard data
    path('api/companies/<int:pk>/',CompanyUpdateView.as_view(),name='job-data'), # to update company details
    path('api/students/<int:pk>/',StudentProfileView.as_view(),name='job-data'), # to fetch student profile details
    path('api/dashboard/student/<int:pk>',StudentDashboardView.as_view(),name='job-data'), # to fetch student dashboard details
    path('api/admin/jobs',AdminJobListView.as_view(),name='job-data'), # to fetch student profile details
    path('api/admin/jobs/shortlist/<int:pk>',AdminJobShortListView.as_view(),name='job-data'), # to fetch student profile details
    #Final
    path('api/students/jobs/recommended',StudentRecommendedJobListView.as_view(),name='job-data'), # to fetch student profile details
    #Final
    path('api/students/jobs/applied',StudentAppliedJobListView.as_view(),name='job-data'), # to fetch student profile details
    #Final
    path('api/apply-job',ApplyJobView.as_view(),name='job-data'), # to fetch student profile details

    path('api/profile/employer/<int:user_id>', EmployerProfile.as_view(), name="employer-profile"),
    # -----------------------------------
    #Company API
    #Final
    path('api/dashboard/employer/', EmployerDashboardView.as_view(), name="employer-profile"), #API to fetch employer dashboard data
    #Final
    path('api/company/manager/jobs/',CompanyManagerJobsView.as_view(),name='jobs'), #API to list jobs corresponding to logged in employer
    #Final
    path('api/job-data/<int:job_id>',JobDetailData.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/job-data/',JobFormData.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/job-initial-data/',JobFormInitialData.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/profile/company/',CompanyUserData.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/profile/company/user/',CompanyUserProfile.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/profile/company/data/',CompanyData.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/profile/company/location/',CompanyLocation.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/profile/company/reset-password/',CompanyPasswordReset.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/company-initial-data/',CompanyRegInitialData.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/register/company/',RegisterCompany.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/student-initial-data/<int:user_id>',StudentProfileInitialData.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    path('api/students/<int:user_id>',StudentUpdateProfile.as_view(),name='job-data'), #API to prepopulate job form with initial options data
    
    
]
