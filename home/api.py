from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, permissions, filters, generics, views
from django_filters import rest_framework as django_filters
from datetime import date
from datetime import datetime, timedelta
from rest_framework import status, viewsets
from .serializers import *
from .models import *
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import random
import string
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils import timezone
from calendar import month_name
from calendar import monthrange, monthcalendar, day_name
import calendar
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
import pandas as pd
from rest_framework.parsers import MultiPartParser, FormParser
# Is line ko upar import section mein ADD karo
from django.http import Http404


# @method_decorator(csrf_exempt, name='dispatch')
# class LoginApiView(APIView):

#     permission_classes = [AllowAny]

#     @swagger_auto_schema(
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or Email'),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
#             },
#             required=['username', 'password'],
#         ),
#         responses={
#             200: 'Login successful',
#             400: 'Invalid input or credentials'
#         }
#     )

#     def post(self, request):
#         res = {}
#         username = request.data.get("username", None)
#         password = request.data.get("password", None)

#         if username is None:
#             res['status'] = False
#             res['message'] = "Email is required"
#             res['data'] = []
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)

#         if password is None:
#             res['status'] = False
#             res['message'] = "Password is required"
#             res['data'] = []
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=username, password=password)
#         user.is_user_login = True
#         user.save()
#         if not user.is_staff_new:
#             res['status'] = False
#             res['message'] = "Only satff user allowed to login!"
#             res['data'] = []
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)
#         if user is None:
#             res['status'] = False
#             res['message'] = "Invalid Email or Password!"
#             res['data'] = []
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)
#         serializer = UserSerializer(
#             user, read_only=True, context={'request': request})
#         if serializer:
#             res['status'] = True
#             res['message'] = "Authenticated successfully"
#             res['data'] = serializer.data
#             return Response(res, status=status.HTTP_200_OK)

#         else:
#             res['status'] = False
#             res['message'] = "No recored found for entered data"
#             res['data'] = []
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)

class IsCustomAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with is_admin=True.
    """
    def has_permission(self, request, view):
        # Check karta hai ki user logged-in hai AUR uska 'is_admin' flag True hai
        return request.user and request.user.is_authenticated and request.user.is_admin
    
class CustomIsSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow Superusers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser    


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000



# Yeh pagination class hai
class ActivityLogPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500




class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins, superusers, or team leaders.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_superuser or 
             request.user.is_admin or 
             request.user.is_team_leader)
        )



# ===================================================================
# 1. LOGIN API VIEW [FINAL FIX - MANUAL AUTH]
# ===================================================================
@method_decorator(csrf_exempt, name='dispatch')
class LoginApiView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password'],
        ),
        responses={
            200: 'Login successful',
            400: 'Invalid input or credentials'
        }
    )
    def post(self, request):
        username_or_email = request.data.get("username", None)
        password = request.data.get("password", None)

        if not username_or_email or not password:
            return Response(
                {'status': False, 'message': 'Username and Password are required', 'data': []}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- YEH HAI FINAL FIX: Hum authenticate ko bypass karenge ---
        try:
            # Hum seedha email se user ko dhoondhenge
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            # Agar email se nahi mila, toh username se dhoondhenge
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                # Ab pakka user nahi hai
                return Response(
                    {'status': False, 'message': 'Invalid username or password', 'data': []}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        # User mil gaya, ab password check karo
        if not user.check_password(password):
            return Response(
                {'status': False, 'message': 'Invalid username or password', 'data': []}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Password sahi hai! Ab user active check karo
        if not user.is_superuser:
            if user.user_active is False:
                return Response(
                    {'status': False, 'message': "Your account is inactive. Please contact admin.", 'data': []}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not (user.is_admin or user.is_team_leader or user.is_staff_new or user.is_it_staff):
                 return Response(
                    {'status': False, 'message': "User role not defined for API access.", 'data': []}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Sab theek hai, login karo
        user.is_user_login = True
        user.save()

        # Serialize the user data
        serializer = UserSerializer(user, read_only=True, context={'request': request})
        
        return Response(
            {'status': True, 'message': 'Authenticated successfully', 'data': serializer.data}, 
            status=status.HTTP_200_OK
        )
        
class staff_assigned_leads(APIView):

    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request):
        
        res = {}
        staff = request.user
        staff_instance = Staff.objects.filter(email=staff.email).last()
        myleads = LeadUser.objects.filter(status="Leads", assigned_to=staff_instance,)

        serializer = StaffAssignedSerializer(myleads, many=True)

        
        today = timezone.now().date()
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)) - timedelta(seconds=1)
        else:
            start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))

        lead_filter = {'updated_date__range': [start_date, end_date]}

        leads = LeadUser.objects.filter(status="Leads", assigned_to=staff_instance)
        interested = LeadUser.objects.filter(status="Intrested", assigned_to=staff_instance, **lead_filter)
        not_interested = LeadUser.objects.filter(status="Not Interested", assigned_to=staff_instance, **lead_filter)
        other_location = LeadUser.objects.filter(status="Other Location", assigned_to=staff_instance, **lead_filter)
        not_picked = LeadUser.objects.filter(status="Not Picked", assigned_to=staff_instance, **lead_filter)
        lost = LeadUser.objects.filter(status="Lost", assigned_to=staff_instance, **lead_filter)
        visits = LeadUser.objects.filter(status="Visit", assigned_to=staff_instance, **lead_filter)

        total_leads = leads.count()
        total_interested_leads = interested.count()
        total_not_interested_leads = not_interested.count()
        total_other_location_leads = other_location.count()
        total_not_picked_leads = not_picked.count()
        total_lost_leads = lost.count()
        total_visits_leads = visits.count()
        total_calls = total_interested_leads + total_not_interested_leads + total_other_location_leads + total_not_picked_leads + total_lost_leads + total_visits_leads

        whatsapp_marketing = Marketing.objects.filter(source="whatsapp", user=request.user).last()
        projects = Project.objects.all()

        leads_data = LeadUserSerializer(leads, many=True).data
        whatsapp_marketing_data = MarketingSerializer(whatsapp_marketing).data if whatsapp_marketing else None
        projects_data = ProjectSerializer(projects, many=True).data

        data1 = {
            'total_calls': total_calls,
            'total_leads': total_leads,
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'total_other_location_leads': total_other_location_leads,
            'total_not_picked_leads': total_not_picked_leads,
            'total_lost_leads': total_lost_leads,
            'total_visits_leads': total_visits_leads,
            'whatsapp_marketing': whatsapp_marketing_data,
            'projects': projects_data,}


        res['status'] = True
        res['message'] = "leads are retrived succefully"
        res['data'] = serializer.data
        res['other_data'] = data1
        return Response(res, status=status.HTTP_200_OK)
    


class StatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        res = {}
        data = {}

        merchant_id = request.data.get('leads_id')
        new_status = request.data.get('new_status')
        remark = request.data.get('remark')
        follow_up_date = request.data.get('follow_up_date')
        follow_up_time = request.data.get('follow_up_time')

        if merchant_id is None:
            res['status'] = False
            res['message'] = "lead id is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        if new_status is None:
            res['status'] = False
            res['message'] = "status is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser:
            user_type = "Super User"
        elif request.user.is_admin:
            user_type = "Admin User"
        elif request.user.is_team_leader:
            user_type = "Team Leader User"
        elif request.user.is_staff_new:
            user_type = "Staff User"

        if merchant_id and new_status:
            try:
                status_update_user = LeadUser.objects.get(id=merchant_id)
                previous_status = status_update_user.status

                tagline = f"Lead status changed from {previous_status} to {new_status} by user[Email: {request.user.email}, {user_type}]"
                status_update_user.status = new_status
                status_update_user.message = remark

                if new_status == 'Intrested':
                    if follow_up_date:
                        status_update_user.follow_up_date = follow_up_date
                    if follow_up_time:
                        status_update_user.follow_up_time = follow_up_time

                status_update_user.save()
                data['id'] = status_update_user.id
                data['status'] = status_update_user.status
                data['follow_up_date'] = status_update_user.follow_up_date
                data['follow_up_time'] = status_update_user.follow_up_time


                Leads_history.objects.create(
                    leads=status_update_user,
                    lead_id=merchant_id,
                    status=new_status,
                    name=status_update_user.name,
                    message=remark,
                )

                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

                if request.user.is_staff_new:
                    admin_email = request.user.email
                    admin_instance = Staff.objects.filter(email=admin_email).last()
                    team_leader = admin_instance.team_leader

                    ActivityLog.objects.create(
                        team_leader=team_leader,
                        description=tagline,
                        ip_address=ip,
                        email=request.user.email,
                        user_type=user_type,
                        activity_type=f"Status changed to {new_status}",
                        name=request.user.name,
                    )
            except LeadUser.DoesNotExist:
                return Response({"error": "LeadUser does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Update Team_LeadData
            # try:
            #     status_update_team_lead = Team_LeadData.objects.get(id=merchant_id)
            #     status_update_team_lead.status = new_status
            #     status_update_team_lead.save()

            #     # Activity log for Team_LeadData
            #     ActivityLog.objects.create(
            #         team_leader=team_leader,
            #         description=f"Lead status changed for Team LeadData by {user_type}",
            #         ip_address=ip,
            #         email=request.user.email,
            #         user_type=user_type,
            #         activity_type=f"Status changed to {new_status}",
            #         name=request.user.name,
            #     )
            # except Team_LeadData.DoesNotExist:
            #     return Response({"error": "Team_LeadData does not exist."}, status=status.HTTP_404_NOT_FOUND)
            res['status'] = True
            res['message'] = "Status updated successfully."
            res['data'] = data
            return Response(res, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
    
class AutoAssignLeadsAPIView(APIView):
    permission_classes = [IsAuthenticated ,  CustomIsSuperuser]

    def post(self, request):
        user_email = request.user.email
        request_user = get_object_or_404(Staff, email=user_email)
        team_leader = request_user.team_leader
        current_total_assign_leads = LeadUser.objects.filter(assigned_to=request_user, status='Leads').count()

        if current_total_assign_leads == 0:
            team_leader_total_leads = Team_LeadData.objects.filter(assigned_to=None, status='Leads')
            leads_count = 0
            leads_assigned = []

            for lead in team_leader_total_leads:
                if leads_count != 20:
                    lead_user = LeadUser.objects.create(
                        name=lead.name,
                        email=lead.email,
                        call=lead.call,
                        send=False,
                        status=lead.status,
                        assigned_to=request_user,
                        team_leader=team_leader,
                        user=lead.user,
                    )
                    lead.assigned_to = request_user
                    lead.save()
                    leads_assigned.append(LeadUserSerializer(lead_user).data)
                    leads_count += 1

            return Response({"message": "Leads assigned successfully.", "leads": leads_assigned}, status=status.HTTP_201_CREATED)

        return Response({"error": "You already have leads."}, status=status.HTTP_400_BAD_REQUEST)
    
class LeadsReportAPIView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request):
        res = {}
        lead_status = request.data.get('status')

        if lead_status is None:
            res['status'] = True
            res['message'] = "lead status is required."
            res['data'] = []
            return Response(res, status=status.HTTP_200_OK)
        
        staff_instance = Staff.objects.filter(user__email=request.user.email).last()
        users_lead_lost = LeadUser.objects.filter(status=lead_status, assigned_to=staff_instance).order_by('-updated_date')
        serializer = LeadUserSerializer(users_lead_lost, many=True)

        res['status'] = True
        res['message'] = lead_status + " leads fetch successfully."
        res['data'] = serializer.data
        return Response(res, status=status.HTTP_200_OK)
    
class LeadHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request):
        res = {}
        lead_id = request.data.get('lead_id')

        if lead_id is None:
            res['status'] = True
            res['message'] = "lead id is required."
            res['data'] = []
            return Response(res, status=status.HTTP_200_OK)
        
        users_lead_lost = Leads_history.objects.filter(lead_id=lead_id,).order_by('-updated_date')
        serializer = LeadsHistorySerializer(users_lead_lost, many=True)

        res['status'] = True
        res['message'] = "leads history fetch successfully."
        res['data'] = serializer.data
        return Response(res, status=status.HTTP_200_OK)

class AddLeadBySelfAPI(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    parser_classes = (MultiPartParser, FormParser) # form-data ke liye

    def post(self, request):
        user = request.user
        data = request.data
        
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        status_value = data.get('status')
        description = data.get('description')

        if not mobile:
            return Response({"message": "Mobile number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mobile number ko string mein convert karo taaki filter sahi chale
        mobile_str = str(mobile)
        if LeadUser.objects.filter(call=mobile_str).exists():
            return Response({"message": "Mobile number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        lead_data = {
            'user': user.id,
            'name': name,
            'email': email,
            'call': mobile_str, # String value use karo
            'message': description,
            'status': status_value
        }
        
        # --- YEH HAI FIX KI HUI LOGIC ---
        # 1. Pehle Team Leader check karo
        if user.is_team_leader:
            team_leader_instance = Team_Leader.objects.filter(email=user.email).last()
            if not team_leader_instance:
                return Response({"error": f"Team Leader profile not found for {user.email}."}, status=status.HTTP_404_NOT_FOUND)
            
            lead_data.update({'team_leader': team_leader_instance.id})
            serializer = LeadUserSerializer(data=lead_data)
        
        # 2. Agar Team Leader nahi hai, tab Staff check karo
        elif user.is_staff_new:
            staff_instance = Staff.objects.filter(email=user.email).last()
            if not staff_instance:
                return Response({"error": f"Staff profile not found for {user.email}."}, status=status.HTTP_404_NOT_FOUND)
            
            if not staff_instance.team_leader:
                 return Response({"error": f"Staff {user.email} is not assigned to any Team Leader."}, status=status.HTTP_400_BAD_REQUEST)

            lead_data.update({
                'team_leader': staff_instance.team_leader.id,
                'assigned_to': staff_instance.id
            })
            serializer = LeadUserSerializer(data=lead_data)
        
        # 3. Agar Admin hai
        elif user.is_admin:
            # Admin ke liye logic yahaan daalo (agar woh self-lead add kar sakta hai)
            serializer = LeadUserSerializer(data=lead_data)
        
        else:
            return Response({"error": "Unauthorized role for this action"}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'lead add successfully', 'status': status.HTTP_201_CREATED, 'data': serializer.data})
        
        # Serializer errors ko detail mein dikhao
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StaffProfileAPIView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request):
        staff_instance = get_object_or_404(Staff, email=request.user.email)
        serializer = StaffProfileSerializer(staff_instance)
        data = serializer.data
        data['image'] = staff_instance.user.profile_image.url
        return Response({'mesage': 'Profile fetch successfully.', 'status': status.HTTP_200_OK, 'data': data,},)
    
    def post(self, request):
        admin = get_object_or_404(Staff, email=request.user.email)
        user_instance = User.objects.filter(email=admin.email).last()
        
        new_email = request.data.get('email')
        if new_email != admin.email and Staff.objects.filter(email=new_email).exclude(id=admin.id).exists():
            return Response({"error": "Email Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        staff_serializer = StaffProfileSerializer(admin, data=request.data, partial=True)
        if staff_serializer.is_valid():
            staff_serializer.save()
        else:
            return Response(staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES.get("profile_image")
        user_data = {
            # 'email': new_email,
            # 'username': new_email,
            'name': request.data.get('name'),
            'mobile': request.data.get('mobile'),
            'profile_image': request.FILES.get("profile_image")
        }
        user_serializer = UserSerializer(user_instance, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Your profile has been successfully updated."}, status=status.HTTP_200_OK)
    
class EditRecordAPIView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request, source):
        user = request.user
        record = Marketing.objects.filter(source=source, user=user).last()
        create_id = 2 if record is None else 1

        if record:
            data = {
                'm_id': record.id,
                'source': record.source,
                'url': record.url,
                'message': record.message,
                'media_file': record.media_file.url if record.media_file else '',
                'create_id': create_id,
            }
        else:
            data = {
                'source': source,
                'create_id': create_id,
            }
        
        return Response(data, status=status.HTTP_200_OK)


class UpdateRecordAPIView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def post(self, request):
        data = request.data
        source = data.get('source')
        message = data.get('message')
        url = data.get('url')
        media_file = data.get('media_file')
        create_id = data.get('create_id')
        user = request.user

        if create_id == "2":
            # Create a new marketing record
            marketing = Marketing.objects.create(
                user=user,
                source=source,
                message=message,
                url=url,
                media_file=media_file
            )
            serializer = MarketingSerializer(marketing)
            return Response({'message': 'Record created successfully', 'status': '200', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # Update the last record for the user and source
            marketing_instance = Marketing.objects.filter(user=user, source=source).last()
            if not marketing_instance:
                return Response({'error': 'Record not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            marketing_instance.message = message
            marketing_instance.url = url
            marketing_instance.media_file = media_file
            marketing_instance.save()

            serializer = MarketingSerializer(marketing_instance)
            return Response({'message': 'Record updated successfully', 'status': '200', 'data': serializer.data}, status=status.HTTP_200_OK)
        

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ActivityLogsAPIView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request):
        user = request.user
        logs = ActivityLog.objects.none()

        if user.is_superuser:
            logs = ActivityLog.objects.all().order_by('-created_date')
        elif user.is_admin:
            admin_user = Admin.objects.filter(email=user.email).last()
            logs = ActivityLog.objects.filter(admin=admin_user).order_by('-created_date')
        elif user.is_team_leader:
            team_leader_user = Team_Leader.objects.filter(email=user.email).last()
            logs = ActivityLog.objects.filter(team_leader=team_leader_user).order_by('-created_date')
        elif user.is_staff_new:
            staff_instance = Staff.objects.filter(email=user.email).last()
            logs = ActivityLog.objects.filter(Q(user=user) | Q(staff=staff_instance)).order_by('-created_date')

        serializer = ActivityLogSerializer(logs, many=True)

        return Response(serializer.data)
    

class IncentiveSlabStaffView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request, staff_id):

        months_list = [(i, month_name[i]) for i in range(1, 13)]

        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))

        if hasattr(request.user, 'is_staff_new') and request.user.is_staff_new:
            user_type = request.user.is_freelancer
        else:
            staff_instance = Staff.objects.filter(id=staff_id).last()
            user_type = User.objects.filter(email=staff_instance.email).last().is_freelancer if staff_instance else None

        slab = Slab.objects.all()

        if request.user.is_superuser or request.user.is_team_leader or request.user.is_admin:
            sell_property = Sell_plot.objects.filter(
                staff=staff_id,
                updated_date__year=year,
                updated_date__month=month
            ).order_by('-created_date')
            total_earn_amount = sell_property.aggregate(total_earn=Sum('earn_amount'))
        else:
            sell_property = Sell_plot.objects.filter(
                staff__email=request.user.email,
                updated_date__year=year,
                updated_date__month=month
            ).order_by('-created_date')
            total_earn_amount = sell_property.aggregate(total_earn=Sum('earn_amount'))

        total_earn = total_earn_amount['total_earn'] if total_earn_amount['total_earn'] else 0

        sell_property_data = SellPlotSerializer(sell_property, many=True).data

        response_data = {
            'slab': slab.values(),
            'sell_property': sell_property_data,
            'total_earn': total_earn,
            'year': year,
            'month': month,
            'months_list': months_list,
            'user_type': user_type,
        }
        return Response(response_data)


class StaffProductivityCalendarAPIView(APIView):
    def get(self, request, staff_id, year=None, month=None):
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))

        if request.user.is_superuser or request.user.is_team_leader or request.user.is_admin:
            staff = Staff.objects.get(id=staff_id)
        else:
            staff = Staff.objects.get(user__id=staff_id)

        days_in_month = monthrange(year, month)[1]
        salary_arg = staff.salary if staff.salary else 0
        daily_salary = round(float(salary_arg) / days_in_month)

        leads_data = LeadUser.objects.filter(
            assigned_to=staff,
            updated_date__year=year,
            updated_date__month=month,
            status='Intrested'
        ).values('updated_date__day').annotate(count=Count('id'))

        productivity_data = {}
        total_salary = 0

        for lead in leads_data:
            day = lead['updated_date__day']
            leads_count = lead['count']
            daily_earned_salary = daily_salary if leads_count >= 10 else round((daily_salary / 10) * leads_count, 2)
            productivity_data[day] = {'leads': leads_count, 'salary': daily_earned_salary}
            total_salary += daily_earned_salary

        calendar_data = monthcalendar(year, month)
        weekdays = list(day_name)
        structured_calendar_data = []

        for week in calendar_data:
            for i, day in enumerate(week):
                if day != 0:
                    structured_calendar_data.append({'day': day, 'day_name': weekdays[i]})

        months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]

        response_data = {
            'staff': StaffProfileSerializer(staff).data,
            'year': year,
            'month': month,
            'productivity_data': [{'day': day, 'day_name': weekdays[(day - 1) % 7], 'leads': data['leads'], 'salary': data['salary']}
                                  for day, data in productivity_data.items()],
            'structured_calendar_data': structured_calendar_data,
            'days_in_month': days_in_month,
            'total_salary': round(total_salary, 2),
            'monthly_salary': salary_arg,
            'months_list': months_list,
        }

        return Response(response_data)
    

User = get_user_model()

# home/api.py (Line ~1070)

# ===================================================================
# 14. SUPER ADMIN DASHBOARD API [ORIGINAL / CORRECTED]
# (Yeh sirf Admins ki list aur global lead counts dikhayega)
# ===================================================================
class SuperAdminDashboardAPIView(APIView):
    """
    API view for the Super Admin Dashboard (Admin Users page).
    Provides aggregated lead counts and stats about ALL ADMINS.
    Only accessible by superusers.
    """
    permission_classes = [IsAuthenticated, CustomIsSuperuser] # Sirf Superuser ke liye

    def get(self, request, *args, **kwargs):
        
        # 1. Saare Admin users ko dhoondo
        admin_users = User.objects.filter(is_admin=True)
        admin_profiles = Admin.objects.filter(self_user__in=admin_users)
        admin_serializer = DashboardAdminSerializer(admin_profiles, many=True) 
        
        # 2. Saara counting logic
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        total_upload_leads = Team_LeadData.objects.filter().count()
        total_left_leads = Team_LeadData.objects.filter(status='Leads', assigned_to=None).count()
        total_assign_leads = LeadUser.objects.filter(status='Leads').count()
        interested_leads_staff = LeadUser.objects.filter(status='Intrested').count()
        not_interested_leads_staff = LeadUser.objects.filter(status='Not Interested').count()
        other_location_leads_staff = LeadUser.objects.filter(status='Other Location').count()
        not_picked_leads_staff = LeadUser.objects.filter(status='Not Picked').count()
        lost_leads_staff = LeadUser.objects.filter(status='Lost').count()
        lost_visit_staff = LeadUser.objects.filter(status='Visit').count()

        pending_followup_staff = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date__isnull=False)
            ).count()
        today_followup_staff = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=today)
            ).count()
        tomorrow_followup_staff = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=tomorrow)
            ).count()

        interested_leads_team_leader = Team_LeadData.objects.filter(status='Intrested').count()
        not_interested_leads_team_leader  = Team_LeadData.objects.filter(status='Not Interested').count()
        other_location_leads_team_leader  = Team_LeadData.objects.filter(status='Other Location').count()
        not_picked_leads_team_leader = Team_LeadData.objects.filter(status='Not Picked').count()
        lost_leads_team_leader  = Team_LeadData.objects.filter(status='Lost').count()
        lost_visit_team_leader  = Team_LeadData.objects.filter(status='Visit').count()

        total_interested = interested_leads_staff + interested_leads_team_leader
        total_not_interested = not_interested_leads_staff + not_interested_leads_team_leader
        total_other_location = other_location_leads_staff + other_location_leads_team_leader
        total_not_picked = not_picked_leads_staff + not_picked_leads_team_leader
        total_lost = lost_leads_staff + lost_leads_team_leader
        total_visits = lost_visit_staff + lost_visit_team_leader

        total_pending_followup = pending_followup_staff
        total_today_followup = today_followup_staff
        total_tomorrow_followup = tomorrow_followup_staff

        # 3. Build the response data dictionary
        data = {
            'users': admin_serializer.data, # Admins ki list
            'total_upload_leads': total_upload_leads,
            'total_assign_leads': total_assign_leads,
            'total_interested': total_interested,
            'total_not_interested': total_not_interested,
            'total_other_location': total_other_location,
            'total_not_picked': total_not_picked,
            'total_lost': total_lost,
            'total_visits': total_visits,
            'total_left_leads': total_left_leads,
            'total_pending_followup': total_pending_followup,
            'total_today_followup': total_today_followup,
            'total_tomorrow_followup': total_tomorrow_followup,
            # (Staff counts yahaan se hata diye hain)
        }
        
        # 4. Return the data as a JSON response
        return Response(data, status=status.HTTP_200_OK)
# ===================================================================
# NAYA DASHBOARD API (Date Filter Waala)
# ===================================================================
class SuperUserDashboardAPIView(APIView):
    """
    Super User Dashboard ke liye API, date filtering ke saath.
    Sirf superusers ke liye accessible hai.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request, *args, **kwargs):
        # Admin profile get karo
        us = request.user
        admin_profiles = Admin.objects.filter(user=us)
        # Naya wala serializer use karo
        admin_serializer = DashboardAdminSerializer(admin_profiles, many=True)

        # Date filtering logic
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        lead_filter = {}
        start_date_for_context = None
        end_date_for_context = None

        if start_date_str and end_date_str:
            try:
                start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
                end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)) - timedelta(seconds=1)
                
                lead_filter = {'updated_date__range': [start_date, end_date]}
                start_date_for_context = start_date_str
                end_date_for_context = end_date_str
            except ValueError:
                pass 

        # Poora counting logic
        total_upload_leads = Team_LeadData.objects.filter(status='Leads').count()
        total_assign_leads = LeadUser.objects.filter(status='Leads').count()
        interested_leads_staff = LeadUser.objects.filter(status='Intrested', **lead_filter).count()
        not_interested_leads_staff = LeadUser.objects.filter(status='Not Interested', **lead_filter).count()
        other_location_leads_staff = LeadUser.objects.filter(status='Other Location', **lead_filter).count()
        not_picked_leads_staff = LeadUser.objects.filter(status='Not Picked', **lead_filter).count()
        lost_leads_staff = LeadUser.objects.filter(status='Lost', **lead_filter).count()
        lost_visit_staff = LeadUser.objects.filter(status='Visit', **lead_filter).count()
        
        interested_leads_team_leader = Team_LeadData.objects.filter(status='Intrested', **lead_filter).count()
        not_interested_leads_team_leader  = Team_LeadData.objects.filter(status='Not Interested', **lead_filter).count()
        other_location_leads_team_leader  = Team_LeadData.objects.filter(status='Other Location', **lead_filter).count()
        not_picked_leads_team_leader = Team_LeadData.objects.filter(status='Not Picked', **lead_filter).count()
        lost_leads_team_leader  = Team_LeadData.objects.filter(status='Lost', **lead_filter).count()
        lost_visit_team_leader  = Team_LeadData.objects.filter(status='Visit', **lead_filter).count()

        # Summing logic
        total_interested = interested_leads_staff + interested_leads_team_leader
        total_not_interested = not_interested_leads_staff + not_interested_leads_team_leader
        total_other_location = other_location_leads_staff + other_location_leads_team_leader
        total_not_picked = not_picked_leads_staff + not_picked_leads_team_leader
        total_lost = lost_leads_staff + lost_leads_team_leader
        total_visits = lost_visit_staff + lost_visit_team_leader

        total_calls = total_interested + total_not_interested + total_other_location + total_not_picked + total_lost + total_visits

        # User stats
        total_users = User.objects.count()
        logged_in_users = User.objects.filter(is_user_login=True).count()
        logged_out_users = User.objects.filter(is_user_login=False).count()

        # Chart data
        data_points = [
            { "label": "Interested", "y": total_interested  },
            { "label": "Lost",  "y": total_lost  },
            { "label": "Visits",  "y": total_visits  },
            { "label": "Not Interested", "y": total_not_interested  },
            { "label": "Other Location",  "y": total_other_location  },
            { "label": "Not Picked",  "y": total_not_picked  },
            { "label": "Total Calls",  "y": total_calls  },
        ]

        # Settings data
        setting_obj = Settings.objects.filter().last()
        # Naya wala serializer use karo
        setting_serializer = DashboardSettingsSerializer(setting_obj)

        # Final JSON response
        data = {
            'users': admin_serializer.data,
            'data_points': data_points,
            'total_upload_leads': total_upload_leads,
            'total_assign_leads': total_assign_leads,
            'total_interested': total_interested,
            'total_not_interested': total_not_interested,
            'total_other_location': total_other_location,
            'total_not_picked': total_not_picked,
            'total_lost': total_lost,
            'total_visits': total_visits,
            'start_date': start_date_for_context,
            'end_date': end_date_for_context,
            'total_users': total_users,
            'logged_in_users': logged_in_users,
            'logged_out_users': logged_out_users,
            'setting': setting_serializer.data if setting_obj else None,
        }
        
        return Response(data, status=status.HTTP_200_OK)

# ===================================================================
# NAYA ADMIN SIDE LEADS RECORD API  - [FIXED]
# ===================================================================
class AdminSideLeadsRecordAPIView(APIView):
    """
    Admin dashboard se leads ko status tag ke hisaab se filter karne ke liye API.
    """
    permission_classes = [IsAdminUser , CustomIsSuperuser]

    def get(self, request, tag, *args, **kwargs):
        # Default (khaali) querysets
        staff_leads_qs = LeadUser.objects.none()
        team_leads_qs = Team_LeadData.objects.none()

        if tag == "total_visit_tag":
            staff_leads_qs = LeadUser.objects.filter(status='Visit')
            team_leads_qs = Team_LeadData.objects.filter(status='Visit')
            
        elif tag == "total_lost_lead_tag":
            staff_leads_qs = LeadUser.objects.filter(status='Lost')
            team_leads_qs = Team_LeadData.objects.filter(status='Lost')
            
        elif tag == "total_not_picked_lead_tag":
            staff_leads_qs = LeadUser.objects.filter(status='Not Picked')
            team_leads_qs = Team_LeadData.objects.filter(status='Not Picked')
            
        elif tag == "total_other_location_lead_tag":
            staff_leads_qs = LeadUser.objects.filter(status='Other Location')
            team_leads_qs = Team_LeadData.objects.filter(status='Other Location')
            
        elif tag == "total_not_interested_lead_tag":
            staff_leads_qs = LeadUser.objects.filter(status='Not Interested')
            team_leads_qs = Team_LeadData.objects.filter(status='Not Interested')
            
        elif tag == "total_upload_lead_tag":
            team_leads_qs = Team_LeadData.objects.filter(status='Leads')
            
        elif tag == "total_assigned_lead_tag":
            staff_leads_qs = LeadUser.objects.filter(status='Leads')
            
        elif tag == "total_interested_lead_tag":
            staff_leads_qs = LeadUser.objects.filter(status='Intrested')
            team_leads_qs = Team_LeadData.objects.filter(status='Intrested')
            
        else:
            # Agar tag match nahi hua
            return Response({"error": "Invalid tag provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Dono querysets ko serialize karo
        staff_serializer = ApiLeadUserSerializer(staff_leads_qs, many=True)
        team_serializer = ApiTeamLeadDataSerializer(team_leads_qs, many=True)

        # Data ko do alag list mein bhej rahe hain taaki frontend ko aasaani ho
        data = {
            "staff_leads": staff_serializer.data,
            "team_leads": team_serializer.data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    

# ===================================================================
# NAYA FILE UPLOAD API (Excel/CSV Waala)
# ===================================================================
class ExcelUploadAPIView(APIView):
    """
    Excel (.xlsx) ya CSV (.csv) file se leads upload karne ke liye API.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser] # User ka login hona zaroori hai
    parser_classes = (MultiPartParser, FormParser) # File uploads ke liye zaroori

# home/api.py -> ExcelUploadAPIView ke andar

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response(
                {"error": "File not provided. Please upload a file with the key 'excel_file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if excel_file.name.endswith('.csv'):
                # 'utf-8-sig' ko rakho, yeh achhi practice hai
                df = pd.read_csv(excel_file, encoding='utf-8-sig') 
            elif excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file, engine='openpyxl')
            else:
                return Response(
                    {"error": "Unsupported file format. Please upload a .csv or .xlsx file."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": f"Error reading file: {e}. Make sure the file is not corrupt."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- [YEH RAHA NAYA FIX] ---
        # Column headers ko zabardasti clean karo:
        # 1. Sabko lowercase me badlo.
        # 2. Shuru aur end ke extra space (whitespace) ko hatao.
        df.columns = df.columns.str.lower().str.strip()
        # --- [FIX ENDS] ---

        # Ab clean kiye hue columns ko check karo
        required_columns = ['name', 'call', 'send', 'status']
        if not all(col in df.columns for col in required_columns):
            return Response(
                {"error": f"File is missing required columns. Make sure these columns exist (all lowercase): {required_columns}. Found columns: {list(df.columns)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_count = df.shape[0]
        duplicates = []
        created_count = 0
        
        team_leader = None
        if request.user.is_team_leader:
            try:
                team_leader = Team_Leader.objects.get(user=request.user)
            except Team_Leader.DoesNotExist:
                return Response(
                    {"error": "Team Leader profile not found for this user."},
                    status=status.HTTP_404_NOT_FOUND
                )

        for i, row in df.iterrows():
            # .get() ki jagah seedha ['name'] use kar sakte hain, kyunki humne check kar liya hai
            name = row['name']
            call = row['call']
            status_val = row['status']
            send_val = row['send']

            if not name or pd.isna(name):
                continue
            if not status_val.lower() == "leads": # .lower() add kiya
                continue
            try:
                if Team_LeadData.objects.filter(call=call).exists():
                    duplicates.append(call)
                    continue

                if request.user.is_team_leader:
                    Team_LeadData.objects.create(
                        call=call,
                        name=name,
                        send=send_val,
                        status=status_val,
                        team_leader=team_leader,
                        user=request.user
                    )
                    created_count += 1
                
                elif request.user.is_superuser:
                    Team_LeadData.objects.create(
                        call=call,
                        name=name,
                        send=send_val,
                        status=status_val,
                        user=request.user
                    )
                    created_count += 1

            except IntegrityError:
                duplicates.append(call)
                continue
            except Exception as e:
                return Response(
                    {"error": f"An error occurred at row {i}: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        message = f"Excel file uploaded successfully! Total Rows: {user_count}, Created: {created_count}, Duplicates Found: {len(duplicates)}"
        
        return Response(
            {
                "message": message,
                "total_rows": user_count,
                "new_leads_created": created_count,
                "duplicates_found": len(duplicates),
                "duplicate_calls_list": duplicates
            },
            status=status.HTTP_201_CREATED
        )


# ===================================================================
# NAYA FREELANCER (ASSOCIATES) DASHBOARD API [FIXED]
# ===================================================================
class FreelancerDashboardAPIView(APIView):
    """
    API for the Super Admin's Freelancer (Associates) Dashboard.
    [FIXED] Ab yeh sahi cards (Total Earning) dikhayega.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request, *args, **kwargs):
        
        # --- 1. Freelancer List ---
        my_staff = Staff.objects.filter(user__is_freelancer=True)
        staff_serializer = ApiStaffSerializer(my_staff, many=True)

        # --- 2. Lead Counts (Sirf Freelancers ke) [EDITED] ---
        total_interested_leads = LeadUser.objects.filter(status="Intrested", assigned_to__user__is_freelancer=True).count()
        total_not_interested_leads = LeadUser.objects.filter(status="Not Interested", assigned_to__user__is_freelancer=True).count()
        total_other_location_leads = LeadUser.objects.filter(status="Other Location", assigned_to__user__is_freelancer=True).count()
        total_not_picked_leads = LeadUser.objects.filter(status="Not Picked", assigned_to__user__is_freelancer=True).count()
        total_visits_leads = LeadUser.objects.filter(status="Visit", assigned_to__user__is_freelancer=True).count()
        # (total_leads aur total_lost_leads hata diye)

        # --- 3. Total Earning Calculation [NEW] ---
        # (Purana salary logic hata diya)
        total_earn_aggregation = Sell_plot.objects.filter(staff__user__is_freelancer=True).aggregate(total_earn=Sum('earn_amount'))
        
        total_earning = total_earn_aggregation.get('total_earn')
        if total_earning is None: # Agar koi sale nahi hui toh 0 dikhao
            total_earning = 0

        # --- 4. Final Response [EDITED] ---
        data = {
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'total_other_location_leads': total_other_location_leads,
            'total_not_picked_leads': total_not_picked_leads,
            'total_visits_leads': total_visits_leads,
            'total_earning': total_earning, # Naya field add kiya
            'my_staff': staff_serializer.data, # Yeh freelancer ki list hai
        }
        
        return Response(data, status=status.HTTP_200_OK)


# ===================================================================
# NAYA IT STAFF LIST API
# ===================================================================
class ITStaffListAPIView(APIView):
    """
    API for the Super Admin's IT Staff list page.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request, *args, **kwargs):
        
        # --- 1. IT Staff List ---
        it_staff_list = Staff.objects.filter(user__is_it_staff=True)
        
        # --- 2. Serialize Data ---
        # Hum pehle waala ApiStaffSerializer use kar rahe hain
        serializer = ApiStaffSerializer(it_staff_list, many=True)

        # --- 3. Final Response ---
        return Response(serializer.data, status=status.HTTP_200_OK)
    




# api.py (AttendanceCalendarAPIView ko isse REPLACE karo)

# ===================================================================
# NAYA ATTENDANCE CALENDAR API [FINAL CORRECT CODE]
# ===================================================================
class AttendanceCalendarAPIView(APIView):
    """
    API provides calendar data, present/absent counts, and color status for each day.
    """
    permission_classes = [IsAuthenticated ] 
    
    def get(self, request, id, *args, **kwargs):
        
        # 1. Get year and month from query parameters
        try:
            year = int(request.query_params.get('year', datetime.today().year))
            month = int(request.query_params.get('month', datetime.today().month))
        except ValueError:
            return Response({"error": "Invalid year or month format."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Get User and Staff Instance
        try:
            if id == 0:
                user_to_check = request.user
            elif id > 0:
                staff_instance = Staff.objects.filter(id=id).last()
                if not staff_instance:
                    return Response({"error": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)
                user_to_check = staff_instance.user
            else:
                return Response({"error": "Invalid ID."}, status=status.HTTP_400_BAD_REQUEST)
        except Staff.DoesNotExist:
             return Response({"error": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)

        # 3. Calendar Data Initialization
        days_in_month = monthrange(year, month)[1]
        
        # Task objects filter karo (assuming Task model represents daily work/presence)
        tasks_for_month = Task.objects.filter(
            user=user_to_check, 
            task_date__month=month, 
            task_date__year=year
        )
        task_dates = {task.task_date for task in tasks_for_month}
        
        present_count = 0
        absent_count = 0
        
        # 4. Structure Data for Calendar (Red/Green Logic)
        weekdays = list(calendar.day_name)
        today = timezone.now().date()
        daily_attendance_list = []
        
        for day in range(1, days_in_month + 1):
            date_obj = datetime(year, month, day).date()
            is_present = date_obj in task_dates
            
            # Future dates ke liye koi status nahi
            if date_obj > today:
                 status_text = "Future"
                 color = "white"
            # Past/Present dates ke liye Red/Green logic
            elif is_present:
                status_text = "Present"
                color = "green"
                present_count += 1
            else:
                status_text = "Absent"
                color = "red"
                absent_count += 1 # Sirf past/today ki dates ko Absent gino

            daily_attendance_list.append({
                "date": date_obj, 
                "has_task": is_present,
                "day_name": weekdays[date_obj.weekday()],
                "status": status_text,
                "status_color": color, 
            })

        # 5. Final Response
        months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]
        
        # Hum naye DailyAttendanceSerializer (jo tumne pichhle fix me banaya tha) use karenge
        calendar_serializer = AttendanceCalendarDaySerializer(daily_attendance_list, many=True)
        
        data = {
            "id": id,
            "user_email": user_to_check.email,
            "month": month,
            "year": year,
            "present_count": present_count,
            "absent_count": absent_count,
            "total_days_checked": days_in_month, # Total days bhi add kar do clarity ke liye
            "days_of_week": days_of_week,
            "calendar_data": calendar_serializer.data,
        }
        
        return Response(data, status=status.HTTP_200_OK)




# ===================================================================
# NAYA STAFF PRODUCTIVITY API
# ===================================================================
class StaffProductivityAPIView(APIView):
    """
    API for the Staff Productivity page.
    Calculates leads, calls, and percentages for staff based on user role and filters.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser] # Use the custom permission

    def get(self, request, *args, **kwargs):
        # 1. Get Filters from query params
        date_filter = request.query_params.get('date', None)
        end_date_str = request.query_params.get('endDate', None)
        teamleader_id = request.query_params.get('teamleader_id', None)
        admin_id = request.query_params.get('admin_id', None)

        # 2. Staff Queryset based on User Role
        staffs = Staff.objects.none() # Start with empty
        fiter_value = 0 # Corresponds to 'fiter' in original view

        if request.user.is_superuser:
            fiter_value = 1
            staffs = Staff.objects.filter(user__user_active=True, user__is_freelancer=False)
            if admin_id:
                staffs = staffs.filter(team_leader__admin=admin_id)
            if teamleader_id:
                staffs = staffs.filter(team_leader=teamleader_id)
        
        elif request.user.is_admin:
            fiter_value = 4
            staffs = Staff.objects.filter(team_leader__admin__self_user=request.user, user__user_active=True, user__is_freelancer=False)
            if teamleader_id:
                staffs = staffs.filter(team_leader=teamleader_id)

        elif request.user.is_team_leader:
            fiter_value = 2
            user_instance = request.user.username
            team_leader_instance = Team_Leader.objects.filter(email=user_instance).last()
            staffs = Staff.objects.filter(team_leader=team_leader_instance, user__user_active=True, user__is_freelancer=False)
        
        total_staff_count = staffs.count()

        # 3. Initialize totals and staff data list
        staff_data_list = []
        total_all_leads = 0
        total_all_interested = 0
        total_all_not_interested = 0
        total_all_other_location = 0
        total_all_not_picked = 0
        total_all_lost = 0
        total_all_visit = 0
        total_all_calls = 0

        # 4. Date Filter Logic
        lead_filter = {}
        lead_filter1 = {}
        date_filter_applied = False
        
        if date_filter and end_date_str:
            try:
                start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
                end_date_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(end_date_dt + timedelta(days=1)) - timedelta(seconds=1)
                lead_filter = {'updated_date__range': [start_date, end_date]}
                lead_filter1 = {'created_date__range': [start_date, end_date]}
                date_filter_applied = True
            except ValueError:
                pass # Invalid date format, filters will be empty
        
        elif date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                lead_filter = {'updated_date__date': date_obj}
                lead_filter1 = {'created_date__date': date_obj}
                date_filter_applied = True
            except ValueError:
                pass # Invalid date format

        # 5. Loop and Aggregate Data
        for staff in staffs:
            
            # Date filter logic from original view
            if date_filter_applied:
                leads_by_date = LeadUser.objects.filter(
                    assigned_to=staff, **lead_filter
                ).aggregate(
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                
                leads_by_date1 = LeadUser.objects.filter(
                    assigned_to=staff, **lead_filter1
                ).aggregate(
                    total_leads=Count('id'),
                )
            
            else: # No date filter applied (original 'else' block)
                leads_by_date_all = LeadUser.objects.filter(assigned_to=staff).aggregate(
                    total_leads=Count('id'),
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date = leads_by_date_all
                leads_by_date1 = {'total_leads': leads_by_date_all['total_leads']}

            
            # Calculations
            total_calls = (
                leads_by_date.get('interested', 0) + 
                leads_by_date.get('not_interested', 0) + 
                leads_by_date.get('other_location', 0) + 
                leads_by_date.get('not_picked', 0) + 
                leads_by_date.get('lost', 0) + 
                leads_by_date.get('visit', 0)
            )
            total_leads_for_staff = leads_by_date1.get('total_leads', 0)
            visit_percentage = (leads_by_date.get('visit', 0) / total_leads_for_staff * 100) if total_leads_for_staff > 0 else 0
            interested_percentage = (leads_by_date.get('interested', 0) / total_leads_for_staff * 100) if total_leads_for_staff > 0 else 0

            staff_data_list.append({
                'id': staff.id,
                'name': staff.name,
                'total_leads': total_leads_for_staff,
                'interested': leads_by_date.get('interested', 0),
                'not_interested': leads_by_date.get('not_interested', 0),
                'other_location': leads_by_date.get('other_location', 0),
                'not_picked': leads_by_date.get('not_picked', 0),
                'lost': leads_by_date.get('lost', 0),
                'visit': leads_by_date.get('visit', 0),
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
            })

            # Add to grand totals
            total_all_leads += total_leads_for_staff
            total_all_interested += leads_by_date.get('interested', 0)
            total_all_not_interested += leads_by_date.get('not_interested', 0)
            total_all_other_location += leads_by_date.get('other_location', 0)
            total_all_not_picked += leads_by_date.get('not_picked', 0)
            total_all_lost += leads_by_date.get('lost', 0)
            total_all_visit += leads_by_date.get('visit', 0)
            total_all_calls += total_calls
        
        # 6. Calculate Grand Totals
        total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
        total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        # 7. Get data for filters (Admins and Team Leaders)
        admins_qs = Admin.objects.all()
        teamleader_qs = Team_Leader.objects.filter(admin__self_user=request.user)
        
        admins_data = DashboardAdminSerializer(admins_qs, many=True).data
        teamleader_data = ProductivityTeamLeaderSerializer(teamleader_qs, many=True).data
        staff_data_serialized = StaffProductivityDataSerializer(staff_data_list, many=True).data

        # 8. Build Final Response
        data = {
            'staff_data': staff_data_serialized,
            'selected_date': date_filter,
            'total_all_leads': total_all_leads,
            'total_all_interested': total_all_interested,
            'total_all_not_interested': total_all_not_interested,
            'total_all_other_location': total_all_other_location,
            'total_all_not_picked': total_all_not_picked,
            'total_all_lost': total_all_lost,
            'total_all_visit': total_all_visit,
            'total_all_calls': total_all_calls,
            'total_visit_percentage': round(total_visit_percentage, 2),
            'total_interested_percentage': round(total_interested_percentage, 2),
            'total_staff_count': total_staff_count,
            'admins_filter_list': admins_data,
            'teamleader_filter_list': teamleader_data,
            'fiter': fiter_value,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    



# ===================================================================
# NAYA TEAM LEADER PRODUCTIVITY API [FIXED]
# ===================================================================
class TeamLeaderProductivityAPIView(APIView):
    """
    API for the Team Leader Productivity page.
    [FIXED] Ab yeh date, endDate, aur no-date, teeno filters ko sahi se handle karega.
    """
    permission_classes = [IsAuthenticated, CustomIsSuperuser] # Sirf admin/superuser hi dekh sakte hain

    def get(self, request, *args, **kwargs):
        # 1. Get Filters from query params
        date_filter = request.query_params.get('date', None)
        end_date_str = request.query_params.get('endDate', None)
        admin_id = request.query_params.get('admin_id', None)
        
        # 2. Team Leader Queryset based on User Role
        team_leaders = Team_Leader.objects.none()
        fiter_value = 0

        if request.user.is_superuser:
            fiter_value = 3
            team_leaders = Team_Leader.objects.filter(user__user_active=True)
            if admin_id:
                team_leaders = team_leaders.filter(admin=admin_id)
        
        elif request.user.is_admin:
            fiter_value = 5
            team_leaders = Team_Leader.objects.filter(admin__self_user=request.user, user__user_active=True)
            if admin_id: # Admin bhi admin_id se filter kar sakta hai (original code ke hisaab se)
                team_leaders = team_leaders.filter(admin=admin_id)
        
        elif request.user.is_team_leader:
             return Response({"error": "Team Leaders cannot view this page."}, status=status.HTTP_403_FORBIDDEN)

        total_team_leaders_count = team_leaders.count()

        # 3. Initialize totals and data list
        team_leader_data_list = []
        total_all_leads = 0
        total_all_interested = 0
        total_all_not_interested = 0
        total_all_other_location = 0
        total_all_not_picked = 0
        total_all_lost = 0
        total_all_visit = 0
        total_all_calls = 0

        # 4. Loop over each Team Leader and Aggregate Data
        for team_leader in team_leaders:
            leads_data_agg = {
                'total_leads': 0, 'interested': 0, 'not_interested': 0,
                'other_location': 0, 'not_picked': 0, 'lost': 0, 'visit': 0
            }
            
            staff_members = Staff.objects.filter(team_leader=team_leader)

            for staff in staff_members:
                
                # --- YEH HAI FIX KI HUI DATE LOGIC ---
                lead_filter = {}
                lead_filter1 = {}
                
                # Condition 1: Start aur End Date dono hain
                if date_filter and end_date_str:
                    try:
                        start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
                        end_date_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
                        end_date = timezone.make_aware(end_date_dt + timedelta(days=1)) - timedelta(seconds=1)
                        lead_filter = {'updated_date__range': [start_date, end_date]}
                        lead_filter1 = {'created_date__range': [start_date, end_date]}
                    except ValueError:
                        pass # Galat format, filter khaali rahega
                
                # Condition 2: Sirf Start Date hai
                elif date_filter:
                    try:
                        date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                        lead_filter = {'updated_date__date': date_obj}
                        lead_filter1 = {'created_date__date': date_obj}
                    except ValueError:
                        pass # Galat format

                # Condition 3: Koi filter nahi hai (yeh default 'else' hai)
                
                # Ab aggregation query chalao
                if lead_filter or lead_filter1:
                     leads_by_date = LeadUser.objects.filter(
                        assigned_to=staff, **lead_filter
                    ).aggregate(
                        interested=Count('id', filter=Q(status='Intrested')),
                        not_interested=Count('id', filter=Q(status='Not Interested')),
                        other_location=Count('id', filter=Q(status='Other Location')),
                        not_picked=Count('id', filter=Q(status='Not Picked')),
                        lost=Count('id', filter=Q(status='Lost')),
                        visit=Count('id', filter=Q(status='Visit'))
                    )
                     leads_by_date1 = LeadUser.objects.filter(
                        assigned_to=staff, **lead_filter1
                    ).aggregate(total_leads=Count('id'))
                else:
                    # Koi date filter nahi
                    leads_by_date_all = LeadUser.objects.filter(assigned_to=staff).aggregate(
                        total_leads=Count('id'),
                        interested=Count('id', filter=Q(status='Intrested')),
                        not_interested=Count('id', filter=Q(status='Not Interested')),
                        other_location=Count('id', filter=Q(status='Other Location')),
                        not_picked=Count('id', filter=Q(status='Not Picked')),
                        lost=Count('id', filter=Q(status='Lost')),
                        visit=Count('id', filter=Q(status='Visit'))
                    )
                    leads_by_date = leads_by_date_all
                    leads_by_date1 = {'total_leads': leads_by_date_all['total_leads']}

                # Staff ka data Team Leader ke data mein add karo
                leads_data_agg['total_leads'] += leads_by_date1.get('total_leads', 0)
                leads_data_agg['interested'] += leads_by_date.get('interested', 0)
                leads_data_agg['not_interested'] += leads_by_date.get('not_interested', 0)
                leads_data_agg['other_location'] += leads_by_date.get('other_location', 0)
                leads_data_agg['not_picked'] += leads_by_date.get('not_picked', 0)
                leads_data_agg['lost'] += leads_by_date.get('lost', 0)
                leads_data_agg['visit'] += leads_by_date.get('visit', 0)

            # Staff loop ke baad, Team Leader ka total calculate karo
            total_calls_tl = (
                leads_data_agg['interested'] + leads_data_agg['not_interested'] + 
                leads_data_agg['other_location'] + leads_data_agg['not_picked'] + 
                leads_data_agg['lost'] + leads_data_agg['visit']
            )
            visit_percentage = (leads_data_agg['visit'] / leads_data_agg['total_leads'] * 100) if leads_data_agg['total_leads'] > 0 else 0
            interested_percentage = (leads_data_agg['interested'] / leads_data_agg['total_leads'] * 100) if leads_data_agg['total_leads'] > 0 else 0

            team_leader_data_list.append({
                'id': team_leader.id,
                'name': team_leader.name,
                'total_leads': leads_data_agg['total_leads'],
                'interested': leads_data_agg['interested'],
                'not_interested': leads_data_agg['not_interested'],
                'other_location': leads_data_agg['other_location'],
                'not_picked': leads_data_agg['not_picked'],
                'lost': leads_data_agg['lost'],
                'visit': leads_data_agg['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls_tl,
            })

            # Grand totals mein add karo
            total_all_leads += leads_data_agg['total_leads']
            total_all_interested += leads_data_agg['interested']
            total_all_not_interested += leads_data_agg['not_interested']
            total_all_other_location += leads_data_agg['other_location']
            total_all_not_picked += leads_data_agg['not_picked']
            total_all_lost += leads_data_agg['lost']
            total_all_visit += leads_data_agg['visit']
            total_all_calls += total_calls_tl
        
        # 6. Calculate Grand Totals
        total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
        total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        # 7. Get data for filters (Admins)
        admins_qs = Admin.objects.all()
        admins_data = DashboardAdminSerializer(admins_qs, many=True).data
        team_leader_data_serialized = StaffProductivityDataSerializer(team_leader_data_list, many=True).data

        # 8. Build Final Response
        data = {
            'staff_data': team_leader_data_serialized,
            'selected_date': date_filter,
            'task_type': 'teamleader',
            'total_all_leads': total_all_leads,
            'total_all_interested': total_all_interested,
            'total_all_not_interested': total_all_not_interested,
            'total_all_other_location': total_all_other_location,
            'total_all_not_picked': total_all_not_picked,
            'total_all_lost': total_all_lost,
            'total_all_visit': total_all_visit,
            'total_all_calls': total_all_calls,
            'total_visit_percentage': round(total_visit_percentage, 2),
            'total_interested_percentage': round(total_interested_percentage, 2),
            'total_staff_count': total_team_leaders_count,
            'admins_filter_list': admins_data,
            'fiter': fiter_value,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    



# ===================================================================
# NAYA ADMIN ADD API
# ===================================================================
class AdminAddAPIView(APIView):
    """
    API Superuser ke liye naya Admin user banane ke liye.
    """
    permission_classes = [IsAuthenticated, CustomIsSuperuser] # Sirf Superuser hi Admin add kar sakta hai
    parser_classes = (MultiPartParser, FormParser) # File upload (profile_image) ke liye

    def post(self, request, *args, **kwargs):
        # Serializer ko request context do taaki woh request.user le sake
        serializer = AdminCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            admin_instance = serializer.save()
            
            # Naye bane hue admin ka poora data dikhao
            read_serializer = DashboardAdminSerializer(admin_instance)
            
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        
        # Agar validation fail ho
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






# ===================================================================
# NAYA ADMIN EDIT API (GET / PATCH)
# ===================================================================
class AdminEditAPIView(APIView):
    """
    API ek Admin ki profile ko Get aur Update karne ke liye.
    """
    permission_classes = [IsAuthenticated, CustomIsSuperuser] # Sirf Superuser hi edit kar sakta hai
    parser_classes = (MultiPartParser, FormParser) # profile_image upload ke liye

    def get_object(self, id):
        """
        Helper method se Admin object get karo
        """
        try:
            return Admin.objects.get(id=id)
        except Admin.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        """
        Ek Admin ki poori details fetch karo.
        """
        admin = self.get_object(id)
        # Data dikhane ke liye DashboardAdminSerializer (jo pehle banaya tha) use karo
        serializer = DashboardAdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id, *args, **kwargs):
        """
        Ek Admin ki profile ko update karo (partial update).
        """
        admin = self.get_object(id)
        # Data update karne ke liye naya 'AdminUpdateSerializer' use karo
        serializer = AdminUpdateSerializer(admin, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_admin = serializer.save()
            # Updated data dikhane ke liye read serializer ka use karo
            read_serializer = DashboardAdminSerializer(updated_admin)
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        
        # Agar error aaye
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# --- Pagination Class (Taaki 10-10 leads karke page mein data aaye) ---
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ===================================================================
# NAYA TEAM CUSTOMER (INTERESTED) LEADS API
# ===================================================================
class TeamCustomerLeadsAPIView(APIView):

    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination # Reuse pagination

    @property
    def paginator(self):
        """Paginator instance for the view."""
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        return self._paginator

    def get(self, request, tag, *args, **kwargs):
        
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        user = request.user
        
        search_query = request.query_params.get('search', None)
        
        # Default empty queryset and serializer
        interested_leads_qs = LeadUser.objects.none()
        serializer_class = ApiLeadUserSerializer # Default serializer

        # --- 1. Search Logic (Yeh sabse pehle check hota hai) ---
        if search_query:
            interested_leads_qs = LeadUser.objects.filter(
                Q(name__icontains=search_query) | 
                Q(call__icontains=search_query) | 
                Q(team_leader__name__icontains=search_query),
                status='Intrested'
            )
            serializer_class = ApiLeadUserSerializer
        
        # --- 2. Superuser Logic ---
        elif user.is_superuser:
            if tag == 'pending_follow':
                interested_leads_qs = LeadUser.objects.filter(
                    Q(status='Intrested') & Q(follow_up_date__isnull=False)
                ).order_by('-updated_date')
            elif tag == 'today_follow':
                interested_leads_qs = LeadUser.objects.filter(
                    Q(status='Intrested') & Q(follow_up_date=today)
                ).order_by('-updated_date')
            elif tag == 'tommorrow_follow':
                interested_leads_qs = LeadUser.objects.filter(
                    Q(status='Intrested') & Q(follow_up_date=tomorrow)
                ).order_by('-updated_date')
            else: # 'else' matlab koi bhi tag ya default 'interested' tag
                interested_leads_qs = LeadUser.objects.filter(status='Intrested').order_by('-updated_date')
            
            serializer_class = ApiLeadUserSerializer

        # --- 3. Team Leader Logic ---
        elif user.is_team_leader:
            try:
                team_leader_instance = Team_Leader.objects.get(user=user)
            except Team_Leader.DoesNotExist:
                 return Response({"error": "Team Leader profile not found."}, status=status.HTTP_404_NOT_FOUND)

            if tag == 'pending_follow':
                interested_leads_qs = LeadUser.objects.filter(
                    Q(status='Intrested') & Q(follow_up_date__isnull=False),
                    team_leader=team_leader_instance,
                ).order_by('-updated_date')
            elif tag == 'today_follow':
                interested_leads_qs = LeadUser.objects.filter(
                    Q(status='Intrested') & Q(follow_up_date=today),
                    team_leader=team_leader_instance,
                ).order_by('-updated_date')
            elif tag == 'tommorrow_follow':
                interested_leads_qs = LeadUser.objects.filter(
                    Q(status='Intrested') & Q(follow_up_date=tomorrow),
                    team_leader=team_leader_instance,
                ).order_by('-updated_date')
            else: # Default 'interested' tag
                interested_leads_qs = LeadUser.objects.filter(
                    follow_up_time__isnull=True, 
                    team_leader=team_leader_instance,
                    status='Intrested'
                ).order_by('-updated_date')
            
            serializer_class = ApiLeadUserSerializer

        # --- 4. Staff Logic (Original code ka 'else' block) ---
        # (Aapke original code ke hisaab se staff user Team_LeadData dekhta hai)
        else:
            try:
                # Yahaan logic thoda ajeeb hai, hum user ke email se Team Leader dhoondh rahe hain
                # Hum original code ko follow karenge
                team_leader = Team_Leader.objects.filter(email=user.email).last()
                if team_leader:
                    interested_leads_qs = Team_LeadData.objects.filter(team_leader=team_leader, status='Intrested')
                    serializer_class = ApiTeamLeadDataSerializer # Serializer badal gaya
                else:
                    # Agar staff/admin user ka email Team Leader se match nahi hota
                     interested_leads_qs = Team_LeadData.objects.none()
                     serializer_class = ApiTeamLeadDataSerializer
            except Exception:
                 return Response({"error": "Could not determine user role for this view."}, status=status.HTTP_400_BAD_REQUEST)


        # --- 5. Paginate aur Serialize ---
        paginated_qs = self.paginator.paginate_queryset(interested_leads_qs, request, view=self)
        serializer = serializer_class(paginated_qs, many=True)
        
        # Paginator se poora response structure banwao (jisme next, previous, count, results honge)
        return self.paginator.get_paginated_response(serializer.data)
    



# ===================================================================
# NAYA USER ACTIVE TOGGLE API [FIXED]
# ===================================================================
class ToggleUserActiveAPIView(APIView):
    """
    API to toggle the 'user_active' status for Staff, Admin, or TeamLeader.
    [FIXED] Ab yeh 'is_active' ko string ("true" ya "false") ki tarah handle karega.
    """
    permission_classes = [IsAuthenticated, CustomIsSuperuser] # Sirf manager/admin hi yeh kar sakte hain

    def post(self, request, *args, **kwargs):
        # request.data 'form-data' aur 'json' dono handle karta hai
        user_id = request.data.get('user_id')
        user_type = request.data.get('user_type')
        is_active_str = request.data.get('is_active') # Value ko string ki tarah lo

        if not all([user_id, user_type, is_active_str is not None]):
            return Response(
                {"error": "user_id (profile_id), user_type, aur is_active zaroori hain."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # --- YEH HAI FIX ---
        # String "true" (kisi bhi case mein) ko boolean true mein badlo
        is_active_bool = str(is_active_str).lower() == 'true'
        
        user_instance_email = None
        try:
            # 1. Profile ID se profile dhoondo
            if user_type == 'staff':
                profile = Staff.objects.get(id=user_id)
                user_instance_email = profile.email
            elif user_type == 'admin':
                profile = Admin.objects.get(id=user_id)
                user_instance_email = profile.email
            elif user_type == 'teamlead':
                profile = Team_Leader.objects.get(id=user_id)
                user_instance_email = profile.email
            else:
                return Response(
                    {"error": "Invalid user_type. Sirf 'staff', 'admin', ya 'teamlead' allowed hai."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except (Staff.DoesNotExist, Admin.DoesNotExist, Team_Leader.DoesNotExist):
             return Response(
                {"error": f"Profile not found for user_type '{user_type}' with id {user_id}."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not user_instance_email:
            return Response({"error": "Profile mil gayi lekin usse koi email linked nahi hai."}, status=status.HTTP_404_NOT_FOUND)

        # 2. Ab email se User ko dhoondo aur update karo
        try:
            user_to_update = User.objects.get(email=user_instance_email)
            user_to_update.user_active = is_active_bool # Sahi boolean value save karo
            user_to_update.save()
            
            return Response(
                {
                    'status': 'success', 
                    'user_email': user_to_update.email,
                    'user_active_is_now': user_to_update.user_active
                },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": f"User not found with email {user_instance_email}."},
                status=status.HTTP_404_NOT_FOUND
            )



# home/api.py (Purana wala delete karke yeh dono add karo)

# ==========================================================
# API: SUPERUSER STAFF LEADS (BY STATUS)
# ==========================================================
class SuperUserStaffLeadsAPIView(APIView):

    permission_classes = [IsAuthenticated, CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination 

    def get(self, request, tag, format=None):
        paginator = self.pagination_class()
        
        # Superuser ko saare leads milte hain
        base_queryset = LeadUser.objects.all()

        status_map = {
            'total_lead': 'Leads',
            'visits': 'Visit',
            'interested': 'Intrested',
            'not_interested': 'Not Interested',
            'other_location': 'Other Location',
            'not_picked': 'Not Picked',
            'lost': 'Lost'
        }

        if tag in status_map:
            queryset = base_queryset.filter(status=status_map[tag])
        else:
            return Response(
                {"error": f"Invalid tag: {tag}. Valid tags are: {list(status_map.keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = queryset.order_by('-updated_date')
        
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = ApiLeadUserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ApiLeadUserSerializer(queryset, many=True)
        return Response(serializer.data)

# ==========================================================
# API: ADMIN STAFF LEADS (BY STATUS)
# ==========================================================
class AdminStaffLeadsAPIView(APIView):
    """
    API endpoint SIRF ADMIN ke liye, jo 'tag' ke hisaab se leads filter karta hai.
    """
    # Permission check: Sirf logged-in Admin (is_admin=True) hi access kar sakta hai
    permission_classes = [IsAuthenticated, IsCustomAdminUser] 
    pagination_class = StandardResultsSetPagination

    def get(self, request, tag, format=None):
        paginator = self.pagination_class()
        user = request.user
        
        # Admin ko sirf apne team leaders ke leads milte hain
        # Admin profile ko 'user' (AbstractUser) se dhoondo
        admin_instance = Admin.objects.filter(user=user).last() 
        if not admin_instance:
            # Aapke purane code me self_user tha, lekin naye me 'user' hona chahiye
            # Hum dono check kar lete hain
            admin_instance = Admin.objects.filter(self_user=user).last()
            if not admin_instance:
                 return Response({"error": "Admin profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        teamleader_instance = Team_Leader.objects.filter(admin=admin_instance)
        base_queryset = LeadUser.objects.filter(team_leader__in=teamleader_instance)

        status_map = {
            'total_lead': 'Leads',
            'visits': 'Visit',
            'interested': 'Intrested',
            'not_interested': 'Not Interested',
            'other_location': 'Other Location',
            'not_picked': 'Not Picked',
            'lost': 'Lost'
        }

        if tag in status_map:
            queryset = base_queryset.filter(status=status_map[tag])
        else:
            return Response(
                {"error": f"Invalid tag: {tag}. Valid tags are: {list(status_map.keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = queryset.order_by('-updated_date')
        
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = ApiLeadUserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ApiLeadUserSerializer(queryset, many=True)
        return Response(serializer.data)

# ===================================================================
# NAYA STAFF ADD API [FIXED]
# ===================================================================
class StaffAddAPIView(APIView):
    """
    API naya Staff user banane ke liye.
    (Team Leader, Admin, ya Superuser chala sakta hai)
    [FIXED] UnboundLocalError ko fix kiya gaya hai.
    """
    permission_classes = [CustomIsSuperuser] # Sirf manager/admin hi add kar sakte hain
    parser_classes = (MultiPartParser, FormParser) # File upload (profile_image) ke liye

    def post(self, request, *args, **kwargs):
        serializer = StaffCreateSerializer(data=request.data, context={'request': request})
        
        # Pehle check karo ki data valid hai ya nahi
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Agar valid hai, tab save karo
        try:
            staff_instance = serializer.save()
        except Exception as e:
            # Agar .save() fail hota hai (jo serializer ke create method mein fail ho sakta hai)
            return Response({"error": f"Failed to save serializer: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Agar save successful hua, tab response serialize karo
        try:
            # Hum 'StaffProfileSerializer' ka use karenge jisme saari details hain
            read_serializer = StaffProfileSerializer(staff_instance, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Agar response serialize fail ho, toh bhi success batao
            return Response(
                {"message": f"Staff created (ID: {staff_instance.id}) but response serialization failed: {e}"}, 
                status=status.HTTP_201_CREATED
            )
        


# ===================================================================
# NAYA TEAM LEADER ADD API (ADD_TEAM_LEADER_USER)
# ===================================================================
class TeamLeaderAddAPIView(APIView):
    """
    API naya Team Leader user banane ke liye.
    (Superuser ya Admin chala sakta hai)
    """
    permission_classes = [CustomIsSuperuser] # Sirf manager/admin hi add kar sakte hain
    parser_classes = (MultiPartParser, FormParser) # File upload (profile_image) ke liye

    def post(self, request, *args, **kwargs):
        # 1. Validation: Superuser ke liye Admin ID zaroori hai agar woh khud Admin nahi hai
        if request.user.is_superuser and not request.data.get('admin_id'):
            # Note: Agar Superuser khud Team Leader ka admin banta hai, tab Admin ID dena padega.
            return Response({"error": "Admin ID is required for Superusers to assign the new Team Leader."}, status=status.HTTP_400_BAD_REQUEST)
            
        # 2. Serializer ko data aur context do
        # Context mein request bhejo taaki Admin/Superuser ka role pata chale
        serializer = TeamLeaderCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                team_leader_instance = serializer.save()
            except Exception as e:
                # Agar custom create() function mein error aaye
                 return Response({"error": f"Failed to save: {e}"}, status=status.HTTP_400_BAD_REQUEST)
            
            # 3. Naye bane hue team leader ka poora data dikhao
            read_serializer = ProductivityTeamLeaderSerializer(team_leader_instance, context={'request': request})
            
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        
        # 4. Validation fail hone par errors dikhao
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# home/api.py

# ===================================================================
# NAYA TEAM LEADER EDIT API (GET / PATCH) [PERMISSION FIX]
# ===================================================================
class TeamLeaderEditAPIView(APIView):
    """
    API ek Team Leader ki profile ko Get aur Update karne ke liye (teamedit function).
    [FIX]: Ab yeh SIRF SUPERUSER ko allow karega.
    """
    
    # --- [YEH RAHA PERMISSION FIX] ---
    # IsCustomAdminUser ko CustomIsSuperuser se badal diya
    permission_classes = [IsAuthenticated, CustomIsSuperuser] 
    
    parser_classes = (MultiPartParser, FormParser) # profile_image upload ke liye

    def get_object(self, id):
        """
        Helper method se Team_Leader object get karo
        """
        try:
            return Team_Leader.objects.get(id=id)
        except Team_Leader.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        """
        Ek Team Leader ki poori details fetch karo.
        """
        teamleader = self.get_object(id)
        # Data dikhane ke liye ProductivityTeamLeaderSerializer use karo
        serializer = ProductivityTeamLeaderSerializer(teamleader, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id, *args, **kwargs):
        """
        Ek Team Leader ki profile ko update karo (PATCH).
        """
        teamleader = self.get_object(id)
        # Data update karne ke liye TeamLeaderUpdateSerializer use karo
        serializer = TeamLeaderUpdateSerializer(teamleader, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_teamleader = serializer.save()
            # Updated data dikhane ke liye read serializer ka use karo
            read_serializer = ProductivityTeamLeaderSerializer(updated_teamleader, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        
        # Agar error aaye
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id, *args, **kwargs):
        # POST ko bhi PATCH ki tarah handle karo
        return self.patch(request, id, format)




# ===================================================================
# NAYA STAFF EDIT API (GET / PATCH)
# ===================================================================
class StaffEditAPIView(APIView):
    """
    API ek Staff/Freelancer ki profile ko Get aur Update karne ke liye.
    """
    permission_classes = [CustomIsSuperuser] # Sirf Admin/TL/Superuser hi edit kar sakta hai
    parser_classes = (MultiPartParser, FormParser) # profile_image upload ke liye

    def get_object(self, id):
        """
        Helper method se Staff object get karo
        """
        try:
            return Staff.objects.get(id=id)
        except Staff.DoesNotExist:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        """
        Ek Staff/Freelancer ki poori details fetch karo.
        """
        staff = self.get_object(id)
        # Data dikhane ke liye FullStaffSerializer use karo (jo humne pichhle fix mein banaya tha)
        serializer = FullStaffSerializer(staff, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id, *args, **kwargs):
        """
        Ek Staff/Freelancer ki profile ko update karo (PATCH).
        """
        staff = self.get_object(id)
        # Data update karne ke liye StaffUpdateSerializer use karo
        serializer = StaffUpdateSerializer(staff, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_staff = serializer.save()
            # Updated data dikhane ke liye read serializer ka use karo
            read_serializer = StaffProfileSerializer(updated_staff, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        
        # Agar error aaye
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# ===================================================================
# NAYA INCENTIVE SLAB API
# ===================================================================
class IncentiveSlabStaffAPIView(APIView):

    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request, staff_id, *args, **kwargs):

        # 1. Filters and Params
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        # 2. Base Query and User Type Check
        sell_property_qs = Sell_plot.objects.none()
        total_earn = 0
        user_type = None
        
        # Agar user khud Staff hai, toh apni email se filter karega
        if request.user.is_staff_new and staff_id == request.user.id:
            # Note: User ki ID aur staff ki ID alag ho sakti hai. 
            # Hum current user ke email se filter karenge jaisa views.py mein tha
            staff_email = request.user.email
            sell_property_qs = Sell_plot.objects.filter(
                staff__email=staff_email, 
                updated_date__year=year,
                updated_date__month=month
            )
            # Freelancer check
            user_type = request.user.is_freelancer
            
        # Agar Superuser, Team Leader, ya Admin check kar rahe hain
        elif request.user.is_superuser or request.user.is_team_leader or request.user.is_admin:
            
            # Agar staff_id=0 bheja gaya ho toh error de do (kyunki yahaan staff_id zaroori hai)
            if int(staff_id) == 0:
                 return Response({"error": "Staff ID is required."}, status=status.HTTP_400_BAD_REQUEST)
                 
            sell_property_qs = Sell_plot.objects.filter(
                staff__id=staff_id, 
                updated_date__year=year,
                updated_date__month=month
            )
            
            # Freelancer status check (Jaisa views.py mein tha)
            try:
                staff_instance = Staff.objects.get(id=staff_id)
                user_type = staff_instance.user.is_freelancer
            except Staff.DoesNotExist:
                 return Response({"error": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)

        else:
             return Response({"error": "You do not have permission for this action."}, status=status.HTTP_403_FORBIDDEN)
        
        
        # 3. Aggregate Total Earnings
        total_earn_amount = sell_property_qs.aggregate(total_earn=Sum('earn_amount'))
        total_earn = total_earn_amount['total_earn'] if total_earn_amount['total_earn'] else 0
        
        # 4. Serialize Data
        slab_data = Slab.objects.all()
        
        response_data = {
            'sell_property': SellPlotSerializer(sell_property_qs.order_by('-created_date'), many=True).data,
            'slab': SlabSerializer(slab_data, many=True).data, # Slab data poora bhejo
            'total_earn': total_earn,
            'year': year,
            'month': month,
            'months_list': [(i, month_name[i]) for i in range(1, 13)],
            'user_type': user_type, # True/False
        }
        return Response(response_data, status=status.HTTP_200_OK)


# ===================================================================
# NAYA STAFF PRODUCTIVITY CALENDAR API [FINAL CORRECT CODE]
# ===================================================================
class StaffProductivityCalendarAPIView(APIView):
    """
    API fetches Staff productivity data (leads and calculated salary) 
    for a specific month and year, structured for a calendar view.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    
    def get(self, request, staff_id, *args, **kwargs):
        
        # 1. Get year and month from query parameters
        try:
            year = int(request.query_params.get('year', datetime.now().year))
            month = int(request.query_params.get('month', datetime.now().month))
        except ValueError:
            return Response({"error": "Invalid year or month format."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Get Staff Instance and Authorization Check
        try:
            # First try to get staff by Staff ID
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            # Agar Staff ID se nahi mila, aur user staff hai, toh user__id se try karo
            if staff_id == request.user.id and not request.user.is_superuser:
                 staff = Staff.objects.get(user=request.user)
            else:
                return Response({"error": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        # Permission Check: Superuser/Admin/TL या Staff खुद ही देख सकता है
        if not (user.is_superuser or user.is_admin or user.is_team_leader or user.id == staff.user.id):
             return Response({"error": "You do not have permission to view this calendar."}, status=status.HTTP_403_FORBIDDEN)

        # 3. Calculation Setup
        days_in_month = monthrange(year, month)[1]
        salary_arg = staff.salary if staff.salary else 0
        
        try:
            salary_float = float(salary_arg)
        except ValueError:
            salary_float = 0

        daily_salary = round(salary_float / days_in_month) if days_in_month > 0 else 0

        # 4. Data Aggregation
        leads_data = LeadUser.objects.filter(
            assigned_to=staff,
            updated_date__year=year,
            updated_date__month=month,
            status='Intrested'
        ).values('updated_date__day').annotate(count=Count('id'))

        productivity_data_dict = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}
        total_salary = 0
        
        # 5. Calculate Daily Productivity and Salary
        for lead in leads_data:
            day = lead['updated_date__day']
            leads_count = lead['count']
            
            if leads_count >= 10:
                daily_earned_salary = daily_salary
            else:
                daily_earned_salary = round((daily_salary / 10) * leads_count, 2)
            
            productivity_data_dict[day] = {'leads': leads_count, 'salary': daily_earned_salary}
            total_salary += daily_earned_salary

        # 6. Structure Data for Calendar
        weekdays = list(calendar.day_name)
        
        productivity_list = []
        for day in range(1, days_in_month + 1):
            date_obj = datetime(year, month, day).date()
            day_data = productivity_data_dict.get(day, {'leads': 0, 'salary': 0})
            
            productivity_list.append({
                'day': day,
                'date': date_obj, # Date object rehne do, serializer handle karega
                'day_name': weekdays[date_obj.weekday()],
                'leads': day_data['leads'],
                'salary': day_data['salary']
            })

        # 7. Final Response
        months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]

        response_data = {
            'staff': StaffProfileSerializer(staff, context={'request': request}).data,
            'year': year,
            'month': month,
            'monthly_salary': salary_arg,
            'total_salary': round(total_salary, 2),
            'months_list': months_list,
            'daily_productivity_data': DailyProductivitySerializer(productivity_list, many=True).data, # Serializer use karo
        }

        return Response(response_data, status=status.HTTP_200_OK)  




# ===================================================================
# NAYA TEAM LEADER PERTICULAR LEADS API
# ===================================================================
class TeamLeaderParticularLeadsAPIView(APIView):
    """
    API fetches leads assigned to a specific staff member (ID) filtered by status tag.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination # Reuse Standard pagination

    @property
    def paginator(self):
        """Paginator instance for the view."""
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        return self._paginator

    def get(self, request, id, tag, *args, **kwargs):
        
        # 1. Base Query based on Tag
        tag = tag.lower()
        if tag == "intrested":
            status_filter = {'status': 'Intrested'}
        elif tag == "not interested":
            status_filter = {'status': 'Not Interested'}
        elif tag == "other location":
            status_filter = {'status': 'Other Location'}
        elif tag == "lost":
            status_filter = {'status': 'Lost'}
        elif tag == "visit":
            status_filter = {'status': 'Visit'}
        elif tag == "all":
            status_filter = {} # No status filter, shows all leads
        else:
            status_filter = {'status': tag.capitalize()} # Catch other statuses

        
        # 2. Final Query: Filter by Staff ID and Status
        staff_leads_qs = LeadUser.objects.filter(
            assigned_to__id=id, # Staff ID se filter karo
            **status_filter
        ).order_by('-updated_date')
        
        # 3. Paginate aur Serialize
        paginated_qs = self.paginator.paginate_queryset(staff_leads_qs, request, view=self)
        serializer = ApiLeadUserSerializer(paginated_qs, many=True)
        
        # 4. Response mein meta data aur leads bhejo
        response = self.paginator.get_paginated_response(serializer.data)
        response.data['staff_id'] = id
        response.data['status_tag'] = tag
        
        return response
    


# ===================================================================
# NAYA ADMIN PRODUCTIVITY API
# ===================================================================
class AdminProductivityAPIView(APIView):
    """
    API fetches total productivity (aggregated leads/calls) for ALL Admin users.
    (Views.py ka 'admin_productivity_view' function)
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser] # Sirf Superuser chala sakta hai
    
    def get(self, request, *args, **kwargs):
        
        # 1. Retrieve all active Admin profiles
        admin_profiles = Admin.objects.filter(self_user__user_active=True)
        total_admins_count = admin_profiles.count()

        # 2. Initialize totals and data list
        admin_data_list = []
        total_all_leads = 0
        total_all_interested = 0
        total_all_not_interested = 0
        total_all_other_location = 0
        total_all_not_picked = 0
        total_all_lost = 0
        total_all_visit = 0
        total_all_calls = 0
        
        # Date Filters (Jo views.py se aayenge)
        date_filter = request.query_params.get('date', None)
        end_date_str = request.query_params.get('endDate', None)

        lead_filter = {}
        lead_filter1 = {}
        date_filter_applied = False
        
        if date_filter and end_date_str:
            try:
                start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
                end_date_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(end_date_dt + timedelta(days=1)) - timedelta(seconds=1)
                lead_filter = {'updated_date__range': [start_date, end_date]}
                lead_filter1 = {'created_date__range': [start_date, end_date]}
                date_filter_applied = True
            except ValueError: pass 
        
        elif date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                lead_filter = {'updated_date__date': date_obj}
                lead_filter1 = {'created_date__date': date_obj}
                date_filter_applied = True
            except ValueError: pass

        # 3. Loop over each Admin profile
        for admin_profile in admin_profiles:
            admin_agg_data = {
                'total_leads': 0, 'interested': 0, 'not_interested': 0,
                'other_location': 0, 'not_picked': 0, 'lost': 0, 'visit': 0
            }

            # Get all staff members under this Admin (via Team Leaders)
            staff_members = Staff.objects.filter(team_leader__admin=admin_profile)

            for staff in staff_members:
                # Use LeadUser filter logic (jaisa tumhare views.py mein tha)
                if date_filter_applied:
                     leads_by_date = LeadUser.objects.filter(assigned_to=staff, **lead_filter).aggregate(
                         interested=Count('id', filter=Q(status='Intrested')),
                         not_interested=Count('id', filter=Q(status='Not Interested')),
                         other_location=Count('id', filter=Q(status='Other Location')),
                         not_picked=Count('id', filter=Q(status='Not Picked')),
                         lost=Count('id', filter=Q(status='Lost')), visit=Count('id', filter=Q(status='Visit'))
                     )
                     leads_by_date1 = LeadUser.objects.filter(assigned_to=staff, **lead_filter1).aggregate(total_leads=Count('id'))
                else:
                    leads_by_date_all = LeadUser.objects.filter(assigned_to=staff).aggregate(
                        total_leads=Count('id'), interested=Count('id', filter=Q(status='Intrested')),
                        not_interested=Count('id', filter=Q(status='Not Interested')), other_location=Count('id', filter=Q(status='Other Location')),
                        not_picked=Count('id', filter=Q(status='Not Picked')), lost=Count('id', filter=Q(status='Lost')), visit=Count('id', filter=Q(status='Visit'))
                    )
                    leads_by_date = leads_by_date_all
                    leads_by_date1 = {'total_leads': leads_by_date_all['total_leads']}

                # Add staff data to admin's aggregate data
                admin_agg_data['total_leads'] += leads_by_date1.get('total_leads', 0)
                admin_agg_data['interested'] += leads_by_date.get('interested', 0)
                admin_agg_data['not_interested'] += leads_by_date.get('not_interested', 0)
                admin_agg_data['other_location'] += leads_by_date.get('other_location', 0)
                admin_agg_data['not_picked'] += leads_by_date.get('not_picked', 0)
                admin_agg_data['lost'] += leads_by_date.get('lost', 0)
                admin_agg_data['visit'] += leads_by_date.get('visit', 0)

            # Admin Total Calculations
            total_calls_admin = (
                admin_agg_data['interested'] + admin_agg_data['not_interested'] + 
                admin_agg_data['other_location'] + admin_agg_data['not_picked'] + 
                admin_agg_data['lost'] + admin_agg_data['visit']
            )
            total_leads_admin = admin_agg_data['total_leads']
            visit_percentage = (admin_agg_data['visit'] / total_leads_admin * 100) if total_leads_admin > 0 else 0
            interested_percentage = (admin_agg_data['interested'] / total_leads_admin * 100) if total_leads_admin > 0 else 0

            admin_data_list.append({
                'id': admin_profile.id,
                'name': admin_profile.name,
                'total_leads': total_leads_admin,
                'interested': admin_agg_data['interested'],
                'not_interested': admin_agg_data['not_interested'],
                'other_location': admin_agg_data['other_location'],
                'not_picked': admin_agg_data['not_picked'],
                'lost': admin_agg_data['lost'],
                'visit': admin_agg_data['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls_admin,
            })

            # 4. Grand Totals Update
            total_all_leads += total_leads_admin
            total_all_interested += admin_agg_data['interested']
            total_all_not_interested += admin_agg_data['not_interested']
            total_all_other_location += admin_agg_data['other_location']
            total_all_not_picked += admin_agg_data['not_picked']
            total_all_lost += admin_agg_data['lost']
            total_all_visit += admin_agg_data['visit']
            total_all_calls += total_calls_admin
        
        # 5. Final Grand Totals
        total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
        total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        # 6. Final Response
        data = {
            'admin_data': StaffProductivityDataSerializer(admin_data_list, many=True).data, # Reuse Staff serializer for data structure
            'task_type': 'admin',
            'total_all_leads': total_all_leads,
            'total_all_interested': total_all_interested,
            'total_all_calls': total_all_calls,
            'total_visit_percentage': round(total_visit_percentage, 2),
            'total_interested_percentage': round(total_interested_percentage, 2),
            'total_staff_count': total_admins_count, # Total admins ki count
            'fiter': 3 if request.user.is_superuser else 5, # 3 for superuser, 5 for admin
        }
        
        return Response(data, status=status.HTTP_200_OK)
    




# ===================================================================
# NAYA FREELANCER PRODUCTIVITY API
# ===================================================================
class FreelancerProductivityAPIView(APIView):
    """
    API fetches total productivity (aggregated leads/calls) for ALL Freelancers, 
    filtered by Admin/TL and date range.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser] # Superuser, Admin, TL chala sakte hain
    
    def get(self, request, *args, **kwargs):
        
        # 1. Get Filters
        date_filter = request.query_params.get('date', None)
        end_date_str = request.query_params.get('endDate', None)
        teamleader_id = request.query_params.get('teamleader_id', None)
        admin_id = request.query_params.get('admin_id', None)
        
        # 2. Staff Queryset (Filter only Freelancers)
        staffs = Staff.objects.filter(user__user_active=True, user__is_freelancer=True)
        fiter_value = 0 
        
        current_user = request.user

        if current_user.is_superuser:
            fiter_value = 1
            if admin_id:
                staffs = staffs.filter(team_leader__admin=admin_id)
            if teamleader_id:
                staffs = staffs.filter(team_leader=teamleader_id)
        
        elif current_user.is_admin:
            fiter_value = 4
            staffs = staffs.filter(team_leader__admin__self_user=current_user)
            if teamleader_id:
                staffs = staffs.filter(team_leader=teamleader_id)

        elif current_user.is_team_leader:
            fiter_value = 2
            team_leader_instance = Team_Leader.objects.filter(user=current_user).last()
            staffs = Staff.objects.filter(team_leader=team_leader_instance)
        
        total_staff_count = staffs.count()

        # 3. Initialization & Date Filter Setup (Same as Admin/Staff Productivity)
        staff_data_list = []
        total_all_leads = 0
        total_all_interested = 0
        total_all_calls = 0
        total_all_visit = 0
        
        lead_filter = {}
        lead_filter1 = {}
        date_filter_applied = False
        
        if date_filter and end_date_str:
            try:
                start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
                end_date_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(end_date_dt + timedelta(days=1)) - timedelta(seconds=1)
                lead_filter = {'updated_date__range': [start_date, end_date]}
                lead_filter1 = {'created_date__range': [start_date, end_date]}
                date_filter_applied = True
            except ValueError: pass 
        
        elif date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                lead_filter = {'updated_date__date': date_obj}
                lead_filter1 = {'created_date__date': date_obj}
                date_filter_applied = True
            except ValueError: pass

        # 4. Loop and Aggregate Data
        for staff in staffs:
            
            # Aggregate leads by Staff Member
            if date_filter_applied:
                 leads_by_date = LeadUser.objects.filter(assigned_to=staff, **lead_filter).aggregate(
                     interested=Count('id', filter=Q(status='Intrested')), 
                     not_interested=Count('id', filter=Q(status='Not Interested')),
                     other_location=Count('id', filter=Q(status='Other Location')),
                     not_picked=Count('id', filter=Q(status='Not Picked')), 
                     lost=Count('id', filter=Q(status='Lost')), visit=Count('id', filter=Q(status='Visit'))
                 )
                 leads_by_date1 = LeadUser.objects.filter(assigned_to=staff, **lead_filter1).aggregate(total_leads=Count('id'))
            else:
                leads_by_date_all = LeadUser.objects.filter(assigned_to=staff).aggregate(
                    total_leads=Count('id'), interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')), other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')), lost=Count('id', filter=Q(status='Lost')), visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date = leads_by_date_all
                leads_by_date1 = {'total_leads': leads_by_date_all['total_leads']}

            
            total_calls = (
                leads_by_date.get('interested', 0) + leads_by_date.get('not_interested', 0) + 
                leads_by_date.get('other_location', 0) + leads_by_date.get('not_picked', 0) + 
                leads_by_date.get('lost', 0) + leads_by_date.get('visit', 0)
            )
            total_leads_for_staff = leads_by_date1.get('total_leads', 0)
            visit_percentage = (leads_by_date.get('visit', 0) / total_leads_for_staff * 100) if total_leads_for_staff > 0 else 0
            interested_percentage = (leads_by_date.get('interested', 0) / total_leads_for_staff * 100) if total_leads_for_staff > 0 else 0

            staff_data_list.append({
                'id': staff.id, 'name': staff.name,
                'total_leads': total_leads_for_staff,
                'interested': leads_by_date.get('interested', 0),
                'not_interested': leads_by_date.get('not_interested', 0),
                'other_location': leads_by_date.get('other_location', 0),
                'not_picked': leads_by_date.get('not_picked', 0),
                'lost': leads_by_date.get('lost', 0),
                'visit': leads_by_date.get('visit', 0),
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
            })

            # Grand Totals Update
            total_all_leads += total_leads_for_staff
            total_all_interested += leads_by_date.get('interested', 0)
            total_all_calls += total_calls
            total_all_visit += leads_by_date.get('visit', 0)
        
        # 5. Final Grand Totals
        total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
        total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        # 6. Final Response
        data = {
            'staff_data': StaffProductivityDataSerializer(staff_data_list, many=True).data, # Reuse Staff serializer
            'task_type': 'freelancer',
            'total_all_leads': total_all_leads,
            'total_all_interested': total_all_interested,
            'total_all_calls': total_all_calls,
            'total_visit_percentage': round(total_visit_percentage, 2),
            'total_interested_percentage': round(total_interested_percentage, 2),
            'total_staff_count': total_staff_count, 
            'fiter': fiter_value,
        }
        
        return Response(data, status=status.HTTP_200_OK)



@api_view(['GET']) # Yeh API sirf GET request legi
@permission_classes([IsAuthenticated , CustomIsSuperuser]) # Sirf logged-in user
def get_team_leader_dashboard_api(request):

    user = request.user

    # 1. Check karo ki user Team Leader hai ya nahi
    if not user.is_team_leader:
        return Response(
            {"error": "Only Team Leaders can access this endpoint."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # 2. Team Leader object fetch karo (get_object_or_404 se error handling ho jaati hai)
    try:
        team_lead = Team_Leader.objects.get(user=user)
    except Team_Leader.DoesNotExist:
        return Response(
            {"error": "Team Leader profile not found for this user."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3. Staff members (user_logs)
    staff_members = Staff.objects.filter(team_leader=team_lead)
    
    # 4. Team leader ke unassigned leads (leads2)
    unassigned_leads = Team_LeadData.objects.filter(assigned_to=None, team_leader=team_lead)

    # 5. Global "Intrested" leads (leads3) - Aapke original logic ke hisaab se
    interested_leads = LeadUser.objects.filter(status="Intrested")

    # 6. Global "Lost" leads (leads4) - Aapke original logic ke hisaab se
    lost_leads = LeadUser.objects.filter(status="Lost")

    # 7. Saare counts calculate karo (Aapke original logic se)
    total_leads, total_lost_leads, total_customer, total_maybe = 0, 0, 0, 0

    for staff in staff_members:
        staff_leads = LeadUser.objects.filter(assigned_to=staff)
        total_leads += staff_leads.filter(status="Leads").count()
        total_lost_leads += staff_leads.filter(status="Lost_Leads").count()
        total_customer += staff_leads.filter(status="Customer").count()
        total_maybe += staff_leads.filter(status="Maybe").count()

    # Team leader ke unassigned leads ke counts add karo
    total_leads += unassigned_leads.filter(status="Leads").count()
    total_lost_leads += unassigned_leads.filter(status="Lost_Leads").count()
    total_customer += unassigned_leads.filter(status="Customer").count()
    total_maybe += unassigned_leads.filter(status="Maybe").count()
    
    # Final counts
    total_uplode_leads = unassigned_leads.count()
    customer_count = interested_leads.count()
    lost_count = lost_leads.count()

    # 8. Data ko Serialize karo (JSON me convert karo)
    user_logs_data = ApiStaffSerializer(staff_members, many=True).data
    leads2_data = ApiTeamLeadDataSerializer(unassigned_leads, many=True).data
    leads3_data = ApiLeadUserSerializer(interested_leads, many=True).data
    leads4_data = ApiLeadUserSerializer(lost_leads, many=True).data

    # 9. Final response (context dictionary) banake bhejo
    response_data = {
        'total_uplode_leads': total_uplode_leads,
        'total_leads': total_leads,
        'total_lost_leads': total_lost_leads,
        'total_customer': total_customer,
        'total_maybe': total_maybe,
        'customer_count': customer_count,
        'lost_count': lost_count,
        'user_logs': user_logs_data, # Serialized data
        'leads2': leads2_data,       # Serialized data
        'leads3': leads3_data,       # Serialized data
        'leads4': leads4_data        # Serialized data
    }

    return Response(response_data, status=status.HTTP_200_OK)



class TeamCustomerLeadsAPIView(APIView):
 
    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, tag, format=None):
        # Paginator ko instantiate karo
        paginator = self.pagination_class()
        
        # 1. Search Query Check (Aapke code me yeh sabse pehle hai)
        search_query = request.query_params.get('search', None)
        
        if search_query:
            # Agar search query hai, toh tag aur role ignore karke search karo
            queryset = LeadUser.objects.filter(
                Q(name__icontains=search_query) | Q(call__icontains=search_query) | Q(team_leader__name__icontains=search_query),
                status='Intrested'
            )
            serializer_class = ApiLeadUserSerializer # Search hamesha LeadUser par hai
        
        else:
            # 2. Koi Search Query Nahi Hai - Role aur Tag ke hisaab se filter karo
            user = request.user
            today = timezone.now().date()
            tomorrow = today + timedelta(days=1)
            team_leader_instance = Team_Leader.objects.filter(email=user.email).last()
            
            queryset = None
            serializer_class = None # Hum ise neeche set karenge

            if user.is_superuser:
                base_queryset = LeadUser.objects.filter(status='Intrested')
                if tag == 'pending_follow':
                    queryset = base_queryset.filter(follow_up_date__isnull=False)
                elif tag == 'today_follow':
                    queryset = base_queryset.filter(follow_up_date=today)
                elif tag == 'tommorrow_follow':
                    queryset = base_queryset.filter(follow_up_date=tomorrow)
                else:
                    queryset = base_queryset
                serializer_class = ApiLeadUserSerializer

            elif user.is_team_leader:
                base_queryset = LeadUser.objects.filter(team_leader=team_leader_instance, status='Intrested')
                if tag == 'pending_follow':
                    queryset = base_queryset.filter(follow_up_date__isnull=False)
                elif tag == 'today_follow':
                    queryset = base_queryset.filter(follow_up_date=today)
                elif tag == 'tommorrow_follow':
                    queryset = base_queryset.filter(follow_up_date=tomorrow)
                else:
                    # Yeh aapka original 'else' logic hai team leader ke liye
                    queryset = base_queryset.filter(follow_up_time__isnull=True)
                serializer_class = ApiLeadUserSerializer

            else:
                # Yeh aapka original 'else' logic hai (e.g., for Staff)
                queryset = Team_LeadData.objects.filter(team_leader=team_leader_instance, status='Intrested')
                serializer_class = ApiTeamLeadDataSerializer
        
        # 3. Sab par ordering lagao
        if queryset is not None:
            queryset = queryset.order_by('-updated_date')
        else:
            queryset = LeadUser.objects.none() # Empty result

        # 4. Paginate karo aur Serialized response bhejo
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        # Yeh check zaroori hai
        if serializer_class is None:
             return Response({"error": "Could not determine serializer."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if page is not None:
            serializer = serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Non-paginated response
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# ==========================================================
# API: EXPORT LEADS (STATUS WISE) [FINAL FIX 2]
# ==========================================================
class ExportLeadsStatusWiseAPIView(APIView):
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def post(self, request, *args, **kwargs):
        # 1. Input ko naye serializer se Validate karo
        serializer = LeadExportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        all_interested = validated_data.get('all_interested')
        staff_id = validated_data.get('staff_id')
        
        # --- FIX: 'status' variable ka naam 'lead_status' kiya ---
        lead_status = validated_data.get('lead_status') 
        
        staff_instance = None
        
        # 2. Date Range Logic
        end_date_for_range = end_date + timedelta(days=1)
        
        # 3. Filtering Logic
        leads = None
        if all_interested != "1":
            staff_instance = Staff.objects.filter(id=staff_id).last()
            if not staff_instance:
                 # YEH LINE AB THEEK SE KAAM KAREGI
                 return Response({"error": f"Staff with id={staff_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            leads = LeadUser.objects.filter(
                updated_date__range=[start_date, end_date_for_range],
                status=lead_status,  # --- FIX: Variable name use kiya ---
                assigned_to=staff_instance,
            )
        else:
            if request.user.is_superuser:
                leads = LeadUser.objects.filter(
                    updated_date__range=[start_date, end_date_for_range],
                    status="Intrested",
                )
            elif request.user.is_team_leader:
                user_email = request.user.username 
                team_leader_instance = Team_Leader.objects.filter(email=user_email).last()
                leads = LeadUser.objects.filter(
                    team_leader=team_leader_instance,
                    updated_date__range=[start_date, end_date_for_range],
                    status="Intrested",
                )
            else:
                return Response({"error": "You do not have permission for 'all_interested' export."}, status=status.HTTP_403_FORBIDDEN)
        
        if leads is None:
            leads = LeadUser.objects.none()

        # 4. Data Preparation
        data = []
        for lead in leads:
            data.append({
                'Name': lead.name,
                'Call': lead.call,
                'Status': lead.status,
                'staff Name': lead.assigned_to.name if lead.assigned_to else 'N/A',
                'Message': lead.message,
                'Date': localtime(lead.updated_date).strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        df = pd.DataFrame(data)

        # 5. Response Generation
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")

        if all_interested == "1":
            response['Content-Disposition'] = f'attachment; filename=interested_{start_str}_to_{end_str}.xlsx'
        else:
            if staff_instance:
                # --- FIX: Variable name use kiya ---
                response['Content-Disposition'] = f'attachment; filename={staff_instance.name}_{lead_status}_{start_str}_to_{end_str}.xlsx'
            else:
                response['Content-Disposition'] = f'attachment; filename=export_{lead_status}_{start_str}_to_{end_str}.xlsx'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Leads')

        return response



# ==========================================================
# API: TEAM LEADER LEADS REPORT (BY STATUS)
# ==========================================================
class TeamLeadLeadsReportAPIView(APIView):

    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination # Paginator set kiya

    def get(self, request, id, tag, format=None):
        # 1. Paginator ko instantiate karo
        paginator = self.pagination_class()

        # 2. Base queryset (Sirf 'id' se team leader par filter)
        base_queryset = LeadUser.objects.filter(team_leader=id)

        # 3. Tag (Status) ke hisaab se filter karo
        
        allowed_tags = ["Intrested", "Not Interested", "Other Location", "Lost", "Visit"]

        if tag in allowed_tags:
            staff_leads = base_queryset.filter(status=tag)
        else:
            # Original function ka 'else' logic (saare leads dikhao)
            staff_leads = base_queryset

        # 4. Ordering lagao
        staff_leads = staff_leads.order_by('-updated_date')

        # 5. Page ko Paginate karo
        page = paginator.paginate_queryset(staff_leads, request, view=self)

        # 6. Serialized data bhejo
        if page is not None:
            serializer = ApiLeadUserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # (Fallback agar pagination na chale)
        serializer = ApiLeadUserSerializer(staff_leads, many=True)
        return Response(serializer.data)
    

# ==========================================================
# API: ADD SELL PLOT (FREELANCER) VIEW
# ==========================================================
class AddSellPlotAPIView(APIView):
    """
    API endpoint 'add_sell_freelancer' function ke liye.
    GET: Form bharne ke liye Admins aur Staffs ki list deta hai.
    POST: Naya sell plot record banata hai.
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]

    def get(self, request, id, format=None):
        """
        Form ke dropdowns ke liye data return karta hai.
        """
        admins = Admin.objects.all()
        
        # Yahan hum existing serializers ka istemal kar rahe hain
        admin_serializer = DashboardAdminSerializer(admins, many=True)
        
        response_data = {
            'admins': admin_serializer.data,
            'staffs': [] # Default khaali rakho
        }
        
        if request.user.is_team_leader:
            staffs = Staff.objects.filter(team_leader__email=request.user.email)
            staff_serializer = ApiStaffSerializer(staffs, many=True)
            response_data['staffs'] = staff_serializer.data
            
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        """
        Naya sell plot record banata hai.
        """
        
        serializer = SellPlotCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # .save() method automatically create() ko call karega
            sell_obj = serializer.save()
            
            # Output ke liye purane 'SellPlotSerializer' ka istemal karo
            output_serializer = SellPlotSerializer(sell_obj)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        
        # Agar validation fail hua
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  




class VisitLeadsAPIView(APIView):
  
    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
        paginator = self.pagination_class()
        user = request.user
        
        # Team leader instance (jo 'is_team_leader' aur 'else' dono me use hota hai)
        team_leader_instance = Team_Leader.objects.filter(email=user.email).last()

        queryset = None
        serializer_class = None # Hum ise role ke hisaab se set karenge

        if user.is_superuser:
            queryset = LeadUser.objects.filter(status='Visit').order_by('-updated_date')
            serializer_class = ApiLeadUserSerializer # Superuser LeadUser model dekhta hai
        
        elif user.is_team_leader:
            if not team_leader_instance:
                 return Response({"error": "Team Leader profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
            queryset = LeadUser.objects.filter(team_leader=team_leader_instance, status='Visit').order_by('-updated_date')
            serializer_class = ApiLeadUserSerializer # Team Leader bhi LeadUser model dekhta hai
        
        else:
            # Yeh 'else' block aapke original function ke 'else' se hai (e.g., Staff ke liye)
            queryset = Team_LeadData.objects.filter(team_leader=team_leader_instance, status='Visit')
            serializer_class = ApiTeamLeadDataSerializer # Baaki users Team_LeadData dekhte hain

        # Ab queryset ko paginate karo
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        if page is not None:
            # Role ke hisaab se jo serializer chuna tha, use istemal karo
            serializer = serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # (Fallback agar pagination na chale)
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)    
    

# ==========================================================
# API: PROJECT (LIST & CREATE)
# ==========================================================
class ProjectListCreateAPIView(APIView):
    """
    API endpoint jo 'project_list' aur 'project_add' ko handle karta hai.
    GET: Saare projects ki list deta hai.
    POST: Naya project banata hai (file upload ke sath).
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    # File upload (media_file) ke liye parser classes
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        """
        Saare projects ki list return karta hai.
        """
        projects = Project.objects.all()
        # ProjectSerializer ka istemal karke data ko JSON me badlo
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Naya project banata hai.
        """
        # Serializer ko request.data se validate karo
        serializer = ProjectSerializer(data=request.data)
        
        if serializer.is_valid():
            # user=request.user ko save karte time alag se pass karo
            # Taaki logged-in user automatically set ho jaaye
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Agar data galat hai
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


# ==========================================================
# API: ACTIVITY LOGS (BY ROLE)
# ==========================================================
from rest_framework.views import APIView

class ActivityLogsAPIView(APIView):
    """
    API endpoint jo 'activitylogs' function ka logic handle karta hai.
    Yeh user role ke hisaab se activity logs nikaalta hai (paginated).
    """
    permission_classes = [IsAuthenticated , CustomIsSuperuser]
    pagination_class = ActivityLogPagination # Custom pagination

    def get(self, request, format=None):
        paginator = self.pagination_class()
        user = request.user
        
        queryset = ActivityLog.objects.none() # Start with an empty queryset

        if user.is_superuser:
            queryset = ActivityLog.objects.all()
        
        elif user.is_admin:
            admin_user = Admin.objects.filter(email=user.email).last()
            if admin_user:
                queryset = ActivityLog.objects.filter(admin=admin_user)
        
        elif user.is_team_leader:
            team_leader_user = Team_Leader.objects.filter(email=user.email).last()
            if team_leader_user:
                queryset = ActivityLog.objects.filter(team_leader=team_leader_user)

        elif user.is_staff_new:
            staff_instance = Staff.objects.filter(email=user.email).last()
            
            # Staff can see logs linked to their user OR their staff profile
            if staff_instance:
                 queryset = ActivityLog.objects.filter(Q(user=user) | Q(staff=staff_instance))
            else:
                # Fallback agar staff profile nahi bana hai
                queryset = ActivityLog.objects.filter(user=user)
        
        # Sab par consistent ordering lagao
        ordered_queryset = queryset.order_by('-created_date')
        
        # Queryset ko Paginate karo
        page = paginator.paginate_queryset(ordered_queryset, request, view=self)
        
        if page is not None:
            serializer = ActivityLogSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # (Fallback agar pagination na chale)
        serializer = ActivityLogSerializer(ordered_queryset, many=True)
        return Response(serializer.data)
    







def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_type(user):
    if user.is_superuser: return "Super User"
    elif user.is_admin: return "Admin User"
    elif user.is_team_leader: return "Team Leader User"
    elif user.is_staff_new: return "Staff User"
    return "User"

# --- Naya API View ---

@api_view(['POST']) # Original function POST method check kar raha tha
@permission_classes([IsAuthenticated , CustomIsSuperuser])
def update_lead_user_api(request, id):
    """
    API endpoint to update lead status, message, and follow-up.
    Yeh user role ke hisaab se LeadUser ya Team_LeadData ko update karta hai.
    """
    user = request.user
    
    # 1. User ke role ke hisaab se sahi lead object (lead_user) get karo
    lead_object = None
    model_type = None
    
    try:
        if user.is_superuser:
            lead_object = get_object_or_404(Team_LeadData, id=id)
            model_type = 'Team_LeadData'
        elif user.is_staff_new:
            lead_object = get_object_or_404(LeadUser, id=id)
            model_type = 'LeadUser'
        elif user.is_team_leader:
            lead_object = get_object_or_404(LeadUser, id=id)
            model_type = 'LeadUser'
        else:
            return Response({"error": "You do not have permission for this lead type."},
                            status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({"error": f"Lead with id={id} not found."}, 
                        status=status.HTTP_404_NOT_FOUND)

    current_status = lead_object.status

    # 2. Input data ko naye serializer se validate karo
    serializer = LeadUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    new_status = validated_data.get('status')
    message = validated_data.get('message', lead_object.message) # Purana message fallback
    follow_date = validated_data.get('followDate')
    follow_time = validated_data.get('followTime')

    # 3. Special Logic: "Not Picked"
    if new_status == "Not Picked" and model_type == 'LeadUser':
        try:
            Team_LeadData.objects.create(
                user=lead_object.user,
                name=lead_object.name,
                call=lead_object.call,
                status="Leads", 
                email=lead_object.email,
            )
            lead_object.delete()
            return Response({'message': 'Success: Lead moved to Team_LeadData'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Failed to move lead: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 4. Normal Update Logic
    lead_object.status = new_status
    lead_object.message = message

    if (user.is_team_leader or user.is_staff_new) and model_type == 'LeadUser':
        if follow_date:
            lead_object.follow_up_date = follow_date
        if follow_time:
            lead_object.follow_up_time = follow_time
            
    lead_object.save()

    # 5. Leads History Create Karo
    try:
        history_leads_obj = lead_object if isinstance(lead_object, LeadUser) else None
        
        Leads_history.objects.create(
            leads=history_leads_obj,
            lead_id=id, 
            status=new_status,
            name=lead_object.name,
            message=message,
        )
    except Exception as e:
        print(f"Failed to create Leads_history: {e}")


    # 6. Activity Log Create Karo
    user_type = get_user_type(user)
    tagline = f"Lead status changed from {current_status} to {new_status} by user[Email: {user.email}, {user_type}]"
    tag2 = new_status
    ip = get_client_ip(request)

    if user.is_staff_new:
        admin_instance = Staff.objects.filter(email=user.email).last()
        if admin_instance:
            my_user2 = admin_instance.team_leader
            ActivityLog.objects.create(
                staff=admin_instance,
                team_leader=my_user2,
                description=tagline,
                ip_address=ip,
                email=user.email,
                user_type=user_type,
                activity_type=tag2,
                name=user.name,
            )
            
    # 7. Success Response
    return Response({'message': 'Success'}, status=status.HTTP_200_OK)




# home/api.py (Line ~1450)

# ==========================================================
# API: ADMIN DASHBOARD - TEAM LEADER REPORT [ORIGINAL / CORRECTED]
# ==========================================================
class AdminTeamLeaderReportAPIView(APIView):
    """
    API endpoint jo 'team_leader_user' function ka logic handle karta hai.
    Yeh API SIRF Admin users ke liye hai.
    Yeh Admin ke under saare Team Leaders ki list aur unke leads ke counts return karta hai.
    """
    
    permission_classes = [IsAuthenticated, IsCustomAdminUser]

    def get(self, request, format=None):
        user = request.user
        
        # 1. Logged-in Admin ka profile dhoondo
        try:
            admin_profile = Admin.objects.get(email=user.username) 
        except Admin.DoesNotExist:
            return Response(
                {"error": "Admin profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 2. Is Admin ke under saare Team Leaders ko dhoondo
        team_leaders_list = Team_Leader.objects.filter(admin=admin_profile)

        # 3. Date Filters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        today = timezone.now().date()

        if start_date_str and end_date_str:
            start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
            end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)) - timedelta(seconds=1)
        else:
            start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
        
        # 4. Saare LEADS Counts Calculate Karo
        lead_filter = {'updated_date__range': [start_date, end_date]}
        base_queryset = LeadUser.objects.filter(team_leader__in=team_leaders_list, **lead_filter)
        
        total_leads = base_queryset.filter(status="Leads").count()
        total_interested_leads = base_queryset.filter(status="Intrested").count()
        total_not_interested_leads = base_queryset.filter(status="Not Interested").count()
        total_other_location_leads = base_queryset.filter(status="Other Location").count()
        total_not_picked_leads = base_queryset.filter(status="Not Picked").count()
        total_lost_leads = base_queryset.filter(status="Lost").count()
        total_visits_leads = base_queryset.filter(status="Visit").count()

        # (Staff counts yahaan se hata diye hain)

        # 5. Settings object dhoondo
        setting = Settings.objects.filter().last()

        # 6. Data ko Serialize karo
        team_leaders_data = ProductivityTeamLeaderSerializer(team_leaders_list, many=True).data
        setting_data = DashboardSettingsSerializer(setting).data if setting else None

        # 7. Final JSON Response Banao
        response_data = {
            'counts': {
                'total_leads': total_leads,
                'total_interested_leads': total_interested_leads,
                'total_not_interested_leads': total_not_interested_leads,
                'total_other_location_leads': total_other_location_leads,
                'total_not_picked_leads': total_not_picked_leads,
                'total_lost_leads': total_lost_leads,
                'total_visits_leads': total_visits_leads,
            },
            'team_leaders_list': team_leaders_data,
            'setting': setting_data,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    




# --- Nayi API View Class ---
# ==========================================================
# API: ADMIN - ADD TEAM LEADER
# ==========================================================
class TeamLeaderAddAPIView(APIView):
    """
    API endpoint naya Team Leader banane ke liye.
    Sirf Admin user hi ise access kar sakte hain.
    GET: Dropdown ke liye Admin ki list deta hai.
    POST: Naya Team Leader banata hai.
    """
    
    # Sirf Admin User hi access kar sakta hai
    permission_classes = [IsAuthenticated, IsCustomAdminUser]
    # File (profile_image) upload ke liye parsers
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Form ke 'Select Admin' dropdown ke liye data return karta hai.
        """
        # Aapke original function ka GET logic
        all_admins = User.objects.filter(is_admin=True)
        serializer = DashboardUserSerializer(all_admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Naya Team Leader create karta hai.
        """
        
        # Hum TeamLeaderCreateSerializer ka istemal karenge jo pehle se bana hai.
        # Hum 'context={'request': request}' bhej rahe hain taaki serializer
        # request.user ko access kar sake (apne logic ke liye).
        serializer = TeamLeaderCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Serializer ka .save() method automatically .create() method 
            # ko call karega aur naya Team Leader bana dega.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Agar validation fail hua
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





# home/api.py

# ==========================================================
# API: ADMIN-ONLY STAFF REPORT DASHBOARD
# ==========================================================
class StaffReportAPIView(APIView):
    """
    API endpoint 'add_staff_admin_side' function ke GET request ke liye.
    SIRF ADMIN ke liye Staff list, Lead Counts, aur Productivity Report deta hai.
    """
    
    # --- [YEH RAHA FIX] ---
    # Sirf Admin user hi access kar sakta hai
    permission_classes = [IsAuthenticated, IsCustomAdminUser] 

    def get(self, request, format=None):
        user = request.user
        
        # --- 1. Role ke hisaab se Staff aur Leads ki base query set karo ---
        # Kyunki yeh sirf Admin ke liye hai, humein Superuser check ki zaroorat nahi hai.
        
        staff_list_qs = Staff.objects.filter(team_leader__admin__self_user=request.user)
        base_lead_qs = LeadUser.objects.filter(team_leader__admin__self_user=request.user)
        
        # --- 2. Lead Counts (Total) ---
        lead_counts = {
            'total_leads': base_lead_qs.filter(status="Leads").count(),
            'total_interested_leads': base_lead_qs.filter(status="Intrested").count(),
            # ... (baaki saare counts waise hi rahenge) ...
            'total_not_interested_leads': base_lead_qs.filter(status="Not Interested").count(),
            'total_other_location_leads': base_lead_qs.filter(status="Other Location").count(),
            'total_not_picked_leads': base_lead_qs.filter(status="Not Picked").count(),
            'total_lost_leads': base_lead_qs.filter(status="Lost").count(),
            'total_visits_leads': base_lead_qs.filter(status="Visit").count()
        }

        # --- 3. Productivity Data (Calendar/Salary) ---
        # (Is poore section me koi change nahi hai)
        
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        
        days_in_month = monthrange(year, month)[1]
        
        total_salary_all_staff = 0
        productivity_data_all_staff = {} 

        for staff in staff_list_qs:
            salary = float(staff.salary or 0)
            daily_salary = round(salary / days_in_month, 2) if days_in_month > 0 else 0

            leads_data = LeadUser.objects.filter(
                assigned_to=staff,
                updated_date__year=year,
                updated_date__month=month,
                status='Intrested'
            ).values('updated_date__day').annotate(count=Count('id'))

            productivity_data_dict = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}
            total_salary = 0

            for lead in leads_data:
                day = lead['updated_date__day']
                if day in productivity_data_dict:
                    leads_count = lead['count']
                    productivity_data_dict[day]['leads'] = leads_count

                    if leads_count >= 10:
                        daily_earned_salary = daily_salary
                    else:
                        daily_earned_salary = round((daily_salary / 10) * leads_count, 2)

                    productivity_data_dict[day]['salary'] = daily_earned_salary
                    total_salary += daily_earned_salary

            productivity_data_all_staff[staff.id] = {
                'name': staff.name,
                'productivity_data': productivity_data_dict, 
                'total_salary': round(total_salary, 2)
            }
            total_salary_all_staff += total_salary

        # --- 4. Calendar Structure ---
        # (Isme koi change nahi hai)
        calendar_data = calendar.monthcalendar(year, month)
        weekdays = list(calendar.day_name)
        structured_calendar_data = []
        for week in calendar_data:
            week_data = []
            for i, day in enumerate(week):
                week_data.append({
                    'day': day,
                    'day_name': weekdays[i]
                })
            structured_calendar_data.append(week_data)
        
        # --- 5. Month List for Dropdown ---
        months_list = [{'id': i, 'name': calendar.month_name[i]} for i in range(1, 13)]

        # --- 6. Serialize and Respond ---
        staff_list_serializer = ApiStaffSerializer(staff_list_qs, many=True)
        
        response_data = {
            'lead_counts': lead_counts,
            'staff_list': staff_list_serializer.data,
            'productivity_report': {
                'total_salary_all_staff': round(total_salary_all_staff, 2),
                'staff_productivity_details': productivity_data_all_staff 
            },
            'calendar_structure': structured_calendar_data,
            'dropdown_data': {
                'months': months_list
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    






class AdminStaffAddAPIView(APIView):
    """
    API endpoint SIRF ADMIN ke naya Staff banane ke liye.
    GET: Dropdown ke liye Admin ke Team Leaders ki list deta hai.
    POST: Naya Staff banata hai.
    """
    
    # Sirf Admin User (is_admin=True) hi access kar sakta hai
    permission_classes = [IsAuthenticated, IsCustomAdminUser]
    # File (profile_image) upload ke liye parsers
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        """
        Form ke 'Select Team Leader' dropdown ke liye data return karta hai.
        """
        # Aapke 'add_staff' function ka Admin GET logic:
        try:
            # 'self_user' ya 'user' - model ke hisaab se check karo
            all_teamleader = Team_Leader.objects.filter(admin__self_user=request.user)
        except FieldError:
            all_teamleader = Team_Leader.objects.filter(admin__user=request.user)
            
        serializer = ProductivityTeamLeaderSerializer(all_teamleader, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Naya Staff create karta hai.
        """
        
        # Hum existing 'StaffCreateSerializer' ka istemal karenge
        serializer = StaffCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Check kar lo ki jo team_leader ID aayi hai, woh isi Admin ki hai ya nahi
            team_leader_id = request.data.get('team_leader')
            try:
                team_leader = Team_Leader.objects.get(id=team_leader_id)
                admin_profile = Admin.objects.get(self_user=request.user) # Ya admin__user
                
                if team_leader.admin != admin_profile:
                    return Response(
                        {"error": "You can only assign staff to your own Team Leaders."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Exception as e:
                 return Response({"error": f"Invalid Team Leader: {e}"}, status=status.HTTP_400_BAD_REQUEST)

            # Agar sab theek hai, toh save karo
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Agar validation fail hua
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class SuperUserTeamLeaderListAPIView(APIView):
    """
    API endpoint SIRF SUPERUSER ke liye, jo database ke
    saare Team Leaders ki list return karta hai.
    """
    
    # Sirf Superuser hi access kar sakta hai
    permission_classes = [IsAuthenticated, CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination # Paginator (optional, par acha hai)

    def get(self, request, format=None):
        paginator = self.pagination_class()
        
        # 1. Saare Team Leaders ko database se fetch karo
        team_leaders = Team_Leader.objects.all().order_by('id')
        
        # 2. Paginate karo
        page = paginator.paginate_queryset(team_leaders, request, view=self)
        
        # 3. ProductivityTeamLeaderSerializer se data ko JSON me badlo
        if page is not None:
            serializer = ProductivityTeamLeaderSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # (Fallback agar pagination na chale)
        serializer = ProductivityTeamLeaderSerializer(team_leaders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    




# ==========================================================
# API: SUPERUSER - TEAM LEADER DASHBOARD (CARDS + LIST)
# ==========================================================
class SuperUserTeamLeaderDashboardAPIView(APIView):
    """
    API for Superuser's 'Team Leader List' dashboard (add_team_leader_admin_side).
    Provides all card counts and the paginated list of Team Leaders.
    """
    permission_classes = [IsAuthenticated, CustomIsSuperuser]
    pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
        paginator = self.pagination_class()
        
        # --- 1. Get Team Leader List (Paginated) ---
        # (Aapke view function ki 'users = Team_Leader.objects.all()' waali line)
        team_leaders_qs = Team_Leader.objects.all().order_by('name')
        
        # Paginate the team leader list
        page = paginator.paginate_queryset(team_leaders_qs, request, view=self)
        team_leaders_serializer = ProductivityTeamLeaderSerializer(page, many=True)

        # --- 2. Calculate All Card Counts (Aapke view function se) ---
        
        # Staff Counts (Aapke view function se)
        active_staff_count = User.objects.filter(is_staff_new=True, is_user_login=True).count()
        total_staff_count = User.objects.filter(is_staff_new=True).count()

        # Lead Counts (Aapke view function se)
        total_leads = LeadUser.objects.filter(status="Leads").count()
        total_interested = LeadUser.objects.filter(status="Intrested").count()
        total_not_interested = LeadUser.objects.filter(status="Not Interested").count()
        total_other_location = LeadUser.objects.filter(status="Other Location").count()
        total_not_picked = LeadUser.objects.filter(status="Not Picked").count()
        total_lost = LeadUser.objects.filter(status="Lost").count()
        total_visits = LeadUser.objects.filter(status="Visit").count()

        # --- 3. Calculate Followup Counts (Yeh aapke screenshot me the) ---
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        
        pending_followups = LeadUser.objects.filter(
            Q(status='Intrested') & Q(follow_up_date__isnull=False)
        ).count()
        today_followups = LeadUser.objects.filter(
            Q(status='Intrested') & Q(follow_up_date=today)
        ).count()
        tomorrow_followups = LeadUser.objects.filter(
            Q(status='Intrested') & Q(follow_up_date=tomorrow)
        ).count()
        
        # --- 4. Saare Counts ko ek dictionary me daalo ---
        counts_data = {
            'pending_followups': pending_followups,
            'tomorrow_followups': tomorrow_followups,
            'today_followups': today_followups,
            'total_leads': total_leads,
            'total_visit': total_visits,
            'interested': total_interested,
            'not_interested': total_not_interested,
            'other_location': total_other_location,
            'not_picked': total_not_picked,
            'total_staff': total_staff_count,
            'active_staff': active_staff_count,
            'total_lost': total_lost, # Yeh aapke view function me tha
        }

        # --- 5. Final Response Banao ---
        # Paginator se poora response structure (count, next, previous, results) lo
        paginated_response = paginator.get_paginated_response(team_leaders_serializer.data)
        
        # Ab us response me 'counts' ka data bhi add kar do
        paginated_response.data['counts'] = counts_data
        
        return paginated_response




# home/api.py

# ==========================================================
# API: SUPERUSER-ONLY - STAFF REPORT DASHBOARD [UPDATED]
# ==========================================================
class SuperUserStaffReportAPIView(APIView):
    """
    API endpoint 'add_staff_admin_side' function ke GET request ke LIYE.
    SIRF SUPERUSER ke liye Staff list, Lead Counts, aur Productivity Report deta hai.
    [UPDATE]: 'total_lost_leads' count hata diya gaya hai.
    """
    
    permission_classes = [IsAuthenticated, CustomIsSuperuser] 

    def get(self, request, format=None):
        user = request.user
        
        # --- 1. Superuser Logic: Saare Staff aur Leads ---
        staff_list_qs = Staff.objects.all()
        base_lead_qs = LeadUser.objects.all()
        
        # --- 2. Lead Counts (Total) ---
        lead_counts = {
            'total_leads': base_lead_qs.filter(status="Leads").count(),
            'total_interested_leads': base_lead_qs.filter(status="Intrested").count(),
            'total_not_interested_leads': base_lead_qs.filter(status="Not Interested").count(),
            'total_other_location_leads': base_lead_qs.filter(status="Other Location").count(),
            'total_not_picked_leads': base_lead_qs.filter(status="Not Picked").count(),
            # --- [FIX] ---
            # 'total_lost_leads': base_lead_qs.filter(status="Lost").count(), # <-- YEH LINE HATA DI HAI
            # --- [FIX ENDS] ---
            'total_visits_leads': base_lead_qs.filter(status="Visit").count()
        }

        # --- 3. Productivity Data (Calendar/Salary) ---
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        
        days_in_month = monthrange(year, month)[1]
        
        total_salary_all_staff = 0
        productivity_data_all_staff = {} 

        for staff in staff_list_qs:
            salary = float(staff.salary or 0)
            daily_salary = round(salary / days_in_month, 2) if days_in_month > 0 else 0

            leads_data = LeadUser.objects.filter(
                assigned_to=staff,
                updated_date__year=year,
                updated_date__month=month,
                status='Intrested'
            ).values('updated_date__day').annotate(count=Count('id'))

            productivity_data_dict = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}
            total_salary = 0

            for lead in leads_data:
                day = lead['updated_date__day']
                if day in productivity_data_dict:
                    leads_count = lead['count']
                    productivity_data_dict[day]['leads'] = leads_count

                    if leads_count >= 10:
                        daily_earned_salary = daily_salary
                    else:
                        daily_earned_salary = round((daily_salary / 10) * leads_count, 2)

                    productivity_data_dict[day]['salary'] = daily_earned_salary
                    total_salary += daily_earned_salary

            productivity_data_all_staff[staff.id] = {
                'name': staff.name,
                'productivity_data': productivity_data_dict, 
                'total_salary': round(total_salary, 2)
            }
            total_salary_all_staff += total_salary

        # --- 4. Calendar Structure ---
        calendar_data = calendar.monthcalendar(year, month)
        weekdays = list(calendar.day_name)
        structured_calendar_data = []
        for week in calendar_data:
            week_data = []
            for i, day in enumerate(week):
                week_data.append({
                    'day': day,
                    'day_name': weekdays[i]
                })
            structured_calendar_data.append(week_data)
        
        # --- 5. Month List for Dropdown ---
        months_list = [{'id': i, 'name': calendar.month_name[i]} for i in range(1, 13)]

        # --- 6. Serialize and Respond ---
        staff_list_serializer = ApiStaffSerializer(staff_list_qs, many=True)
        
        # --- [TOTAL EARNING FIX] ---
        total_earning_aggregation = Sell_plot.objects.filter(staff__in=staff_list_qs).aggregate(total_earn=Sum('earn_amount'))
        total_earning = total_earning_aggregation.get('total_earn') or 0
        lead_counts['total_earning'] = total_earning
        
        response_data = {
            'lead_counts': lead_counts,
            'staff_list': staff_list_serializer.data,
            'productivity_report': {
                'total_salary_all_staff': round(total_salary_all_staff, 2),
                'staff_productivity_details': productivity_data_all_staff 
            },
            'calendar_structure': structured_calendar_data,
            'dropdown_data': {
                'months': months_list
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    


class AdminStaffEditAPIView(APIView):
    """
    API endpoint 'staffedit' function ke liye (Admin Dashboard).
    GET: Staff ki current details laata hai.
    PATCH: Staff ki profile ko update karta hai.
    SIRF ADMIN hi ise access kar sakta hai.
    """
    
    # Sirf Admin User (is_admin=True) hi access kar sakta hai
    permission_classes = [IsAuthenticated, IsCustomAdminUser]
    parser_classes = [MultiPartParser, FormParser] # File upload (profile_image) ke liye

    def get_object(self, id):
        # Helper function to get the object
        return get_object_or_404(Staff, id=id)

    def get(self, request, id, format=None):
        """
        GET request: Staff ki current details return karta hai.
        """
        staff = self.get_object(id)
        
        # Security check: Kya yeh Admin is staff ko edit kar sakta hai?
        # (Hum check kar rahe hain ki staff ka admin, logged-in admin hai ya nahi)
        admin_profile = Admin.objects.get(self_user=request.user)
        if staff.team_leader.admin != admin_profile:
             return Response(
                {"error": "You do not have permission to edit this staff member."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = FullStaffSerializer(staff, context={'request': request}) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id, format=None):
        """
        PATCH request: Staff ki profile ko update karta hai.
        """
        staff = self.get_object(id)

        # Security check
        admin_profile = Admin.objects.get(self_user=request.user)
        if staff.team_leader.admin != admin_profile:
             return Response(
                {"error": "You do not have permission to edit this staff member."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # StaffUpdateSerializer ka istemal karo
        serializer = StaffUpdateSerializer(instance=staff, data=request.data, partial=True) 
        
        if serializer.is_valid():
            updated_instance = serializer.save()
            
            # Updated data ko 'FullStaffSerializer' se wapas bhejo
            read_serializer = StaffProfileSerializer(updated_instance, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_200_OK) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id, format=None):
        # POST ko bhi PATCH ki tarah handle karo
        return self.patch(request, id, format)
    





# ==========================================================
# API: ADMIN-ONLY - EDIT TEAM LEADER (GET/UPDATE)
# ==========================================================
class AdminTeamLeaderEditAPIView(APIView):
    """
    API endpoint 'teamedit' function ke liye (Admin Dashboard).
    GET: Team Leader ki current details laata hai.
    PATCH: Team Leader ki profile ko update karta hai.
    SIRF ADMIN hi ise access kar sakta hai.
    """
    
    # Sirf Admin User (is_admin=True) hi access kar sakta hai
    permission_classes = [IsAuthenticated, IsCustomAdminUser]
    parser_classes = [MultiPartParser, FormParser] # File upload (profile_image) ke liye

    def get_object(self, id):
        # Helper function se Team_Leader object get karo
        return get_object_or_404(Team_Leader, id=id)

    def get(self, request, id, format=None):
        """
        GET request: Team Leader ki current details return karta hai.
        """
        team_leader = self.get_object(id)
        
        # --- Security Check ---
        # Check karo ki yeh Admin is Team Leader ko edit kar sakta hai ya nahi
        try:
            admin_profile = Admin.objects.get(self_user=request.user)
        except Admin.DoesNotExist:
            return Response({"error": "Admin profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
        if team_leader.admin != admin_profile:
             return Response(
                {"error": "You do not have permission to edit this Team Leader."},
                status=status.HTTP_403_FORBIDDEN
            )
        # --- Check Ends ---

        serializer = ProductivityTeamLeaderSerializer(team_leader) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id, format=None):
        """
        PATCH request: Team Leader ki profile ko update karta hai.
        """
        team_leader = self.get_object(id)

        # --- Security Check ---
        try:
            admin_profile = Admin.objects.get(self_user=request.user)
        except Admin.DoesNotExist:
            return Response({"error": "Admin profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
        if team_leader.admin != admin_profile:
             return Response(
                {"error": "You do not have permission to edit this Team Leader."},
                status=status.HTTP_403_FORBIDDEN
            )
        # --- Check Ends ---
        
        # TeamLeaderUpdateSerializer ka istemal karo
        serializer = TeamLeaderUpdateSerializer(instance=team_leader, data=request.data, partial=True) 
        
        if serializer.is_valid():
            updated_instance = serializer.save()
            
            # Updated data ko 'ProductivityTeamLeaderSerializer' se wapas bhejo
            read_serializer = ProductivityTeamLeaderSerializer(updated_instance)
            return Response(read_serializer.data, status=status.HTTP_200_OK) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id, format=None):
        # POST ko bhi PATCH ki tarah handle karo
        return self.patch(request, id, format)
    



