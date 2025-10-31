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
from django.shortcuts import render, get_object_or_404
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


# Yeh nayi class file mein upar ADD karo

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
        res = {}
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        # Check if username and password are provided
        if not username:
            return Response(
                {'status': False, 'message': 'Username is required', 'data': []}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {'status': False, 'message': 'Password is required', 'data': []}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'status': False, 'message': 'Invalid username or password', 'data': []}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the user is a staff member
        # if not user.is_staff_new:
        #     return Response(
        #         {'status': False, 'message': 'Only staff users are allowed to log in', 'data': []}, 
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # if user.user_active is False:
        #     return Response(
        #         {'status': False, 'message': "You don't have permission to login please contact admin", 'data': []}, 
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Mark user as logged in
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        status_value = data.get('status')
        description = data.get('description')

        if mobile == None:
            return Response({"message": "Mobile number is required."}, status=status.HTTP_400_BAD_REQUEST)
        if LeadUser.objects.filter(call=mobile).exists():
            return Response({"message": "Mobile number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        lead_data = {
            'user': user.id,
            'name': name,
            'email': email,
            'call': mobile,
            'message': description,
            'status': status_value
        }
        
        if user.is_staff_new:
            staff_instance = Staff.objects.filter(email=user.email).last()
            lead_data.update({
                'team_leader': staff_instance.team_leader.id,
                'assigned_to': staff_instance.id
            })
            serializer = LeadUserSerializer(data=lead_data)
        
        elif user.is_team_leader:
            team_leader_instance = Team_Leader.objects.filter(email=user.email).last()
            lead_data.update({'team_leader': team_leader_instance.id})
            serializer = LeadUserSerializer(data=lead_data)
        
        elif user.is_admin:
            admin_instance = Admin.objects.filter(email=user.email).last()
            serializer = LeadUserSerializer(data=lead_data)
        
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'lead add successfully', 'status': status.HTTP_201_CREATED, 'data': serializer.data},)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StaffProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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

class SuperAdminDashboardAPIView(APIView):
    """
    API view for the Super Admin Dashboard.
    Provides aggregated lead counts and stats.
    Only accessible by superusers.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # request.user is already the logged-in superuser object
        us = request.user 
        admin_profiles = Admin.objects.filter(user=us)
        admin_serializer = AdminSerializer(admin_profiles, many=True)

        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        # All your counting logic, unchanged
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

        # All your summing logic, unchanged
        total_interested = interested_leads_staff + interested_leads_team_leader
        total_not_interested = not_interested_leads_staff + not_interested_leads_team_leader
        total_other_location = other_location_leads_staff + other_location_leads_team_leader
        total_not_picked = not_picked_leads_staff + not_picked_leads_team_leader
        total_lost = lost_leads_staff + lost_leads_team_leader
        total_visits = lost_visit_staff + lost_visit_team_leader

        total_pending_followup = pending_followup_staff
        total_today_followup = today_followup_staff
        total_tomorrow_followup = tomorrow_followup_staff

        # Build the response data dictionary
        data = {
            'users': admin_serializer.data, # Use serialized data here
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
        }
        
        # Return the data as a JSON response
        return Response(data, status=status.HTTP_200_OK)    
    




# ===================================================================
# NAYA DASHBOARD API (Date Filter Waala)
# ===================================================================
class SuperUserDashboardAPIView(APIView):
    """
    Super User Dashboard ke liye API, date filtering ke saath.
    Sirf superusers ke liye accessible hai.
    """
    permission_classes = [IsAdminUser]

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
# NAYA ADMIN SIDE LEADS RECORD API (Tag Waala)
# ===================================================================
# ===================================================================
# NAYA ADMIN SIDE LEADS RECORD API (Tag Waala) - [FIXED]
# ===================================================================
class AdminSideLeadsRecordAPIView(APIView):
    """
    Admin dashboard se leads ko status tag ke hisaab se filter karne ke liye API.
    """
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAuthenticated] # User ka login hona zaroori hai
    parser_classes = (MultiPartParser, FormParser) # File uploads ke liye zaroori

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response(
                {"error": "File not provided. Please upload a file with the key 'excel_file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # File ko uske naam se padhne ki koshish karo (CSV ya Excel)
        try:
            if excel_file.name.endswith('.csv'):
                df = pd.read_csv(excel_file, encoding='utf-8')
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

        # KeyError se bachne ke liye headers check karo
        required_columns = ['name', 'call', 'send', 'status']
        if not all(col in df.columns for col in required_columns):
            return Response(
                {"error": f"File is missing required columns. Make sure these columns exist (all lowercase): {required_columns}"},
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
            # KeyError se bachne ke liye .get() ka istemaal karo
            name = row.get('name')
            call = row.get('call')
            status_val = row.get('status')
            send_val = row.get('send')

            if not name or pd.isna(name):
                continue
            if not status_val == "Leads":
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
                # Baaki errors ke liye
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






# Yeh code file ke end mein ADD karo

# ===================================================================
# NAYA FREELANCER (ASSOCIATES) DASHBOARD API
# ===================================================================
class FreelancerDashboardAPIView(APIView):
    """
    API for the Super Admin's Freelancer (Associates) Dashboard.
    Shows lead counts and list of freelancers.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        
        # --- 1. Freelancer List ---
        my_staff = Staff.objects.filter(user__is_freelancer=True)
        staff_serializer = ApiStaffSerializer(my_staff, many=True)

        # --- 2. Lead Counts (Sirf Freelancers ke) ---
        total_leads = LeadUser.objects.filter(status="Leads").count() # Note: Original view mein yeh filter freelancer par nahi tha
        total_interested_leads = LeadUser.objects.filter(status="Intrested", assigned_to__user__is_freelancer=True).count()
        total_not_interested_leads = LeadUser.objects.filter(status="Not Interested", assigned_to__user__is_freelancer=True).count()
        total_other_location_leads = LeadUser.objects.filter(status="Other Location", assigned_to__user__is_freelancer=True).count()
        total_not_picked_leads = LeadUser.objects.filter(status="Not Picked", assigned_to__user__is_freelancer=True).count()
        total_lost_leads = LeadUser.objects.filter(status="Lost", assigned_to__user__is_freelancer=True).count()
        total_visits_leads = LeadUser.objects.filter(status="Visit", assigned_to__user__is_freelancer=True).count()

        # --- 3. Salary Calculation Logic (Original code se copy kiya) ---
        # Note: Original code mein `staff_list` sabhi staff ka tha, `my_staff` sirf freelancers ka.
        # Hum original logic ko hi follow karenge.
        
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        
        staff_list = Staff.objects.all() # Original code ke mutabik
        
        days_in_month = monthrange(year, month)[1]
        total_salary_all_staff = 0
        
        for staff in staff_list:
            salary_arg = staff.salary
            if salary_arg is None or salary_arg == "":
                salary_arg = 0
            salary = salary_arg
            daily_salary = round(float(salary) / int(days_in_month))

            leads_data = LeadUser.objects.filter(
                assigned_to=staff,
                updated_date__year=year,
                updated_date__month=month,
                status='Intrested'
            ).values('updated_date__day').annotate(count=Count('id'))

            total_salary = 0
            productivity_data = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}

            for lead in leads_data:
                day = lead['updated_date__day']
                leads_count = lead['count']
                productivity_data[day]['leads'] = leads_count

                if leads_count >= 10:
                    daily_earned_salary = daily_salary
                else:
                    daily_earned_salary = round((daily_salary / 10) * leads_count, 2)

                productivity_data[day]['salary'] = daily_earned_salary
                total_salary += daily_earned_salary
            
            total_salary_all_staff += total_salary
        
        # --- 4. Final Response ---
        data = {
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'total_other_location_leads': total_other_location_leads,
            'total_not_picked_leads': total_not_picked_leads,
            'total_lost_leads': total_lost_leads,
            'total_leads': total_leads,
            'total_visits_leads': total_visits_leads,
            'my_staff': staff_serializer.data, # Yeh freelancer ki list hai
            'total_salary_all_staff': round(total_salary_all_staff, 2), # Yeh sabhi staff ki salary hai
        }
        
        return Response(data, status=status.HTTP_200_OK)
    


# Yeh code file ke end mein ADD karo

# ===================================================================
# NAYA IT STAFF LIST API
# ===================================================================
class ITStaffListAPIView(APIView):
    """
    API for the Super Admin's IT Staff list page.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        
        # --- 1. IT Staff List ---
        it_staff_list = Staff.objects.filter(user__is_it_staff=True)
        
        # --- 2. Serialize Data ---
        # Hum pehle waala ApiStaffSerializer use kar rahe hain
        serializer = ApiStaffSerializer(it_staff_list, many=True)

        # --- 3. Final Response ---
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# Yeh code file ke end mein ADD karo

# ===================================================================
# NAYA ATTENDANCE CALENDAR API
# ===================================================================
class AttendanceCalendarAPIView(APIView):
    """
    API for the attendance calendar.
    Provides calendar data, present/absent counts for a given user and month/year.
    """
    permission_classes = [IsAuthenticated] # User ka login hona zaroori hai

    def get(self, request, id, *args, **kwargs):
        # 1. Get year and month from query parameters
        try:
            year = int(request.query_params.get('year', datetime.today().year))
            month = int(request.query_params.get('month', datetime.today().month))
        except ValueError:
            return Response({"error": "Invalid year or month format."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Get all dates for the month
        _, num_days = monthrange(year, month)
        all_dates = [datetime(year, month, day).date() for day in range(1, num_days + 1)]
        
        today = datetime.today().date()
        
        # 3. Get tasks based on the user ID
        user_to_check = None
        try:
            # 'id=0' ka matlab hai user khud ka attendance check kar raha hai
            if id == 0:
                user_to_check = request.user
            # 'id > 0' ka matlab hai doosre staff member ka check kar rahe hain
            elif id > 0:
                staff_instance = Staff.objects.filter(id=id).last()
                if not staff_instance:
                    return Response({"error": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)
                user_to_check = staff_instance.user
            else:
                return Response({"error": "Invalid ID."}, status=status.HTTP_400_BAD_REQUEST)
                
        except Staff.DoesNotExist:
             return Response({"error": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)

        # Task objects filter karo
        tasks = Task.objects.filter(
            user=user_to_check, 
            task_date__month=month, 
            task_date__year=year
        )
        
        # 4. Task data process karo
        task_dates = {task.task_date for task in tasks}
        
        calendar_data_list = [
            {"date": date, "has_task": date in task_dates, "day_name": date.strftime("%a")}
            for date in all_dates
        ]

        present_count = len(task_dates)
        # Absent days sirf aaj tak ke gino
        absent_count = len([d for d in all_dates if d not in task_dates and d <= today])

        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # 5. Final Response banao
        calendar_serializer = AttendanceCalendarDaySerializer(calendar_data_list, many=True)
        
        data = {
            "id": id, # Jo ID check kar rahe hain
            "user_email": user_to_check.email, # Taki pata chale kiska data hai
            "month": month,
            "year": year,
            "present_count": present_count,
            "absent_count": absent_count,
            "days_of_week": days_of_week,
            "calendar_data": calendar_serializer.data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    



# Yeh code file ke end mein ADD karo

# ===================================================================
# NAYA STAFF PRODUCTIVITY API
# ===================================================================
class StaffProductivityAPIView(APIView):
    """
    API for the Staff Productivity page.
    Calculates leads, calls, and percentages for staff based on user role and filters.
    """
    permission_classes = [IsManagerOrAdmin] # Use the custom permission

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
    


# Yeh code file ke end mein ADD karo (ya purane waale ko replace karo)

# ===================================================================
# NAYA TEAM LEADER PRODUCTIVITY API [FIXED]
# ===================================================================
class TeamLeaderProductivityAPIView(APIView):
    """
    API for the Team Leader Productivity page.
    [FIXED] Ab yeh date, endDate, aur no-date, teeno filters ko sahi se handle karega.
    """
    permission_classes = [IsManagerOrAdmin] # Sirf admin/superuser hi dekh sakte hain

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