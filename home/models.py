from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from uuid import uuid4
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from home.models import *
from pytz import timezone
from django.utils.timezone import now
from django.utils import timezone
import random
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    name            = models.CharField(max_length=200, null=True, blank=True)
    mobile          = models.CharField(max_length=200, unique=True)
    email           = models.CharField(max_length=200, unique=True)
    is_admin        = models.BooleanField(default=False)
    is_team_leader  = models.BooleanField(default=False)
    is_staff_new    = models.BooleanField(default=False)
    is_freelancer   = models.BooleanField(default=False)
    is_it_staff     = models.BooleanField(default=False)
    login_time      = models.DateTimeField(default=timezone.now)
    logout_time     = models.DateTimeField(null=True, blank=True)
    profile_image   = models.FileField(upload_to ='profile_image/', null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)
    user_active     = models.BooleanField(default=False)
    is_user_login   = models.BooleanField(default=False)
    on_boarding_manager  = models.BooleanField(default=False,null=True, blank=True)
    dsr_manager          =  models.BooleanField(default=False, null=True, blank=True)
    executive_manager    =   models.BooleanField(default=False,null=True, blank=True)
    delivery_manager     = models.BooleanField(default=False,null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile']
    
    @property
    def is_active(self):
        return self.logout_time is None

    @property
    def duration(self):
        if self.logout_time:
            duration = self.logout_time - self.login_time
        else:
            duration = timezone.now() - self.login_time

        return int(duration.total_seconds())

    def _str_(self):
        return f"{self.username} - {self.login_time} to {self.logout_time if self.logout_time else 'Active'}"


class UserActivityLog(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    login_time      = models.DateTimeField(default=timezone.now)
    logout_time     = models.DateTimeField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)

    def _str_(self):
        return f"{self.user.username} - {self.login_time} to {self.logout_time if self.logout_time else 'Active'}"
    

class Admin(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_user', null=True, blank=True)
    self_user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_self_user', null=True, blank=True)
    admin_id        = models.CharField(max_length=200, unique=True, default=uuid4,)
    name            = models.CharField(max_length=200, null=True, blank=True)
    email           = models.CharField(max_length=200, unique=True)
    mobile          = models.CharField(max_length=200, null=True, blank=True)
    address         = models.CharField(max_length=200, null=True, blank=True)
    city            = models.CharField(max_length=25, null=True, blank=True)
    pincode         = models.CharField(max_length=6, null=True, blank=True)
    state           = models.CharField(max_length=30, null=True, blank=True)
    dob             = models.CharField(max_length=12, null=True, blank=True)
    pancard         = models.CharField(max_length=15, null=True, blank=True)
    aadharCard      = models.CharField(max_length=15, null=True, blank=True)
    marksheet       = models.CharField(max_length=50, null=True, blank=True)
    degree          = models.CharField(max_length=50, null=True, blank=True)
    account_number  = models.CharField(max_length=20, null=True, blank=True)
    upi_id          = models.CharField(max_length=30, null=True, blank=True)
    bank_name       = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code       = models.CharField(max_length=30, null=True, blank=True)
    salary          = models.CharField(max_length=30, null=True, blank=True)
    achived_slab    = models.CharField(max_length=30, default=00, null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Team_Leader(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    admin           = models.ForeignKey(Admin, on_delete=models.CASCADE)
    team_leader_id  = models.CharField(max_length=200, unique=True, default=uuid4)
    name            = models.CharField(max_length=200, null=True, blank=True)
    email           = models.CharField(max_length=200, unique=True)
    mobile          = models.CharField(max_length=200, null=True, blank=True)
    address         = models.CharField(max_length=200, null=True, blank=True)
    city            = models.CharField(max_length=25, null=True, blank=True)
    pincode         = models.CharField(max_length=6, null=True, blank=True)
    state           = models.CharField(max_length=30, null=True, blank=True)
    dob             = models.CharField(max_length=12, null=True, blank=True)
    pancard         = models.CharField(max_length=15, null=True, blank=True)
    aadharCard      = models.CharField(max_length=15, null=True, blank=True)
    marksheet       = models.CharField(max_length=50, null=True, blank=True)
    degree          = models.CharField(max_length=50, null=True, blank=True)
    account_number  = models.CharField(max_length=20, null=True, blank=True)
    upi_id          = models.CharField(max_length=30, null=True, blank=True)
    bank_name       = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code       = models.CharField(max_length=30, null=True, blank=True)
    salary          = models.CharField(max_length=30, null=True, blank=True)
    achived_slab    = models.CharField(max_length=30, default=00, null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Staff(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team_leader     = models.ForeignKey(Team_Leader, on_delete=models.CASCADE, null=True, blank=True)
    staff_id        = models.CharField(max_length=10, unique=True, blank=True)
    name            = models.CharField(max_length=200, null=True, blank=True)
    email           = models.CharField(max_length=200, unique=True)
    mobile          = models.CharField(max_length=200, null=True, blank=True)
    address         = models.CharField(max_length=200, null=True, blank=True)
    city            = models.CharField(max_length=25, null=True, blank=True)
    pincode         = models.CharField(max_length=6, null=True, blank=True)
    state           = models.CharField(max_length=30, null=True, blank=True)
    dob             = models.CharField(max_length=12, null=True, blank=True)
    pancard         = models.CharField(max_length=15, null=True, blank=True)
    aadharCard      = models.CharField(max_length=15, null=True, blank=True)
    marksheet       = models.CharField(max_length=50, null=True, blank=True)
    degree          = models.CharField(max_length=50, null=True, blank=True)
    account_number  = models.CharField(max_length=20, null=True, blank=True)
    upi_id          = models.CharField(max_length=30, null=True, blank=True)
    bank_name       = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code       = models.CharField(max_length=30, null=True, blank=True)
    salary          = models.CharField(max_length=30, null=True, blank=True)
    achived_slab    = models.CharField(max_length=30, default=00, null=True, blank=True)
    referral_code   = models.CharField(max_length=10, unique=True, null=True, blank=True)
    join_referral   = models.CharField(max_length=10, null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()
        
        if not self.staff_id:
            self.staff_id = self.generate_unique_staff_id()
        
        super().save(*args, **kwargs)

    def generate_unique_referral_code(self):
        name_part = (self.name[:3].upper() if self.name else 'STA').ljust(3, 'X')
        
        num_part = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        
        referral_code = f"{name_part}{num_part}"
        
        while Staff.objects.filter(referral_code=referral_code).exists():
            num_part = ''.join([str(random.randint(0, 9)) for _ in range(5)])
            referral_code = f"{name_part}{num_part}"
        
        return referral_code

    def generate_unique_staff_id(self):
        prefix = "VRI"
        start_number = 315

        last_staff = Staff.objects.filter(staff_id__startswith=prefix).order_by('-staff_id').first()

        if last_staff:
            last_number = int(last_staff.staff_id[3:])
            new_number = last_number + 1
        else:
            new_number = start_number

        if new_number > 999:
            raise ValueError("Staff ID exceeds the limit of 999.")

        staff_id = f"{prefix}{new_number:03d}"

        while Staff.objects.filter(staff_id=staff_id).exists():
            new_number += 1
            if new_number > 999:
                raise ValueError("Staff ID exceeds the limit of 999.")
            staff_id = f"{prefix}{new_number:03d}"

        return staff_id

    def __str__(self):
        return f"{self.name} ({self.staff_id})"
    
class Team_LeadData(models.Model):
    STATUS_LEAD = (
        ('Leads', 'Leads'),
        ('Interested', 'Interested'),           # ← FIXED
        ('Not Interested', 'Not Interested'),
        ('Other Location', 'Other Location'),
        ('Not Picked', 'Not Picked'),
        ('Lost', 'Lost'),
        ('Visit', 'Visit'),
)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team_leader = models.ForeignKey(Team_Leader, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    name        = models.CharField(max_length=255)
    email       = models.CharField(max_length=200, null=True, blank=True)
    call        = models.CharField(max_length=255, blank=True, null=True)
    send        = models.CharField(max_length=255, blank=True, null=True)
    status      = models.CharField(max_length=255,default='Leads', choices=STATUS_LEAD)
    message     = models.TextField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date    = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name
    

class LeadUser(models.Model):
    STATUS_LEAD = (
        ('Leads', 'Leads'),
        ('Intrested', 'Intrested'),
        ('Not Interested', 'Not Interested'),
        ('Other Location', 'Other Location'),
        ('Not Picked', 'Not Picked'),
        ('Lost', 'Lost'),
        ('Visit', 'Visit'),
    )
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team_leader = models.ForeignKey(Team_Leader, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    name        = models.CharField(max_length=255)
    email       = models.CharField(max_length=200, null=True, blank=True)
    call        = models.CharField(max_length=255, blank=True, null=True)
    send        = models.CharField(max_length=255, blank=True, null=True)
    status      = models.CharField(max_length=255,default='Leads', choices=STATUS_LEAD)
    message     = models.TextField(null=True, blank=True)
    follow_up_date  = models.DateField(null=True, blank=True)
    follow_up_time  = models.TimeField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date    = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name
    

class ProjectFile(models.Model):
    file        = models.FileField(upload_to='projectfile/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.file.name
    
class Marketing(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    admin       = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    team_leader = models.ForeignKey(Team_Leader, on_delete=models.CASCADE, null=True, blank=True)
    staff       = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    source      = models.CharField(max_length=50, null=True, blank=True)
    message     = models.TextField(null=True, blank=True)
    media_file  = models.FileField(upload_to ='marketing_media/', null=True, blank=True)
    url         = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.source
    
class ActivityLog(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    admin           = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    team_leader     = models.ForeignKey(Team_Leader, on_delete=models.CASCADE, null=True, blank=True)
    staff           = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    name            = models.CharField(max_length=200, null=True, blank=True)
    description     = models.CharField(max_length=200, null=True, blank=True)
    email           = models.CharField(max_length=50, null=True, blank=True)
    user_type       = models.CharField(max_length=50, null=True, blank=True)
    activity_type   = models.CharField(max_length=50, null=True, blank=True)
    ip_address      = models.CharField(max_length=15, null=True, blank=True)
    created_date    = models.DateTimeField(default=timezone.now)
    updated_date    = models.DateTimeField(auto_now=True)

    def __st__(self):
        return self.user
    
class Project(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    admin               = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    team_leader         = models.ForeignKey(Team_Leader, on_delete=models.CASCADE, null=True, blank=True)
    staff               = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    name                = models.CharField(max_length=200, null=True, blank=True)
    message             = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    youtube_link        = models.URLField(null=True, blank=True)
    media_file          = models.FileField(upload_to='project/')
    created_date        = models.DateTimeField(auto_now_add=True)
    updated_date        = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name
    
class Leads_history(models.Model):
    leads           = models.ForeignKey(LeadUser, on_delete=models.CASCADE, null=True, blank=True)
    lead_id         = models.IntegerField(null=True, blank=True)
    status          = models.CharField(max_length=50, null=True, blank=True)
    name            = models.CharField(max_length=100, null=True, blank=True)
    message         = models.TextField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name

class Slab(models.Model):
    start_value = models.CharField(max_length=50, null=True, blank=True)
    end_value = models.CharField(max_length=50, null=True, blank=True)
    amount = models.CharField(max_length=50, null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.amount
    
class Sell_plot(models.Model):
    admin           = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    team_leader     = models.ForeignKey(Team_Leader, on_delete=models.CASCADE, null=True, blank=True)
    staff           = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    project_name    = models.CharField(max_length=100, null=True, blank=True)
    project_location= models.CharField(max_length=100, null=True, blank=True)
    description     = models.TextField(null=True, blank=True)
    size_in_gaj     = models.CharField(max_length=50, null=True, blank=True)
    plot_no         = models.CharField(max_length=50, null=True, blank=True)
    earn_amount     = models.CharField(max_length=50, null=True, blank=True)
    slab            = models.CharField(max_length=50, null=True, blank=True)
    slab_amount     = models.IntegerField(null=True, blank=True)
    date            = models.DateField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.staff.name
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

class Settings(models.Model):
    logo = models.FileField(upload_to='project/')
    
    def __str__(self):
        return self.logo.name.split('/')[-1] if self.logo else "No Logo"

    
class MerchantInquiry(models.Model):
    STATUS_CHOICES = [
        ('New Inquiry', 'New Inquiry'),
        ('Pending Delivery', 'Pending Delivery'),
        ('Completed', 'Completed'),
    ]

    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    is_interested = models.BooleanField(default=False)
    inquiry_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New Inquiry')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)
    
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="assigned_inquiry", null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="submit_by", null=True, blank=True)
    delivery_manager =  models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_by", null=True, blank=True)
    def __str__(self):
        return self.full_name


class MerchantFormsData(models.Model):
    # Choices for Constitution Type
    CONSTITUTION_TYPE_CHOICES = [
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Partnership', 'Partnership'),
        ('Public / Pvt Ltd', 'Public / Pvt Ltd'),
        ('HUF', 'HUF'),
        ('Govt. Establishments', 'Govt. Establishments'),
        ('Others', 'Others'),
    ]
    POS_TYPE_CHOICES = [
        ('android_wifi', 'Andswipe Android/WIFI (AL9220) (With Printer)'),
        ('gprs_wifi', 'Andswipe GPRS/WIFI (L7220) (With Printer)'),
    ]
    OPERATION_MODEL_CHOICES = [
        ('monthly_rental', 'Monthly Rental'),
        ('fixed_cost', 'Fixed Cost'),
    ]
    MOP_CHOICES = [
        ('upi_neft_rtgs', 'UPI/NEFT/RTGS'),
        ('cheque', 'Cheque'),
        ('e_nach', 'E-Nach'),
        ('amount', 'Amount')
    ]

    # Choices for Status
    
    # Merchant Details
    merchant_inquiry = models.ForeignKey('MerchantInquiry', on_delete=models.CASCADE, related_name='merchant_inquiries')
    legal_name = models.CharField(max_length=255)
    marchant_dba_name = models.CharField(max_length=255)
    installation_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField(blank=True, null=True)
    state = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=255)
    telephone = models.PositiveIntegerField(blank=True, null=True)
    primary_mobile = models.PositiveIntegerField()
    secondary_mobile = models.PositiveIntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=20)
    gst_no = models.CharField(max_length=20)
    business_type = models.CharField(max_length=100)
    constitution_type = models.CharField(max_length=50, choices=CONSTITUTION_TYPE_CHOICES)
    others = models.CharField(max_length=100, blank=True, null=True)

    # Merchant Settlement Details
    beneficiary_name = models.CharField(max_length=255)
    bank_account_no = models.PositiveIntegerField()
    bank_name = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    pos_type_opted = models.CharField(max_length=255, blank=True, null=True)
    post_terminal = models.CharField(max_length=255, blank=True, null=True)
    value_added_services = models.CharField(max_length=255, blank=True, null=True)
    # Pos details fields
    pos_type_opted = models.CharField(max_length=50, choices=POS_TYPE_CHOICES, null=True, blank=True)
    number_of_pos_terminals = models.PositiveIntegerField(null=True, blank=True)
    value_added_services_required = models.BooleanField(default=False, null=True, blank=True)
    emi_facility_on_credit_card = models.BooleanField(default=False, null=True, blank=True)
    sodexo = models.BooleanField(default=False, null=True, blank=True)
    amex = models.BooleanField(default=False, null=True, blank=True)
    operation_model = models.CharField(max_length=20, choices=OPERATION_MODEL_CHOICES, null=True, blank=True)
    monthly_rental_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fixed_cost_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    device_security_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mop = models.CharField(max_length=20, choices=MOP_CHOICES, null=True, blank=True)
    mop_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cheque_number = models.CharField(max_length=50, null=True, blank=True)
    payment_ref_number = models.CharField(max_length=50, null=True, blank=True)
    # Status and Assignment
    assigned_delivery_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="assigned_user", null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="submitted_by", null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Merchant: {self.legal_name} ({self.marchant_dba_name})"
