from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, permissions, filters, generics, views
from django_filters import rest_framework as django_filters
from datetime import date
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