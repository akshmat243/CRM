from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth import get_user_model
from .models import Admin


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
            'is_admin', 'is_team_leader', 'is_staff_new'
        ]

class DashboardAdminSerializer(serializers.ModelSerializer):
    """
    Naye dashboard ke liye Admin model serializer.
    """
    user = DashboardUserSerializer(read_only=True)

    class Meta:
        model = Admin
        # Admin model ki saari fields
        fields = [
            'id', 'user', 'admin_id', 'name', 'email', 'mobile', 
            'address', 'city', 'pincode', 'state', 'dob', 'pancard', 
            'aadharCard', 'account_number', 'upi_id', 'bank_name', 
            'ifsc_code', 'salary', 'achived_slab'
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

class ApiLeadUserSerializer(serializers.ModelSerializer):
    """
    Staff ke Leads (LeadUser model) ke liye serializer.
    """
    assigned_to = ApiStaffSerializer(read_only=True)
    
    class Meta:
        model = LeadUser
        fields = [
            'id', 'name', 'email', 'call', 'send', 'status', 'message', 
            'follow_up_date', 'follow_up_time', 'created_date', 'assigned_to'
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



# ==========================================================
# ATTENDANCE CALENDAR API SERIALIZER
# ==========================================================

class AttendanceCalendarDaySerializer(serializers.Serializer):
    """
    Serializer for a single day in the attendance calendar.
    """
    date = serializers.DateField()
    has_task = serializers.BooleanField()
    day_name = serializers.CharField(max_length=3)



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