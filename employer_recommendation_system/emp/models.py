from django.db import models
from django.conf import settings
import datetime
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.urls import reverse
from spoken.models import AcademicCenter, FossMdlCourses
import os
from spoken.models import SpokenUser, SpokenState, SpokenCity
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from utilities.models import FossCategory, State, District, City, InstituteType, Location
from moodle.models import MdlUser, MdlQuizGrades 
# from .managers import JobDetailManager    
ACTIVATION_STATUS = ((None, "--------"),(1, "Active"),(3, "Deactive"))
GENDER = [('a','No Criteria'),('f','F-Female Candidates'),('m','M-Male Candidates'),]
START_YEAR_CHOICES = []
END_YEAR_CHOICES = []
DEFAULT_NUM_EMP = '100_500'
NUM_OF_EMPS = [('less_than_50','< 50'),('50_100','50 - 100'),('100_500','100 - 500'),('greater_than_500','> 500'),]
STATUS = {'ACTIVE' :1,'INACTIVE' :0}

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Invalid.")

for r in range(2000, (datetime.datetime.now().year+4)):
    START_YEAR_CHOICES.append((r,r))
    END_YEAR_CHOICES.append((r+1,r+1))

def profile_picture(instance, filename):
    ext = os.path.splitext(filename)[1]
    ext = ext.lower()
    return '/'.join(['user', str(instance.user.id), str(instance.user.id) + ext])

class CustomDegreeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')

class Degree(models.Model): # eg. BTech-Mechanical, MCA, BSc 
    objects = CustomDegreeManager()
    name = models.CharField(max_length=200,verbose_name='Degree',unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True )
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('degree-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            obj = Degree.objects.get(name=self.name,date_created=self.date_created)
            obj.slug = slugify(obj.id) 
            obj.save()

class Course(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Domain(models.Model):
    name = models.CharField(max_length=200,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True )
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('domain-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            obj = Domain.objects.get(name=self.name,date_created=self.date_created)
            obj.slug = slugify(obj.id) 
            obj.save()

class CustomJobTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('jobtype')

class JobType(models.Model):
    objects = CustomJobTypeManager()
    jobtype = models.CharField(max_length=200,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True )
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    def __str__(self):
        return self.jobtype

    def get_absolute_url(self):
        return reverse('job-type-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            obj = JobType.objects.get(jobtype=self.jobtype,date_created=self.date_created)
            obj.slug = slugify(obj.id) 
            obj.save()

    # def get_absolute_url(self):
    #     return reverse('degree-detail', kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if not self.slug:
    #         obj = Degree.objects.get(name=self.name,date_created=self.date_created)
    #         obj.slug = slugify(obj.id) 
    #         obj.save()

class CustomDisciplineManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')

class Discipline(models.Model):
    objects = CustomDisciplineManager()
    name = models.CharField(max_length=200,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True )
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('update-discipline', kwargs={'slug': self.slug})
        return reverse('update-discipline', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            obj = Discipline.objects.get(name=self.name,date_created=self.date_created)
            obj.slug = slugify(obj.id) 
            obj.save()

class Education(models.Model):
    degree = models.ForeignKey(Degree,null=True,on_delete=models.CASCADE)
    acad_discipline = models.ForeignKey(Discipline,on_delete=models.CASCADE,verbose_name='Academic Discipline',null=True)
    # institute = models.CharField(max_length=400) #Institute name
    #institute = models.ForeignKey(AcademicCenter,max_length=400,on_delete=models.CASCADE,null=True,blank=True) #Institute name
    institute = models.IntegerField(null=True,blank=True)
    start_year = models.IntegerField(choices=START_YEAR_CHOICES, null=True)
    end_year = models.IntegerField(choices=END_YEAR_CHOICES, null=True)
    gpa = models.CharField(max_length=10,null=True)
    order = models.IntegerField(default=1) #1 : Current Education 2: Pas education
    # def __str__(self):
    #     return self.degree.name+'_'+str(self.institute)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Project(models.Model):
    url = models.URLField(null=True,blank=True)
    desc = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.url)

class SkillGroup(models.Model):
    name = models.CharField(max_length=220)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=250)
    group = models.ForeignKey(SkillGroup, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(validators=[phone_regex], max_length=17)
    address = models.CharField(max_length=400, null=True,blank=True,verbose_name='Home Address')  #spk
    #spk_institute = models.CharField(max_length=200) #spk
    education = models.ManyToManyField(Education, null=True)
    spk_institute = models.IntegerField(null=True)  #spk
    #course = models.ForeignKey(Course,null=True,blank=True,on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, null=True,blank=True)
    about = models.TextField(null=True,blank=True,verbose_name='About Yourself*') #Short description/introduction about student profile
    projects = models.ManyToManyField(Project, null=True,blank=True)
    #photo = models.ImageField(null=True,blank=True) #profile photo
    picture = models.FileField(upload_to=profile_picture, null=True, blank=True)    #spk
    github = models.URLField(null=True,blank=True)
    linkedin = models.URLField(null=True,blank=True)
    cover_letter = models.FileField(null=True,blank=True,upload_to='')
    resume = models.FileField(null=True,blank=True,upload_to='resumes/',verbose_name='Resume*')
    # cover_letter = models.FileField(null=True,blank=True,upload_to=user_directory_path)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    #spoken_score = 
    status = models.BooleanField(default=True) #False to restrict student from accessing
    spk_usr_id = models.IntegerField(null=True)  # spoken student id
    spk_student_id = models.IntegerField(null=True)  # spoken student id
    gender = models.CharField(max_length=10, null=True) # autopopulated spk cms profile
    location = models.CharField(max_length=400,null=True,blank=True)  #spk
    state = models.CharField(max_length=100, null=True)  #spk
    district = models.CharField(max_length=200, null=True)  #spk
    city = models.CharField(max_length=200, null=True)  #spk
    alternate_email = models.EmailField(null=True,blank=True)
    certifications = models.TextField(null=True,blank=True)
    notified_date = models.DateTimeField(null=True,blank=True)
    profile_update_date = models.DateTimeField(null=True,blank=True)
    joining_immediate = models.BooleanField(null=True,blank=False)
    avail_for_intern = models.BooleanField(null=True,blank=False)
    willing_to_relocate = models.JSONField(null=True,blank=False)
    skills = models.ManyToManyField(Skill)
    def __str__(self):
        return self.user.username+'-'+self.user.email+'-'+str(self.id)


    def get_absolute_url(self):
        url = str(self.id)+'/'+'profile'
        return reverse('student_profile',kwargs={'pk':self.id}) 
    
    def get_appiled_jobs(self):
        print(f"\033[92m 1 \033[0m")
        data  = JobShortlist.objects.filter(student_id=self.id).order_by('date_updated')
        print(f"\033[92m 2 \033[0m")
        # print(f"\033[93m data get_appiled_jobs : {data} \033[0m")
        return data

#Final
    def is_qualified_for_job(self,student_scores,job):
         # Retrieve mandatory FOSS requirements for the job
        job_foss_data = JobFoss.objects.filter(job=job, type="Mandatory").values('foss', 'grade')

        # Check if student meets all mandatory FOSS requirements
        for requirement in job_foss_data:
            foss = requirement['foss']
            grade = requirement['grade']
            foss = int(foss)

            # Since we are checking mandatory criteria, exit if anyone requirement fails
            if foss not in student_scores.keys():
                d = list(student_scores.keys())[0]
                return False
            # Check if the student has taken the course and achieved at least the required grade
            if student_scores[foss] < grade:
                return False
            return True

#Final 
    def get_recommended_jobs(self):
        # Fetch active jobs and the current user
        available_jobs = JobDetail.get_active_jobs()
        user = self.user
        print(f"\033[93m available_jobs : {available_jobs} \033[0m")
        print(f"\033[93m user : {user} \033[0m")

        # Scores are to be compared from moodle ,so get Moodle user details
        mdl_user = MdlUser.objects.get(email=user.email)
        mdl_grades = MdlQuizGrades.objects.filter(userid=mdl_user.id).values('quiz', 'grade')

        # In JRS DB, we are mapping Job requirements with foss id, so it is necessary to map quiz data to foss data
        quiz_ids = [x['quiz'] for x in mdl_grades]
        quiz_foss = FossMdlCourses.objects.filter(mdlquiz_id__in=quiz_ids).values('mdlquiz_id', 'foss__id')
        quiz_foss_map = {}
        for item in quiz_foss:
            quiz_foss_map[item['mdlquiz_id']] = item['foss__id']
        
        # Construct a map of FOSS IDs and corresponding grades
        student_scores = {}
        for item in mdl_grades:
            quiz = item['quiz']
            grade = item['grade']
            fosses = FossMdlCourses.objects.filter(mdlquiz_id=quiz).values_list('foss_id', flat=True) # this is required because 1 mdlquiz can have 2 similar foss mapped
            for foss in fosses:
                try:
                    student_scores[foss] = grade
                except Exception as e:
                    print(e)
        
        # Get list of job IDs already applied for
        applied_jobs = [x.job_detail_id for x in self.get_appiled_jobs()]

        # Filter jobs that the user is qualified for and has not applied to yet
        recommended_jobs = []
        for job in available_jobs:
            if job.id in applied_jobs:
                continue
            if self.is_qualified_for_job(student_scores, job):
                recommended_jobs.append(job)
        return recommended_jobs
    
    class Meta:
        ordering = ('-date_created', '-date_updated')

    

class Company(models.Model):
    STATUS_CHOICES = [
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    name = models.CharField(max_length=200, unique=True,verbose_name="Company Name")
    website = models.URLField(null=True,blank=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    emp_name = models.CharField(max_length=200,verbose_name="Company HR Representative Name") #Name of the company representative
    email = models.EmailField(null=True,blank=True) #Email for correspondence
    emp_contact = models.CharField(validators=[phone_regex], max_length=17,verbose_name="Phone Number")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    # address = models.ForeignKey(Location, on_delete=models.CASCADE)
    # state_c = models.IntegerField(null=True,verbose_name='State (Company Headquarters)',blank=True)
    # city_c = models.IntegerField(null=True,verbose_name='City (Company Headquarters)',blank=True)    
    # address = models.CharField(max_length=250) #Company Address for correspondence
    # state_c = models.ForeignKey(SpokenState,on_delete=models.CASCADE,null=True,blank=True) #Company Address for correspondence
    # city_c = models.ForeignKey(SpokenCity,on_delete=models.CASCADE,null=True,blank=True) #Company Address for correspondence
    logo = models.ImageField(upload_to='logo/',null=True,blank=True)
    description = models.TextField(null=True,blank=True,verbose_name="Description about the company")
    # domain = models.ForeignKey(Domain,on_delete=models.CASCADE) 
    domain = models.ManyToManyField(Domain,blank=True,related_name='domains',null=True) #Domain of work Eg. Consultancy, Development, Software etc
    company_size = models.CharField(max_length=25,choices=NUM_OF_EMPS,default=DEFAULT_NUM_EMP) #Number of employees in company
    # status = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    agency = models.ForeignKey('self',null=True,on_delete=models.SET_NULL, blank=True,related_name='client_companies')
    is_agency = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True )

    class Meta:
        ordering = [('-date_updated')]
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            obj = Company.objects.get(name=self.name,date_created=self.date_created)
            obj.slug = slugify(obj.id) 
            obj.save()

    # def get_jobs_count(self):
    #     return Job.objects.filter(company=self).count()

class Foss(models.Model):
    foss = models.IntegerField(null=True,blank=True)  #spk foss id
    mdl_course = models.IntegerField(null=True,blank=True)  #mdlcourse id
    mdl_quiz = models.IntegerField(null=True,blank=True)  #mdl quiz id

    def __str__(self):
        return self.foss
    
from django.db.models import Count, Prefetch
class JobDetailManager(models.Manager):
    def with_applicants_count(self):
        data = self.get_queryset().select_related('company').annotate(applicants=Count('jobshortlist'))
        return data
    
class JobDetail(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('pending_approval', 'pending approval'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('deleted', 'Deleted'),
        ('rejected', 'rejected'),
    ]
    designation = models.CharField(max_length=250,verbose_name='Designation (Job Position)') 
    company=models.ForeignKey(Company,null=True,on_delete=models.CASCADE)
    state_job = models.ForeignKey(State, on_delete=models.CASCADE, null=True,blank=True)
    city_job = models.ForeignKey(City, on_delete=models.CASCADE, null=True,blank=True)
    # skills = models.ManyToManyField(Skill, related_name='jobs')
    skills = models.ManyToManyField(Skill, related_name='jobs', null=True, blank=True)
    
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,verbose_name='Job Sector', null=True) #Domain od work Eg. Consultancy, Development, Software etc
    salary_range_min = models.IntegerField(null=True,blank=True,verbose_name='Annual Salary (Minimum)')
    salary_range_max = models.IntegerField(null=True,blank=True,verbose_name='Annual Salary (Maximum)')
    
    job_type = models.ForeignKey(JobType,on_delete=models.CASCADE, null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    description = RichTextField(null=True,blank=True,verbose_name="Job Description")
    requirements = RichTextField(null=True,blank=True,verbose_name="Qualifications/Skills Required") #Educational qualifications, other criteria
    key_job_responsibilities = RichTextField(null=True,blank=True,verbose_name="Key Job Responsibilities")
    shift_time = models.CharField(max_length=200,blank=True, null=True)
    gender = models.CharField(max_length=10,choices=GENDER,default='a')
    # last_app_date = models.DateTimeField(verbose_name="Last Application Date", null=True,blank=True)
    last_application_date = models.DateField(null=True,blank=True)
    num_vacancies = models.IntegerField(default=1,blank=True, null=True)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    degree = models.ManyToManyField(Degree,blank=True,related_name='degrees', null=True)
    discipline = models.ManyToManyField(Discipline,blank=True,related_name='disciplines', null=True)
    # job_foss = models.ManyToManyField(Foss,null=True,blank=True,related_name='fosses')
    date_created = models.DateTimeField(auto_now_add=True,null = True, blank = True)
    date_updated = models.DateTimeField(auto_now=True,null = True, blank = True )
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    objects = JobDetailManager()
    def __str__(self):
        return self.designation
    #Final
    @classmethod
    def get_active_jobs(cls):
        jobs = cls.objects.filter(status='published', last_application_date__gte=datetime.date.today())
        return jobs
    
    # @property
    # def total_applicants(self):
    #     return JobShortlist.objects.filter(job_detail_id=self.id).count()
    
    class Meta:
        ordering = ['-date_updated']

class StudentFilterLocation(models.Model):
    job = models.ForeignKey(JobDetail, related_name='location', on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null = True, blank = True)
    date_updated = models.DateTimeField(auto_now=True,null = True, blank = True )

    class Meta:
        unique_together = ('job', 'city')

class StudentFilterFoss(models.Model):
    CHOICES = (
        ('Mandatory', 'Mandatory'),
        ('Optional', 'Optional'),
    )
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    foss = models.ForeignKey(FossCategory,on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=CHOICES, default='Mandatory')
    status = models.BooleanField(default=True)
    grade = models.IntegerField(null=True,blank=True, default=60)
    date_created = models.DateTimeField(auto_now_add=True,null = True, blank = True)
    date_updated = models.DateTimeField(auto_now=True,null = True, blank = True )

    def __str__(self):
        return str(self.job)+'-'+str(self.foss)
    
    class Meta:
        unique_together = ('job', 'foss',)

class StudentFilterYear(models.Model):
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    year = models.IntegerField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.job)+'-'+str(self.year)
    
    class Meta:
        unique_together = ('job', 'year',) 
    
class StudentFilterInstituteType(models.Model):
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    insti_type = models.ForeignKey(InstituteType, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class Job(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('pending_approval', 'pending approval'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=250,verbose_name="Title of the job page") #filter
    designation = models.CharField(max_length=250,verbose_name='Designation (Job Position)') 
    state_job = models.IntegerField(null=True,blank=False)  
    #state_job = models.ForeignKey(SpokenState,on_delete=models.CASCADE,null=True,blank=True) #Company Address for correspondence
    # city_job = models.IntegerField(null=True,blank=False)  
    city_job = models.ManyToManyField(City,related_name='jobs1')
    #city_job = models.ForeignKey(SpokenCity,on_delete=models.CASCADE,null=True,blank=True) #Company Address for correspondence
    skills = models.ManyToManyField(Skill, related_name='jobs1')
    description = RichTextField(null=True,blank=True,verbose_name="Job Description")
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,verbose_name='Job Sector', null=True) #Domain od work Eg. Consultancy, Development, Software etc
    salary_range_min = models.IntegerField(null=True,blank=True,verbose_name='Annual Salary (Minimum)')
    salary_range_max = models.IntegerField(null=True,blank=True,verbose_name='Annual Salary (Maximum)')
    date_created = models.DateTimeField(auto_now_add=True,null = True, blank = True)
    date_updated = models.DateTimeField(auto_now=True,null = True, blank = True )
    job_type = models.ForeignKey(JobType,on_delete=models.CASCADE)
    # 0: Job is inactive(added but not visible to students)
    # 1: Job is active(added & available to students for apply)
    # 2: Job Application Date is over
    # 3: Job Application is in process with HR & Company
    # 4: Student selected & job closed.
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    requirements = RichTextField(null=True,blank=True,verbose_name="Qualifications/Skills Required") #Educational qualifications, other criteria
    shift_time = models.CharField(max_length=200,blank=True, null=True)
    key_job_responsibilities = RichTextField(null=True,blank=True,verbose_name="Key Job Responsibilities")
    gender = models.CharField(max_length=10,choices=GENDER,default='a')
    company=models.ForeignKey(Company,null=True,on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    last_app_date = models.DateTimeField(verbose_name="Last Application Date", null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True,verbose_name="Visibility")
    foss = models.CharField(max_length=200) #TODO
    # institute_type = models.CharField(max_length=200,null=True,blank=True)
    institute_type = models.CharField(max_length=200,blank=True) #TODO
    # state = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=200,blank=True, null=True)#spk #filter #TODO
    # city = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,blank=True, null=True)#spk #filter #TODO
    grade = models.IntegerField(null=True) #TODO
    activation_status = models.IntegerField(max_length=10,choices=ACTIVATION_STATUS,blank=True,null=True) #TODO
    from_date = models.DateField(null=True,blank=True,verbose_name='Test Date From') #TODO
    to_date = models.DateField(null=True,blank=True,verbose_name='Test Date Upto') #TODO
    num_vacancies = models.IntegerField(default=1,blank=True, null=True)
    degree = models.ManyToManyField(Degree,blank=True,related_name='degrees1', null=True)
    discipline = models.ManyToManyField(Discipline,blank=True,related_name='disciplines1', null=True)
    job_foss = models.ManyToManyField(Foss,null=True,blank=True,related_name='fosses1')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            obj = Job.objects.get(title=self.title,date_created=self.date_created)
            obj.slug = slugify(obj.id) 
            obj.save()

    def get_applicants_count(self):
        return JobShortlist.objects.filter(job=self).count()

    class Meta:
        ordering = [('-date_updated')]


class JobShortlist(models.Model): #Record is created when a student applies for a job, with status 0.The status changes to 1 when HR further shortlists it.
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    APPLICATION_STATUS = [
        ('Applied', 'Applied'),
        ('Shortlisted By JRS Admin', 'Shortlisted By JRS Admin'),
        ('Rejected By JRS Admin', 'Rejected By JRS Admin'),
        ('Shortlisted By Employer', 'Shortlisted By Employer'),
        ('Rejected By Employer', 'Rejected By Employer'),
        ('Job Offered', 'Job Offered'),
        ('Accepted Offer', 'Accepted Offer'),
        ('Rejected Offer', 'Rejected Offer'),
    ]
    spk_user=models.IntegerField(null=True)  #spk
    student=models.ForeignKey(Student,on_delete=models.CASCADE)  #rec
    job = models.ForeignKey(Job,on_delete=models.CASCADE, null=True, blank=True)
    job_detail = models.ForeignKey(JobDetail,on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True,blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    #0 : student has applied but not yet shortlisted by HR Manager
    #1 : student has applied & shortlisted by HR Manager
    status = models.IntegerField(null=True,blank=True)
    app_status = models.CharField(max_length=100, choices=APPLICATION_STATUS, default='Applied')

    def __str__(self):
        return str(self.spk_user)+'-'+self.job.title


class JobShortlistLog(models.Model):
    job_shortlist_detail = models.ForeignKey(JobShortlist, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    previous_status = models.CharField(max_length=100, choices=JobShortlist.APPLICATION_STATUS)
    status_changed_to = models.CharField(max_length=100, choices=JobShortlist.APPLICATION_STATUS)

class ShortlistEmailStatus(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    email_sequence = models.IntegerField(null=True,blank=True)
    total_mails = models.IntegerField()
    success_mails = models.IntegerField()
    job_id = models.IntegerField()
    log_file = models.CharField(max_length=250)
    message = models.TextField(default="Data is not available. Data is available only for mails sent after 21st Jan, 2023")
    subject = models.CharField(max_length=255,default="Data is not available. Data is available only for mails sent after 21st Jan, 2023")

class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mail_order = models.IntegerField(default=1)
    mail_date = models.DateTimeField(auto_now_add=True)

# landing page models
# class GalleryImage(models.Model):
#     desc = models.TextField(null=True,blank=True,verbose_name='Description about image')
#     location = models.FileField(upload_to=settings.GALLERY_IMAGES)    #spk
#     display_on_homepage = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#     slug = models.SlugField(blank=True, unique=True)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.desc
    
#     def get_absolute_url(self):
#         # return reverse('gallery-image-detail', kwargs={'pk': self.pk})
#         return reverse('add_image')

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if not self.slug:
#             obj = GalleryImage.objects.get(location=self.location,date_created=self.date_created,desc=self.desc)
#             obj.slug = slugify(obj.id) 
#             obj.save()


# class Testimonial(models.Model):
#     name = models.CharField(max_length=250) #name of the person giving testimonial
#     about = models.CharField(max_length=250,null=True,blank=True,verbose_name='About attestant') # about person givingn testimonial
#     desc = models.TextField(null=True,blank=True,verbose_name='Text Testimonial (If any)') #text testimonial
#     location = models.FileField(upload_to=settings.GALLERY_TESTIMONIAL, null=True, blank=True)    #spk
#     display_on_homepage = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#     # slug = models.SlugField(blank=True, unique=True)
#     active = models.BooleanField(default=True)
    

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         # return reverse('gallery-image-detail', kwargs={'pk': self.pk})
#         return reverse('add_testimonial')

class Feedback(models.Model):
    name = models.CharField(max_length=250,verbose_name='Your Name')
    email = models.EmailField(null=True,blank=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class JobFoss(models.Model):
    CHOICES = (
        ('Mandatory', 'Mandatory'),
        ('Optional', 'Optional'),
    )
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    foss = models.ForeignKey(FossCategory,on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=CHOICES, default='Mandatory')
    status = models.BooleanField(default=True)
    grade = models.IntegerField(null=True,blank=True, default=60)

    def __str__(self):
        return str(self.job)+'-'+str(self.foss)
    
    class Meta:
        unique_together = ('job', 'foss',)
    
class JobGraduatingYear(models.Model):
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    year = models.IntegerField(null=True,blank=True)

    class Meta:
        ordering = ['year']
    def __str__(self):
        return str(self.job)+'-'+str(self.year)
    
class CompanyManagers(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company)+'-'+str(self.user)
    
class JobFilterState(models.Model):
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.job)+'-'+str(self.state)
    
class JobFilterCity(models.Model):
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.job)+'-'+str(self.city)
    
# class JobFilterDegree(models.Model):
#     job = models.ForeignKey(Job,on_delete=models.CASCADE)
#     degree = models.ForeignKey(Degree,on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.job)+'-'+str(self.degree)
    
# class JobFilterDiscipline(models.Model):
#     job = models.ForeignKey(Job,on_delete=models.CASCADE)
#     discipline = models.ForeignKey(Discipline,on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.job)+'-'+str(self.discipline)
    
class JobFilterYear(models.Model):
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    year = models.IntegerField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.job)+'-'+str(self.year)
    

class JobFilterLocation(models.Model):
    job = models.ForeignKey(JobDetail,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job} - {self.state} = {self.city}"