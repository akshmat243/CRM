from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *

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

