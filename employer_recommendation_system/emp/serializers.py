from rest_framework import serializers
from events.models import Event
from spoken.models import SpokenState, SpokenCity,Profile, SpokenStudent, StudentBatch, StudentMaster, TestAttendance
from accounts.serializers import UserSerializer
from datetime import datetime
from .mixins import DateFormatterMixin
from django.db.models import Max, Prefetch, Count
from django.shortcuts import get_object_or_404
from .models import *
from utilities.serializers import LocationSerializer
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from accounts.serializers import UserRegSerializer
from django.core.files.storage import FileSystemStorage

class CompanyManagerSerializer1(serializers.ModelSerializer):
        user = UserSerializer()
        class Meta:
            model = CompanyManagers
            fields = ['id', 'user', 'company', 'phone']

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['jobtype']


class CompanySerializer1(serializers.ModelSerializer):
    managers = serializers.SerializerMethodField()
    domain = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ['id', 'name','date_created', 'is_agency', 'domain','managers']

    def get_managers(self, obj):
         managers = obj.companymanagers_set.all()
         manager_data = []
         for manager in managers:
             phone=''
             if hasattr(manager.user, 'user_profile'): 
                phone = manager.user.user_profile[0].phone if manager.user.user_profile else None
             manager_data.append({'name': manager.user.first_name, 'email': manager.user.email, 'phone': phone})
         return manager_data
    
    def get_domain(self, obj):
        return [domain.name for domain in obj.domain.all()]

class CustomDegreeField(serializers.StringRelatedField):
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        return get_object_or_404(Degree, id=data)
    
class CustomDisciplineField(serializers.StringRelatedField):
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        return get_object_or_404(Discipline, id=data)

class JobSerializer(serializers.ModelSerializer, DateFormatterMixin):
    job_state = serializers.SerializerMethodField()
    city_state = serializers.SerializerMethodField()
    domain = DomainSerializer()
    job_type = JobTypeSerializer()
    company = serializers.CharField(source='company.name')
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    last_app_date = serializers.SerializerMethodField()
    degree = CustomDegreeField(many=True)
    # discipline = serializers.SerializerMethodField()
    class Meta:
        model = Job
        fields = '__all__'
        fields = ['id', 'designation', 'job_state', 'city_state', 'salary_range_min', 'salary_range_max', 'created',
                  'updated', 'requirements',  'key_job_responsibilities', 'last_app_date', 'num_vacancies',
                   'domain', 'job_type', 'company', 'skills', 'degree', 'discipline', 'get_applicants_count' ]
        date_fields = ['last_app_date']
        
    def get_job_state(self, obj):
        try:
            return SpokenState.objects.get(id=obj.state_job).name
        except:
            return None
    
    def get_city_state(self, obj):
        try:
            return SpokenCity.objects.get(id=obj.city_job).name
        except:
            return None
    
    def get_created(self, obj):
        return datetime.strftime(obj.date_created, "%d %B %Y %H:%M:%S")
    
    def get_updated(self, obj):
        return datetime.strftime(obj.date_updated, "%d %B %Y %H:%M:%S")
    
    def get_last_app_date(self, obj):
        return datetime.strftime(obj.last_app_date, "%d %B %Y") if obj.last_app_date else None
        

#################################### Serializers V2 ####################################
from django.contrib.auth.models import User
from accounts.serializers import ProfileSerializer
from accounts.models import Profile as JRSProfile
from django.db import transaction, IntegrityError
from utilities.models import State, City

#--------------------------------------Common--------------------------------------------------
class DateFormatterMixin:
    """
    Mixin for formatting date fields in a model. To use this mixin, you need to define
    a list of date field names in the Meta class of your serializer. The mixin will
    automatically create formatted versions of these date fields.

    Example:
    class YourSerializer(DateFormatterMixin, serializers.ModelSerializer):
        class Meta:
            model = YourModel
            fields = ['field1', 'field2', '...']
            date_fields = ['start_date', 'end_date']  # List of date fields to be formatted

    This will add 'formatted_start_date' and 'formatted_end_date' to your serializer
    with the dates formatted as 'dd MMM YYYY'.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.date_fields:
            formatted_field = f'formatted_{field}'
            method_name = f'get_{formatted_field}'
            self.fields[formatted_field] = serializers.SerializerMethodField(method_name=f'{method_name}')
            setattr(self, method_name, self.create_date_formatter(field))


    def create_date_formatter(self, field):
        def _date_formatter(obj):
            date = getattr(obj, field, None)
            return date.strftime('%d %b %Y ') if date else None
        return _date_formatter


class FormattedDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        if value is not None:
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return None
#--------------------------------------Misc--------------------------------------------------
class EventSerializer(DateFormatterMixin, serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','name', 'type', 'status', 'description']
        date_fields = ['start_date', 'end_date']

#--------------------------------------Student--------------------------------------------------  
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['url', 'desc']

class CustomSkillField(serializers.StringRelatedField):
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        return get_object_or_404(Skill, id=data)

class StudentDetailSerializer(DateFormatterMixin, serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    contact = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)
    test_details = serializers.SerializerMethodField(read_only=True)
    skills = CustomSkillField(many=True)
    projects = ProjectSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        student_master = StudentMaster.objects.filter(student_id=instance.spk_student_id).select_related('batch', 'batch__academic',
                                                                                                     'batch__academic__state', 'batch__academic__city').first()
        if student_master:
            data['institute'] = student_master.batch.academic.institution_name
            data['state'] = student_master.batch.academic.state.name
            data['city'] = student_master.batch.academic.city.name
        else:
            data['institute'] = None
            data['state'] = None
            data['city'] = None
        return data
    
    def update(self, instance, validated_data):
        projects_data = validated_data.pop('projects', [])
        instance = super().update(instance, validated_data)
        instance.projects.clear()
        for project_data in projects_data:
            project, created = Project.objects.get_or_create(**project_data)
            instance.projects.add(project)
        instance.save()
        return instance
    
    class Meta:
        model = Student
        fields = ['name', 'address', 'email', 'alternate_email','contact', 'gender',  'test_details', 'skills',
                  'about', 'projects', 'github', 'linkedin', 'resume', 'date_created', 'date_updated', 'certifications',
                   'notified_date', 'profile_update_date', 'joining_immediate', 'avail_for_intern',
                    'willing_to_relocate', 'phone', 'state', 'city']
        date_fields = ['date_created', 'date_updated', 'notified_date', 'profile_update_date']

    def get_profile(self, obj):
        return Profile.objects.filter(user_id=obj.spk_usr_id).first()

    def get_address(self, obj):
        profile = self.get_profile(obj)
        return profile.address if profile else None
        
    def get_contact(self, obj):
        profile = self.get_profile(obj)
        return profile.phone if profile else None
    
    def get_gender(self, obj):
        spoken_student = SpokenStudent.objects.filter(user_id=obj.spk_usr_id).first()
        return spoken_student.gender if spoken_student else None
    
    def get_test_details(self, obj):
        ta = TestAttendance.objects.filter(student_id=obj.spk_student_id).values('test__foss__foss').annotate(
            grade=Max('mdlgrade'), test_date=Max('test__tdate')
        )
        formatted_ta = []
        for item in ta:
            formatted_ta.append({
                'foss': item['test__foss__foss'],
                'grade': item['grade'],
                'test_date': item['test_date'].strftime('%d %b %Y ')
            })
        return formatted_ta
    

class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    contact = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'contact']

    def get_profile(self, obj):
        return Profile.objects.filter(user_id=obj.spk_usr_id).first()
    
    def get_contact(self, obj):
        profile = self.get_profile(obj)
        return profile.phone if profile else None

#Final
class StudentProfileSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    education_details  = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['about', 'joining_immediate', 'avail_for_intern', 'willing_to_relocate',
                   'skills', 'certifications', 'resume',
                   'projects', 'education_details' ]
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(f"\033[92m 1 \033[0m")
        groups = user.groups.all().values_list('name', flat=True)
        print(f"\033[92m 2 \033[0m")
        if 'STUDENT' in groups or 'MANAGER' in groups:
            print(f"\033[91m 10 \033[0m")
            self.fields['name'] = serializers.SerializerMethodField()
            self.fields['email'] = serializers.SerializerMethodField()
            self.Meta.fields = ['name', 'email', 'phone', 'address', 'alternate_email',
                  'about', 'joining_immediate', 'avail_for_intern', 'willing_to_relocate',
                   'skills', 'certifications', 'linkedin' , 'github', 'resume',
                   'projects', 'education_details' ]
        print(f"\033[92m 3 \033[0m")
        super().__init__(*args, **kwargs)
    
    def get_name(self, obj):
        print(f"\033[92m 4 \033[0m")
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else None
    
    def get_email(self, obj):
        print(f"\033[92m 5 \033[0m")
        return f"{obj.user.email}" if obj.user else None
    
    def get_education_details(self, obj):
        try:
            student_master = StudentMaster.objects.select_related('batch').select_related(
                'batch__academic').select_related(
                'batch__department').get(student_id = obj.spk_student_id)
            batch = student_master.batch
            return {
                "academic" : batch.academic.institution_name,
                "department" : batch.department.name
            }
        except StudentMaster.DoesNotExist:
            return None
        
    def update(self, instance, validated_data):
        projects_data = validated_data.pop('projects', None)
        if projects_data is not None:
            instance.projects.clear()
            for project_data in projects_data:
                project = Project.objects.create(**project_data)
                instance.projects.add(project)
        instance = super().update(instance, validated_data)
        return instance


class StudentDashboardJobSerializier(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name')
    class Meta:
        model = JobDetail
        fields = ['id','designation', 'company_name']

#Final
class StudentAppliedJobSerializer(serializers.ModelSerializer):
    job_detail = StudentDashboardJobSerializier()
    applied_on_date = serializers.SerializerMethodField()
    class Meta:
        model = JobShortlist
        fields = ['job_detail', 'app_status', 'applied_on_date' ]

    def get_applied_on_date(self, obj):
        return obj.date_created.strftime('%d-%B-%Y')

class StudentRecommendedJobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name')
    formatted_last_app_date = serializers.SerializerMethodField()
    job_type = serializers.CharField(source='job_type.jobtype')
    class Meta:
        model = JobDetail
        fields = ['id', 'company_name', 'designation', 'description', 'last_application_date', 'job_type', 'formatted_last_app_date' ]

    def get_formatted_last_app_date(self, obj):
        if obj.last_application_date:
            return obj.last_application_date.strftime('%d-%B-%Y')
        return None

#--------------------------------------Job--------------------------------------------------
class JobFossSerializer(serializers.Serializer):   
    class Meta:
        model = JobFoss
        fields = ['job', 'foss', 'type', 'grade']
        read_only_fields = ['job']  # Define read-only fields here

class JobRegistrationSerializer(serializers.ModelSerializer):
    jobfoss = JobFossSerializer(many=True, required=False)
    
    class Meta:
        model = JobDetail
        fields = ['designation', 'company', 'state_job','city_job','skills','domain', 'salary_range_min',
                  'salary_range_max', 'job_type', 'description' , 'requirements', 'key_job_responsibilities','gender',
                     'last_app_date', 'num_vacancies','degree','discipline', "jobfoss" ]

    def to_internal_value(self, data):
        mappings = {
            'state_job': State,
            'city_job': City,
            'job_type': JobType,
            'domain': Domain,
        }

        for field, modelClass in mappings.items():
            value = data.get(field)
            if isinstance(value, modelClass):
                data[field] = value.id

        for field in ['skills', 'degree', 'discipline']:
            value = data.get(field)
            if value:
                try:
                    data[field] = [x.id for x in value]
                except Exception as e:
                    print(e)
        return super().to_internal_value(data)  
        
class JobDetailListSerializer(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()
    last_application_date = serializers.SerializerMethodField()
    total_applicants = serializers.IntegerField()

    
    def get_date_created(self, obj):
        return obj.date_created.strftime("%d %B %Y")
    
    def get_last_application_date(self, obj):
        return obj.last_application_date.strftime("%d %B %Y ")
    
    class Meta:
        model = JobDetail
        # fields = ['id', 'designation', 'date_created', 'last_application_date', 'applicants_count', 'company', 'status']
        fields = ['id', 'designation', 'date_created', 'last_application_date', 'status', 'total_applicants']

class JobDetailCreateSerializer2(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = ['id', 'designation', 'date_created', 'last_application_date', 'status', 'total_applicants']
    

class StudentFilterYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFilterYear
        fields = ['job', 'year']

class JobDetailSerializer1(serializers.ModelSerializer):
    date_created = FormattedDateTimeField()
    date_updated = FormattedDateTimeField()
    filter_year = serializers.SerializerMethodField()
    mandatory_foss = serializers.SerializerMethodField()
    optional_foss = serializers.SerializerMethodField()
    filter_location = serializers.SerializerMethodField()

    filter_year_w = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    mandatory_foss_w = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)
    optional_foss_w = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    filter_location_w = serializers.ListField(child=serializers.DictField(child=serializers.IntegerField()), write_only=True, required=False)
    class Meta:
        model = JobDetail
        fields = ['designation', 'state_job', 'city_job', 'skills', 'domain', 'salary_range_min',
                    'salary_range_max', 'job_type', 'status', 'description', 
                    'requirements', 'key_job_responsibilities', 'gender',
                    'last_app_date', 'num_vacancies', 'degree', 'discipline', 'date_created',
                    'date_updated', 'filter_year', 'mandatory_foss', 'optional_foss', 'filter_location',
                    'filter_year_w', 'mandatory_foss_w', 'optional_foss_w', 'filter_location_w' ]
    
    def get_filter_year(self, obj):
        return StudentFilterYear.objects.filter(job=obj).values_list('year', flat=True)
    
    def get_mandatory_foss(self, obj):
        return StudentFilterFoss.objects.filter(job=obj, type="Mandatory").values_list('foss', flat=True)
    
    def get_optional_foss(self, obj):
        return StudentFilterFoss.objects.filter(job=obj, type="Optional").values_list('foss', flat=True)
    
    def get_filter_location(self, obj):
        return StudentFilterLocation.objects.filter(job=obj).values('state','city')
    
    def update_student_filter_year(self, instance, filter_year):
        try:
                existing_years = StudentFilterYear.objects.filter(job=instance)
                for item in existing_years:
                    if item.year not in filter_year:
                        item.delete()
                    else:
                        filter_year.remove(item.year)
                year_data = [StudentFilterYear(job=instance, year=year) for year in filter_year]
                StudentFilterYear.objects.bulk_create(year_data)
        except IntegrityError:
            pass
    
    def update_student_filter_foss(self, instance, foss_list, foss_type):
        try:
            data = StudentFilterFoss.objects.filter(job=instance, type=foss_type)
            for item in data:
                if item.foss not in foss_list:
                    item.delete()
                else:
                    foss_list.remove(item.foss)
            fosses_data = [StudentFilterFoss(job=instance, foss_id=foss, type=foss_type) for foss in foss_list]
            StudentFilterFoss.objects.bulk_create(fosses_data)
        except IntegrityError as e:
            pass

    def update_student_filter_location(self, instance, filter_location):
        city_list = [location['city'] for location in filter_location]
        existing_locations = StudentFilterLocation.objects.filter(job=instance)
        for item in existing_locations:
            if item.city not in  city_list:
                item.delete()
            else:
                for data in filter_location:
                    if data.city ==  item.city:
                        filter_location.pop(data)
        
        filter_location_data = [
            StudentFilterLocation(job=instance, state_id=loc.get('state'), city_id=loc.get('city', None)) 
            if loc.get('city') != 0 else 
            StudentFilterLocation(job=instance, state_id=loc.get('state'), city=None)
            for loc in filter_location
        ]
        for item in filter_location_data:
            try:
                item.save()
            except:
                pass
        # StudentFilterLocation.objects.bulk_create(filter_location_data)
        
        
        
    
    def update_student_filter(self, instance, validated_data):
        filter_year = validated_data.pop('filter_year_w', [])
        mandatory_foss = validated_data.pop('mandatory_foss_w', [])
        optional_foss = validated_data.pop('optional_foss_w', [])
        filter_location = validated_data.pop('filter_location_w', [])
        
        try:
            if filter_year:
                year_data = [StudentFilterYear(job=instance, year=year) for year in filter_year]
                StudentFilterYear.objects.bulk_create(year_data)
        except IntegrityError:
            pass
        try:
            if mandatory_foss:
                mandatory_fosses_data = [StudentFilterFoss(job=instance, foss_id=foss, type='Mandatory') for foss in mandatory_foss]
                StudentFilterFoss.objects.bulk_create(mandatory_fosses_data)
        except IntegrityError:
            pass
        try:
            if optional_foss:
                data = StudentFilterFoss.objects.filter(job=instance)
                for item in data:
                    if item.foss not in optional_foss:
                        item.delete()
                    else:
                        optional_foss.remove(item.foss)
                optional_fosses_data = [StudentFilterFoss(job=instance, foss_id=foss, type='Optional') for foss in optional_foss]
                StudentFilterFoss.objects.bulk_create(optional_fosses_data)
        except IntegrityError:
            pass
        try:
            if filter_location:
                filter_location_data = [
                    StudentFilterLocation(job=instance, state_id=loc.get('state'), city_id=loc.get('city', None)) 
                    if loc.get('city') != 0 else 
                    StudentFilterLocation(job=instance, state_id=loc.get('state'), city=None)
                    for loc in filter_location
                ]
                StudentFilterLocation.objects.bulk_create(filter_location_data)
        except IntegrityError:
            pass

    def update(self, instance, validated_data):
        keys = list(validated_data.keys())
        filter_year = validated_data.pop('filter_year_w', [])
        mandatory_foss = validated_data.pop('mandatory_foss_w', [])
        optional_foss = validated_data.pop('optional_foss_w', [])
        filter_location = validated_data.pop('filter_location_w', [])

        instance = super().update(instance, validated_data)
        
        if "filter_year_w" in keys:
            self.update_student_filter_year(instance, filter_year)
        if "mandatory_foss_w" in keys:
            self.update_student_filter_foss(instance, mandatory_foss, "Mandatory")
        if "optional_foss_w" in keys:
            self.update_student_filter_foss(instance, optional_foss, "Optional")
        if "filter_location_w" in keys:
            self.update_student_filter_location(instance, filter_location)
        return instance

#Final
class JobDetailSerializer(serializers.ModelSerializer):
    filter_year = serializers.SerializerMethodField()
    filter_mandatory_skills = serializers.SerializerMethodField()
    filter_optional_skills = serializers.SerializerMethodField()
    filter_location = serializers.SerializerMethodField()
    filter_cities = serializers.SerializerMethodField()
    filter_states = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()
    date_updated = serializers.SerializerMethodField()
    # last_application_date = serializers.SerializerMethodField()
    last_app_date = serializers.SerializerMethodField()
    total_applicants = serializers.IntegerField(read_only=True)  # annotated field
    class Meta:
        model = JobDetail
        fields = '__all__'

    def get_filter_year(self, obj):
        # print(f"\033[97m INSIDE  get_filter_year\033[0m")
        return JobFilterYear.objects.filter(job=obj).values_list('year', flat=True)
    
    def get_filter_mandatory_skills(self, obj):
        return JobFoss.objects.filter(job=obj, type="Mandatory").values_list('foss_id', flat=True)
    
    def get_filter_optional_skills(self, obj):
        return JobFoss.objects.filter(job=obj, type="Optional").values_list('foss_id', flat=True)
    
    def get_filter_location(self, obj):
        return JobFilterLocation.objects.filter(job=obj).values('city_id', 'state_id')
    
    def get_filter_states(self, obj):
        return JobFilterLocation.objects.filter(job=obj, city__isnull=True).values_list('state_id', flat=True)
    
    def get_filter_cities(self, obj):
        return JobFilterLocation.objects.filter(job=obj, city__isnull=False).values_list('city_id', flat=True)

    def get_date_created(self, obj):
        return obj.date_created.strftime('%d %b %Y ') 

    def get_date_updated(self, obj):
        return obj.date_updated.strftime('%d %b %Y ') 
    
    def get_last_app_date(self, obj):
        return obj.last_application_date.strftime('%d %b %Y ') 

#Final
class JobDetailCreateSerializer(serializers.ModelSerializer):
    # Field for all filters which will be used to filter students for a particular job
    filters = serializers.DictField(child=serializers.ListField(child=serializers.IntegerField()), required=False)
    state_job = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), required=False)
    city_job = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False)

    class Meta:
        model = JobDetail
        exclude = ['date_created', 'date_updated']
        

    def to_internal_value(self, data):
        print(f"\033[97m To internale Value : ********* \033[0m")
        print(f"\033[93m data from to_internal_value: {data} \033[0m")
        internal_value = super().to_internal_value(data)
        if 'state_job' in data:
        #     # internal_value['state_job'] = data.get('state_job').id
            internal_value['state_job'] = data.get('state_job')
        if 'city_job' in data:
        #     # internal_value['state_job'] = data.get('state_job').id
            internal_value['city_job'] = data.get('city_job')

        return internal_value

    def validate(self, data):
        print(f"\033[97m data : from validate \033[0m")
        print(f"\033[97m data from validate: {data} \033[0m")
        # Validation for salary range

        if data.get('salary_range_min') and data.get('salary_range_max', 0):
            if data.get('salary_range_min') > data.get('salary_range_max'):
                raise serializers.ValidationError("Minimum salary must be less than maximum salary value")
        # Validation for last application date
        if (data.get('last_application_date', None) and data.get('last_application_date') < datetime.date.today()):
                raise serializers.ValidationError("Last Application date should be greater than toady")
        status = data.get('status', 'draft')
        # if status == 'draft':
        #     return data
        # else:
        #     for field in self.REQUIRED_FIELDS:
        #         if not data.get(field):
        #             raise serializers.ValidationError('Please fill all the fields to submit the job application.')
        state = data.get('state_job', None)
        city = data.get('city_job', None)
        print(f"\033[95m state ****** {state} \033[0m")
        print(f"\033[95m city ****** {city} \033[0m")
        # if state:
        #     data['state_job'] = state
        # if city:
        #     data['city_job'] = city
        # print(f"\033[97m  state : {data.get('state_job')} \033[0m")
        # print(f"\033[97m type state : {type(data.get('state_job'))} \033[0m")

        return data
    
    def create(self, validated_data):
        filters = validated_data.pop('filters', {})
        try:
            with transaction.atomic():
                print(f"\033[97m validated_data from create job: {validated_data} \033[0m")
                print(f"\033[92m ******* This \033[0m")
                state_job = validated_data.pop('state_job', None)
                city_job = validated_data.pop('city_job', None)

                instance = super().create(validated_data)
                if state_job:
                    instance.state_job_id = state_job

                if city_job:
                    instance.city_job_id = city_job
                if state_job or city_job:
                    instance.save()
                print(f"\033[93m 1 ***** \033[0m")
                self.create_filter_years(instance, filters.get('filter_year', []))
                print(f"\033[93m 2 ***** \033[0m")
                self.create_fosses(instance, filters.get('filter_mandatory_skills', []), type="Mandatory")
                print(f"\033[93m 3 ***** \033[0m")
                self.create_fosses(instance, filters.get('filter_optional_skills', []), type="Optional")
                print(f"\033[93m 4 ***** \033[0m")
                # self.create_locations(instance, filters.get('city', []), filters.get('state', []))
                self.update_city(instance, filters.get('filter_cities', []))
                self.update_state(instance, filters.get('filter_states', []))
                return instance
        except Exception as e:
            print(f"\033[91m Exceptionfrom job create  {e} \033[0m")
            return None
        
    def update(self, instance, validated_data):
        filters = validated_data.pop('filters', {})
        print(f"\033[93m filters : {filters} \033[0m")
        try:
            if "filter_year" in filters:
                self.update_filter_years(instance, filters.get('filter_year', []))
            if "filter_mandatory_skills" in filters:
                self.update_fosses(instance, filters.get('filter_mandatory_skills', []), type="Mandatory")
            if "filter_optional_skills" in filters:
                self.update_fosses(instance, filters.get('filter_optional_skills', []), type="Optional")
            if "filter_cities" in filters:
                print(f"\033[92m City in filter \033[0m")
                self.update_city(instance, filters.get('filter_cities', []))
            if "filter_states" in filters:
                print(f"\033[92m State in filter \033[0m")
                self.update_state(instance, filters.get('filter_states', []))
            
            instance = super().update(instance, validated_data)
            return instance
        except Exception as e:
            print(f"\033[91m e : {e} \033[0m")
            return instance
        
    # Helper method to create filter years
    def create_filter_years(self, job_detail, years):
        year_data = [JobFilterYear(job=job_detail, year=year) for year in years]
        JobFilterYear.objects.bulk_create(year_data)

    # Helper method to create fosses (skills)
    def create_fosses(self, job_detail, fosses, type):
        foss_data = [JobFoss(job=job_detail, foss_id=foss, type=type) for foss in fosses]
        JobFoss.objects.bulk_create(foss_data)

    # Helper method to create locations
    def create_locations(self, job_detail, cities, states):
        city_ids = City.objects.filter(id__in=cities).values_list('id', 'state_id')
        location_data = [JobFilterLocation(job=job_detail, city_id=id, state_id=state) for id, state in city_ids]
        saved_state_ids = {state_id for _, state_id in city_ids}
        for state in states:
            if state not in saved_state_ids:
                location_data.append(JobFilterLocation(job=job_detail, state_id=state))
        JobFilterLocation.objects.bulk_create(location_data)

    # Helper method to update filter years
    def update_filter_years(self, job_detail, years):
        JobFilterYear.objects.filter(job=job_detail).delete()
        self.create_filter_years(job_detail, years)

    # Helper method to update fosses (skills)
    def update_fosses(self, job_detail, fosses, type):
        print(f"\033[92m update_fosses: {fosses} \033[0m")
        JobFoss.objects.filter(job=job_detail, type=type).delete()
        self.create_fosses(job_detail, fosses, type)
    
    # Helper method to update locations
    def update_locations(self, job_detail, cities, states):
        JobFilterLocation.objects.filter(job=job_detail).delete()
        self.create_locations(job_detail, cities, states)

    def update_city(self, job_detail, cities):
        print(f"\033[93m updating cities : {cities} \033[0m")
        # Delete existing cities filter locations
        # job_filter_locations_with_city = JobFilterLocation.objects.exclude(job = job_detail,city__isnull=True)
        job_filter_locations_with_city = JobFilterLocation.objects.filter(job = job_detail).exclude(city__isnull=True)
        job_filter_locations_with_city.delete()
        print(f"\033[92m Deleted the cities \033[0m")
        # Delete filter locations having state same as incoming city data state
        new_city_ids = City.objects.filter(id__in=cities).values_list('id', 'state_id')
        new_state_ids = {state_id for _, state_id in new_city_ids}
        job_filter_locations_with_new_state = JobFilterLocation.objects.filter(job = job_detail,state_id__in=new_state_ids)
        job_filter_locations_with_new_state.delete()
        print(f"\033[92m Deleted the states with incoming cities \033[0m")
        # Save new city data
        location_data = [JobFilterLocation(job=job_detail, city_id=id, state_id=state) for id, state in new_city_ids]
        JobFilterLocation.objects.bulk_create(location_data)
        print(f"\033[92m saved the data \033[0m")

    def update_state(self, job_detail, states):
        print(f"\033[93m updating states : {states} \033[0m")
        # Delete existing state filter locations
        job_filter_locations_with_state = JobFilterLocation.objects.filter(Q(job = job_detail) & Q(city__isnull=True))
        job_filter_locations_with_state.delete()

        # Save new state data
        location_data = [JobFilterLocation(job=job_detail, state_id=state) for state in states]
        JobFilterLocation.objects.bulk_create(location_data)
    

class JobDetailCreateSerializer1(serializers.ModelSerializer):
    filter_year = serializers.ListField(child=serializers.IntegerField(), required=False)
    filter_mandatory_skills = serializers.ListField(child=serializers.IntegerField())
    filter_optional_skills = serializers.ListField(child=serializers.IntegerField())
    filter_state = serializers.ListField(child=serializers.IntegerField(), required=False)
    filter_city = serializers.ListField(child=serializers.IntegerField(), required=False)

    REQUIRED_FIELDS = ['designation', 'state_job', 'city_job', 'job_type',
                  'domain', 'salary_range_min', 'salary_range_max',
                'description', 'requirements', 'key_job_responsibilities',
                'last_application_date', 'num_vacancies', 
                'filter_year', 'filter_mandatory_skills', 'filter_optional_skills',
                # 'filter_degree' ,'filter_discipline', #ToDo for degree, discipline
                'filter_state', 'filter_city'
                  ]

    def validate(self, data):
        status = data.get('status', 'draft')
        if status == 'draft':
            return data
        else:
            for field in self.REQUIRED_FIELDS:
                if not data.get(field):
                    raise serializers.ValidationError('Please fill all the fields to submit the job application.')
        return data
    
    class Meta:
        model = JobDetail
        fields = ['designation', 'state_job', 'city_job', 'job_type',
                  'domain', 'salary_range_min', 'salary_range_max',
                'description', 'requirements', 'key_job_responsibilities',
                'last_application_date', 'num_vacancies', 
                'filter_year', 'filter_mandatory_skills', 'filter_optional_skills',
                # 'filter_degree' ,'filter_discipline', #ToDo for degree, discipline
                'filter_state', 'filter_city','status'
                  ]
        extra_kwargs = {
            'designation' : {'required': False}
        }
    def create(self, validated_data):
        try:
            filter_year = validated_data.pop('filter_year', [])
            filter_mandatory_skills = validated_data.pop('filter_mandatory_skills', [])
            filter_optional_skills = validated_data.pop('filter_optional_skills', [])
            # filter_degree = validated_data.pop('filter_degree', [])
            # filter_discipline = validated_data.pop('filter_discipline', [])
            filter_state = validated_data.pop('filter_state', [])
            filter_city = validated_data.pop('filter_city', [])
            
            with transaction.atomic():
                instance = super().create(validated_data)
                year_data = [JobFilterYear(job=instance, year=year) for  year in filter_year]
                JobFilterYear.objects.bulk_create(year_data)
                mandatory_skills_data = [ JobFoss(job=instance, foss_id=foss, type='Mandatory') for foss in filter_mandatory_skills]
                JobFoss.objects.bulk_create(mandatory_skills_data)
                optional_skills_data = [ JobFoss(job=instance, foss_id=foss, type='Optional') for foss in filter_optional_skills]
                JobFoss.objects.bulk_create(optional_skills_data)
                cities = City.objects.filter(id__in=filter_city).values_list('id', 'state_id')
                location_data = [JobFilterLocation(job=instance, city_id=id, state_id=state) for id, state in cities]
                saved_state_ids = [x[1] for x in cities]
                for state in filter_state:
                    if state not in saved_state_ids:
                        location_data.append(JobFilterLocation(job=instance, state_id=state, city=None))
                JobFilterLocation.objects.bulk_create(location_data)
                return instance
        except Exception as e:
            print(e)
        return None

class JobShortlistSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(source='student.phone')
    
    class Meta:
        model = JobShortlist
        fields = ['full_name', 'email', 'phone','job_detail', 'student' ,'date_created','date_updated', 'app_status'  ]
#--------------------------------------Company--------------------------------------------------
class CompanyDataSerializer(serializers.ModelSerializer):
    domain = serializers.SerializerMethodField()
    num_jobs = serializers.IntegerField(read_only=True)
    class Meta:
        model = Company
        fields = ['id', 'name', 'domain', 'logo', 'description', 'num_jobs']

    def get_domain(self, obj):
        return [domain.name for domain in obj.domain.all()]    

class CompanyRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegSerializer(write_only=True)
    job = JobDetailCreateSerializer(write_only=True)
    location = LocationSerializer(write_only=True)
    
    class Meta:
            model = Company
            fields = ['name', 'website', 'description', 'domain' ,'user', 'job', 'location']

    def create_user(self, user_data):
        # user_data['username'] = user_data['email']
        user_serializer = UserRegSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        return user_serializer.save()

    def create_job(self, job_data, company, user):
        print(f"\033[97m inside create job ********** \033[0m")
        job_serializer = JobDetailCreateSerializer(data=job_data)
        print(f"\033[95m Before job_serializer.is_valid ********** \033[0m")
        job_serializer.is_valid(raise_exception=True)
        print(f"\033[95m After job_serializer.is_valid ********** \033[0m")

        job = job_serializer.save()
        print(f"\033[97m saved job ****** \033[0m")
        job.company = company
        job.added_by = user
        job.save()
        return job 
    
    def create_location(self, location_data):
        print(f"\033[93m location_data : {location_data} \033[0m")
        location_serializer = LocationSerializer(data=location_data)
        location_serializer.is_valid(raise_exception=True)
        location = location_serializer.save()
        print(f"\033[97m saved location \033[0m")
        return location


    def create(self, validated_data):
        print(f"\033[92m create of register company \033[0m")
        user_data = validated_data.pop('user', None)
        job_data = validated_data.pop('job', None)
        location_data = validated_data.pop('location', None)
        if user_data and job_data:
            with transaction.atomic():
                print(f"\033[92m in transaction \033[0m")
                user = self.create_user(user_data)
                print(f"\033[92m created user \033[0m")
                validated_data['added_by_id'] = user.id
                location = self.create_location(location_data)
                print(f"\033[92m created location : {location} \033[0m")
                # company = Company.objects.create(**validated_data)
                # validated_data['location_id'] = location.id
                company = super().create(validated_data)
                print(f"\033[92m created company \033[0m")
                cm = CompanyManagers.objects.create(user=user, company=company, group_id=3)
                print(f"\033[92m created company manager \033[0m")
                job = self.create_job(job_data, company, user=user)
                print(f"\033[92m created job \033[0m")
                company.location = location
                company.save()
                print(f"\033[92m saved company location \033[0m")
                return company
    

        # return super().create(validated_data)


class CompanyRegistrationSerializer1(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)
    job = JobRegistrationSerializer(write_only=True)
    filter_year = serializers.ListField(child=serializers.IntegerField(), required=False)
    mandatory_foss = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)
    optional_foss = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    filter_location = serializers.ListField(child=serializers.DictField(child=serializers.IntegerField()), write_only=True, required=False)
    class Meta:
        model = Company
        fields = ['name', 'website', 'is_agency','user','job', 'filter_year', 'mandatory_foss', 'optional_foss', 
                  'filter_location']

    def create_user(self, user_data):
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        return user_serializer.save()
    
    def create_job(self, job_data, company, user):
        job_serializer = JobRegistrationSerializer(data=job_data)
        job_serializer.is_valid(raise_exception=True)
        job = job_serializer.save()
        job.company = company
        job.added_by = user
        job.save()
        return job
    
    def create_filters(self, job, filter_year, mandatory_foss, optional_foss, filter_location):
        if filter_year:
            year_data = [StudentFilterYear(job=job, year=year) for year in filter_year]
            StudentFilterYear.objects.bulk_create(year_data)
        if mandatory_foss:
            mandatory_fosses_data = [StudentFilterFoss(job=job, foss_id=foss, type='Mandatory') for foss in mandatory_foss]
            StudentFilterFoss.objects.bulk_create(mandatory_fosses_data)
        if optional_foss:
            optional_fosses_data = [StudentFilterFoss(job=job, foss_id=foss, type='Optional') for foss in optional_foss]
            StudentFilterFoss.objects.bulk_create(optional_fosses_data)
        if filter_location:
            filter_location_data = [
                StudentFilterLocation(job=job, state_id=loc.get('state'), city_id=loc.get('city', None)) 
                if loc.get('city') != 0 else 
                StudentFilterLocation(job=job, state_id=loc.get('state'), city=None)
                for loc in filter_location
            ]
            StudentFilterLocation.objects.bulk_create(filter_location_data)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        job_data = validated_data.pop('job')
        filter_year = validated_data.pop('filter_year', [])
        mandatory_foss = validated_data.pop('mandatory_foss', [])
        optional_foss = validated_data.pop('optional_foss', [])
        filter_location = validated_data.pop('filter_location', [])

        with transaction.atomic():
            user = self.create_user(user_data)
            validated_data['added_by_id'] = user.id
            company = Company.objects.create(**validated_data)
            cm = CompanyManagers.objects.create(user=user, company=company, group_id=3)
            job = self.create_job(job_data, company, user=user)
            degree = job_data.pop('degree', [])
            discipline = job_data.pop('discipline', [])
            job.degree.set(degree)
            job.discipline.set(discipline)
            self.create_filters(job, filter_year, mandatory_foss, optional_foss, filter_location)
            return company
        
class CompanyUpdateSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Company
        fields = ['name', 'website', 'location', 'description',
                  'domain', 'company_size' ]
        
    def update(self, instance, validated_data):
        location = validated_data.pop('location', None)
        if location : 
            if instance.location:
                location_serializer = LocationSerializer(instance.location,data=location, partial=True )
            else:
                location_serializer = LocationSerializer(data=location )
            location_serializer.is_valid(raise_exception=True)
            location_serializer.save()
        instance = super().update(instance, validated_data)
        return instance
    
#Final
class EmployerUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
        read_only_fields = ['email']

#Final
class EmployerProfileSerializer(serializers.ModelSerializer):
    user = EmployerUserSerializer()
    company = serializers.CharField(source='company.name')
    date_created = serializers.SerializerMethodField()
    class Meta:
        model = CompanyManagers
        fields = ['user', 'company', 'phone', 'date_created']

    def get_date_created(self, obj):
        return obj.date_created.strftime("%d %B %Y")
    
    def update(self, instance, validated_data):
        phone = validated_data.get('phone', None)
        if phone:
            instance.phone = validated_data.get('phone')
            instance.save()
        user_data = validated_data.pop("user", {})
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        return instance
    

class CompanyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'domain']

class PasswordResetSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    retype_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        print(f"\033[93m Inside validate ************ \033[0m")
        if attrs['new_password'] != attrs['retype_new_password']:
            raise serializers.ValidationError({"retype_new_password": "New passwords do not match."})
        return attrs
    
    def validate_current_password(self, value):
        print(f"\033[93m validate_current_password ************ \033[0m")
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def save(self, **kwargs):
        print(f"\033[93m save ************ \033[0m")
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class StudentUpdateSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    class Meta:
        model = Student
        fields = ['phone', 'about', 'alternate_email', 'joining_immediate', 'avail_for_intern', 'projects', 'certifications',
                  'github', 'linkedin', 'resume']
        
    def update(self, instance, validated_data):
        projects = validated_data.pop('projects', None)
        if projects is not None:
            instance.projects.clear()
            data = []
            for project in projects:
                p = Project.objects.create(**project)
                data.append(p)
            instance.projects.set(data)
        # resume = validated_data.pop('resume')
        # try:
        #     if resume:
                
        #         for file in redundant_resume:
        #             os.remove(os.path.join(location,file))
        #         resume = request.FILES['resume']
        #         filename_resume = 'resume'+str(request.user.id)+'.pdf'
        #         filename_r = fs.save(filename_resume, resume)
        #         student.resume=fs.url(os.path.join('students',str(request.user.id),filename_r))
        # except MultiValueDictKeyError as e:
        #     print(e)
       

        return super().update(instance, validated_data)