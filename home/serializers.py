from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth import get_user_model
from .models import Admin
# Yeh line file ke sabse upar add karo
from django.db import IntegrityError
from .models import Project

class UserSerializer(serializers.ModelSerializer):
    """ user serializer """

    token_detail = serializers.SerializerMethodField("get_token_detail")
    class Meta:
        model = User 
        fields = ('id', 'username', 'name', 'email', 'mobile', 'profile_image', 'is_admin', 'is_team_leader', 'is_staff_new', 'is_freelancer', 'login_time', 'logout_time', 'token_detail',)
        extra_kwargs = {
            'token_detail': {'read_only': True}
        }
        
    def get_token_detail(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def get_user(self, request):
        user = request
        return user
    
class StaffAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadUser
        fields = ('id', 'user', 'team_leader', 'assigned_to', 'name', 'email', 'call', 'status', 'message', 'created_date', 'updated_date', )

class LeadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadUser
        fields = '__all__'

class MarketingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketing
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class LeadsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads_history
        fields = '__all__'

class TeamLeadDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team_LeadData
        fields = '__all__'

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            'user','name', 'email', 'mobile', 'address', 'city', 'pincode', 'state',
            'dob', 'pancard', 'aadharCard', 'marksheet', 'degree', 'account_number',
            'upi_id', 'bank_name', 'ifsc_code', 'salary', 'achived_slab',
            'referral_code', 'join_referral', 'created_date', 'updated_date'
        ]
        read_only_fields = ['referral_code', 'created_date', 'updated_date']

class MarketingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketing
        fields = ['id', 'user', 'source', 'message', 'media_file', 'url']
        read_only_fields = ['id', 'user']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'

class SellPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell_plot
        fields = [
            'id', 'admin', 'team_leader', 'staff', 'project_name', 
            'project_location', 'description', 'size_in_gaj', 
            'plot_no', 'earn_amount', 'slab', 'slab_amount', 
            'date', 'created_date', 'updated_date'
        ]


class ProductivityDataSerializer(serializers.Serializer):
    day = serializers.IntegerField()
    day_name = serializers.CharField()
    leads = serializers.IntegerField()
    salary = serializers.FloatField()

class StructuredCalendarDataSerializer(serializers.Serializer):
    day = serializers.IntegerField()
    day_name = serializers.CharField()

class AdminSerializer(serializers.ModelSerializer):
    """
    Serializer for the Admin model, with nested User details.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'user'] # Add any other Admin model fields you want




# ==========================================================
# NAYE SUPER-USER DASHBOARD KE LIYE NAYE SERIALIZERS
# ==========================================================

class DashboardUserSerializer(serializers.ModelSerializer):
    """
    Naye dashboard ke liye User model serializer.
    """
    profile_image = serializers.FileField(use_url=True, allow_null=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'mobile', 'profile_image', 
            'is_admin', 'is_team_leader', 'is_staff_new' , 'created_date',  # <--- YEH LINE ADD KARNI HAI
            'user_active'    # <--- YEH LINE ADD KARNI HAI
        ]

class DashboardAdminSerializer(serializers.ModelSerializer):
    """
    Naye dashboard ke liye Admin model serializer.
    """
 # home/serializers.py (Line ~153)

    user = DashboardUserSerializer(read_only=True, source='self_user')

    class Meta:
        model = Admin
        # Admin model ki saari fields
        fields = [
            'id', 'user', 'admin_id', 'name', 'email', 'mobile', 
            'address', 'city', 'pincode', 'state', 'dob', 'pancard', 
            'aadharCard', 'account_number', 'upi_id', 'bank_name', 
            'ifsc_code', 'salary', 'achived_slab' , 'created_date'
        ]

class DashboardSettingsSerializer(serializers.ModelSerializer):
    """
    Naye dashboard ke liye Settings model serializer.
    """
    logo = serializers.FileField(use_url=True)

    class Meta:
        model = Settings
        fields = ['id', 'logo']





# ==========================================================
# ADMIN SIDE LEADS RECORD KE LIYE NAYE SERIALIZERS
# ==========================================================

class ApiStaffSerializer(serializers.ModelSerializer):
    """
    Staff ki basic details ke liye serializer.
    """
    class Meta:
        model = Staff
        fields = ['id', 'name', 'staff_id', 'email', 'mobile']


# upar pe ensure ProjectSerializer imported / defined before using it
class ApiLeadUserSerializer(serializers.ModelSerializer):
    assigned_to = ApiStaffSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(source='project', read_only=True)
    project = ProjectSerializer(read_only=True)
    team_leader = serializers.CharField(source='team_leader.name', read_only=True)
    follow_up_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)
    follow_up_time = serializers.TimeField(format="%H:%M:%S", allow_null=True)

    class Meta:
        model = LeadUser
        fields = [
            'id', 'name', 'email', 'call', 'send', 'status', 'message', 'team_leader',
            'follow_up_date', 'follow_up_time', 'created_date', 'assigned_to',
            'project_id', 'project'
        ]




class ApiTeamLeadDataSerializer(serializers.ModelSerializer):
    """
    Team Leader ke Leads (Team_LeadData model) ke liye serializer.
    """
    assigned_to = ApiStaffSerializer(read_only=True)

    class Meta:
        model = Team_LeadData
        fields = [
            'id', 'name', 'email', 'call', 'send', 'status', 'message', 
            'created_date', 'assigned_to'
        ]



# serializers.py (AttendanceCalendarDaySerializer ko isse REPLACE karo)

# ==========================================================
# ATTENDANCE CALENDAR API SERIALIZER [FINAL FIX]
# ==========================================================

class AttendanceCalendarDaySerializer(serializers.Serializer):
    """
    Serializer for a single day in the attendance calendar.
    Ab ismein status aur color bhi hai.
    """
    date = serializers.DateField()
    has_task = serializers.BooleanField()
    day_name = serializers.CharField(max_length=10)
    # Naye fields jismein Absent/Present status aur color hoga
    status = serializers.CharField(max_length=10) 
    status_color = serializers.CharField(max_length=10)


# ==========================================================
# STAFF PRODUCTIVITY API SERIALIZERS
# ==========================================================

class ProductivityTeamLeaderSerializer(serializers.ModelSerializer):
    """
    Productivity page par Team Leader ki list dikhane ke liye Serializer.
    """
    # Hum pehle banaye hue serializers ko reuse kar rahe hain
    user = DashboardUserSerializer(read_only=True)
    admin = DashboardAdminSerializer(read_only=True)

    class Meta:
        model = Team_Leader
        fields = [
            'id', 'user', 'admin', 'team_leader_id', 'name', 'email', 
            'mobile', 'address', 'city', 'pincode', 'state', 'dob', 
            'pancard', 'aadharCard', 'account_number', 'upi_id', 
            'bank_name', 'ifsc_code', 'salary', 'achived_slab'
        ]

class StaffProductivityDataSerializer(serializers.Serializer):
    """
    Har staff ke calculated productivity data ke liye Serializer.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    total_leads = serializers.IntegerField()
    interested = serializers.IntegerField()
    not_interested = serializers.IntegerField()
    other_location = serializers.IntegerField()
    not_picked = serializers.IntegerField()
    lost = serializers.IntegerField()
    visit = serializers.IntegerField()
    visit_percentage = serializers.FloatField()
    interested_percentage = serializers.FloatField()
    total_calls = serializers.IntegerField()



# ==========================================================
# ADMIN ADD API SERIALIZER
# ==========================================================
class AdminCreateSerializer(serializers.ModelSerializer):
    """
    Serializer naya Admin User aur Admin Profile banane ke liye.
    """
    # Yeh fields User model se aa rahi hain
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    profile_image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Admin
        # Form ke saare fields yahaan daalo
        fields = [
            'name', 'email', 'mobile', 'password', 'profile_image',
            'address', 'city', 'state', 'pincode', 'dob', 'pancard', 
            'aadharCard', 'marksheet', 'degree', 'account_number', 
            'upi_id', 'bank_name', 'ifsc_code', 'salary'
        ]
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        """
        Check karo ki email (jo username bhi hai) pehle se hai ya nahi.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username (Email) Already Exists")
        return value

    def create(self, validated_data):
        # 1. Jo user API chala raha hai (Superuser)
        creator_user = self.context['request'].user
        
        # 2. User model ke fields ko data se alag karo
        password = validated_data.pop('password')
        profile_image = validated_data.pop('profile_image', None)
        email = validated_data.get('email')
        name = validated_data.get('name')
        mobile = validated_data.get('mobile')

        # 3. Naya User object banao
        try:
            new_user = User.objects.create(
                username=email,
                email=email,
                profile_image=profile_image,
                name=name,
                mobile=mobile,
                is_admin=True  # Naya user Admin banega
            )
            new_user.set_password(password)
            new_user.save()
        except IntegrityError as e:
            raise serializers.ValidationError(f"Error creating user: {e}")
        
        # 4. Naya Admin profile object banao
        try:
            # `validated_data` mein ab sirf Admin model ke fields bache hain
            admin = Admin.objects.create(
                user=creator_user,      # Jo Superuser yeh account bana raha hai
                self_user=new_user,     # Jo naya admin user abhi bana hai
                **validated_data
            )
        except IntegrityError as e:
            # Agar Admin profile fail ho, toh naya banaya user delete kardo
            new_user.delete()
            raise serializers.ValidationError(f"Error creating admin profile: {e}")

        return admin
    


# ==========================================================
# ADMIN EDIT API SERIALIZER
# ==========================================================
class AdminUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer ek Admin ki profile aur related User object ko update karne ke liye.
    Yeh profile_image ko bhi handle karta hai.
    """
    # Yeh field User model par hai, lekin hum ise yahaan accept karenge
    profile_image = serializers.FileField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Admin
        # Yeh saare fields hain jo aapke form update kar raha hai
        fields = [
            'name', 'email', 'mobile', 'address', 'city', 'state', 'pincode', 
            'dob', 'pancard', 'aadharCard', 'marksheet', 'degree', 
            'account_number', 'upi_id', 'bank_name', 'ifsc_code', 'salary',
            'profile_image' # Yeh naya field humne add kiya
        ]
        # Hum email ko required nahi maan rahe hain, taaki partial update (PATCH) kaam kare
        extra_kwargs = {
            'email': {'required': False}
        }

    def update(self, instance, validated_data):
        # 1. 'profile_image' ko data se nikaal lo, kyunki yeh Admin model par nahi hai
        profile_image = validated_data.pop('profile_image', None)

        # 2. Admin instance ko update karo (salary, address, etc.)
        admin_instance = super().update(instance, validated_data)
        
        # 3. Related User instance ko get karo (self_user se)
        user_instance = admin_instance.self_user
        
        if user_instance:
            # 4. User instance ko bhi update karo (jaisa aapka function kar raha tha)
            user_instance.email = validated_data.get('email', user_instance.email)
            user_instance.username = validated_data.get('email', user_instance.username) # Email ko username banao
            user_instance.name = validated_data.get('name', user_instance.name)
            user_instance.mobile = validated_data.get('mobile', user_instance.mobile)
            
            if profile_image:
                user_instance.profile_image = profile_image
            
            user_instance.save()
        
        return admin_instance
    
# ==========================================================
# STAFF ADD API SERIALIZER [FIXED]
# ==========================================================
class StaffCreateSerializer(serializers.ModelSerializer):
    """
    Serializer naya Staff User aur Staff Profile banane ke liye.
    [FIXED] Activity Log logic ko theek kiya gaya hai.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    profile_image = serializers.FileField(required=False, allow_null=True)
    team_leader = serializers.PrimaryKeyRelatedField(queryset=Team_Leader.objects.all(), required=True)

    class Meta:
        model = Staff
        fields = [
            'team_leader', 'name', 'email', 'mobile', 'password', 'profile_image',
            'address', 'city', 'state', 'pincode', 'dob', 'pancard', 
            'aadharCard', 'marksheet', 'degree', 'account_number', 
            'upi_id', 'bank_name', 'ifsc_code', 'salary'
        ]
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username (Email) Already Exists")
        return value

    def create(self, validated_data):
        # 1. User model ke fields ko data se alag karo
        password = validated_data.pop('password')
        profile_image = validated_data.pop('profile_image', None)
        email = validated_data.get('email')
        name = validated_data.get('name')
        mobile = validated_data.get('mobile')

        # 2. Naya User object banao
        try:
            new_user = User.objects.create_user(
                username=email, email=email, password=password,
                profile_image=profile_image, name=name,
                mobile=mobile, is_staff_new=True
            )
        except IntegrityError as e:
            raise serializers.ValidationError(f"Error creating user: {e}")
        
        # 3. Naya Staff profile object banao
        try:
            staff = Staff.objects.create(
                user=new_user,
                **validated_data
            )
            
            # --- Activity Log Logic (Aapke function se copy kiya) ---
            request = self.context['request']
            user_type = ""
            if request.user.is_superuser: user_type = "Super User"
            elif request.user.is_admin: user_type = "Admin User"
            elif request.user.is_team_leader: user_type = "Team leader User"
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            
            tagline = f"staff : {staff.name} created by user[Email : {request.user.email}, {user_type}]"
            tag2 = f"staff : {staff.name} created"

            if request.user.is_team_leader:
                # --- YEH LINE FIX KI HAI ---
                team_leader_instance = Team_Leader.objects.get(user=request.user)
                my_user1 = team_leader_instance.admin
                # --- FIX ENDS ---
                ActivityLog.objects.create(
                    admin=my_user1, description=tagline, ip_address=ip,
                    email=request.user.email, user_type=user_type, activity_type=tag2, name=request.user.name
                )
            elif request.user.is_admin:
                # Admin profile ko dhoondo
                admin_instance = Admin.objects.filter(self_user=request.user).last() 
                ActivityLog.objects.create(
                    admin=admin_instance, 
                    description=tagline, 
                    ip_address=ip,
                    email=request.user.email, 
                    user_type=user_type, 
                    activity_type=tag2, 
                    name=request.user.name
                )    
            elif request.user.is_superuser:
                 ActivityLog.objects.create(
                    user=request.user, description=tagline, ip_address=ip,
                    email=request.user.email, user_type=user_type, activity_type=tag2, name=request.user.name
                )
            
        except Exception as e:
            new_user.delete()
            raise serializers.ValidationError(f"Error creating staff profile: {e}")

        return staff
    



# ==========================================================
# TEAM LEADER ADD API SERIALIZER [FINAL FIX]
# ==========================================================
class TeamLeaderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer naya Team Leader User aur Profile banane ke liye.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    profile_image = serializers.FileField(required=False, allow_null=True)
    admin_id = serializers.IntegerField(write_only=True, required=False) 

    # User ke roles
    on_boarding_manager = serializers.BooleanField(required=False)
    dsr_manager = serializers.BooleanField(required=False)
    executive_manager = serializers.BooleanField(required=False)
    delivery_manager = serializers.BooleanField(required=False)

    class Meta:
        model = Team_Leader
        fields = [
            'name', 'email', 'mobile', 'password', 'profile_image',
            'address', 'city', 'state', 'pincode', 'dob', 'pancard', 
            'aadharCard', 'marksheet', 'degree', 'account_number', 
            'upi_id', 'bank_name', 'ifsc_code', 'salary',
            'admin_id', 'on_boarding_manager', 'dsr_manager', 'executive_manager', 'delivery_manager'
        ]
        extra_kwargs = {'email': {'required': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username (Email) Already Exists")
        return value

    # serializers.py (def create method ko isse REPLACE karo)

    # serializers.py (def create method ko isse REPLACE karo)

    def create(self, validated_data):
        # 1. Data separation
        password = validated_data.pop('password')
        profile_image = validated_data.pop('profile_image', None)
        admin_id = validated_data.pop('admin_id', None)
        
        on_boarding_manager = validated_data.pop('on_boarding_manager', False)
        dsr_manager = validated_data.pop('dsr_manager', False)
        executive_manager = validated_data.pop('executive_manager', False)
        delivery_manager = validated_data.pop('delivery_manager', False)
        
        email = validated_data.get('email')
        name = validated_data.get('name')
        mobile = validated_data.get('mobile')
        request = self.context['request']

        # 2. Admin Object fetch karo (FINAL ROBUST LOGIC)
        admin_obj = None
        current_user = request.user
        
        if current_user.is_superuser:
            # Superuser always uses the provided admin_id
            if admin_id:
                try:
                    admin_obj = Admin.objects.get(id=int(admin_id))
                except (Admin.DoesNotExist, ValueError):
                    raise serializers.ValidationError({"admin_id": "Admin profile not found with this ID or ID is invalid."})

        elif current_user.is_admin:
            # Admin must be creating for themselves (i.e., they are the admin_obj)
            admin_obj = Admin.objects.filter(self_user=current_user).last()
            
        if not admin_obj:
            # Agar koi Admin profile nahi mili, toh error raise karo
            # Yeh error ab Admin, Superuser dono cases ko handle karega
            raise serializers.ValidationError({"admin": "Admin profile is required and could not be determined."})

        # 3. Naya User object banao
        try:
            new_user = User.objects.create_user(
                username=email, email=email, password=password,
                profile_image=profile_image, name=name, mobile=mobile, 
                is_team_leader=True, on_boarding_manager=on_boarding_manager,
                dsr_manager=dsr_manager, executive_manager=executive_manager, 
                delivery_manager=delivery_manager
            )
        except IntegrityError as e:
            raise serializers.ValidationError(f"Error creating user: {e}")
        
        # 4. Naya Team Leader profile object banao
        try:
            team_leader = Team_Leader.objects.create(
                admin=admin_obj, 
                user=new_user,
                **validated_data
            )
            
            # --- Activity Log Logic ---
            user_type = ""
            if current_user.is_superuser: user_type = "Super User"
            elif current_user.is_admin: user_type = "Admin User"
            
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            tagline = f"Team Lead({name}) created by user[Email : {current_user.email}, {user_type}]"
            tag2 = f"Team Lead({name}) created"
            
            if current_user.is_superuser:
                 ActivityLog.objects.create(
                    user=current_user, description=tagline, ip_address=ip, email=current_user.email,
                    user_type=user_type, activity_type=tag2, name=current_user.name
                )
            elif current_user.is_admin:
                ActivityLog.objects.create(
                    admin=admin_obj, 
                    description=tagline, ip_address=ip, email=current_user.email,
                    user_type=user_type, activity_type=tag2, name=current_user.name
                )
            
        except Exception as e:
            new_user.delete()
            raise serializers.ValidationError({"non_field_errors": f"Error creating team leader profile: {e}"})

        return team_leader
    





# ==========================================================
# TEAM LEADER EDIT/UPDATE API SERIALIZER
# ==========================================================
class TeamLeaderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer ek Team Leader ki profile aur related User object ko update karne ke liye.
    """
    profile_image = serializers.FileField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Team_Leader
        fields = [
            'name', 'email', 'mobile', 'address', 'city', 'pincode', 'state',
            'dob', 'pancard', 'aadharCard', 'marksheet', 'degree',
            'account_number', 'upi_id', 'bank_name', 'ifsc_code', 'salary',
            'profile_image' 
        ]
        extra_kwargs = {
            'email': {'required': False}, 
            'name': {'required': False}
        }

    def update(self, instance, validated_data):
        # 1. 'profile_image' ko data se nikaal lo
        profile_image = validated_data.pop('profile_image', None)

        # 2. Team Leader instance ko update karo
        team_leader_instance = super().update(instance, validated_data)
        
        # 3. Related User instance ko get karo
        user_instance = team_leader_instance.user
        
        if user_instance:
            # 4. User instance ko update karo (email, name, mobile)
            user_instance.email = validated_data.get('email', user_instance.email)
            user_instance.username = validated_data.get('email', user_instance.username) 
            user_instance.name = validated_data.get('name', user_instance.name)
            user_instance.mobile = validated_data.get('mobile', user_instance.mobile)
            
            if profile_image:
                user_instance.profile_image = profile_image
            
            user_instance.save()
        
        return team_leader_instance
    

# ==========================================================
# STAFF EDIT (FREELANCER EDIT) API SERIALIZERS
# ==========================================================

class FullStaffSerializer(serializers.ModelSerializer):
    """
    Staff/Freelancer ki poori profile (GET request ke liye)
    """
    user = DashboardUserSerializer(read_only=True) 
    team_leader = ProductivityTeamLeaderSerializer(read_only=True) 

    class Meta:
        model = Staff
        fields = '__all__' # Staff model ki saari fields dikhao

class StaffUpdateSerializer(serializers.ModelSerializer):
    """
    Staff/Freelancer ki profile aur related User object ko update karne ke liye.
    """
    profile_image = serializers.FileField(required=False, allow_null=True, write_only=True)
    team_leader_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Staff
        fields = [
            'name', 'email', 'mobile', 'address', 'city', 'pincode', 'state',
            'dob', 'pancard', 'aadharCard', 'marksheet', 'degree', 
            'account_number', 'upi_id', 'bank_name', 'ifsc_code', 'salary',
            'profile_image', 'team_leader_id'
        ]
        extra_kwargs = {
            'email': {'required': False}, 
            'name': {'required': False}
        }

    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        team_leader_id = validated_data.pop('team_leader_id', None)

        staff_instance = super().update(instance, validated_data)
        
        if team_leader_id:
            try:
                new_team_leader = Team_Leader.objects.get(id=team_leader_id)
                staff_instance.team_leader = new_team_leader
                staff_instance.save()
            except Team_Leader.DoesNotExist:
                pass # Validation error yahaan nahi, APIView me handle ho sakta hai
        
        user_instance = staff_instance.user
        if user_instance:
            user_instance.email = validated_data.get('email', user_instance.email)
            user_instance.username = validated_data.get('email', user_instance.username)
            user_instance.name = validated_data.get('name', user_instance.name)
            user_instance.mobile = validated_data.get('mobile', user_instance.mobile)
            
            if profile_image:
                user_instance.profile_image = profile_image
            
            user_instance.save()
        
        return staff_instance
    


# ==========================================================
# SLAB SERIALIZER
# ==========================================================
class SlabSerializer(serializers.ModelSerializer):
    """
    Serializer for Slab model data.
    """
    class Meta:
        model = Slab
        fields = '__all__'    



# ==========================================================
# STAFF PRODUCTIVITY CALENDAR SERIALIZER
# ==========================================================

class DailyProductivitySerializer(serializers.Serializer):
    """
    Ek din ke leads aur salary data ke liye serializer.
    """
    day = serializers.IntegerField()
    date = serializers.DateField()
    day_name = serializers.CharField(max_length=10)
    leads = serializers.IntegerField()
    salary = serializers.FloatField()






# ==========================================================
# SERIALIZER: LEAD EXPORT [FIXED VARIABLE NAME]
# ==========================================================
class LeadExportSerializer(serializers.Serializer):
    """
    Serializer jo Excel export API ke liye input parameters
    (dates, staff, status) ko validate karta hai.
    """
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    
    all_interested = serializers.CharField(required=False, allow_blank=True, max_length=10)
    staff_id = serializers.IntegerField(required=False, allow_null=True)
    
    # --- FIX: 'status' variable ka naam change kiya 'lead_status' ---
    lead_status = serializers.CharField(required=False, allow_blank=True, max_length=100) 

    def validate(self, data):
        """
        Check karta hai ki agar 'all_interested' != "1", toh 'staff_id' 
        aur 'lead_status' zaroor hone chahiye.
        """
        all_interested = data.get('all_interested')
        
        if all_interested != "1":
            if not data.get('staff_id'):
                raise serializers.ValidationError({"staff_id": "This field is required when not exporting 'all_interested'."})
            
            # --- FIX: 'status' ko 'lead_status' se badla ---
            if not data.get('lead_status'):
                raise serializers.ValidationError({"lead_status": "This field is required when not exporting 'all_interested'."})
        
        return data
    


# home/serializers.py (file ke end me add karo)

# ==========================================================
# NAYA SERIALIZER: SIMPLE TEAM LEADER (SIRF FLAT DATA KE LIYE)
# ==========================================================
class SimpleTeamLeaderSerializer(serializers.ModelSerializer):
    """
    Serializer jo Team Leader ki flat details dikhata hai (bina nested user/admin ke).
    """
    class Meta:
        model = Team_Leader
        # Yahaan 'user' aur 'admin' fields nahi hain
        fields = [
            'id', 'team_leader_id', 'name', 'email', 'mobile', 
            'address', 'city', 'pincode', 'state', 'dob', 'pancard', 
            'aadharCard', 'account_number', 'upi_id', 'bank_name', 
            'ifsc_code', 'salary', 'achived_slab', 'created_date' 
        ]
        read_only_fields = ['created_date']    
    




# ==========================================================
# API: ADD SELL PLOT (FREELANCER) SERIALIZER
# ==========================================================

class SellPlotCreateSerializer(serializers.ModelSerializer):
    """
    Serializer naya Sell_plot object banane ke liye.
    Yeh 'create' method ke andar poora slab calculation logic handle karta hai.
    """
    
    # Hum form se 'staff_id' lenge (agar URL me id=0 hai)
    # 'write_only=True' ka matlab hai ki yeh field sirf input lene ke liye hai, 
    # output (response) me nahi dikhega.
    staff_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Sell_plot
        # Yeh woh fields hain jo hum JSON body se expect kar rahe hain
        fields = [
            'project_name', 
            'project_location', 
            'description', 
            'size_in_gaj', 
            'plot_no', 
            'date',
            'staff_id', # Yeh virtual field
        ]
        # 'date' ko required banate hain
        extra_kwargs = {
            'date': {'required': True}
        }

    def validate_size_in_gaj(self, value):
       
        try:
            int(value or 0)
        except ValueError:
            raise serializers.ValidationError("Size (Gaj) must be a valid number.")
        
        if int(value or 0) <= 0:
            raise serializers.ValidationError("Size (Gaj) must be greater than 0.")
        
        return value # Original string value return karo (aapke model ke hisaab se)


    # home/serializers.py
# (SellPlotCreateSerializer class ke andar)

    def create(self, validated_data):
        # 1. Staff instance dhoondo (Aapke original view logic se)
        
        # URL se 'id' nikaalo (e.g., /add_sell_freelancer/3/)
        view_id = self.context['request'].parser_context['kwargs']['id']
        staff_id_from_post = validated_data.pop('staff_id', None)
        
        user_instance = None
        if view_id != 0:
            user_instance = Staff.objects.filter(id=view_id).last()
        else:
            user_instance = Staff.objects.filter(id=staff_id_from_post).last()

        if not user_instance:
            raise serializers.ValidationError({"staff_id": f"Staff not found."})
        
        # 2. Team Leader aur Admin dhoondo
        team_leader_insatnce = user_instance.team_leader
        if not team_leader_insatnce:
            raise serializers.ValidationError({"team_leader": f"Team Leader not found for staff {user_instance.name}."})
        
        admin_instance = team_leader_insatnce.admin
        if not admin_instance:
            raise serializers.ValidationError({"admin": f"Admin not found for team leader {team_leader_insatnce.name}."})

        # 3. Slab Update Logic (Aapke view logic se)
        size_in_gaj_str = validated_data.get('size_in_gaj')
        size_in_gaj_int = int(size_in_gaj_str or 0)

        # Staff Slab
        staff_slab = user_instance.achived_slab
        update_staff_slab = int(staff_slab or 0) + size_in_gaj_int
        user_instance.achived_slab = update_staff_slab
        user_instance.save()

        # Team Leader Slab
        team_lead_slab = team_leader_insatnce.achived_slab
        update_staff_slab1 = int(team_lead_slab or 0) + size_in_gaj_int
        team_leader_insatnce.achived_slab = update_staff_slab1
        team_leader_insatnce.save()

        # Admin Slab
        admin_slab = admin_instance.achived_slab
        update_staff_slab2 = int(admin_slab or 0) + size_in_gaj_int
        admin_instance.achived_slab = update_staff_slab2
        admin_instance.save()

        # 4. Payout Calculation Logic (Aapke view logic se)
        current_slab = int(user_instance.achived_slab or 0)
        slabs = Slab.objects.all()

        slab_amount = 0
        myslab = "N/A"
        current_slab_amount = 0

        for slab in slabs:
            start_value = int(slab.start_value or 0)
            if slab.end_value is not None:
                end_value = int(slab.end_value or 0)
                if start_value <= current_slab <= end_value:
                    slab_amount_base = int(slab.amount or 0)
                    if user_instance.user.is_freelancer:
                        slab_amount = slab_amount_base * size_in_gaj_int
                    
                    # --- [YEH LINE FIX KI HAI] ---
                    elif user_instance.user.is_staff_new: 
                        slab_amount = (slab_amount_base - 100) * size_in_gaj_int
                    
                    myslab = f"{start_value}-{end_value}"
                    current_slab_amount = slab_amount_base
                    break
            else:
                if current_slab >= start_value:
                    slab_amount_base = int(slab.amount or 0)
                    if user_instance.user.is_freelancer:
                        slab_amount = slab_amount_base * size_in_gaj_int
                    
                    # --- [YEH LINE BHI FIX KI HAI] ---
                    elif user_instance.user.is_staff_new:
                        slab_amount = (slab_amount_base - 100) * size_in_gaj_int
                    
                    myslab = f"{start_value}+"
                    current_slab_amount = slab_amount_base
                    break
        
        # 5. Naya Sell_plot object banao
        sell = Sell_plot.objects.create(
            admin=admin_instance,
            team_leader=team_leader_insatnce,
            staff=user_instance,
            earn_amount=slab_amount,
            slab=myslab,
            slab_amount=current_slab_amount,
            **validated_data  
        )
        return sell





# serializers.py (file ke end me yeh add karo)

# ==========================================================
# LEAD UPDATE (STATUS/MESSAGE) API SERIALIZER
# ==========================================================
class LeadUpdateSerializer(serializers.Serializer):
    """
    Serializer jo 'status', 'message', 'followDate', aur 'followTime'
    ko API request se validate karne ke liye hai.
    """
    status = serializers.CharField(max_length=100, required=True)
    message = serializers.CharField(required=False, allow_blank=True)
    followDate = serializers.DateField(required=False, allow_null=True)
    followTime = serializers.TimeField(required=False, allow_null=True)



# home/serializers.py (file ke end me add karo)

# ==========================================================
# API: STAFF-ONLY - ADD NEW LEAD (BY SELF)
# ==========================================================
class StaffLeadCreateSerializer(serializers.ModelSerializer):
    """
    Serializer naya LeadUser banane ke liye (Staff Dashboard).
    Yeh 'create' method ke andar staff, team_leader, aur user ko automatically set karta hai.
    """
    
    # Hum form se 'mobile' lenge, lekin model me 'call' save karenge
    mobile = serializers.CharField(source='call', required=True)
    # Hum form se 'description' lenge, lekin model me 'message' save karenge
    description = serializers.CharField(source='message', allow_blank=True, required=False)

    class Meta:
        model = LeadUser
        # Yeh fields hain jo hum POST request se expect kar rahe hain
        fields = [
            'name', 
            'email', 
            'mobile',  # (call ban jaayega)
            'status', 
            'description' # (message ban jaayega)
        ]

    def validate_mobile(self, value):
        """
        Check karta hai ki mobile number pehle se hai ya nahi.
        """
        if LeadUser.objects.filter(call=value).exists():
            raise serializers.ValidationError("Mobile number already exists.")
        return value

    def create(self, validated_data):
        # 1. Logged-in staff user ko context se nikaalo
        user = self.context['request'].user

        # 2. Staff ka profile dhoondo
        try:
            staff_instance = Staff.objects.get(email=user.email)
        except Staff.DoesNotExist:
            raise serializers.ValidationError("Staff profile not found for this user.")
        
        if not staff_instance.team_leader:
             raise serializers.ValidationError("Staff is not assigned to any Team Leader.")

        # 3. Bachi hui fields (user, team_leader, assigned_to) add karo
        validated_data['user'] = user
        validated_data['assigned_to'] = staff_instance
        validated_data['team_leader'] = staff_instance.team_leader

        # 4. Naya LeadUser create karo
        lead = LeadUser.objects.create(**validated_data)
        return lead    
class ApiUserSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    # updated_at = serializers.DateTimeField(source='updated_date', format="%d-%b-%Y %I:%M %p", read_only=True)
  # ← FIXED: NO source!

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'email', 'mobile',
            'is_team_leader', 'is_staff_new', 'is_admin',
            'is_active', 'duration', 'login_time', 'logout_time',
            'profile_image', 'user_active', 'is_user_login'
        ]

    def get_duration(self, obj):
        return obj.duration  # ← This works because @property


# home/serializers.py (file ke end me add karo)

# ==========================================================
# NAYA SERIALIZER: STAFF PROFILE (BINA TEAMLEADER KE)
# ==========================================================
class StaffOnlyProfileSerializer(serializers.ModelSerializer):
    """
    Serializer jo Staff ki poori profile dikhata hai, 
    lekin nested 'team_leader' object ke BINA.
    """
    
    # Hum User ki details (email, name, etc.) dikhayenge
    user = DashboardUserSerializer(read_only=True) 

    class Meta:
        model = Staff
        
        # Hum '__all__' ki jagah, 'team_leader' ko chhod kar
        # baaki saari fields dikhayenge
        fields = [
            'id', 'user', 'staff_id', 'name', 'email', 'mobile', 
            'address', 'city', 'pincode', 'state', 'dob', 'pancard', 
            'aadharCard', 'marksheet', 'degree', 'account_number', 
            'upi_id', 'bank_name', 'ifsc_code', 'salary', 'achived_slab',
            'referral_code', 'join_referral', 'created_date', 'updated_date'
        ]




# home/serializers.py

# ==========================================================
# SUPERUSER PROFILE & SETTINGS SERIALIZERS
# ==========================================================

class SuperUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Superuser profile update.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile', 'profile_image']

class DashboardSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for Global Settings (Logo).
    """
    class Meta:
        model = Settings
        fields = ['id', 'logo']



# home/serializers.py

class TeamLeaderAddStaffSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for Team Leader to add a new Staff.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = Staff
        # Saare fields jo form me hain
        fields = [
            'name', 'email', 'password', 'mobile', 'address', 'city', 'state', 'pincode',
            'dob', 'pancard', 'aadharCard', 'marksheet', 'degree', 'account_number',
            'upi_id', 'bank_name', 'ifsc_code', 'salary', 'profile_image'
        ]

    def validate_email(self, value):
        # Check karo email pehle se registered hai ya nahi
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        return value

    def create(self, validated_data):
        # Data nikaalo
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        # 1. User Create Karo
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password, 
            name=validated_data.get('name'),
            mobile=validated_data.get('mobile'),
            is_staff_new=True, # Important flag
            profile_image=validated_data.get('profile_image')
        )
        
        # 2. Logged-in Team Leader ko dhoondo
        request = self.context.get('request')
        team_leader_instance = Team_Leader.objects.get(user=request.user)

        # 3. Staff Create Karo (Automatically assigned to this Team Leader)
        staff = Staff.objects.create(
            user=user, 
            email=email, 
            team_leader=team_leader_instance, 
            **validated_data
        )
        return staff
    



class LeadForDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadUser
        fields = '__all__' 




# ==========================================================
# API: TEAM-LEADER - ADD NEW LEAD (BY SELF) SERIALIZER
# ==========================================================
class TeamLeaderLeadCreateSerializer(serializers.ModelSerializer):
    """
    Use this for the endpoint that allows a Team Leader to create a lead.
    Frontend sends: name, email, mobile, status, description
    We map: mobile -> call, description -> message
    The view should pass team_leader and user via serializer.save()
    """
    mobile = serializers.CharField(write_only=True, required=False, allow_blank=True)
    description = serializers.CharField(source='message', write_only=True, required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = LeadUser
        # We only accept minimal fields from client
        fields = ('id', 'name', 'email', 'mobile', 'status', 'description')

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()

    def create(self, validated_data):
        # map mobile -> call and description->message
        mobile = validated_data.pop('mobile', '') or ''
        message = validated_data.pop('message', '')  # because source='message' maps description -> message
        # team_leader and user must be passed by view in serializer.save()
        team_leader = self.context.get('team_leader') or self._kwargs.get('team_leader') if hasattr(self, '_kwargs') else None
        user = self.context.get('request').user if self.context.get('request') else None

        # if the view passes team_leader in save(kwargs), that will be available in validated_data kwargs,
        # so we try to fetch from self._kwargs passed by DRF - but safest is to allow view to pass via save()
        extra_kwargs = {}
        # If team_leader passed via save(kwargs) it will be in self.context or view must provide; below we check validated_data
        # Create lead:
        lead = LeadUser.objects.create(
            user = user,
            team_leader = team_leader,
            name = validated_data.get('name', ''),
            email = validated_data.get('email', ''),
            call = mobile,
            message = message,
            status = validated_data.get('status', '')
        )
        return lead




class LeadCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Lead from Team Leader API.
    Frontend sends: name, email, mobile, status, description
    We map mobile -> call and description -> message (model fields)
    """
    mobile = serializers.CharField(write_only=True, required=False, allow_blank=True)
    description = serializers.CharField(source='message', write_only=True, required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = LeadUser
        fields = ('id', 'name', 'email', 'mobile', 'status', 'description')

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()

    def create(self, validated_data):
        # map mobile -> call and description -> message
        mobile = validated_data.pop('mobile', '') or ''
        message = validated_data.pop('message', '')  # because source='message' maps description -> message

        # team_leader and user should be passed by the view via serializer.context or serializer.save(kwargs)
        team_leader = self.context.get('team_leader', None)
        user = self.context.get('request').user if self.context.get('request') else None

        lead = LeadUser.objects.create(
            user = user,
            team_leader = team_leader,
            name = validated_data.get('name', ''),
            email = validated_data.get('email', ''),
            call = mobile,
            message = message,
            status = validated_data.get('status', '')
        )
        return lead
# ------------------------------


# home/serializers.py

# ==========================================================
# TEAM LEADER PROFILE SERIALIZER
# ==========================================================
class TeamLeaderProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Team Leader Profile View.
    Shows TL details and User details.
    """
    user = DashboardUserSerializer(read_only=True)
    
    class Meta:
        model = Team_Leader
        fields = [
            'id', 'user', 'team_leader_id', 'name', 'email', 'mobile',
            'address', 'city', 'pincode', 'state', 'dob', 
            'created_date', 'updated_date'
        ]





# home/serializers.py

# ==========================================================
# SUPERUSER PROFILE SERIALIZERS
# ==========================================================

class SuperUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Superuser profile update (User model).
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile', 'profile_image', 'username']
        read_only_fields = ['username'] # Username change nahi hoga (email se sync hoga)

class DashboardSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for Global Settings (Logo).
    """
    class Meta:
        model = Settings
        fields = ['id', 'logo']



# home/serializers.py

# ==========================================================
# ADMIN PROFILE SERIALIZER
# ==========================================================
class AdminProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Admin Profile View.
    Shows Admin details and User details.
    """
    user = DashboardUserSerializer(read_only=True)
    
    class Meta:
        model = Admin
        fields = [
            'id', 'user', 'admin_id', 'name', 'email', 'mobile',
            'address', 'city', 'pincode', 'state', 'dob', 'pancard',
            'aadharCard', 'account_number', 'upi_id', 'bank_name', 'ifsc_code',
            'created_date'
        ]




class ActivityLogMinimalSerializer(serializers.ModelSerializer):
    # Column mapping:
    #  - "E-mail" column in your screenshot is actually the description text,
    #    so we expose it as `description` but you can rename key if UI expects 'email'.
    description = serializers.CharField(source='description', read_only=True)
    activity_type = serializers.CharField(source='activity_type', read_only=True)
    user_type = serializers.CharField(source='user_type', read_only=True)

    # Format created_date exactly like template (example: "Nov. 21, 2025, 7:19 a.m.")
    created_date = serializers.DateTimeField(format="%b. %d, %Y, %I:%M %p", read_only=True)

    class Meta:
        model = ActivityLog
        # We will expose only these fields in the order you want
        fields = ['name', 'description', 'activity_type', 'user_type', 'created_date']







# home/serializers.py

class TeamLeaderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to UPDATE Team Leader Profile (and underlying User).
    """
    # Yeh fields User model se aa rahe hain, inhe writable banao
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = Team_Leader
        fields = [
            'name', 'email', 'mobile', 'address', 'city', 'state', 'pincode',
            'dob', 'pancard', 'aadharCard', 'profile_image'
        ]

    def update(self, instance, validated_data):
        # 1. User Data Nikaalo (Email update ke liye)
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')

        # 2. Update Team Leader Fields
        instance.name = validated_data.get('name', instance.name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.pancard = validated_data.get('pancard', instance.pancard)
        instance.aadharCard = validated_data.get('aadharCard', instance.aadharCard)
        
        # Image update logic (agar nayi image aayi hai)
        if 'profile_image' in validated_data:
            instance.profile_image = validated_data['profile_image']

        instance.save()

        # 3. Update User Fields (Email sync karna zaroori hai)
        user = instance.user
        if email and user.email != email:
            # Check duplicate email
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise serializers.ValidationError({"email": "Email already exists."})
            user.email = email
            user.username = email # Username ko bhi email bana do
            user.save()
            
        # User name aur mobile bhi sync kar sakte ho agar chahiye
        user.name = instance.name
        user.mobile = instance.mobile
        user.save()

        return instance
    




