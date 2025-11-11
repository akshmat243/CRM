from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import LeadUser
from .models import Admin, Team_Leader, Staff, ProjectFile, Team_LeadData, MerchantInquiry,MerchantFormsData
from django.contrib.auth.models import User
from home.models import *
from django.contrib.auth import authenticate, login as auth_login
import pandas as pd
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .form import ProjectFileForm
User = get_user_model()
from .models import UserActivityLog
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Staff, LeadUser
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
import datetime
import openpyxl
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import datetime
from django.db.models import Count, Q
import calendar
from calendar import monthrange, month_name
import math
from django.db.models import Sum
from django.utils.timezone import now, localtime
from datetime import date
from django.core import serializers
from django.db.models import Count

@login_required(login_url='login')
def super_admin(request):
    if request.method == 'GET':
        user = request.user
        if not request.user.is_superuser:
            
            if request.user.is_superuser:
                user_type = "Super User"
            if request.user.is_admin:
                user_type = "Admin User"
            if request.user.is_team_leader:
                user_type = "Team leader User"
            if request.user.is_staff_new:
                user_type = "Staff User"

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            tagline = f"Log-out user[Email : {request.user.email}, {user_type}, IP : {ip}]"

            ActivityLog.objects.create(
                user = request.user,
                description = tagline,
                ip_address = ip,
                email = request.user.email,
                user_type = user_type,
                activity_type = "Log-out",
                name = request.user.name,
            )
            logout(request)
            return redirect('login') 
    user = user.email
    us = User.objects.get(email=user)
    users = Admin.objects.filter(user=us)
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

    # pending_followup_leader = Team_LeadData.objects.filter(
    #             Q(status='Intrested') & Q(follow_up_date__isnull=False)
    #         ).count()
    # today_followup_leader = Team_LeadData.objects.filter(
    #             Q(status='Intrested') & Q(follow_up_date=today)
    #         ).count()
    # tomorrow_followup_leader = Team_LeadData.objects.filter(
    #             Q(status='Intrested') & Q(follow_up_date=tomorrow)
    #         ).count()

    total_interested = interested_leads_staff + interested_leads_team_leader
    total_not_interested = not_interested_leads_staff + not_interested_leads_team_leader
    total_other_location = other_location_leads_staff + other_location_leads_team_leader
    total_not_picked = not_picked_leads_staff + not_picked_leads_team_leader
    total_lost = lost_leads_staff + lost_leads_team_leader
    total_visits = lost_visit_staff + lost_visit_team_leader

    total_pending_followup = pending_followup_staff
    total_today_followup = today_followup_staff
    total_tomorrow_followup = tomorrow_followup_staff

    context = {
        'users': users,
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
    return render(request, "admin_user.html", context)
    
def super_user_dashboard(request):
    if request.method == 'GET':
        user = request.user
        if not request.user.is_superuser:
            
            if request.user.is_superuser:
                user_type = "Super User"
            if request.user.is_admin:
                user_type = "Admin User"
            if request.user.is_team_leader:
                user_type = "Team leader User"
            if request.user.is_staff_new:
                user_type = "Staff User"

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            tagline = f"Log-out user[Email : {request.user.email}, {user_type}, IP : {ip}]"

            ActivityLog.objects.create(
                user = request.user,
                description = tagline,
                ip_address = ip,
                email = request.user.email,
                user_type = user_type,
                activity_type = "Log-out",
                name = request.user.name,
            )
            logout(request)
            return redirect('login') 
    user = request.user.email
    us = User.objects.get(email=user)
    users = Admin.objects.filter(user=us)

    # Retrieve date range from GET parameters (if provided)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse the dates if they exist
    # if start_date and end_date:
    #     start_date = timezone.make_aware(timezone.datetime.strptime(start_date, '%Y-%m-%d'))
    #     end_date = timezone.make_aware(datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)) - datetime.timedelta(seconds=1)
    #     lead_filter = {'updated_date__range': [start_date, end_date]}

    if start_date and end_date:
        start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)) - timedelta(seconds=1)
        lead_filter = {'updated_date__range': [start_date, end_date]}
    else:
        lead_filter = {}

    # Apply filters
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

    total_interested = interested_leads_staff + interested_leads_team_leader
    total_not_interested = not_interested_leads_staff + not_interested_leads_team_leader
    total_other_location = other_location_leads_staff + other_location_leads_team_leader
    total_not_picked = not_picked_leads_staff + not_picked_leads_team_leader
    total_lost = lost_leads_staff + lost_leads_team_leader
    total_visits = lost_visit_staff + lost_visit_team_leader

    total_calls = total_interested + total_not_interested + total_other_location + total_not_picked + total_lost + total_visits

    total_users = User.objects.count()
    logged_in_users = User.objects.filter(is_user_login=True).count()
    logged_out_users = User.objects.filter(is_user_login=False).count()

    data_points = [
        { "label": "Interested", "y": total_interested  },
        { "label": "Lost",  "y": total_lost  },
        { "label": "Visits",  "y": total_visits  },
        { "label": "Not Interested", "y": total_not_interested  },
        { "label": "Other Location",  "y": total_other_location  },
        { "label": "Not Picked",  "y": total_not_picked  },
        { "label": "Total Calls",  "y": total_calls  },
    ]

    setting = Settings.objects.filter().last()
    context = {
        'users': users,
        'data_points': data_points,
        'total_upload_leads': total_upload_leads,
        'total_assign_leads': total_assign_leads,
        'total_interested': total_interested,
        'total_not_interested': total_not_interested,
        'total_other_location': total_other_location,
        'total_not_picked': total_not_picked,
        'total_lost': total_lost,
        'total_visits': total_visits,
        'start_date': start_date,
        'end_date': end_date,
        'total_users': total_users,
        'logged_in_users': logged_in_users,
        'logged_out_users': logged_out_users,
        'setting': setting,
    }

    return render(request, "super_admin_dash.html", context)

def admin_side_leads_record(request, tag):
    
    total_upload_leads = Team_LeadData.objects.filter(status='Leads')
    total_assign_leads = LeadUser.objects.filter(status='Leads')

    interested_leads_staff = LeadUser.objects.filter(status='Intrested')
    interested_leads_team_leader = Team_LeadData.objects.filter(status='Intrested')

    not_interested_leads_staff = LeadUser.objects.filter(status='Not Interested')
    other_location_leads_staff = LeadUser.objects.filter(status='Other Location')
    not_picked_leads_staff = LeadUser.objects.filter(status='Not Picked')
    lost_leads_staff = LeadUser.objects.filter(status='Lost')
    lost_visit_staff = LeadUser.objects.filter(status='Visit')
    
    not_interested_leads_team_leader  = Team_LeadData.objects.filter(status='Not Interested')
    other_location_leads_team_leader  = Team_LeadData.objects.filter(status='Other Location')
    not_picked_leads_team_leader = Team_LeadData.objects.filter(status='Not Picked')
    lost_leads_team_leader  = Team_LeadData.objects.filter(status='Lost')
    lost_visit_team_leader  = Team_LeadData.objects.filter(status='Visit')

    if tag == "total_visit_tag":
        combined_visit_leads = list(lost_visit_staff) + list(lost_visit_team_leader)
        context = {
            "leads": combined_visit_leads,
        }
    if tag == "total_lost_lead_tag":
        combined_lost_leads = list(lost_leads_staff) + list(lost_leads_team_leader)
        context = {
            "leads": combined_lost_leads,
        }
    if tag == "total_not_picked_lead_tag":
        combined_not_picked_leads = list(not_picked_leads_staff) + list(not_picked_leads_team_leader)
        context = {
            "leads": combined_not_picked_leads,
        }
    if tag == "total_other_location_lead_tag":
        combined_other_location_leads = list(other_location_leads_staff) + list(other_location_leads_team_leader)
        context = {
            "leads": combined_other_location_leads,
        }
    if tag == "total_not_interested_lead_tag":
        combined_not_interested_leads = list(not_interested_leads_staff) + list(not_interested_leads_team_leader)
        context = {
            "leads": combined_not_interested_leads,
        }
    if tag == "total_upload_lead_tag":
        context = {
            "leads": total_upload_leads,
        }
    if tag == "total_assigned_lead_tag":
        context = {
            "leads": total_assign_leads,
        }
    if tag == "total_interested_lead_tag":
        combined_interested_leads = list(interested_leads_staff) + list(interested_leads_team_leader)
        context = {
            "leads": combined_interested_leads,
        }
    return render(request, "admin_side_leads_record.html", context)


@login_required(login_url='login')
def admin_add(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        profile_image = request.FILES.get("profile_image")

        dob = request.POST['dob']
        pancard = request.POST['pancard']
        aadharCard = request.POST['aadharCard']
        marksheet = request.POST['marksheet']
        degree = request.POST['degree']
        account_number = request.POST['account_number']
        upi_id = request.POST['upi_id']
        bank_name = request.POST['bank_name']
        ifsc_code = request.POST['ifsc_code']
        salary = request.POST['salary']

        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('admin_add')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('admin_add')

        user = User.objects.create(username=username, password=password,
                email=username, profile_image=profile_image, name=name, mobile=mobile, is_admin=True)
        user.set_password(password)
        user.save()

        admin = Admin.objects.create(
            user=request.user,
            self_user=user,
            email=username,
            name=name,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,

            dob=dob,
            pancard=pancard,
            aadharCard=aadharCard,
            marksheet=marksheet,
            degree=degree,
            account_number=account_number,
            upi_id=upi_id,
            bank_name=bank_name,
            ifsc_code=ifsc_code,
            salary=salary,
        )
        messages.success(request, "Admin Created Successfully.")
        return redirect('super_admin')
    context = {
        'messages': messages.get_messages(request),
    }
    return render(request, 'admin_add.html', context)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Email/Username or Password Incorrect")
            return redirect('login')
        if user is not None:
            if not user.is_superuser:
                if user.user_active is False:
                    messages.error(request, "You don't have permission to login please contact admin")
                    return redirect('login')
            
            auth.login(request, user)
            if request.user.is_superuser:
                user_type = "Super User"
            if request.user.is_admin:
                user_type = "Admin User"
            if request.user.is_team_leader:
                user_type = "Team leader User"
            if request.user.is_staff_new:
                user_type = "Staff User"

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            tagline = f"Log-In user[Email : {request.user.email}, {user_type}, IP : {ip}]"
            user = request.user
            user.is_user_login = True
            user.save()
            if request.user.is_admin:
                admin_email = user.email
                admin_instance = Admin.objects.filter(email=admin_email).last()
                my_user = admin_instance.user
                ActivityLog.objects.create(
                    user = my_user,
                    description = tagline,
                    ip_address = ip,
                    email = request.user.email,
                    user_type = user_type,
                    activity_type = "Log-In",
                    name = request.user.name,
                )
            if request.user.is_team_leader:
                admin_email = user.email
                admin_instance = Team_Leader.objects.filter(email=admin_email).last()
                my_user1 = admin_instance.admin
                ActivityLog.objects.create(
                    admin = my_user1,
                    description = tagline,
                    ip_address = ip,
                    email = request.user.email,
                    user_type = user_type,
                    activity_type = "Log-In",
                    name = request.user.name,
                )

            if request.user.is_staff_new:
                admin_email = user.email
                admin_instance = Staff.objects.filter(email=admin_email).last()
                my_user2 = admin_instance.team_leader
                ActivityLog.objects.create(
                    team_leader = my_user2,
                    description = tagline,
                    ip_address = ip,
                    email = request.user.email,
                    user_type = user_type,
                    activity_type = "Log-In",
                    name = request.user.name,
                )

            # if not request.user.is_superuser:
                # ActivityLog.objects.create(
                #     user = my_user,
                #     admin = my_user1,
                #     team_leader = my_user2,
                #     description = tagline,
                #     ip_address = ip,
                # )
            if user.is_superuser:
                # messages.success(request, "Super User Login Successful")
                return redirect('super_user_dashboard')
            elif user.is_admin:
                user1 = user.username
                user = Admin.objects.get(email=user1)
                # messages.success(request, "Admin Login Successful")
                return redirect('team_leader_user')
            elif user.is_team_leader:
                # messages.success(request, "Team Leader Login Successful")
                return redirect('staff_user')
            elif user.is_staff_new:
                request.session['staff_email'] = user.email
                # messages.success(request, "Staff Login Successful")
                return redirect('leads')
            else:
                # messages.error(request, "User role not recognized")
                return redirect('login')
            
    return render(request, 'Login.html')

@csrf_exempt
def toggle_user_active(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_type = request.POST.get('user_type')
        is_active = request.POST.get('is_active') == 'true'
        if user_type == 'staff':
            user_instance = Staff.objects.filter(id=user_id).last().email
        if user_type == 'admin':
            user_instance = Admin.objects.filter(id=user_id).last().email
        if user_type == 'teamlead':
            user_instance = Team_Leader.objects.filter(id=user_id).last().email

        try:
            user = User.objects.get(email=user_instance)
            user.user_active = is_active
            user.save()
            return JsonResponse({'status': 'success'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def team_dashboard(request):
    return render(request, "admin_dashboard/index.html")


@login_required(login_url='login')
def team_leader_user(request):
    if request.method == 'GET':
        user = request.user
        user1 = user.username
        us = Admin.objects.get(email=user1)
        users = Team_Leader.objects.filter(admin=us)

        today = timezone.now().date()
        setting = Settings.objects.filter().last()

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)) - timedelta(seconds=1)
        else:
            start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
        
        lead_filter = {'updated_date__range': [start_date, end_date]}
        total_leads = LeadUser.objects.filter(status="Leads", team_leader__in=users, **lead_filter).count()
        total_interested_leads = LeadUser.objects.filter(status="Intrested", **lead_filter, team_leader__in=users).count()
        total_not_interested_leads = LeadUser.objects.filter(status="Not Interested", **lead_filter, team_leader__in=users).count()
        total_other_location_leads = LeadUser.objects.filter(status="Other Location", **lead_filter, team_leader__in=users).count()
        total_not_picked_leads = LeadUser.objects.filter(status="Not Picked", **lead_filter, team_leader__in=users).count()
        total_lost_leads = LeadUser.objects.filter(status="Lost", **lead_filter, team_leader__in=users).count()
        total_visits_leads = LeadUser.objects.filter(status="Visit", **lead_filter, team_leader__in=users).count()

        context = {
            # 'users': users, 
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'total_other_location_leads': total_other_location_leads,
            'total_not_picked_leads': total_not_picked_leads,
            'total_lost_leads': total_lost_leads,
            'total_leads': total_leads,
            'total_visits_leads': total_visits_leads,
            'users': users,
            'setting': setting,
        }
    return render(request, "admin_dashboard/team_leader_user.html", context)


# @login_required(login_url='login')
# def home(request):
#     return render(request, "admin_dashboard/team_leader/index.html")


@login_required(login_url='login')
def view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = LeadUser.objects.get(email=request.user.username)
            return render(request, 'admin_dashboard/team_leader/view-profile.html', {'admin': admin})
    if request.method == 'POST':
        admin = LeadUser.objects.get(email=request.user.username)
        new_email = request.POST['email']
        username = request.user.username
        user = Staff.objects.get(username=username)
        if new_email != admin.email and LeadUser.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('view_profile')

        user.email = request.POST['email']
        user.username = request.POST['email']

        admin.name = request.POST.get('name', admin.name)
        admin.email = new_email
        admin.call = request.POST.get('call', admin.call)
        admin.save()
        user.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('leads')

    return render(request, "admin_dashboard/team_leader/user-profile.html")

# def staff(request):
#     users = Staff.objects.all()
#     return render(request, "home/staff.html", {'users': users})

@login_required(login_url='login')
def logout_view(request):
    # if request.session['staff_email']:
    #     del request.session['staff_email']
    if request.user:
        request.user.is_login = False
        request.user.save()
    if request.user.is_superuser:
        user_type = "Super User"
    if request.user.is_admin:
        user_type = "Admin User"
    if request.user.is_team_leader:
        user_type = "Team leader User"
    if request.user.is_staff_new:
        user_type = "Staff User"

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    tagline = f"Log-out user[Email : {request.user.email}, {user_type}, IP : {ip}]"

    user = request.user
    if request.user.is_admin:
        admin_email = user.email
        admin_instance = Admin.objects.filter(email=admin_email).last()
        my_user = admin_instance.user
        ActivityLog.objects.create(
            user = my_user,
            description = tagline,
            ip_address = ip,
            email = request.user.email,
            user_type = user_type,
            activity_type = "Log-out",
            name = request.user.name,
        )
    if request.user.is_team_leader:
        admin_email = user.email
        admin_instance = Team_Leader.objects.filter(email=admin_email).last()
        my_user1 = admin_instance.admin
        ActivityLog.objects.create(
            admin = my_user1,
            description = tagline,
            ip_address = ip,
            email = request.user.email,
            user_type = user_type,
            activity_type = "Log-out",
            name = request.user.name,
        )

    if request.user.is_staff_new:
        name = request.user.name
        admin_email = user.email
        admin_instance = Staff.objects.filter(email=admin_email).last()
        my_user2 = admin_instance.team_leader
        ActivityLog.objects.create(
            team_leader = my_user2,
            description = tagline,
            ip_address = ip,
            email = request.user.email,
            user_type = user_type,
            activity_type = "Log-out",
            name = request.user.name,
        )
    # if request.user.is_team_leader:
    #     admin_email = user.email
    #     admin_instance = Team_Leader.objects.filter(email=admin_email).last()
    #     my_user = admin_instance.user
    # ActivityLog.objects.create(
    #     user = my_user,
    #     description = tagline,
    #     ip_address = ip
    # )
    user = request.user
    user.is_user_login = False
    user.save()
    logout(request)
    messages.success(request, "Logout Successfully")
    return render(request, 'Login.html')

def update_password(request):
    if request.method == 'GET':
        # if request.user.is_team_leader:
        #     user_email = request.user.email
        #     team_leader_instance = Team_Leader.objects.filter(email=user_email).last()
        #     staff_instance = Staff.objects.filter(team_leader=team_leader_instance)

        return render(request, 'admin-dashboard/staff/view-profile.html')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            user = get_object_or_404(User, email=user_id)
            user.password = make_password(password)
            user.save()
            messages.success(request, f'Password for {user.name} has been updated successfully.')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return redirect('team_view_profile')

@login_required(login_url='login')
def status_update(request):
    if request.method == 'POST':
        merchant_id = request.POST.get('leads_id')

        if request.user.is_superuser: 
            user_type = "Super User"
        elif request.user.is_admin:
            user_type = "Admin User"
        elif request.user.is_team_leader:
            user_type = "Team Leader User"
        elif request.user.is_staff_new:
            user_type = "Staff User"

        if merchant_id:
            new_status = request.POST.get('new_status')
            try:
                # Update status for LeadUser
                status_update_user = LeadUser.objects.get(id=merchant_id)
                tagline = f"Lead status changed from {status_update_user.status} to {new_status} by user[Email: {request.user.email}, {user_type}]"
                tag2 = f"Lead status changed from {status_update_user.status} to {new_status}"
                status_update_user.status = new_status
                status_update_user.save()

                # Log activity for LeadUser
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                if request.user.is_staff_new:
                    admin_email = request.user.email
                    admin_instance = Staff.objects.filter(email=admin_email).last()
                    my_user2 = admin_instance.team_leader
                    ActivityLog.objects.create(
                        team_leader=my_user2,
                        description=tagline,
                        ip_address=ip,
                        email = request.user.email,
                        user_type = user_type,
                        activity_type = tag2,
                        name = request.user.name,
                    )
            except LeadUser.DoesNotExist:
                # Handle the case where LeadUser does not exist
                pass

            try:
                # Update status for Team_LeadData
                status_update_team_lead = Team_LeadData.objects.get(id=merchant_id)
                tagline_team_lead = f"Lead status changed from {status_update_team_lead.status} to {new_status} by user[Email: {request.user.email}, {user_type}]"
                tag2 = f"Lead status changed from {status_update_user.status} to {new_status}"
                status_update_team_lead.status = new_status
                status_update_team_lead.save()

                # Log activity for Team_LeadData
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                if request.user.is_staff_new:
                    admin_email = request.user.email
                    admin_instance = Staff.objects.filter(email=admin_email).last()
                    my_user2 = admin_instance.team_leader
                    ActivityLog.objects.create(
                        team_leader=my_user2,
                        description=tagline_team_lead,
                        ip_address=ip,
                        email = request.user.email,
                        user_type = user_type,
                        activity_type = tag2,
                        name = request.user.name,
                    )
            except Team_LeadData.DoesNotExist:
                # Handle the case where Team_LeadData does not exist
                pass
        if request.user.is_team_leader:
            return redirect('lead')
        if request.user.is_staff_new:
            return redirect('leads')
    return render(request, 'admin_dashboard/team_leader/leads.html')



# @login_required(login_url='login')
# def status_update(request):
#     if request.method == 'POST':
#         merchant_id = request.POST.get('leads_id')
#         print(merchant_id, 'AAAAAAAAAAAAAAAA')

#         if request.user.is_superuser:
#             user_type = "Super User"
#         if request.user.is_admin:
#             user_type = "Admin User"
#         if request.user.is_team_leader:
#             user_type = "Team leader User"
#         if request.user.is_staff_new:
#             user_type = "Staff User"

#         if merchant_id:
#             new_status = request.POST.get('new_status')
#             status_update_user = LeadUser.objects.get(id=merchant_id)
#             tagline = f"Lead status change from {status_update_user.status} to {new_status} by user[Email : {request.user.email}, {user_type}]"
#             status_update_user.status = new_status
#             status_update_user.save()

#             x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#             if x_forwarded_for:
#                 ip = x_forwarded_for.split(',')[0]
#             else:
#                 ip = request.META.get('REMOTE_ADDR')

#             user = request.user
#             if request.user.is_staff_new:
#                 admin_email = user.email
#                 admin_instance = Staff.objects.filter(email=admin_email).last()
#                 my_user2 = admin_instance.team_leader
#                 ActivityLog.objects.create(
#                     team_leader = my_user2,
#                     description = tagline,
#                     ip_address = ip
#                 )

#         return redirect('leads')
#     return render(request, 'admin_dashboard/team_leader/leads.html', {'status_update_user': status_update_user})





@login_required(login_url='login')
def staff_user(request):
    if request.method == 'GET':
        user = request.user
        user1 = user.username
        us = Team_Leader.objects.get(email=user1)
        users = Staff.objects.filter(team_leader=us)
        now = timezone.now()
        setting = Settings.objects.filter().last()

        user_logs = []
        logged_in_count = 0
        logged_out_count = 0

        for staff in users:
            last_log = UserActivityLog.objects.filter(user=staff.user).order_by('-login_time').first()
            if last_log:
                if last_log.logout_time:
                    status = 'Inactive'
                    duration = str(last_log.logout_time - last_log.login_time).split('.')[0]
                    logged_out_count+=1
                else:
                    status = 'Active'
                    duration = str(now - last_log.login_time).split('.')[0]
                    logged_in_count+=1
            else:
                status = 'No data'
                duration = 'No data'
                logged_out_count+=1
            user_logs.append({
                'user': staff.user,
                'username':staff.name,
                'mobile': staff.mobile,
                'email': staff.user.email,
                'created_date': staff.user.date_joined,
                # 'updated_date':staff.user.updated_date,
                'status': status,
                'duration': duration,
                'id' : staff.id
            })

        total_staff=logged_in_count+logged_out_count

# -------------------- xxx ------------------------------------------

        user = request.user
        total_leads, visits_leads, total_interested_leads, total_not_interested_leads, other_location_leads, not_picked_leads, lost_leads = 0, 0, 0, 0, 0, 0, 0
        total_leads_instance = []
        total_interested_leads_instance = []
        total_not_interested_leads_instance = []
        other_location_leads_instance = []
        not_picked_leads_instance = []
        lost_leads_instance = []
        visits_leads_instance = []
        
        try:
            team_lead = Team_Leader.objects.get(user=user)
        except Team_Leader.DoesNotExist:
            team_lead = None

        if team_lead:
            # Team leader's unassigned leads
            leads2 = Team_LeadData.objects.filter(assigned_to=None, team_leader=team_lead,)
            total_uplode_leads = leads2.count()

            # Staff assigned to the team leader
            staff_members = Staff.objects.filter(team_leader=team_lead)

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
            
            # Collect data for each staff member
            for staff in staff_members:
                staff_leads = LeadUser.objects.filter(assigned_to=staff)
                total_leads += staff_leads.filter(status="Leads", **lead_filter).count()
                total_interested_leads += staff_leads.filter(status="Intrested", **lead_filter).count()
                total_not_interested_leads += staff_leads.filter(status="Not Interested", **lead_filter).count()
                other_location_leads += staff_leads.filter(status="Other Location", **lead_filter).count()
                not_picked_leads += staff_leads.filter(status="Not Picked", **lead_filter).count()
                lost_leads += staff_leads.filter(status="Lost", **lead_filter).count()
                visits_leads += staff_leads.filter(status="Visit", **lead_filter).count()

                total_leads_instance += staff_leads.filter(status="Leads", **lead_filter)
                total_interested_leads_instance += staff_leads.filter(status="Intrested", **lead_filter)
                total_not_interested_leads_instance += staff_leads.filter(status="Not Interested", **lead_filter)
                other_location_leads_instance += staff_leads.filter(status="Other Location", **lead_filter)
                not_picked_leads_instance += staff_leads.filter(status="Not Picked", **lead_filter)
                lost_leads_instance += staff_leads.filter(status="Lost", **lead_filter)
                visits_leads_instance += staff_leads.filter(status="Visit", **lead_filter)

            # Add team leader's own data
            total_leads += leads2.filter(status="Leads", **lead_filter).count()
            total_interested_leads += leads2.filter(status="Intrested", **lead_filter).count()
            total_not_interested_leads += leads2.filter(status="Not Interested", **lead_filter).count()
            other_location_leads += leads2.filter(status="Other Location", **lead_filter).count()
            not_picked_leads += leads2.filter(status="Not Picked", **lead_filter).count()
            lost_leads += leads2.filter(status="Lost", **lead_filter).count()
            visits_leads += leads2.filter(status="Visit", **lead_filter).count()

            total_leads_instance += leads2.filter(status="Leads", **lead_filter)
            total_interested_leads_instance += leads2.filter(status="Intrested", **lead_filter)
            total_not_interested_leads_instance += leads2.filter(status="Not Interested", **lead_filter)
            other_location_leads_instance += leads2.filter(status="Other Location", **lead_filter)
            not_picked_leads_instance += leads2.filter(status="Not Picked", **lead_filter)
            lost_leads_instance += leads2.filter(status="Lost", **lead_filter)
            visits_leads_instance += leads2.filter(status="Visit", **lead_filter)

        else:
            leads2 = Team_LeadData.objects.none()
        not_interested_inquiry_data = ""
        if user.dsr_manager:
            not_interested_inquiry_data = MerchantInquiry.objects.filter(is_interested=False).order_by('-id')
        executive_manager_inquiry_data = []
        interested_count = 0
        not_interested_count = 0
        new_inquiries_count = 0
        pending_inquiries_count =  0 
        completed_inquiries_count = 0
        if user.executive_manager:
                executive_manager_inquiry_data = MerchantInquiry.objects.filter(submitted_by=user).order_by("-id")
                interested_count = executive_manager_inquiry_data.filter(submitted_by=user, is_interested=True).count()
                not_interested_count = executive_manager_inquiry_data.filter(submitted_by=user, is_interested=False).count()
                new_inquiries_count = executive_manager_inquiry_data.filter(submitted_by=user, inquiry_status='New Inquiry').count()
        on_boarding_manager_inquiry_data = []

        if user.on_boarding_manager:
                on_boarding_manager_inquiry_data = MerchantInquiry.objects.filter(assigned_user=user).order_by("-id")
                interested_count = on_boarding_manager_inquiry_data.filter(assigned_user=user, is_interested=True).count()
                new_inquiries_count = on_boarding_manager_inquiry_data.filter(assigned_user = user, inquiry_status='New Inquiry').count()
        delivery_manager_inquiry_data = []        
        if user.delivery_manager :
                delivery_manager_inquiry_data = MerchantInquiry.objects.filter(assigned_user=user).order_by("-id")
                pending_inquiries_count = delivery_manager_inquiry_data.filter(assigned_user = user, inquiry_status='Pending Delivery').count()
                completed_inquiries_count = delivery_manager_inquiry_data.filter(assigned_user = user, inquiry_status='Completed').count()
                new_inquiries_count = delivery_manager_inquiry_data.filter(assigned_user = user, inquiry_status='New Inquiry').count()

        context = {
            'user_logs': user_logs,
            'total_staff':total_staff,
            'logged_in_count': logged_in_count,
            'logged_out_count': logged_out_count,
            'total_uplode_leads':total_uplode_leads,
            'leads2': leads2,
            'total_leads': total_leads,
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'other_location_leads': other_location_leads,
            'not_picked_leads': not_picked_leads,
            'lost_leads': lost_leads,
            'visits_leads': visits_leads,

            'total_leads_instance': total_leads_instance,
            'total_interested_leads_instance': total_interested_leads_instance,
            'total_not_interested_leads_instance': total_not_interested_leads_instance,
            'other_location_leads_instance': other_location_leads_instance,
            'not_picked_leads_instance': not_picked_leads_instance,
            'lost_leads_instance': lost_leads_instance,
            'visits_leads_instance': visits_leads_instance,
            'setting': setting,
            'not_interested_inquiry_data':not_interested_inquiry_data,
            'executive_manager_inquiry_data' : executive_manager_inquiry_data,
            'on_boarding_manager_inquiry_data': on_boarding_manager_inquiry_data,
            'interested_count': interested_count,
            'not_interested_count': not_interested_count,
            'new_inquiries_count': new_inquiries_count,
            'delivery_manager_inquiry_data': delivery_manager_inquiry_data,
            'pending_inquiries_count' : pending_inquiries_count,
            'completed_inquiries_count':completed_inquiries_count

            }

        return render(request, "admin_dashboard/staff/staff_user.html", context)
    
def all_leads_data(request, tag):
    user = request.user
    total_leads, total_visits_leads, total_interested_leads, total_not_interested_leads, other_location_leads, not_picked_leads, lost_leads = 0, 0, 0, 0, 0, 0, 0
    total_leads_instance = []
    total_interested_leads_instance = []
    total_not_interested_leads_instance = []
    other_location_leads_instance = []
    not_picked_leads_instance = []
    lost_leads_instance = []
    visits_leads_instance = []
    
    try:
        team_lead = Team_Leader.objects.get(user=user)
    except Team_Leader.DoesNotExist:
        team_lead = None

    if team_lead:
        # Team leader's unassigned leads
        leads2 = Team_LeadData.objects.filter(assigned_to=None, team_leader=team_lead)
        total_uplode_leads = leads2.count()

        # Staff assigned to the team leader
        staff_members = Staff.objects.filter(team_leader=team_lead)
        
        # Collect data for each staff member
        for staff in staff_members:
            staff_leads = LeadUser.objects.filter(assigned_to=staff)
            total_leads += staff_leads.filter(status="Leads").count()
            total_interested_leads += staff_leads.filter(status="Intrested").count()
            total_not_interested_leads += staff_leads.filter(status="Not Interested").count()
            other_location_leads += staff_leads.filter(status="Other Location").count()
            not_picked_leads += staff_leads.filter(status="Not Picked").count()
            lost_leads += staff_leads.filter(status="Lost").count()
            total_visits_leads += staff_leads.filter(status="Visit").count()

            total_leads_instance += staff_leads.filter(status="Leads")
            total_interested_leads_instance += staff_leads.filter(status="Intrested")
            total_not_interested_leads_instance += staff_leads.filter(status="Not Interested")
            other_location_leads_instance += staff_leads.filter(status="Other Location")
            not_picked_leads_instance += staff_leads.filter(status="Not Picked")
            lost_leads_instance += staff_leads.filter(status="Lost")
            visits_leads_instance += staff_leads.filter(status="Visit")

        # Add team leader's own data
        total_leads += leads2.filter(status="Leads").count()
        total_interested_leads += leads2.filter(status="Intrested").count()
        total_not_interested_leads += leads2.filter(status="Not Interested").count()
        other_location_leads += leads2.filter(status="Other Location").count()
        not_picked_leads += leads2.filter(status="Not Picked").count()
        lost_leads += leads2.filter(status="Lost").count()
        total_visits_leads += leads2.filter(status="Visit").count()

        total_leads_instance += leads2.filter(status="Leads")
        total_interested_leads_instance += leads2.filter(status="Intrested")
        total_not_interested_leads_instance += leads2.filter(status="Not Interested")
        other_location_leads_instance += leads2.filter(status="Other Location")
        not_picked_leads_instance += leads2.filter(status="Not Picked")
        lost_leads_instance += leads2.filter(status="Lost")
        visits_leads_instance += leads2.filter(status="Visit")

    else:
        leads2 = Team_LeadData.objects.none()
    
    if tag == 'total_visit_tag':
        context = {
            'leads' : visits_leads_instance,
        }
    if tag == 'total_leads_tag':
        context = {
            'leads' : total_leads_instance,
        }
    if tag == 'total_interested_tag':
        context = {
            'leads' : total_interested_leads_instance,
        }
    if tag == 'total_not_interested_tag':
        context = {
            'leads' : total_not_interested_leads_instance,
        }
    if tag == 'total_other_location_tag':
        context = {
            'leads' : other_location_leads_instance,
        }
    if tag == 'total_not_picked_tag':
        context = {
            'leads' : not_picked_leads_instance,
        }
    if tag == 'total_lost_tag':
        context = {
            'leads' : lost_leads_instance,
        }
    # context = {
    #     'total_uplode_leads':total_uplode_leads,
    #     'leads2': leads2,
    #     'total_leads': total_leads,
    #     'total_interested_leads': total_interested_leads,
    #     'total_not_interested_leads': total_not_interested_leads,
    #     'other_location_leads': other_location_leads,
    #     'not_picked_leads': not_picked_leads,
    #     'lost_leads': lost_leads,

    #     'total_leads_instance': total_leads_instance,
    #     'total_interested_leads_instance': total_interested_leads_instance,
    #     'total_not_interested_leads_instance': total_not_interested_leads_instance,
    #     'other_location_leads_instance': other_location_leads_instance,
    #     'not_picked_leads_instance': not_picked_leads_instance,
    #     'lost_leads_instance': lost_leads_instance,
    #     }
    return render(request, "admin_dashboard/staff/all_leads_data.html", context)





@login_required(login_url='login')
def lead(request):

    user = request.user

    user1 = user.username
    us = Team_Leader.objects.get(email=user1)
    users = Staff.objects.filter(team_leader=us)

    user_logs = []
    for staff in users:
        user_logs.append({
                'user': staff.user,
                'username':staff.name,
                'mobile': staff.mobile,
                'email': staff.user.email,
            })


    total_leads, total_lost_leads, total_customer, total_maybe = 0, 0, 0, 0

    try:
        team_lead = Team_Leader.objects.get(user=user)
    except Team_Leader.DoesNotExist:
        team_lead = None

    if team_lead:
        # Team leader's unassigned leads
        leads2 = Team_LeadData.objects.filter(assigned_to=None, team_leader=team_lead)
        total_uplode_leads = leads2.count()
        leads3=LeadUser.objects.filter(status="Intrested")
        customer_count=leads3.count()
        leads4=LeadUser.objects.filter(status="Lost")
        lost_count=leads4.count()
        # Staff assigned to the team leader
        staff_members = Staff.objects.filter(team_leader=team_lead)
        
        # Collect data for each staff member
        for staff in staff_members:
            staff_leads = LeadUser.objects.filter(assigned_to=staff)
            total_leads += staff_leads.filter(status="Leads").count()
            total_lost_leads += staff_leads.filter(status="Lost_Leads").count()
            total_customer += staff_leads.filter(status="Customer").count()
            total_maybe += staff_leads.filter(status="Maybe").count()

        # Add team leader's own data
        total_leads += leads2.filter(status="Leads").count()
        total_lost_leads += leads2.filter(status="Lost_Leads").count()
        total_customer += leads2.filter(status="Customer").count()
        total_maybe += leads2.filter(status="Maybe").count()
    else:
        leads2 = Team_LeadData.objects.none()
        leads3= Team_LeadData.objects.none()

    context = {
        'total_uplode_leads':total_uplode_leads,
        'leads2': leads2,
        'total_leads': total_leads,
        'total_lost_leads': total_lost_leads,
        'total_customer': total_customer,
        'total_maybe': total_maybe,
        'user_logs': user_logs,
        'leads3':leads3,
        'customer_count':customer_count,
        'leads4':leads4,
        'lost_count':lost_count,
    }

    return render(request, "admin_dashboard/staff/lead.html", context)







@login_required(login_url='login')
def staff_dashboard(request):
    return render(request, "admin_dashboard/staff/index.html")


@login_required(login_url='login')
def view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = User.objects.get(email=request.user.email)
            return render(request, 'view-profile.html', {'admin': admin})
    if request.method == 'POST':
        admin = User.objects.get(email=request.user.email)
        tag = request.POST.get('tag', None)
        if tag == 'logo':
            logo = request.FILES.get('logo', None)
            if logo:
                setting = Settings.objects.filter().last()
                if setting:
                    setting.logo = logo
                    setting.save()
                else:
                    setting = Settings.objects.create(logo=logo)
                return redirect('view_profile')
            return redirect('view_profile')

        new_email = request.POST['email']
        username = request.user.username
        user = User.objects.get(username=username)
        if new_email != admin.email and User.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('view_profile')

        user.email = request.POST['email']
        user.username = request.POST['email']
        user.profile_image = request.FILES.get("profile_image")

        admin.name = request.POST.get('name', admin.name)
        admin.email = new_email
        admin.save()
        user.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('super_admin')

    return render(request, "user-profile.html")

@login_required(login_url='login')
def admin_view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = Admin.objects.get(email=request.user.email)
            return render(request, 'admin_dashboard/view-profile.html', {'admin': admin})

    if request.method == 'POST':
        admin = get_object_or_404(Admin, email=request.user.email)
        teamlead_email = admin.email
        user_instance = User.objects.filter(email=teamlead_email).last()
        new_email = request.POST.get('email')

        if new_email != admin.email and Admin.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('admin_view_profile')

        admin.email = new_email
        admin.name = request.POST.get('name')
        admin.mobile = request.POST.get('mobile')
        admin.address = request.POST.get('address')
        admin.city = request.POST.get('city')
        admin.state = request.POST.get('state')
        admin.pincode = request.POST.get('pincode')

        admin.save()
        user_instance.email = new_email
        user_instance.username = new_email
        user_instance.name = request.POST.get('name')
        user_instance.mobile = request.POST.get('mobile')
        user_instance.profile_image = request.FILES.get("profile_image")
        user_instance.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('team_leader_user')

    return render(request, "admin_dashboard/user-profile.html")


@login_required(login_url='login')
def team_view_profile(request):
    if request.method == 'GET':

        if request.user:
            if request.user.is_team_leader:
                user_email = request.user.email
                team_leader_instance = Team_Leader.objects.filter(email=user_email).last()
                staff_instance = Staff.objects.filter(team_leader=team_leader_instance)

                admin = Team_Leader.objects.get(email=request.user.email)
                context = {
                    'admin': admin,
                    'staff_instance': staff_instance,
                }
            return render(request, 'admin_dashboard/staff/view-profile.html', context)

    if request.method == 'POST':
        admin = get_object_or_404(Team_Leader, email=request.user.email)
        teamlead_email = admin.email
        user_instance = User.objects.filter(email=teamlead_email).last()
        new_email = request.POST.get('email')

        if new_email != admin.email and Team_Leader.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('team_view_profile')

        admin.email = new_email
        admin.name = request.POST.get('name')
        admin.mobile = request.POST.get('mobile')
        admin.address = request.POST.get('address')
        admin.city = request.POST.get('city')
        admin.state = request.POST.get('state')
        admin.pincode = request.POST.get('pincode')

        admin.save()
        user_instance.email = new_email
        user_instance.username = new_email
        user_instance.name = request.POST.get('name')
        user_instance.mobile = request.POST.get('mobile')
        user_instance.profile_image = request.FILES.get("profile_image")
        user_instance.save()
        user_instance.save()

        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('staff_user')

    return render(request, "admin_dashboard/staff/user-profile.html")








@login_required(login_url='login')
def staff_view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = Staff.objects.get(email=request.user.email)
            return render(request, "admin_dashboard/team_leader/view-profile.html", {'admin': admin})

    if request.method == 'POST':
        admin = get_object_or_404(Staff, email=request.user.email)
        teamlead_email = admin.email
        user_instance = User.objects.filter(email=teamlead_email).last()
        new_email = request.POST.get('email')

        if new_email != admin.email and Staff.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('staff_view_profile')

        admin.email = new_email
        admin.name = request.POST.get('name')
        admin.mobile = request.POST.get('mobile')
        admin.address = request.POST.get('address')
        admin.city = request.POST.get('city')
        admin.state = request.POST.get('state')
        admin.pincode = request.POST.get('pincode')

        admin.dob = request.POST['dob']
        admin.pancard = request.POST['pancard']
        admin.aadharCard = request.POST['aadharCard']
        admin.marksheet = request.POST.get('marksheet', None)
        admin.degree = request.POST['degree']
        admin.account_number = request.POST['account_number']
        admin.upi_id = request.POST['upi_id']
        admin.bank_name = request.POST['bank_name']
        admin.ifsc_code = request.POST['ifsc_code']

        admin.save()

        user_instance.email = new_email
        user_instance.username = new_email
        user_instance.name = request.POST.get('name')
        user_instance.mobile = request.POST.get('mobile')
        user_instance.profile_image = request.FILES.get("profile_image")
        user_instance.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('staff_view_profile')

    return render(request, "admin_dashboard/team_leader/view-profile.html")


# @login_required(login_url='login')
# def update_user(request):
#     users = LeadUser.objects.all()

#     if request.method == 'POST':
#         merchant_id = request.POST.get('leads_id')
#         new_status = request.POST.get('new_status')

#         if merchant_id and new_status:
#             try:
#                 user_to_update = LeadUser.objects.get(id=merchant_id)
#                 user_to_update.status = new_status
#                 user_to_update.save()

#                 # Recalculate statistics after update
#                 total_leads = LeadUser.objects.filter(status='Leads').count()
#                 total_lost_leads = LeadUser.objects.filter(status='Lost_Leads').count()
#                 total_customer = LeadUser.objects.filter(status='Customer').count()
#                 total_maybe = LeadUser.objects.filter(status='Maybe').count()

#                 return render(request, "admin_dashboard/team_leader/leads.html", {
#                     'users': users,
#                     'total_leads': total_leads,
#                     'total_lost_leads': total_lost_leads,
#                     'total_customer': total_customer,
#                     'total_maybe': total_maybe,
#                 })

#             except LeadUser.DoesNotExist:
#                 pass

#     return redirect('lead')


@login_required(login_url='login')
def add_team_leader_user(request):
    all_admins = User.objects.filter(is_admin=True)
    
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        # dob = request.POST['dob']
        pancard = request.POST['pancard']
        aadharCard = request.POST['aadharCard']
        marksheet = request.POST['marksheet']
        degree = request.POST['degree']
        account_number = request.POST['account_number']
        upi_id = request.POST['upi_id']
        bank_name = request.POST['bank_name']
        ifsc_code = request.POST['ifsc_code']
        salary = request.POST['salary']
        profile_image = request.FILES.get("profile_image")
        selected_role = request.POST.getlist('role_checkbox')
        selected_role_list = request.POST.getlist('role_checkbox')
        on_boarding_manager = False
        dsr_manager = False
        executive_manager = False
        delivery_manager = False

        if selected_role_list:
            selected_role = selected_role_list[0]
            if selected_role == "on_boarding_manager":
                on_boarding_manager = True
            elif selected_role == "dsr_manager":
                dsr_manager = True
            elif selected_role == "executive_manager":
                executive_manager = True
            elif selected_role == "delivery_manager":
                delivery_manager = True

        if request.user.is_superuser:
            admin_id = request.POST['admin_id']
            admin_instance = User.objects.filter(id=admin_id).last()
            admin_emails = admin_instance.email
            admin_obj = Admin.objects.filter(email=admin_emails).last()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_team_leader_user')

        if User.objects.filter(email=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_team_leader_user')
        user = User.objects.create_user(
            username=username, profile_image=profile_image, password=password,
            email=username, name=name, mobile=mobile, is_team_leader=True,
            on_boarding_manager=on_boarding_manager,dsr_manager=dsr_manager,executive_manager=executive_manager,delivery_manager=delivery_manager)
        user.set_password(password)
        user.save()
        admin_email = request.user.email
        if request.user.is_admin:
            admin1 = Admin.objects.get(email=admin_email)
        if request.user.is_superuser:
            admin1 = admin_obj

        admin2 = Team_Leader.objects.create(
            admin=admin1,
            user=user,
            name=name,
            email=username,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,

            # dob=dob,
            pancard=pancard,
            aadharCard=aadharCard,
            marksheet=marksheet,
            degree=degree,
            account_number=account_number,
            upi_id=upi_id,
            bank_name=bank_name,
            ifsc_code=ifsc_code,
            salary=salary,
        )
        current_user = request.user
        super_admin = admin1.user

        if request.user.is_superuser:
                user_type = "Super User"
        if request.user.is_admin:
            user_type = "Admin User"
        if request.user.is_team_leader:
            user_type = "Team leader User"
        if request.user.is_staff_new:
            user_type = "Staff User"

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        tagline = f"Team Lead({name}) created by user[Email : {request.user.email}, {user_type}]"
        tag2 = f"Team Lead({name}) created"

        ActivityLog.objects.create(
            user = super_admin,
            description = tagline,
            ip_address = ip,
            email = request.user.email,
            user_type = user_type,
            activity_type = tag2,
            name = request.user.name,
        )
        # messages.success(request, "Team Leader Created Successfully.")
        if request.user.is_admin:
            return redirect('team_leader_user')
        if request.user.is_superuser:
            return redirect('add_team_leader_admin_side')

    context = {
        'messages': messages.get_messages(request),
        'all_admins': all_admins,
    }
    return render(request, "admin_dashboard/add_team_leader_user.html", context)

# home/views.py

@login_required(login_url='login')
def add_staff(request):
    if request.user.is_superuser:
        template = 'base.html'
    elif request.user.is_staff_new:
        template = 'admin_dashboard/team_leader/base.html'
    elif request.user.is_admin:
        template = 'admin_dashboard/base.html'
    else:
        template = 'admin_dashboard/staff/base.html'

    all_admins = User.objects.filter(is_admin=True)
    
    # --- [FIX START] ---
    # Yahan purana logic tha, use is naye logic se badal diya hai
    
    all_teamleader = Team_Leader.objects.none() # Pehle khaali set karo

    if request.user.is_superuser:
        # Superuser ko saare team leaders dikhne chahiye
        all_teamleader = Team_Leader.objects.all()
    
    elif request.user.is_admin:
        # Admin ko sirf apne team leaders dikhne chahiye (EMAIL SE)
        all_teamleader = Team_Leader.objects.filter(admin__email=request.user.email)
    
    elif request.user.is_team_leader:
        # Team Leader ko uske Admin ke baaki Team Leaders dikhne chahiye
        team_leader_profile = Team_Leader.objects.filter(user=request.user).last()
        if team_leader_profile and team_leader_profile.admin:
            all_teamleader = Team_Leader.objects.filter(admin=team_leader_profile.admin)
            
    # --- [FIX END] ---

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        dob = request.POST['dob']
        pancard = request.POST['pancard']
        aadharCard = request.POST['aadharCard']
        marksheet = request.POST['marksheet']
        degree = request.POST['degree']
        account_number = request.POST['account_number']
        upi_id = request.POST['upi_id']
        bank_name = request.POST['bank_name']
        ifsc_code = request.POST['ifsc_code']
        salary = request.POST['salary']
        profile_image = request.FILES.get("profile_image")

        if request.user.is_superuser:
            admin_id = request.POST['admin_id']
            team_leader_id = request.POST['team_leader_id']
        if request.user.is_admin:
            team_leader_id = request.POST['team_leader_id']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_staff')

        if User.objects.filter(email=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_staff')

        user = User.objects.create_user(
            username=username, profile_image=profile_image, password=password, email=username, name=name, mobile=mobile, is_staff_new=True)
        user.set_password(password)
        user.save()
        if request.user.is_team_leader:
            user1 = request.user
            admin_email = request.user.email
            team_leader = Team_Leader.objects.get(email=admin_email)
        if request.user.is_superuser:
            user1 = team_leader_id
            # admin_user_instance = User.objects.filter(id=admin_id).last()
            team_leader = Team_Leader.objects.filter(id=team_leader_id).last()
        if request.user.is_admin:
            user1 = team_leader_id
            team_leader = Team_Leader.objects.filter(id=team_leader_id).last()


        # team_leader_user = request.user
        # admin_email = request.user.email
        # team_leader = Team_Leader.objects.get(email=admin_email)

        staff = Staff.objects.create(
            team_leader=team_leader,
            user=user,
            name=name,
            email=username,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            dob=dob,
            pancard=pancard,
            aadharCard=aadharCard,
            marksheet=marksheet,
            degree=degree,
            account_number=account_number,
            upi_id=upi_id,
            bank_name=bank_name,
            ifsc_code=ifsc_code,
            salary=salary,
        )

        if request.user.is_superuser:
            user_type = "Super User"
        if request.user.is_admin:
            user_type = "Admin User"
        if request.user.is_team_leader:
            user_type = "Team leader User"
        if request.user.is_staff_new:
            user_type = "Staff User"

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        tagline = f"staff : {staff.name} created by user[Email : {request.user.email}, {user_type}]"
        tag2 = f"staff : {staff.name} created"

        login_user = request.user
        admin_email = login_user.email
        admin_instance = Team_Leader.objects.filter(email=admin_email).last()
        if request.user.is_team_leader:
            my_user1 = admin_instance.admin
            ActivityLog.objects.create(
                admin = my_user1,
                description = tagline,
                ip_address = ip,
                email = request.user.email,
                user_type = user_type,
                activity_type = tag2,
                name = request.user.name,
            )
        if request.user.is_superuser:
            ActivityLog.objects.create(
                user = request.user,
                description = tagline,
                ip_address = ip,
                email = request.user.email,
                user_type = user_type,
                activity_type = tag2,
                name = request.user.name,
            )

        messages.success(request, "Staff Created Successfully.")
        if request.user.is_superuser:
            return redirect('add_staff_admin_side')
        if request.user.is_admin:
            return redirect('add_staff_admin_side')
        return redirect('staff_user')
    context = {
        'messages': messages.get_messages(request),
        'all_admins': all_admins,
        'template': template,
        'all_teamleader': all_teamleader, # <-- Nayi query ab yahan pass ho rahi hai
    }

    return render(request, "admin_dashboard/staff/add_staff.html", context)


def adminedit(request, id):
    admin = get_object_or_404(Admin, id=id)
    
    if request.method == 'GET':
        admin = Admin.objects.get(id=id)
        return render(request, 'edit.html', {'admin': admin})

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']

        dob = request.POST['dob']
        pancard = request.POST['pancard']
        aadharCard = request.POST['aadharCard']
        marksheet = request.POST['marksheet']
        degree = request.POST['degree']
        account_number = request.POST['account_number']
        upi_id = request.POST['upi_id']
        bank_name = request.POST['bank_name']
        ifsc_code = request.POST['ifsc_code']
        salary = request.POST['salary']
        profile_image = request.FILES.get("profile_image")

        admin.name = name
        admin.email = email
        admin.mobile = mobile
        admin.address = address
        admin.city = city
        admin.pincode = pincode
        admin.state = state
        admin.dob = dob
        admin.pancard = pancard
        admin.aadharCard = aadharCard
        admin.marksheet = marksheet
        admin.degree = degree
        admin.account_number = account_number
        admin.upi_id = upi_id
        admin.bank_name = bank_name
        admin.ifsc_code = ifsc_code
        admin.salary = salary

        admin.save()

        user_instance = User.objects.filter(email=admin.email).last()
        user_instance.email = email
        user_instance.name = name
        user_instance.username = email
        user_instance.mobile = mobile
        user_instance.profile_image = profile_image
        user_instance.save()
        messages.success(request, 'Your Admin Edit successfully updated.')

    return redirect('super_admin')


def teamedit(request, id):
    teamleader = get_object_or_404(Team_Leader, id=id)
    if request.method == 'GET':
        teamleader = Team_Leader.objects.get(id=id)
        return render(request, 'admin_dashboard/teamleadedit.html', {'teamleader': teamleader})


    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']

        dob = request.POST['dob']
        pancard = request.POST['pancard']
        aadharCard = request.POST['aadharCard']
        marksheet = request.POST['marksheet']
        degree = request.POST['degree']
        account_number = request.POST['account_number']
        upi_id = request.POST['upi_id']
        bank_name = request.POST['bank_name']
        ifsc_code = request.POST['ifsc_code']
        salary = request.POST['salary']
        profile_image = request.FILES.get("profile_image")

        teamleader.name = name
        teamleader.email = email
        teamleader.mobile = mobile
        teamleader.address = address
        teamleader.city = city
        teamleader.pincode = pincode
        teamleader.state = state

        teamleader.dob = dob
        teamleader.pancard = pancard
        teamleader.aadharCard = aadharCard
        teamleader.marksheet = marksheet
        teamleader.degree = degree
        teamleader.account_number = account_number
        teamleader.upi_id = upi_id
        teamleader.bank_name = bank_name
        teamleader.ifsc_code = ifsc_code
        teamleader.salary = salary

        teamleader.save()

        user_instance = User.objects.filter(email=teamleader.email).last()
        user_instance.email = email
        user_instance.name = name
        user_instance.username = email
        user_instance.mobile = mobile
        user_instance.profile_image = profile_image
        user_instance.save()

        teamleader.save()
        messages.success(request, 'Your Team Leader Edit successfully updated.')
    if request.user.is_superuser:
        return redirect('add_team_leader_admin_side')
    return redirect('team_leader_user')
    


def staffedit(request, id):
    if request.method == 'GET':
        all_admins = User.objects.filter(is_admin=True)
        staff = get_object_or_404(Staff, id=id)
        if staff.user.is_freelancer:
            keys = 3
        if staff.user.is_freelancer:
            context = {
                'staff': staff, 
                'all_admins': all_admins,
                'keys': keys,
            }
        else:
            context = {
                'staff': staff, 
                'all_admins': all_admins,
            }
        return render(request, 'admin_dashboard/staff/editstaff.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']
        dob = request.POST['dob']
        pancard = request.POST['pancard']
        aadharCard = request.POST['aadharCard']
        marksheet = request.POST['marksheet']
        degree = request.POST['degree']
        account_number = request.POST['account_number']
        upi_id = request.POST['upi_id']
        bank_name = request.POST['bank_name']
        ifsc_code = request.POST['ifsc_code']
        salary = request.POST['salary']
        profile_image = request.FILES.get("profile_image")

        staff = get_object_or_404(Staff, id=id)
        if staff.user.is_freelancer:
            admin_id = request.POST['admin_id']
            team_leader_id = request.POST['team_leader_id']
            teamleader_instance = Team_Leader.objects.filter(id=team_leader_id).last()

        staff = get_object_or_404(Staff, id=id)
        staff_email = staff.email
        staff.name = name
        staff.email = email
        staff.mobile = mobile
        staff.address = address
        staff.city = city
        staff.pincode = pincode
        staff.state = state

        staff.dob = dob
        staff.pancard = pancard
        staff.aadharCard = aadharCard
        staff.marksheet = marksheet
        staff.degree = degree
        staff.account_number = account_number
        staff.upi_id = upi_id
        staff.bank_name = bank_name
        staff.ifsc_code = ifsc_code
        staff.salary = salary

        if staff.user.is_freelancer:
            staff.team_leader = teamleader_instance

        staff.save()

        user_instance = User.objects.filter(email=staff_email).last()
        user_instance.email = email
        user_instance.name = name
        user_instance.username = email
        user_instance.mobile = mobile
        user_instance.profile_image = profile_image
        user_instance.save()

        messages.success(request, 'Your Staff Edit successfully updated.')
    if staff.user.is_freelancer:
        return redirect('add_freelancer_super_side')
    if request.user.is_superuser:
        return redirect('add_staff_admin_side')
    # --- [YEH RAHA NAYA FIX] ---
    if request.user.is_admin:
        return redirect('add_staff_admin_side') # Admin ko Admin ke staff page par bhejo
    # --- [FIX ENDS] ---
    return redirect('staff_user')



@login_required(login_url='login')
def project(request):
    files = ProjectFile.objects.all()
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = ProjectFileForm()
    return render(request, 'admin_dashboard/team_leader/project.html', {'files': files, 'form': form})



def send_file_to_client(request, file_id):
    project_file = get_object_or_404(ProjectFile, id=file_id)
    LeadUser.objects.filter(send=True).update(
        send=False) 
    return redirect('leads')


@csrf_exempt
def update_send_status(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_id = data.get('id')
        new_send_status = data.get('send')

        try:
            user = LeadUser.objects.get(id=user_id)
            user.send = new_send_status
            user.save()
            return JsonResponse({'success': True, 'new_send_status': new_send_status})
        except LeadUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})



def bulk_from(request):
    if request.method == 'POST':
        assigned_id = request.POST.get('assigned_id')
        selected_lead_ids = request.POST.getlist('user_ids')
        request.session['selected_lead_ids'] = selected_lead_ids

        if not selected_lead_ids:
            messages.error(request, 'Assigned ID is missing.')
            return redirect('bulk_from')

        if not selected_lead_ids:
            messages.error(request, 'No leads selected.')
            return redirect('bulk_from')
        
        if selected_lead_ids:
            messages.error(request, 'Selected Leads Successfully')
            return redirect('bulk_from')

        try:
            assigned_user = get_object_or_404(Staff, id=assigned_id)
            for lead_id in selected_lead_ids:
                teams_leaders = Team_LeadData.objects.get(id=lead_id)
                lead_user = LeadUser.objects.create(
                    id=assigned_user,
                )
                lead_user.save()
            messages.success(request, 'Leads have been successfully assigned.')
        except Staff.DoesNotExist:
            messages.error(request, 'Assigned user does not exist.')
        except LeadUser.DoesNotExist:
            messages.error(request, 'One or more selected leads do not exist.')

    selected_lead_ids = request.session.get('selected_lead_ids', [])

    user = request.user
    user1 = user.username
    us = Team_Leader.objects.get(email=user1)
    staff_users2 = Staff.objects.filter(team_leader=us)
    lead_users = LeadUser.objects.all()

    context = {
        'staff_users2': staff_users2,
        'lead_users': lead_users,
        'selected_lead_ids': selected_lead_ids, 
    }
    return render(request, "admin_dashboard/staff/bulk_from.html", context)




def bulk_from_data(request):
    if request.method == 'POST':
        selected_lead_ids = request.session.get('selected_lead_ids', [])
        assigned_id = request.POST.get('assigned_id', [])
        selected_lead_ids = selected_lead_ids[0].split(',')
        # Ensure selected_lead_ids is a list of strings
        if isinstance(selected_lead_ids, str):
            selected_lead_ids = selected_lead_ids.split(',')
        teams_leader = Staff.objects.get(id=assigned_id)


        action = request.POST.get('action')

        # Process the action based on the value of `action`
        if action == 'assign_leads':

            selected_lead_ids = [lead_id.strip() for lead_id in selected_lead_ids if lead_id.strip()]
            
            
            teams_leader = get_object_or_404(Staff, id=assigned_id)
            email = request.user.email
            team_leader_instance = Team_Leader.objects.filter(email=email).last()
            
            for lead_id1 in selected_lead_ids:
                try:
                    if lead_id1.strip():
                        lead_id_int = int(lead_id1)
                    
                        teams_leaders = Team_LeadData.objects.get(id=lead_id_int)
                        teams_leaders.assigned_to = teams_leader  # Replace new_assigned_to with the new value
                        teams_leaders.save()
                        lead_user = LeadUser(
                            name=teams_leaders.name,
                            email=teams_leaders.email,
                            call=teams_leaders.call,
                            send=False,
                            status="Leads",
                            assigned_to=teams_leader,
                            team_leader=team_leader_instance,
                            )
                        lead_user.save()
                except ValueError:
                    print(f"Invalid ID value: ")
                except Team_LeadData.DoesNotExist:
                    print(f"Team_LeadData with id {lead_id_str} does not exist.")
            
            messages.success(request, 'Leads have been successfully assigned.')
        elif action == 'delete_leads':
            if isinstance(selected_lead_ids, str):
                selected_lead_ids = selected_lead_ids.split(',')
            
            selected_lead_ids = [lead_id.strip() for lead_id in selected_lead_ids if lead_id.strip()]
            
            for lead_id_str in selected_lead_ids:
                try:
                    lead_id_int = int(lead_id_str)
                    lead_to_delete = get_object_or_404(Team_LeadData, id=lead_id_int)
                    lead_to_delete.delete()
                except ValueError:
                    print(f"Invalid ID value: {lead_id_str}")
                except Team_LeadData.DoesNotExist:
                    print(f"Team_LeadData with id {lead_id_str} does not exist.")
            
            messages.success(request, 'Selected leads have been successfully deleted.')

        return redirect('lead')

    # If GET request, or after form submission, render the page
    selected_lead_ids = request.session.get('selected_lead_ids', [])
    staff_users = Staff.objects.all()
    lead_users = LeadUser.objects.all()

    context = {
        'staff_users': staff_users,
        'lead_users': lead_users,
        'selected_lead_ids': selected_lead_ids,
    }
    return render(request, "admin_dashboard/staff/bulk_from.html", context)




def excel_upload(request):
    
    # --- GET Request Logic (Page load hone par) ---
    if request.method == 'GET':
        users = Team_LeadData.objects.none() # Default empty rakho
        if request.user.is_team_leader:
            team_leader = Team_Leader.objects.filter(user=request.user).last()
            if team_leader:
                users = Team_LeadData.objects.filter(assigned_to = None, team_leader=team_leader)
        if request.user.is_superuser:
            users = Team_LeadData.objects.filter(assigned_to = None)
        
        return render(request, "admin_dashboard/staff/importlead.html", {'users': users})

    # --- POST Request Logic (File upload hone par) ---
    if request.method == 'POST':
        
        # --- [FIX 1: File Check] ---
        # .get() ka istemal kiya taaki code crash na ho agar file na mile
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            messages.error(request, "No file was uploaded. Please select a file.")
            # Yahan 'import_leads' aapke us page ka URL name hona chahiye jahan upload form hai
            return redirect('import_leads') 

        try:
            if excel_file.name.endswith('.csv'):
                # 'utf-8-sig' BOM (hidden characters) ko handle karta hai
                df = pd.read_csv(excel_file, encoding='utf-8-sig') 
            elif excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file, engine='openpyxl')
            else:
                messages.error(request, "Unsupported file format. Please upload a .csv or .xlsx file.")
                return redirect('import_leads')
        except Exception as e:
            messages.error(request, f"Error reading file: {e}.")
            return redirect('import_leads')

        # --- [FIX 2: Column Header Check] ---
        # Column headers ko clean karo (lowercase aur extra space hatao)
        df.columns = df.columns.str.lower().str.strip()
        
        required_columns = ['name', 'call', 'send', 'status']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            # Agar koi column missing hai, toh error dikhao aur crash hone se bacho
            messages.error(request, f"File is missing required columns: {', '.join(missing_cols)}")
            return redirect('import_leads')
        # --- [FIX 2 ENDS] ---

        user_count = df.shape[0]
        duplicates = []
        created_count = 0
        team_leader = None # Ise pehle define karo
        
        if request.user.is_team_leader:
            try:
                team_leader = Team_Leader.objects.get(user=request.user)
            except Team_Leader.DoesNotExist:
                messages.error(request, "Your Team Leader profile could not be found.")
                return redirect('import_leads')

        for i, row in df.iterrows():
            try:
                # Ab yeh code safe hai, kyunki humne columns pehle hi check kar liye hain
                name = row['name']
                call = row['call']
                status_val = row['status']
                send_val = row['send']

                # --- [FIX 3: Status Check (case insensitive)] ---
                # 'Leads' aur 'leads' dono ko handle karega
                if not name or pd.isna(name) or not str(status_val).lower() == "leads":
                    continue
                
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
                messages.error(request, f"An error occurred while processing row {i}: {e}")
                return redirect('import_leads')

        message = f"Excel file uploaded! Total: {user_count}, Created: {created_count}, Duplicates: {len(duplicates)}"
        messages.success(request, message) 

        return redirect("lead")

@login_required(login_url='login')
def leads(request):
    staff_email = request.session.get('staff_email', '')
    today = timezone.now().date()
    setting = Settings.objects.filter().last()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)) - timedelta(seconds=1)
    else:
        start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    lead_filter = {'updated_date__range': [start_date, end_date]}

    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        users = LeadUser.objects.filter(status="Leads", assigned_to=staff,)
        interested = LeadUser.objects.filter(status="Intrested", assigned_to=staff, **lead_filter)
        not_interested = LeadUser.objects.filter(status="Not Interested", assigned_to=staff, **lead_filter)
        other_location = LeadUser.objects.filter(status="Other Location", assigned_to=staff, **lead_filter)
        not_picked = LeadUser.objects.filter(status="Not Picked", assigned_to=staff, **lead_filter)
        lost = LeadUser.objects.filter(status="Lost", assigned_to=staff, **lead_filter)
        visits = LeadUser.objects.filter(status="Visit", assigned_to=staff, **lead_filter)
    else:
        users = LeadUser.objects.none()
    total_leads = users.count()
    
    total_interested_leads = interested.count()
    total_not_interested_leads = not_interested.count()
    total_other_location_leads = other_location.count()
    total_not_picked_leads = not_picked.count()
    total_lost_leads = lost.count()
    total_visits_leads = visits.count()

    user_email = request.user
    whatsapp_marketing = Marketing.objects.filter(source="whatsapp", user=user_email).last()
    projects = Project.objects.all()
    for proj in projects:
        if proj.media_file:
            proj.media_file_url = request.build_absolute_uri(proj.media_file.url)
        else:
            proj.media_file_url = None

    if request.user.is_it_staff:
        today = date.today()
        attendance, _ = Attendance.objects.get_or_create(user=request.user, date=today)

        if request.method == 'POST':
            description = request.POST['description']
            Task.objects.create(user=request.user, description=description)

            attendance.is_present = True
            attendance.save()

            return redirect('leads')

        tasks = Task.objects.filter(user=request.user).order_by('-created_date')
        attendance_records = Attendance.objects.filter(user=request.user)
        return render(request, "admin_dashboard/team_leader/leads.html", { 
                                                                        'tasks': tasks,
                                                                        'attendance_records': attendance_records,
                                                                        'setting': setting,
                                                                      })

    return render(request, "admin_dashboard/team_leader/leads.html", {'users': users, 
                                                                      'total_interested_leads': total_interested_leads,
                                                                      'total_not_interested_leads': total_not_interested_leads,
                                                                      'total_other_location_leads': total_other_location_leads,
                                                                      'total_not_picked_leads': total_not_picked_leads,
                                                                      'total_lost_leads': total_lost_leads,
                                                                      'total_leads': total_leads,
                                                                      'total_visits_leads': total_visits_leads,
                                                                      'whatsapp_marketing': whatsapp_marketing,
                                                                      'setting': setting,
                                                                      'projects': projects})


def attendance_calendar(request, id):
    year = int(request.GET.get('year', datetime.today().year))
    month = int(request.GET.get('month', datetime.today().month))
    
    _, num_days = monthrange(year, month)

    all_dates = [datetime(year, month, day).date() for day in range(1, num_days + 1)]
    
    today = datetime.today().date()
    if id == 0:
        tasks = Task.objects.filter(user=request.user, task_date__month=month, task_date__year=year)
    if id and id != 0:
        staff_instance = Staff.objects.filter(id=id).last().user
        tasks = Task.objects.filter(user=staff_instance, task_date__month=month, task_date__year=year)
    
    task_dates = {task.task_date for task in tasks}
    
    calendar_data = [
        {"date": date, "has_task": date in task_dates, "day_name": date.strftime("%a")}
        for date in all_dates
    ]

    present_count = len(task_dates)
    absent_count = len([d for d in all_dates if d not in task_dates and d <= today])

    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    context = {
        "calendar_data": calendar_data,
        "month": month,
        "year": year,
        "present_count": present_count,
        "absent_count": absent_count,
        "days_of_week": days_of_week,
        "id": id,
    }
    return render(request, 'admin_dashboard/staff/attendance.html', context)

def get_task_details(request):
    date = request.GET.get('date')
    id = request.GET.get('id')
    if int(id) > 0:
        staff_instance = Staff.objects.filter(id=id).last().user
        tasks = Task.objects.filter(user=staff_instance, task_date=date)
    else:
        tasks = Task.objects.filter(user=request.user, task_date=date)

    task_list = [{"description": task.description} for task in tasks]
    return JsonResponse({"tasks": task_list})

def export_leads_staff(request):
    user_email = request.user.email
    if request.user.is_staff_new:
        staff_instance = Staff.objects.filter(email=user_email).last()
        lead_users = LeadUser.objects.filter(status='Leads', assigned_to_id=staff_instance)
    if request.user.is_team_leader:
        team_lead_instance = Team_Leader.objects.filter(email=user_email).last()
        lead_users = Team_LeadData.objects.filter(status='Leads', team_leader=team_lead_instance)
    staff_name = request.user.name

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leads"

    headers = ['Name', 'Email', 'Call', 'Status', 'Message', 'Created Date', 'Updated Date']
    ws.append(headers)

    for lead_user in lead_users:
        ws.append([
            lead_user.name,
            lead_user.email,
            lead_user.call,
            lead_user.status,
            lead_user.message,
            lead_user.created_date.strftime('%Y-%m-%d %H:%M:%S') if lead_user.created_date else '',
            lead_user.updated_date.strftime('%Y-%m-%d %H:%M:%S') if lead_user.updated_date else '',
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={staff_name}_leads.xlsx'

    wb.save(response)
    return response

def lost_leads(request, tag):
    if request.method == "GET":
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)

        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        if request.user.is_admin:
            key = 5
            admin_instance = Admin.objects.filter(self_user=request.user).last()
            interested_leads = LeadUser.objects.filter(status="Intrested", team_leader__admin=admin_instance)

        else:    
            staff_email = request.session.get('staff_email', '')
            try:
                staff = Staff.objects.get(email=staff_email)
            except Staff.DoesNotExist:
                staff = None
            if staff:
                # users_lead_lost = LeadUser.objects.filter(status="Intrested", assigned_to=staff)
                if tag == 'pending_follow':
                    key = 1
                    interested_leads = LeadUser.objects.filter(
                        Q(status='Intrested') & Q(follow_up_date__isnull=False),
                        assigned_to=staff,
                    ).order_by('-updated_date')
                    interested_leads_count = LeadUser.objects.filter(
                        Q(status='Intrested') & Q(follow_up_date__isnull=False),
                        assigned_to=staff,
                    ).count()
                elif tag == 'today_follow':
                    key = 1
                    interested_leads = LeadUser.objects.filter(
                        Q(status='Intrested') & Q(follow_up_date=today),
                        assigned_to=staff,
                    ).order_by('-updated_date')
                    interested_leads_count = LeadUser.objects.filter(
                        Q(status='Intrested') & Q(follow_up_date=today),
                        assigned_to=staff,
                    ).count()
                elif tag == 'tommorrow_follow':
                    key = 1
                    interested_leads = LeadUser.objects.filter(
                        Q(status='Intrested') & Q(follow_up_date=tomorrow),
                        assigned_to=staff,
                    ).order_by('-updated_date')
                    interested_leads_count = LeadUser.objects.filter(
                        Q(status='Intrested') & Q(follow_up_date=tomorrow),
                        assigned_to=staff,
                    ).count()
                else:
                    key = 5
                    interested_leads = LeadUser.objects.filter(follow_up_time__isnull=True, assigned_to=staff ,status='Intrested').order_by('-updated_date')
                    interested_leads_count = LeadUser.objects.filter(follow_up_time__isnull=True, assigned_to=staff ,status='Intrested').count()
            else:
                interested_leads = LeadUser.objects.none()

        context = {
            'template': template,
            'users_lead_lost': interested_leads,
            'key': key,
        }
    return render(request, "admin_dashboard/team_leader/lost_leads.html", context)


def import_leads(request):
    return render(request, "admin_dashboard/staff/importlead.html")



@login_required(login_url='login')
def assigned(request,email):
    staff = get_object_or_404(Staff, email=email)
    if request.method == 'GET':
        abc = Staff.objects.get(email=email)
    # staff_email = request.session.get('staff_email', '')
    try:
        staff = abc
    except Staff.DoesNotExist:
        staff = None
    
    if staff:
        assign = LeadUser.objects.filter(assigned_to=staff, status='Leads')
        total_interested_leads = LeadUser.objects.filter(assigned_to=staff, status='Intrested').count()
        total_not_interested_leads = LeadUser.objects.filter(assigned_to=staff, status='Not Interested').count()
        total_other_location_leads = LeadUser.objects.filter(assigned_to=staff, status='Other Location').count()
        total_not_picked_leads = LeadUser.objects.filter(assigned_to=staff, status='Not Picked').count()
        total_lost_leads = LeadUser.objects.filter(assigned_to=staff, status='Lost').count()
        total_visit_leads = LeadUser.objects.filter(assigned_to=staff, status='Visit').count()

    else:
        assign = LeadUser.objects.none()
    
    assign_count=assign.count()
    context = {
        'assign': assign,
        'assign_count':assign_count,
        'total_interested_leads': total_interested_leads,
        'total_not_interested_leads':total_not_interested_leads,
        'total_other_location_leads': total_other_location_leads,
        'total_not_picked_leads':total_not_picked_leads,
        'total_lost_leads': total_lost_leads,
        'total_visit_leads': total_visit_leads,
    }
    
    return render(request, "admin_dashboard/staff/assigned.html", context)

# def team_leader_staff_interested_leads(request, id):
#     my_staff = Staff.objects.filter(id=id).last()
#     email = request.user.email
#     team_leader_instance = Team_Leader.objects.filter(email=email).last()
#     interested_leads = LeadUser.objects.filter(assigned_to=my_staff, status='Intrested', team_leader=team_leader_instance)
#     print(interested_leads, 'HHHHHHHHHHHHHHHH')
#     context = {
#         'assign': interested_leads,
#     }
#     return render(request, "admin_dashboard/staff/assigned.html", context)
def team_leader_staff_interested_leads(request, id):
    my_staff = Staff.objects.filter(id=id).last()
    email = request.user.email
    team_leader_instance = Team_Leader.objects.filter(email=email).last()

    # total_interested_leads_instance = LeadUser.objects.filter(
    #     assigned_to=my_staff, status="Intrested", team_leader=team_leader_instance).count()
    # total_not_interested_leads_instance = LeadUser.objects.filter(assigned_to=my_staff,
    #                                                             status="Not Interested", team_leader=team_leader_instance).count()
    # other_location_leads_instance = LeadUser.objects.filter(
    #     assigned_to=my_staff, status="Other Location", team_leader=team_leader_instance).count()
    # not_picked_leads_instance = LeadUser.objects.filter(
    #     assigned_to=my_staff, status="Not Picked", team_leader=team_leader_instance).count()
    # lost_leads_instance = LeadUser.objects.filter(
    #     assigned_to=my_staff, status="Lost", team_leader=team_leader_instance).count()
    # interested_leads = LeadUser.objects.filter(
    #     assigned_to=my_staff, status='Intrested', team_leader=team_leader_instance)

    total_interested_leads_instance = LeadUser.objects.filter(
        assigned_to=my_staff, status="Intrested",).count()
    total_not_interested_leads_instance = LeadUser.objects.filter(assigned_to=my_staff,
                                                                status="Not Interested",).count()
    other_location_leads_instance = LeadUser.objects.filter(
        assigned_to=my_staff, status="Other Location",).count()
    not_picked_leads_instance = LeadUser.objects.filter(
        assigned_to=my_staff, status="Not Picked",).count()
    lost_leads_instance = LeadUser.objects.filter(
        assigned_to=my_staff, status="Lost",).count()
    interested_leads = LeadUser.objects.filter(
        assigned_to=my_staff, status='Intrested',)

#     interested_leads = LeadUser.objects.filter(assigned_to=my_staff, status='Intrested', team_leader=team_leader_instance)

    context = {
        'assign': interested_leads,
        'assign_count': total_interested_leads_instance,
        'total_interested_leads_instance': total_interested_leads_instance,
        'total_not_interested_leads_instance': total_not_interested_leads_instance,
        'other_location_leads_instance': other_location_leads_instance,
        'not_picked_leads_instance': not_picked_leads_instance,
        'lost_leads_instance': lost_leads_instance,
    }
    return render(request, "admin_dashboard/staff/assigned.html", context)



@login_required(login_url='login')
def customer(request):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        if request.user.is_admin:
            admin_instance = Admin.objects.filter(self_user=request.user).last()
            customer_lead_lost = LeadUser.objects.filter(status="Not Interested", team_leader__admin=admin_instance)

        else:    
            staff_email = request.session.get('staff_email', '')
            try:
                staff = Staff.objects.get(email=staff_email)
            except Staff.DoesNotExist:
                staff = None
            if staff:
                customer_lead_lost = LeadUser.objects.filter(status="Not Interested", assigned_to=staff).order_by("-updated_date")
            else:
                customer_lead_lost = LeadUser.objects.none()

        context = {
            'template': template,
            'users_lead_lost': customer_lead_lost,
        }

    return render(request, "admin_dashboard/team_leader/Customer.html", context)

@login_required(login_url='login')
def visits_staff(request):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        if request.user.is_admin:
            admin_instance = Admin.objects.filter(self_user=request.user).last()
            customer_lead_lost = LeadUser.objects.filter(status="Visit", team_leader__admin=admin_instance)

        else:    
            staff_email = request.session.get('staff_email', '')
            try:
                staff = Staff.objects.get(email=staff_email)
            except Staff.DoesNotExist:
                staff = None
            if staff:
                customer_lead_lost = LeadUser.objects.filter(status="Visit", assigned_to=staff)
            else:
                customer_lead_lost = LeadUser.objects.none()

        context = {
            'template': template,
            'users_lead_lost': customer_lead_lost,
        }

    return render(request, "admin_dashboard/team_leader/visits_staff.html", context)

@login_required(login_url='login')
def maybe(request):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        if request.user.is_admin:
            admin_instance = Admin.objects.filter(self_user=request.user).last()
            lead_maybe = LeadUser.objects.filter(status="Other Location", team_leader__admin=admin_instance)

        else:    
            staff_email = request.session.get('staff_email', '')
            try:
                staff = Staff.objects.get(email=staff_email)
            except Staff.DoesNotExist:
                staff = None
            if staff:
                lead_maybe = LeadUser.objects.filter(status="Other Location", assigned_to=staff)
            else:
                lead_maybe = LeadUser.objects.none()

        context = {
            'template': template,
            'lead_maybe': lead_maybe,
        }

    return render(request, "admin_dashboard/team_leader/follow.html", context)

@login_required(login_url='login')
def not_picked(request):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        if request.user.is_admin:
            admin_instance = Admin.objects.filter(self_user=request.user).last()
            lead_maybe = LeadUser.objects.filter(status="Not Picked", team_leader__admin=admin_instance)

        else:    
            staff_email = request.session.get('staff_email', '')
            try:
                staff = Staff.objects.get(email=staff_email)
            except Staff.DoesNotExist:
                staff = None
            if staff:
                lead_maybe = LeadUser.objects.filter(status="Not Picked", assigned_to=staff)
            else:
                lead_maybe = LeadUser.objects.none()

        context = {
            'template': template,
            'lead_maybe': lead_maybe,
        }

    return render(request, "admin_dashboard/team_leader/not_picked.html", context)

@login_required(login_url='login')
def lost(request):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        if request.user.is_admin:
            admin_instance = Admin.objects.filter(self_user=request.user).last()
            lead_maybe = LeadUser.objects.filter(status="Lost", team_leader__admin=admin_instance)

        else:    
            staff_email = request.session.get('staff_email', '')
            try:
                staff = Staff.objects.get(email=staff_email)
            except Staff.DoesNotExist:
                staff = None
            if staff:
                lead_maybe = LeadUser.objects.filter(status="Lost", assigned_to=staff)
            else:
                lead_maybe = LeadUser.objects.none()

        context = {
            'template': template,
            'lead_maybe': lead_maybe,
        }

    return render(request, "admin_dashboard/team_leader/lost.html", context)

@login_required(login_url='login')
def total_leads_admin(request):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        if request.user.is_admin:
            admin_instance = Admin.objects.filter(self_user=request.user).last()
            lead_maybe = LeadUser.objects.filter(status="Leads", user=request.user,)

        else:    
            staff_email = request.session.get('staff_email', '')
            try:
                staff = Staff.objects.get(email=staff_email)
            except Staff.DoesNotExist:
                staff = None
            if staff:
                lead_maybe = LeadUser.objects.filter(status="Leads", assigned_to=staff)
            else:
                lead_maybe = LeadUser.objects.none()

        context = {
            'template': template,
            'lead_maybe': lead_maybe,
        }

    return render(request, "admin_dashboard/team_leader/lost.html", context)

@login_required(login_url='login')
def visit_lead_staff_side(request):
    staff_email = request.session.get('staff_email', '')
    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        lead_maybe = LeadUser.objects.filter(status="Visit", assigned_to=staff)
    else:
        lead_maybe = LeadUser.objects.none()
    return render(request, "admin_dashboard/team_leader/visit_lead_staff_side.html", {'lead_maybe': lead_maybe})



@login_required(login_url='login')
def lead(request):
    user = request.user
    total_leads, total_interested_leads, total_not_interested_leads, other_location_leads, not_picked_leads, lost_leads = 0, 0, 0, 0, 0, 0

    try:
        team_lead = Team_Leader.objects.get(user=user)
    except Team_Leader.DoesNotExist:
        team_lead = None

    user = request.user

    user1 = user.username
    if request.user.is_team_leader:
        us = Team_Leader.objects.get(email=user1)
        users = Staff.objects.filter(team_leader=us)

        user_logs = []
        for staff in users:
            user_logs.append({
                    'user': staff.user,
                    'username':staff.name,
                    'mobile': staff.mobile,
                    'email': staff.user.email,
                    'id' : staff.id,
            })

    if team_lead:
        # Team leader's unassigned leads
        leads2 = LeadUser.objects.filter(assigned_to=None, team_leader=team_lead, status='Leads')
        paginator = Paginator(leads2, per_page=10)

        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        total_upload_leads = leads2.count()

        num_pages = paginator.num_pages
        page_range = []
        
        if num_pages <= 7:
            page_range = list(paginator.page_range)
        else:
            page_range = list(paginator.page_range[:3])  
            if page.number > 4:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
            if page.number < num_pages - 3:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[-3:]))

        # Staff assigned to the team leader
        staff_members = Staff.objects.filter(team_leader=team_lead)
        
        # Collect data for each staff member
        for staff in staff_members:
            staff_leads = LeadUser.objects.filter(assigned_to=staff)
            total_leads += staff_leads.filter(status="Leads").count()
            total_interested_leads += staff_leads.filter(status="Intrested").count()
            total_not_interested_leads += staff_leads.filter(status="Not Interested").count()
            other_location_leads += staff_leads.filter(status="Other Location").count()
            not_picked_leads += staff_leads.filter(status="Not Picked").count()
            lost_leads += staff_leads.filter(status="Lost").count()

        # Add team leader's own data
        total_leads += leads2.filter(status="Leads").count()
        total_interested_leads += leads2.filter(status="Intrested").count()
        total_not_interested_leads += leads2.filter(status="Not Interested").count()
        other_location_leads += leads2.filter(status="Other Location").count()
        not_picked_leads += leads2.filter(status="Not Picked").count()
        lost_leads += leads2.filter(status="Lost").count()
    else:
        leads2 = Team_LeadData.objects.none()
        paginator = Paginator(leads2, per_page=10)

        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        total_upload_leads = leads2.count()

        num_pages = paginator.num_pages
        page_range = []
        
        if num_pages <= 7:
            page_range = list(paginator.page_range)
        else:
            page_range = list(paginator.page_range[:3])  
            if page.number > 4:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
            if page.number < num_pages - 3:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[-3:]))

    # if request.user.is_superuser:
    #     leads2 = Team_LeadData.objects.filter(assigned_to=None, status='Leads')
    #     paginator = Paginator(leads2, per_page=10)
            
    #     page_number = request.GET.get('page')
    #     page = paginator.get_page(page_number)
    #     total_uplode_leads = leads2.count()

    if request.user.is_superuser:
        leads2 = Team_LeadData.objects.filter(assigned_to=None, status='Leads')
        paginator = Paginator(leads2, per_page=10)

        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        total_upload_leads = leads2.count()

        num_pages = paginator.num_pages
        page_range = []
        
        if num_pages <= 7:
            page_range = list(paginator.page_range)
        else:
            page_range = list(paginator.page_range[:3])  
            if page.number > 4:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
            if page.number < num_pages - 3:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[-3:]))

    user_email = request.user
    whatsapp_marketing = Marketing.objects.filter(source="whatsapp", user=user_email).last()

    if request.user.is_team_leader:
        context = {
        'total_uplode_leads':total_upload_leads,
        'page_range': page_range,
        'page': page,
        'total_leads': total_leads,
        'total_interested_leads': total_interested_leads,
        'total_not_interested_leads': total_not_interested_leads,
        'other_location_leads': other_location_leads,
        'not_picked_leads': not_picked_leads,
        'lost_leads': lost_leads,
        'user_logs': user_logs,
        'whatsapp_marketing': whatsapp_marketing,
    }
    if request.user.is_superuser:
        context = {
            # 'total_uplode_leads':total_uplode_leads,
            'page': page,
            'page_range': page_range,
            'total_leads': total_leads,
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'other_location_leads': other_location_leads,
            'not_picked_leads': not_picked_leads,
            'lost_leads': lost_leads,
            # 'user_logs': user_logs,
            'whatsapp_marketing': whatsapp_marketing,
        }

    return render(request, "admin_dashboard/staff/lead.html", context)



def activitylogs(request):
    if request.method == "GET":
        if request.user.is_superuser:
            logs = ActivityLog.objects.all().order_by('-created_date')
            paginator = Paginator(logs, per_page=100)

            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)

            num_pages = paginator.num_pages
            page_range = []
            
            if num_pages <= 7:
                page_range = list(paginator.page_range)
            else:
                page_range = list(paginator.page_range[:3])  
                if page.number > 4:
                    page_range.append('...')
                page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
                if page.number < num_pages - 3:
                    page_range.append('...')
                page_range.extend(list(paginator.page_range[-3:]))

            context = {
                'logs': logs,
                'page': page,
                'page_range': page_range,
            }
            return render(request, "activity_log.html", context)
        if request.user.is_admin:
            user_email = request.user.email
            admin_user = Admin.objects.filter(email=user_email).last()
            logs = ActivityLog.objects.filter(admin=admin_user).order_by('-created_date')
            context = {
                'logs': logs,
            }
            return render(request, "admin_dashboard/activity_log.html", context)
        
        if request.user.is_team_leader:
            user_email = request.user.email
            admin_user = Team_Leader.objects.filter(email=user_email).last()
            logs = ActivityLog.objects.filter(team_leader=admin_user).order_by('-created_date')
            context = {
                'logs': logs,
            }
            return render(request, "admin_dashboard/staff/activity_log.html", context)
        
        if request.user.is_staff_new:
            user_email = request.user.email
            staff_instance = Staff.objects.filter(email=user_email).last()
            logs = ActivityLog.objects.filter(Q(user=request.user) | Q(staff=staff_instance)).order_by('-created_date')
            context = {
                'logs': logs,
            }
            return render(request, "admin_dashboard/team_leader/activity_log.html", context)

    return render(request, "activity_log.html", context)

@csrf_exempt
def log_activity_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_email = data.get('user_id')
        activity_type = data.get('activity_type')

        staff_instance = Staff.objects.filter(email=user_email).last()
        teal_leader_instance = staff_instance.team_leader
        teal_leader_instance_id = teal_leader_instance.id
        admin_instance = Admin.objects.filter(id=teal_leader_instance_id).last()

        if request.user.is_superuser:
            user_type = "Super User"
        if request.user.is_admin:
            user_type = "Admin User"
        if request.user.is_team_leader:
            user_type = "Team leader User"
        if request.user.is_staff_new:
            user_type = "Staff User"

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')


        # Log the activity
        ActivityLog.objects.create(
            staff=staff_instance,
            admin=admin_instance,
            team_leader=teal_leader_instance,
            activity_type=activity_type,
            user_type=user_type,
            ip_address=ip,
            name=request.user.name,
            email=request.user.email,
            description=f"User {user_email} performed {activity_type}"
        )

        return JsonResponse({'status': 'Activity logged successfully'})
    return JsonResponse({'status': 'Invalid request'}, status=400)


def edit_record(request, source):
    user = request.user
    record = Marketing.objects.filter(source=source, user=user).last()
    if record==None:
        create_id = 2
    else:
        create_id = 1
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
    return JsonResponse(data)

def update_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # record_id = data.get('m_id', None)
        source = data.get('source')
        message = data.get('message')
        url = data.get('url')
        media_file = data.get('media_file')
        create_id = data.get('create_id')

        user = request.user
        if create_id == "2":
            marketing = Marketing.objects.create(
                user = user,
                source = source,
                message = message,
                url = url,
                media_file = media_file
            )
        else:
            marketing_instance = Marketing.objects.filter(user=request.user, source=source).last()
            marketing_instance.user = user
            marketing_instance.source = source
            marketing_instance.message = message
            marketing_instance.url = url
            marketing_instance.media_file = media_file
            marketing_instance.save()
        
        return JsonResponse({'message': 'Record updated successfully', 'status':'200'})
    return HttpResponse(status=400)

def export_users(request):
    if request.method == 'POST':
        columns = ['name', 'call', 'send', 'status']
        df = pd.DataFrame(columns=columns)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="format.xlsx"'

        df.to_excel(response, index=False)

        return response
    else:
        return HttpResponse("Invalid request method.")
    

def teamleader_perticular_leads(request, id, tag):
    if tag == "Intrested":
        staff_leads = LeadUser.objects.filter(assigned_to=id, status='Intrested').order_by('-updated_date')
    elif tag == "Not Interested":
        staff_leads = LeadUser.objects.filter(assigned_to=id, status='Not Interested').order_by('-updated_date')
    elif tag == "Other Location":
        staff_leads = LeadUser.objects.filter(assigned_to=id, status='Other Location').order_by('-updated_date')
    elif tag == "Lost":
        staff_leads = LeadUser.objects.filter(assigned_to=id, status='Lost').order_by('-updated_date')
    elif tag == "Visit":
        staff_leads = LeadUser.objects.filter(assigned_to=id, status='Visit').order_by('-updated_date')
    else:
        staff_leads = LeadUser.objects.filter(assigned_to=id).order_by('-updated_date') 
    paginator = Paginator(staff_leads, per_page=50)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # total_upload_leads = leads2.count()

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))

    context = {
        'staff_leads': staff_leads,
        'page_range': page_range,
        'page': page,
        'staff_id': id,
    }
    # if request.user.is_superuser:
    #     return render(request, 'super_admin/staff_add_admin_side.html', context)
    return render(request, 'admin_dashboard/staff/perticular_leads.html', context)

def export_leads_status_wise_staff(request):
    if request.method == 'POST':
        all_interested = request.POST.get('all_interested')
        if all_interested != "1":
            staff_id = request.POST.get('staff_id')
            status = request.POST.get('status')
            staff_instance = Staff.objects.filter(id=staff_id).last()

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
            

        

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

        if all_interested != "1":
            leads = LeadUser.objects.filter(
                updated_date__range=[start_date, end_date],
                status=status,
                assigned_to=staff_id,
            )
        else:
            if request.user.is_superuser:
                leads = LeadUser.objects.filter(
                        updated_date__range=[start_date, end_date],
                        status="Intrested",
                    )
            if request.user.is_team_leader:
                user_email = request.user.username
                team_leader_instance = Team_Leader.objects.filter(email=user_email).last()
                leads = LeadUser.objects.filter(
                        team_leader=team_leader_instance,
                        updated_date__range=[start_date, end_date],
                        status="Intrested",
                    )
        from django.utils.timezone import localtime

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

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        if all_interested == "1":
            response['Content-Disposition'] = f'attachment; filename=interested_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.xlsx'
        else:
            response['Content-Disposition'] = f'attachment; filename={staff_instance.name}_{status}_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.xlsx'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Leads')

        return response

    # return render(request, 'admin_dashboard/staff/perticular_leads.html')


@login_required(login_url='login')
def customer_details(request,email):
    
    staff = get_object_or_404(Staff, email=email)
    if request.method == 'GET':
        abc = Staff.objects.get(email=email)
    # staff_email = request.session.get('staff_email', '')
    if staff:
        users_lead_lost = LeadUser.objects.filter(status="Intrested", assigned_to=staff)
    else:
        users_lead_lost = LeadUser.objects.none()
  

    assign_count=users_lead_lost.count()
    print(f"Assigned leads for staff with email {staff}: {users_lead_lost}")

    return render(request, "admin_dashboard/staff/customer_details.html", {'users_lead_lost': users_lead_lost,'assign_count':assign_count})

# def lost(request):
#     # staff_email = request.session.get('staff_email', '')
#     # try:
#     #     staff = Staff.objects.get(email=staff_email)
#     # except Staff.DoesNotExist:
#     #     staff = None
#     # if staff:
#     lead_maybe = LeadUser.objects.filter(status="Lost", assigned_to=staff)
#     # else:
#     #     lead_maybe = LeadUser.objects.none()
#     return render(request, "admin_dashboard/team_leader/lost.html", {'lead_maybe': lead_maybe})

@login_required(login_url='login')
def teamcustomer(request, tag):
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    user = request.user.email
    team_leader = Team_Leader.objects.filter(email=user).last()

    search_query = request.GET.get('search', '')
    if search_query:
        search_query = request.GET.get('search', '')
        interested_leads = LeadUser.objects.filter(
            Q(name__icontains=search_query) | Q(call__icontains=search_query) | Q(team_leader__name__icontains=search_query),
            status='Intrested'
        )
        paginator = Paginator(interested_leads, per_page=50)

        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        num_pages = paginator.num_pages
        page_range = []
        
        if num_pages <= 7:
            page_range = list(paginator.page_range)
        else:
            page_range = list(paginator.page_range[:3])  
            if page.number > 4:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
            if page.number < num_pages - 3:
                page_range.append('...')
            page_range.extend(list(paginator.page_range[-3:]))
        context = {
            'interested_leads': interested_leads,
            'page_range': page_range,
            'page': page,
        }
        return render(request, "admin_dashboard/staff/Customer.html", context)
    
    if request.user.is_superuser:
        if tag == 'pending_follow':
            key = 1
            interested_leads = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date__isnull=False)
            ).order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date__isnull=False)
            ).count()
        elif tag == 'today_follow':
            key = 1
            interested_leads = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=today)
            ).order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=today)
            ).count()
        elif tag == 'tommorrow_follow':
            key = 1
            interested_leads = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=tomorrow)
            ).order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=tomorrow)
            ).count()
        else:
            interested_leads = LeadUser.objects.filter(status='Intrested').order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(status='Intrested').count()
    
    elif request.user.is_team_leader:
        user = request.user.email
        team_leader_instance = Team_Leader.objects.filter(email=user).last()
        if tag == 'pending_follow':
            key = 1
            interested_leads = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date__isnull=False),
                team_leader=team_leader_instance,
            ).order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date__isnull=False),
                team_leader=team_leader_instance,
            ).count()
        elif tag == 'today_follow':
            key = 1
            interested_leads = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=today),
                team_leader=team_leader_instance,
            ).order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=today),
                team_leader=team_leader_instance,
            ).count()
        elif tag == 'tommorrow_follow':
            key = 1
            interested_leads = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=tomorrow),
                team_leader=team_leader_instance,
            ).order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(
                Q(status='Intrested') & Q(follow_up_date=tomorrow),
                team_leader=team_leader_instance,
            ).count()
        else:
            interested_leads = LeadUser.objects.filter(follow_up_time__isnull=True, team_leader=team_leader_instance ,status='Intrested').order_by('-updated_date')
            interested_leads_count = LeadUser.objects.filter(follow_up_time__isnull=True, team_leader=team_leader_instance ,status='Intrested').count()
            if search_query:
                search_query = request.GET.get('search', '')
                interested_leads = LeadUser.objects.filter(
                    Q(name__icontains=search_query) | Q(call__icontains=search_query) | Q(team_leader__name__icontains=search_query),
                    status='Intrested'
                )
                paginator = Paginator(interested_leads, per_page=50)

                page_number = request.GET.get('page')
                page = paginator.get_page(page_number)

                num_pages = paginator.num_pages
                page_range = []
                
                if num_pages <= 7:
                    page_range = list(paginator.page_range)
                else:
                    page_range = list(paginator.page_range[:3])  
                    if page.number > 4:
                        page_range.append('...')
                    page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
                    if page.number < num_pages - 3:
                        page_range.append('...')
                    page_range.extend(list(paginator.page_range[-3:]))
                context = {
                    'interested_leads': interested_leads,
                    'page_range': page_range,
                    'page': page,
                }
                return render(request, "admin_dashboard/staff/Customer.html", context)

    else:
        interested_leads = Team_LeadData.objects.filter(team_leader=team_leader, status='Intrested')
        interested_leads_count = Team_LeadData.objects.filter(team_leader=team_leader, status='Intrested').count()
    paginator = Paginator(interested_leads, per_page=50)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))
    
    if tag == 'pending_follow' or tag == 'today_follow' or tag == 'tommorrow_follow':
        context = {
        'interested_leads': interested_leads,
        'interested_leads_count': interested_leads_count,
        'page_range': page_range,
        'page': page,
        'key':key,
    }
    else:
        context = {
            'interested_leads': interested_leads,
            'interested_leads_count': interested_leads_count,
            'page_range': page_range,
            'page': page,
        }
    return render(request, "admin_dashboard/staff/Customer.html", context)

@login_required(login_url='login')
def teamlost_leads(request):
    user = request.user.email
    team_leader = Team_Leader.objects.filter(email=user).last()
    not_interested_leads = Team_LeadData.objects.filter(team_leader=team_leader, status='Not Interested')
    paginator = Paginator(not_interested_leads, per_page=10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))
    context = {
        'not_interested_leads': not_interested_leads,
        'page_range': page_range,
        'page': page,
    }
    return render(request, "admin_dashboard/staff/lost_leads.html", context)

@login_required(login_url='login')
def teammaybe(request):
    user = request.user
    user = request.user.email
    team_leader = Team_Leader.objects.filter(email=user).last()
    other_location_leads = Team_LeadData.objects.filter(team_leader=team_leader, status='Other Location')
    paginator = Paginator(other_location_leads, per_page=10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))
    context = {
        'other_location_leads': other_location_leads,
        'page_range': page_range,
        'page': page,
    }
    return render(request, "admin_dashboard/staff/follow.html", context)

@login_required(login_url='login')
def teamnot_picked(request):
    user = request.user
    user = request.user.email
    team_leader = Team_Leader.objects.filter(email=user).last()
    not_picked_leads = Team_LeadData.objects.filter(team_leader=team_leader, status='Not Picked')
    paginator = Paginator(not_picked_leads, per_page=10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))
    context = {
        'not_picked_leads': not_picked_leads,
        'page_range': page_range,
        'page': page,
    }
    return render(request, "admin_dashboard/staff/not_picked.html", context)


@login_required(login_url='login')
def teamlost(request):
    user = request.user
    user = request.user.email
    team_leader = Team_Leader.objects.filter(email=user).last()
    lost_leads = Team_LeadData.objects.filter(team_leader=team_leader, status='Lost')
    paginator = Paginator(lost_leads, per_page=10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))
    context = {
        'lost_leads': lost_leads,
        'page_range': page_range,
        'page': page,
    }
    return render(request, "admin_dashboard/staff/lost.html", context)

@login_required(login_url='login')
def visit_team_leader_side(request):
    user = request.user
    user = request.user.email
    team_leader = Team_Leader.objects.filter(email=user).last()
    if request.user.is_superuser:
        lost_leads = LeadUser.objects.filter(status='Visit').order_by('-updated_date')
    elif request.user.is_team_leader:
        user = request.user.email
        team_leader_instance = Team_Leader.objects.filter(email=user).last()
        lost_leads = LeadUser.objects.filter(team_leader=team_leader_instance ,status='Visit').order_by('-updated_date')
    else:
        lost_leads = Team_LeadData.objects.filter(team_leader=team_leader, status='Visit')
    paginator = Paginator(lost_leads, per_page=50)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))
    context = {
        'interested_leads': lost_leads,
        'page_range': page_range,
        'page': page,
    }
    return render(request, "admin_dashboard/staff/visit_team_lead.html", context)

def get_lead_user_data(request, id):
    if request.user.is_superuser:
        lead_user = get_object_or_404(Team_LeadData, id=id)
    if request.user.is_staff_new:
        lead_user = get_object_or_404(LeadUser, id=id)
    if request.user.is_team_leader:
        lead_user = get_object_or_404(LeadUser, id=id)
        # lead_user = get_object_or_404(Team_LeadData, id=id)
    data = {
        'id': lead_user.id,
        'status': lead_user.status,
        'message': lead_user.message,
        'follow_up_date': lead_user.follow_up_date,
        'follow_up_time': lead_user.follow_up_time    
    }
    return JsonResponse(data)

@csrf_exempt
def update_lead_user(request, id):
    if request.user.is_superuser:
        lead_user = get_object_or_404(Team_LeadData, id=id)
    if request.user.is_staff_new:
        lead_user = get_object_or_404(LeadUser, id=id)
    if request.user.is_team_leader:
        lead_user = get_object_or_404(LeadUser, id=id)
        # lead_user = get_object_or_404(Team_LeadData, id=id)
    current_status = lead_user.status
    # tagline = f"Lead status changed from {lead_user.status} to {new_status} by user[Email: {request.user.email}, {user_type}]"
    # tag2 = f"Lead status changed from {lead_user.status} to {new_status}"

    if request.method == 'POST':
        lead_status = request.POST.get('status')
        lead_user.status = request.POST.get('status')
        lead_user.message = request.POST.get('message')

        if lead_status == "Not Picked":
            lead_data = Team_LeadData.objects.create(
                user=lead_user.user,
                name=lead_user.name,
                call=lead_user.call,
                status="Leads",
                email=lead_user.email,
            )
            lead_user.delete()
            return JsonResponse({'message': 'Success'})

        if request.user.is_team_leader:
            lead_user.follow_up_date = request.POST.get('followDate')
            lead_user.follow_up_time = request.POST.get('followTime')
        if request.user.is_staff_new:
            lead_user.follow_up_date = request.POST.get('followDate')
            lead_user.follow_up_time = request.POST.get('followTime')    
        lead_user.save()

        Leads_history.objects.create(
            leads=lead_user,
            lead_id=id,
            status=lead_status,
            name=lead_user.name,
            message=lead_user.message,
        )

        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     "notifications",
        #     {
        #         'type': 'send_notification',
        #         'message': 'New inquiry received!'
        #     }
        # )
        
        if request.user.is_superuser:
            user_type = "Super User"
        elif request.user.is_admin:
            user_type = "Admin User"
        elif request.user.is_team_leader:
            user_type = "Team Leader User"
        elif request.user.is_staff_new:
            user_type = "Staff User"
        new_status = lead_user.status
        
        tagline = f"Lead status changed from {current_status} to {new_status} by user[Email: {request.user.email}, {user_type}]"
        # tag2 = f"Lead status changed from {current_status} to {new_status}"
        tag2 = new_status

        # Log activity for LeadUser
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if request.user.is_staff_new:
            admin_email = request.user.email
            admin_instance = Staff.objects.filter(email=admin_email).last()
            my_user2 = admin_instance.team_leader
            ActivityLog.objects.create(
                staff=admin_instance,
                team_leader=my_user2,
                description=tagline,
                ip_address=ip,
                email = request.user.email,
                user_type = user_type,
                activity_type = tag2,
                name = request.user.name,
            )

        return JsonResponse({'message': 'Success'})
    return JsonResponse({'message': 'Failed'}, status=400)


def auto_assign_leads(request):
    user_email = request.user.email
    request_user = Staff.objects.filter(email=user_email).last()
    team_leader = request_user.team_leader
    current_total_assign_leads = LeadUser.objects.filter(assigned_to=request_user, status='Leads').count()
    if current_total_assign_leads == 0:
        # if request.user.is_team_leader:
        # team_leader_total_leads = Team_LeadData.objects.filter(team_leader=team_leader, assigned_to=None)
        # if request.user.is_superuser:
        team_leader_total_leads = Team_LeadData.objects.filter(assigned_to=None, status='Leads')
        leads_count = 0
        for lead in team_leader_total_leads:
            
            if leads_count != 100:
                if LeadUser.objects.filter(call=lead.call).exists():
                    continue
                assign_leads = LeadUser.objects.create(
                    name=lead.name,
                    email=lead.email,
                    call=lead.call,
                    send=False,
                    status=lead.status,
                    assigned_to=request_user,
                    team_leader=team_leader,
                    user = lead.user,
                )
                # lead.assigned_to=request_user
                lead.delete()
                leads_count += 1
            
        # messages.success(request, "Auto leads Assign successfully.")
        return redirect('leads')
    messages.error(request, 'You already have leads.')
    return redirect('leads')


#--------------------------- Super Admin ----------------------------

def add_team_leader_admin_side(request):
    if request.method == "GET":
        users = Team_Leader.objects.all()
        active_staff_instance = User.objects.filter(is_staff_new=True, is_user_login=True).count()
        not_active_staff_instance = User.objects.filter(is_staff_new=True, is_user_login=False).count()
        all_staff = User.objects.filter(is_staff_new=True).count()

        total_leads = LeadUser.objects.filter(status="Leads").count()
        total_interested_leads = LeadUser.objects.filter(status="Intrested").count()
        total_not_interested_leads = LeadUser.objects.filter(status="Not Interested").count()
        total_other_location_leads = LeadUser.objects.filter(status="Other Location").count()
        total_not_picked_leads = LeadUser.objects.filter(status="Not Picked").count()
        total_lost_leads = LeadUser.objects.filter(status="Lost").count()
        total_visits_leads = LeadUser.objects.filter(status="Visit").count()

        context = {
            # 'users': users, 
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'total_other_location_leads': total_other_location_leads,
            'total_not_picked_leads': total_not_picked_leads,
            'total_lost_leads': total_lost_leads,
            'total_leads': total_leads,
            'total_visits_leads': total_visits_leads,
            'users': users,
            'active_staff_instance': active_staff_instance,
            'not_active_staff_instance': not_active_staff_instance,
            'all_staff': all_staff,
        }
        
    return render(request, 'super_admin/team_lead_add.html', context)

def add_staff_admin_side(request):
    if request.method == "GET":
        if request.user.is_superuser:
            my_staff = Staff.objects.all()
        if request.user.is_admin:
            my_staff = Staff.objects.filter(team_leader__admin__self_user=request.user)

        if request.user.is_superuser:
            total_leads = LeadUser.objects.filter(status="Leads").count()
            total_interested_leads = LeadUser.objects.filter(status="Intrested").count()
            total_not_interested_leads = LeadUser.objects.filter(status="Not Interested").count()
            total_other_location_leads = LeadUser.objects.filter(status="Other Location").count()
            total_not_picked_leads = LeadUser.objects.filter(status="Not Picked").count()
            total_lost_leads = LeadUser.objects.filter(status="Lost").count()
            total_visits_leads = LeadUser.objects.filter(status="Visit").count()

        if request.user.is_admin:
            total_leads = LeadUser.objects.filter(status="Leads", team_leader__admin__self_user=request.user).count()
            total_interested_leads = LeadUser.objects.filter(status="Intrested", team_leader__admin__self_user=request.user).count()
            total_not_interested_leads = LeadUser.objects.filter(status="Not Interested", team_leader__admin__self_user=request.user).count()
            total_other_location_leads = LeadUser.objects.filter(status="Other Location", team_leader__admin__self_user=request.user).count()
            total_not_picked_leads = LeadUser.objects.filter(status="Not Picked", team_leader__admin__self_user=request.user).count()
            total_lost_leads = LeadUser.objects.filter(status="Lost", team_leader__admin__self_user=request.user).count()
            total_visits_leads = LeadUser.objects.filter(status="Visit", team_leader__admin__self_user=request.user).count()

        months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
        
        if request.user.is_superuser:
            staff_list = Staff.objects.all()
        if request.user.is_admin:
            staff_list = Staff.objects.filter(team_leader__admin__self_user=request.user)
        
        days_in_month = monthrange(year, month)[1]
        
        total_salary_all_staff = 0
        productivity_data_all_staff = {}

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

            productivity_data = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}
            total_salary = 0

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

            productivity_data_all_staff[staff.id] = {
                'name': staff.name,
                'productivity_data': productivity_data,
                'total_salary': round(total_salary, 2)
            }
            
            total_salary_all_staff += total_salary

        calendar_data = calendar.monthcalendar(year, month)
        weekdays = list(calendar.day_name)

        structured_calendar_data = []
        for week in calendar_data:
            week_data = []
            for i, day in enumerate(week):
                day_name = weekdays[i]
                week_data.append({
                    'day': day,
                    'day_name': day_name
                })
            structured_calendar_data.append(week_data)

        context = {
            # 'users': users, 
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'total_other_location_leads': total_other_location_leads,
            'total_not_picked_leads': total_not_picked_leads,
            'total_lost_leads': total_lost_leads,
            'total_leads': total_leads,
            'total_visits_leads': total_visits_leads,
            'my_staff': my_staff,
            'total_salary_all_staff': total_salary_all_staff,
        }
        
    return render(request, 'super_admin/staff_add_admin_side.html', context)

def super_user_side_staff_leads(request, tag):
    if request.user.is_superuser:
        total_leads = LeadUser.objects.filter(status="Leads")
        total_interested_leads = LeadUser.objects.filter(status="Intrested")
        total_not_interested_leads = LeadUser.objects.filter(status="Not Interested")
        total_other_location_leads = LeadUser.objects.filter(status="Other Location")
        total_not_picked_leads = LeadUser.objects.filter(status="Not Picked")
        total_lost_leads = LeadUser.objects.filter(status="Lost")
        total_visits_leads = LeadUser.objects.filter(status="Visit")

    if request.user.is_admin:
        user = request.user
        admin_instance = Admin.objects.filter(user=user).last()
        teamleader_instance = Team_Leader.objects.filter(admin=admin_instance)

        total_leads = LeadUser.objects.filter(status="Leads", team_leader__in=teamleader_instance)
        total_interested_leads = LeadUser.objects.filter(status="Intrested", team_leader__in=teamleader_instance)
        total_not_interested_leads = LeadUser.objects.filter(status="Not Interested", team_leader__in=teamleader_instance)
        total_other_location_leads = LeadUser.objects.filter(status="Other Location", team_leader__in=teamleader_instance)
        total_not_picked_leads = LeadUser.objects.filter(status="Not Picked", team_leader__in=teamleader_instance)
        total_lost_leads = LeadUser.objects.filter(status="Lost", team_leader__in=teamleader_instance)
        total_visits_leads = LeadUser.objects.filter(status="Visit", team_leader__in=teamleader_instance)

    if tag == 'total_lead':
        context = {
            'leads' : total_leads,
        }
    if tag == 'visits':
        context = {
            'leads' : total_visits_leads,
        }
    if tag == 'interested':
        context = {
            'leads' : total_interested_leads,
        }
    if tag == 'not_interested':
        context = {
            'leads' : total_not_interested_leads,
        }
    if tag == 'other_location':
        context = {
            'leads' : total_other_location_leads,
        }
    if tag == 'not_picked':
        context = {
            'leads' : total_not_picked_leads,
        }

    return render(request, 'super_admin/super_admin_side_staff_leads.html', context)

def get_team_leaders_admin_side(request):
    admin_id = request.GET.get('admin_id')
    admin_user_instance = User.objects.filter(id=admin_id).last().email
    admin_instance = Admin.objects.filter(email=admin_user_instance).last()
    team_leaders = Team_Leader.objects.filter(admin=admin_instance).values('id', 'name')
    return JsonResponse({'team_leaders': list(team_leaders)})

def productivity_index(request):

    date_filter = request.GET.get('date', None)

    staff_data = []

    staffs = Staff.objects.all()
    for staff in staffs:
        if date_filter:
            leads_by_date = LeadUser.objects.filter(
                assigned_to=staff,
                created_date__date=date_filter
            ).aggregate(
                total_leads=Count('id'),
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )

        else:
            leads_by_date = LeadUser.objects.filter(assigned_to=staff).aggregate(
                total_leads=Count('id'),
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )

        visit_percentage = (leads_by_date['visit'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0
        interested_percentage = (leads_by_date['interested'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0

        staff_data.append({
            'name': staff.name,
            'total_leads': leads_by_date['total_leads'],
            'interested': leads_by_date['interested'],
            'not_interested': leads_by_date['not_interested'],
            'other_location': leads_by_date['other_location'],
            'not_picked': leads_by_date['not_picked'],
            'lost': leads_by_date['lost'],
            'visit': leads_by_date['visit'],
            'visit_percentage': round(visit_percentage, 2),
            'interested_percentage': round(interested_percentage, 2),
        })

    context = {
        'staff_data': staff_data,
    }

    return render(request, "admin_dashboard/staff/productivity_index.html", context)

def staff_productivity_view(request):
    date_filter = request.GET.get('date', None)
    end_date = request.GET.get('endDate', None)
    teamleader_id = request.GET.get('teamleader_id', None)
    admin_id = request.GET.get('admin_id', None)
    task_type = "staff"

    if request.user.is_superuser:
        template = 'base.html'
    elif request.user.is_staff_new:
        template = 'admin_dashboard/team_leader/base.html'
    elif request.user.is_admin:
        template = 'admin_dashboard/base.html'
    else:
        template = 'admin_dashboard/staff/base.html'

    staff_data = []

    total_all_leads = 0
    total_all_interested = 0
    total_all_not_interested = 0
    total_all_other_location = 0
    total_all_not_picked = 0
    total_all_lost = 0
    total_all_visit = 0
    total_all_calls = 0
    
    if request.user.is_superuser:
        fiter = 1
        staffs = Staff.objects.filter(user__user_active=True, user__is_freelancer=False)
        if admin_id:
            staffs = staffs.filter(team_leader__admin=admin_id)  # Filter by admin
        # if not admin_id:
        #     staffs = staffs.filter(team_leader__admin=None)
        if teamleader_id:
            staffs = staffs.filter(team_leader=teamleader_id)  # Filter by team leader
        # if not teamleader_id:
        #     staffs = staffs.filter(team_leader=None)

    if request.user.is_admin:
        fiter = 4

        user_instance = request.user
        team_leader_instance = Team_Leader.objects.filter(email=user_instance).last()
        staffs = Staff.objects.filter(team_leader__admin__self_user=user_instance, user__user_active=True, user__is_freelancer=False)
        if teamleader_id:
            staffs = staffs.filter(team_leader=teamleader_id)

    if request.user.is_team_leader:
        fiter = 2
        user_instance = request.user.username
        team_leader_instance = Team_Leader.objects.filter(email=user_instance).last()
        staffs = Staff.objects.filter(team_leader=team_leader_instance, user__user_active=True, user__is_freelancer=False)
    total_staff_count = staffs.count()
    for staff in staffs:
        # if date_filter and end_date:
        if date_filter != None and end_date != '':

            start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
            # end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
            # # end_date = timezone.make_aware(datetime.strptime(end_date_dt, '%Y-%m-%d') + timedelta(days=1)) - timedelta(seconds=1)
            # end_date = timezone.make_aware(end_date_dt + timedelta(days=1)) - timedelta(seconds=1)

            # lead_filter = {'updated_date__range': [start_date, end_date]}
            # lead_filter1 = {'created_date__range': [start_date, end_date]}
            # Check if end_date is a string before parsing it
            # Check if end_date is a string before parsing it
            if isinstance(end_date, str):
                end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')  # Convert string to datetime
            else:
                end_date_dt = end_date  # It's already a datetime object

            # Add one day and set to the end of that day
            end_date_dt += timedelta(days=1) - timedelta(seconds=1)

            # Check if end_date is naive, if so, make it aware
            if timezone.is_naive(end_date_dt):
                end_date = timezone.make_aware(end_date_dt)
            else:
                end_date = end_date_dt  # It's already aware

            # Create filters
            lead_filter = {'updated_date__range': [start_date, end_date]}
            lead_filter1 = {'created_date__range': [start_date, end_date]}

            leads_by_date = LeadUser.objects.filter(
                assigned_to=staff,
                **lead_filter
            ).aggregate(
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )
            leads_by_date1 = LeadUser.objects.filter(
                assigned_to=staff,
                **lead_filter1
            ).aggregate(
                total_leads=Count('id'),
            )
            total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
            visit_percentage = (leads_by_date['visit'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0
            interested_percentage = (leads_by_date['interested'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0

            # total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            # total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

            # staff_data.append({
            #     'id': staff.id,
            #     'name': staff.name,
            #     'total_leads': leads_by_date1['total_leads'],
            #     'interested': leads_by_date['interested'],
            #     'not_interested': leads_by_date['not_interested'],
            #     'other_location': leads_by_date['other_location'],
            #     'not_picked': leads_by_date['not_picked'],
            #     'lost': leads_by_date['lost'],
            #     'visit': leads_by_date['visit'],
            #     'visit_percentage': round(visit_percentage, 2),
            #     'interested_percentage': round(interested_percentage, 2),
            #     'total_calls': total_calls,
            # })

            staff_data.append({
                'id': staff.id,
                'name': staff.name,
                'total_leads': leads_by_date1['total_leads'],
                'interested': leads_by_date['interested'],
                'not_interested': leads_by_date['not_interested'],
                'other_location': leads_by_date['other_location'],
                'not_picked': leads_by_date['not_picked'],
                'lost': leads_by_date['lost'],
                'visit': leads_by_date['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
            })

            total_all_leads += leads_by_date1['total_leads']
            total_all_interested += leads_by_date['interested']
            total_all_not_interested += leads_by_date['not_interested']
            total_all_other_location += leads_by_date['other_location']
            total_all_not_picked += leads_by_date['not_picked']
            total_all_lost += leads_by_date['lost']
            total_all_visit += leads_by_date['visit']
            total_all_calls += total_calls

            total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        elif date_filter:
        # elif date_filter and end_date is None:
            leads_by_date = LeadUser.objects.filter(
                assigned_to=staff,
                updated_date__date=date_filter
            ).aggregate(
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )
            leads_by_date1 = LeadUser.objects.filter(
                assigned_to=staff,
                created_date__date=date_filter
            ).aggregate(
                total_leads=Count('id'),
            )
            total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
            visit_percentage = (leads_by_date['visit'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0
            interested_percentage = (leads_by_date['interested'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0

            # total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            # total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

            staff_data.append({
                'id': staff.id,
                'name': staff.name,
                'total_leads': leads_by_date1['total_leads'],
                'interested': leads_by_date['interested'],
                'not_interested': leads_by_date['not_interested'],
                'other_location': leads_by_date['other_location'],
                'not_picked': leads_by_date['not_picked'],
                'lost': leads_by_date['lost'],
                'visit': leads_by_date['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
            })

            total_all_leads += leads_by_date1['total_leads']
            total_all_interested += leads_by_date['interested']
            total_all_not_interested += leads_by_date['not_interested']
            total_all_other_location += leads_by_date['other_location']
            total_all_not_picked += leads_by_date['not_picked']
            total_all_lost += leads_by_date['lost']
            total_all_visit += leads_by_date['visit']
            total_all_calls += total_calls

            total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        else:
            leads_by_date = LeadUser.objects.filter(assigned_to=staff).aggregate(
                total_leads=Count('id'),
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )

            total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
            visit_percentage = (leads_by_date['visit'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0
            interested_percentage = (leads_by_date['interested'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0

            total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

            staff_data.append({
                'name': staff.name,
                'total_leads': leads_by_date['total_leads'],
                'interested': leads_by_date['interested'],
                'not_interested': leads_by_date['not_interested'],
                'other_location': leads_by_date['other_location'],
                'not_picked': leads_by_date['not_picked'],
                'lost': leads_by_date['lost'],
                'visit': leads_by_date['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
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
            })

            total_all_leads += leads_by_date['total_leads']
            total_all_interested += leads_by_date['interested']
            total_all_not_interested += leads_by_date['not_interested']
            total_all_other_location += leads_by_date['other_location']
            total_all_not_picked += leads_by_date['not_picked']
            total_all_lost += leads_by_date['lost']
            total_all_visit += leads_by_date['visit']
            total_all_calls += total_calls
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'staff_data': staff_data,
                             'total_calls': total_calls,
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
                'total_staff_count': total_staff_count,})
    
    admins = Admin.objects.all()
    teamleader = Team_Leader.objects.filter(admin__self_user=request.user)

    return render(request, 'admin_dashboard/staff/my1.html', {
        'staff_data': staff_data,
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
        'admins': admins,
        'fiter': fiter,
        'template': template,
        'teamleader': teamleader,
    })

def get_admin(request):
    admin = Admin.objects.all().values('id', 'name')
    return JsonResponse({'admin': list(admin)})

def get_team_leaders(request):
    admin_id = request.GET.get('admin_id')
    team_leaders = Team_Leader.objects.filter(admin_id=admin_id).values('id', 'name')
    return JsonResponse({'team_leaders': list(team_leaders)})

def get_staff(request):
    team_leader_id = request.GET.get('team_leader_id')
    staff_members = Staff.objects.filter(team_leader_id=team_leader_id).values('id', 'name')
    return JsonResponse({'staff': list(staff_members)})

def freelancer_productivity_view(request):
    date_filter = request.GET.get('date', None)
    end_date = request.GET.get('endDate', None)
    teamleader_id = request.GET.get('teamleader_id', None)
    admin_id = request.GET.get('admin_id', None)
    task_type = "freelancer"

    if request.user.is_superuser:
        template = 'base.html'
    elif request.user.is_staff_new:
        template = 'admin_dashboard/team_leader/base.html'
    elif request.user.is_admin:
        template = 'admin_dashboard/base.html'
    else:
        template = 'admin_dashboard/staff/base.html'

    staff_data = []

    total_all_leads = 0
    total_all_interested = 0
    total_all_not_interested = 0
    total_all_other_location = 0
    total_all_not_picked = 0
    total_all_lost = 0
    total_all_visit = 0
    total_all_calls = 0
    total_visit_percentage = 0
    # total_interested_percentage = 0
    total_interested_percentage = 0
    # if request.user.is_superuser:
    #     staffs = Staff.objects.filter(user__user_active=True, user__is_freelancer=True)
    # if request.user.is_team_leader:
    #     user_instance = request.user.username
    #     team_leader_instance = Team_Leader.objects.filter(email=user_instance).last()
    #     staffs = Staff.objects.filter(team_leader=team_leader_instance, user__user_active=True, user__is_freelancer=True)

    if request.user.is_superuser:
        fiter = 1
        staffs = Staff.objects.filter(user__user_active=True, user__is_freelancer=True)
        if admin_id:
            staffs = staffs.filter(team_leader__admin=admin_id)  # Filter by admin
        # if not admin_id:
        #     staffs = staffs.filter(team_leader__admin=None)
        if teamleader_id:
            staffs = staffs.filter(team_leader=teamleader_id)  # Filter by team leader
        # if not teamleader_id:
        #     staffs = staffs.filter(team_leader=None)

    if request.user.is_admin:
        fiter = 4

        user_instance = request.user
        team_leader_instance = Team_Leader.objects.filter(email=user_instance).last()
        staffs = Staff.objects.filter(team_leader__admin__self_user=user_instance, user__user_active=True, user__is_freelancer=True)
        if teamleader_id:
            staffs = staffs.filter(team_leader=teamleader_id)

    if request.user.is_team_leader:
        fiter = 2
        user_instance = request.user.username
        team_leader_instance = Team_Leader.objects.filter(email=user_instance).last()
        staffs = Staff.objects.filter(team_leader=team_leader_instance, user__user_active=True, user__is_freelancer=True)
    total_staff_count = staffs.count()
    for staff in staffs:
        if date_filter != None and end_date != '':
            start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
                
            if isinstance(end_date, str):
                end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
            else:
                end_date_dt = end_date

            end_date_dt += timedelta(days=1) - timedelta(seconds=1)

            if timezone.is_naive(end_date_dt):
                end_date = timezone.make_aware(end_date_dt)
            else:
                end_date = end_date_dt

            lead_filter = {'updated_date__range': [start_date, end_date]}
            lead_filter1 = {'created_date__range': [start_date, end_date]}

            leads_by_date = LeadUser.objects.filter(
                assigned_to=staff,
                **lead_filter
            ).aggregate(
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )
            leads_by_date1 = LeadUser.objects.filter(
                assigned_to=staff,
                **lead_filter1
            ).aggregate(
                total_leads=Count('id'),
            )
            total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
            visit_percentage = (leads_by_date['visit'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0
            interested_percentage = (leads_by_date['interested'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0

            staff_data.append({
                'name': staff.name,
                'total_leads': leads_by_date1['total_leads'],
                'interested': leads_by_date['interested'],
                'not_interested': leads_by_date['not_interested'],
                'other_location': leads_by_date['other_location'],
                'not_picked': leads_by_date['not_picked'],
                'lost': leads_by_date['lost'],
                'visit': leads_by_date['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
            })

            total_all_leads += leads_by_date1['total_leads']
            total_all_interested += leads_by_date['interested']
            total_all_not_interested += leads_by_date['not_interested']
            total_all_other_location += leads_by_date['other_location']
            total_all_not_picked += leads_by_date['not_picked']
            total_all_lost += leads_by_date['lost']
            total_all_visit += leads_by_date['visit']
            total_all_calls += total_calls

            total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        elif date_filter:
            leads_by_date = LeadUser.objects.filter(
                assigned_to=staff,
                updated_date__date=date_filter
            ).aggregate(
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )
            leads_by_date1 = LeadUser.objects.filter(
                assigned_to=staff,
                created_date__date=date_filter
            ).aggregate(
                total_leads=Count('id'),
            )
            total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
            visit_percentage = (leads_by_date['visit'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0
            interested_percentage = (leads_by_date['interested'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0

            staff_data.append({
                'name': staff.name,
                'total_leads': leads_by_date1['total_leads'],
                'interested': leads_by_date['interested'],
                'not_interested': leads_by_date['not_interested'],
                'other_location': leads_by_date['other_location'],
                'not_picked': leads_by_date['not_picked'],
                'lost': leads_by_date['lost'],
                'visit': leads_by_date['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
            })

            total_all_leads += leads_by_date1['total_leads']
            total_all_interested += leads_by_date['interested']
            total_all_not_interested += leads_by_date['not_interested']
            total_all_other_location += leads_by_date['other_location']
            total_all_not_picked += leads_by_date['not_picked']
            total_all_lost += leads_by_date['lost']
            total_all_visit += leads_by_date['visit']
            total_all_calls += total_calls

            total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

        else:
            leads_by_date = LeadUser.objects.filter(assigned_to=staff).aggregate(
                total_leads=Count('id'),
                interested=Count('id', filter=Q(status='Intrested')),
                not_interested=Count('id', filter=Q(status='Not Interested')),
                other_location=Count('id', filter=Q(status='Other Location')),
                not_picked=Count('id', filter=Q(status='Not Picked')),
                lost=Count('id', filter=Q(status='Lost')),
                visit=Count('id', filter=Q(status='Visit'))
            )

            total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
            visit_percentage = (leads_by_date['visit'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0
            interested_percentage = (leads_by_date['interested'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0

            total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
            total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

            staff_data.append({
                'name': staff.name,
                'total_leads': leads_by_date['total_leads'],
                'interested': leads_by_date['interested'],
                'not_interested': leads_by_date['not_interested'],
                'other_location': leads_by_date['other_location'],
                'not_picked': leads_by_date['not_picked'],
                'lost': leads_by_date['lost'],
                'visit': leads_by_date['visit'],
                'visit_percentage': round(visit_percentage, 2),
                'interested_percentage': round(interested_percentage, 2),
                'total_calls': total_calls,
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
            })

            total_all_leads += leads_by_date['total_leads']
            total_all_interested += leads_by_date['interested']
            total_all_not_interested += leads_by_date['not_interested']
            total_all_other_location += leads_by_date['other_location']
            total_all_not_picked += leads_by_date['not_picked']
            total_all_lost += leads_by_date['lost']
            total_all_visit += leads_by_date['visit']
            total_all_calls += total_calls
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'staff_data': staff_data,
                             'total_calls': total_calls,
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
                'total_staff_count': total_staff_count,})
    
    admins = Admin.objects.all()
    teamleader = Team_Leader.objects.filter(admin__self_user=request.user)
    return render(request, 'admin_dashboard/staff/my1.html', {
        'staff_data': staff_data,
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
        'admins': admins,
        'fiter': fiter,
        'template': template,
        'teamleader': teamleader,
    })


# def teamleader_productivity_view(request):
#     date_filter = request.GET.get('date', None)
#     task_type = "teamleader"

#     staff_data = []

#     total_all_leads = 0
#     total_all_interested = 0
#     total_all_not_interested = 0
#     total_all_other_location = 0
#     total_all_not_picked = 0
#     total_all_lost = 0
#     total_all_visit = 0
#     total_all_calls = 0

#     staffs = Team_Leader.objects.filter(user__user_active=True)
#     total_staffs = Team_Leader.objects.filter(user__user_active=True).count()
    
#     for staff in staffs:
#         if date_filter:
#             leads_by_date = Team_LeadData.objects.filter(
#                 assigned_to=None,
#                 team_leader=staff,
#                 updated_date__date=date_filter
#             ).aggregate(
#                 interested=Count('id', filter=Q(status='Intrested')),
#                 not_interested=Count('id', filter=Q(status='Not Interested')),
#                 other_location=Count('id', filter=Q(status='Other Location')),
#                 not_picked=Count('id', filter=Q(status='Not Picked')),
#                 lost=Count('id', filter=Q(status='Lost')),
#                 visit=Count('id', filter=Q(status='Visit'))
#             )
#             leads_by_date1 = Team_LeadData.objects.filter(
#                 assigned_to=None,
#                 team_leader=staff,
#                 created_date__date=date_filter
#             ).aggregate(
#                 total_leads=Count('id'),
#             )

#             total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
#             visit_percentage = (leads_by_date['visit'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0
#             interested_percentage = (leads_by_date['interested'] / leads_by_date1['total_leads'] * 100) if leads_by_date1['total_leads'] > 0 else 0

#             staff_data.append({
#                 'name': staff.name,
#                 'total_leads': leads_by_date1['total_leads'],
#                 'interested': leads_by_date['interested'],
#                 'not_interested': leads_by_date['not_interested'],
#                 'other_location': leads_by_date['other_location'],
#                 'not_picked': leads_by_date['not_picked'],
#                 'lost': leads_by_date['lost'],
#                 'visit': leads_by_date['visit'],
#                 'visit_percentage': round(visit_percentage, 2),
#                 'interested_percentage': round(interested_percentage, 2),
#                 'total_calls': total_calls
#             })

#             total_all_leads += leads_by_date1['total_leads']
#             total_all_interested += leads_by_date['interested']
#             total_all_not_interested += leads_by_date['not_interested']
#             total_all_other_location += leads_by_date['other_location']
#             total_all_not_picked += leads_by_date['not_picked']
#             total_all_lost += leads_by_date['lost']
#             total_all_visit += leads_by_date['visit']
#             total_all_calls += total_calls

#         else:
#             leads_by_date = Team_LeadData.objects.filter(assigned_to=None, team_leader=staff).aggregate(
#                 total_leads=Count('id'),
#                 interested=Count('id', filter=Q(status='Intrested')),
#                 not_interested=Count('id', filter=Q(status='Not Interested')),
#                 other_location=Count('id', filter=Q(status='Other Location')),
#                 not_picked=Count('id', filter=Q(status='Not Picked')),
#                 lost=Count('id', filter=Q(status='Lost')),
#                 visit=Count('id', filter=Q(status='Visit'))
#             )

#             total_calls = leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']
#             visit_percentage = (leads_by_date['visit'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0
#             interested_percentage = (leads_by_date['interested'] / leads_by_date['total_leads'] * 100) if leads_by_date['total_leads'] > 0 else 0

#             staff_data.append({
#                 'name': staff.name,
#                 'total_leads': leads_by_date['total_leads'],
#                 'interested': leads_by_date['interested'],
#                 'not_interested': leads_by_date['not_interested'],
#                 'other_location': leads_by_date['other_location'],
#                 'not_picked': leads_by_date['not_picked'],
#                 'lost': leads_by_date['lost'],
#                 'visit': leads_by_date['visit'],
#                 'visit_percentage': round(visit_percentage, 2),
#                 'interested_percentage': round(interested_percentage, 2),
#                 'total_calls': total_calls
#             })

#             total_all_leads += leads_by_date['total_leads']
#             total_all_interested += leads_by_date['interested']
#             total_all_not_interested += leads_by_date['not_interested']
#             total_all_other_location += leads_by_date['other_location']
#             total_all_not_picked += leads_by_date['not_picked']
#             total_all_lost += leads_by_date['lost']
#             total_all_visit += leads_by_date['visit']
#             total_all_calls += total_calls

#     total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
#     total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return JsonResponse({'staff_data': staff_data,
#                              'total_all_leads': total_all_leads,
#         'total_all_interested': total_all_interested,
#         'total_all_not_interested': total_all_not_interested,
#         'total_all_other_location': total_all_other_location,
#         'total_all_not_picked': total_all_not_picked,
#         'total_all_lost': total_all_lost,
#         'total_all_visit': total_all_visit,
#         'total_all_calls': total_all_calls,
#         'total_visit_percentage': round(total_visit_percentage, 2),
#         'total_interested_percentage': round(total_interested_percentage, 2),
#         'total_staff_count': total_staffs,})

#     return render(request, 'admin_dashboard/staff/my1.html', {
#         'staff_data': staff_data,
#         'selected_date': date_filter,
#         'task_type': task_type,
#         'total_all_leads': total_all_leads,
#         'total_all_interested': total_all_interested,
#         'total_all_not_interested': total_all_not_interested,
#         'total_all_other_location': total_all_other_location,
#         'total_all_not_picked': total_all_not_picked,
#         'total_all_lost': total_all_lost,
#         'total_all_visit': total_all_visit,
#         'total_all_calls': total_all_calls,
#         'total_visit_percentage': round(total_visit_percentage, 2),
#         'total_interested_percentage': round(total_interested_percentage, 2)
#     })


def teamleader_productivity_view(request):
    date_filter = request.GET.get('date', None)
    end_date = request.GET.get('endDate', None)
    admin_id = request.GET.get('admin_id', None)
    task_type = "teamleader"

    if request.user.is_superuser:
        template = 'base.html'
    elif request.user.is_staff_new:
        template = 'admin_dashboard/team_leader/base.html'
    elif request.user.is_admin:
        template = 'admin_dashboard/base.html'
    else:
        template = 'admin_dashboard/staff/base.html'

    staff_data = []

    total_all_leads = 0
    total_all_interested = 0
    total_all_not_interested = 0
    total_all_other_location = 0
    total_all_not_picked = 0
    total_all_lost = 0
    total_all_visit = 0
    total_all_calls = 0

    # Retrieve all active team leaders
    if request.user.is_superuser:
        fiter = 3
        team_leaders = Team_Leader.objects.filter(user__user_active=True)
        if admin_id:
            team_leaders = team_leaders.filter(admin=admin_id)
    
    if request.user.is_admin:
        fiter = 5
        team_leaders = Team_Leader.objects.filter(admin__self_user=request.user, user__user_active=True)
        if admin_id:
            team_leaders = team_leaders.filter(admin=admin_id)
    total_staffs = team_leaders.count()

    for team_leader in team_leaders:
        leads_data = {
            'total_leads': 0,
            'interested': 0,
            'not_interested': 0,
            'other_location': 0,
            'not_picked': 0,
            'lost': 0,
            'visit': 0,
            'total_calls': 0
        }

        # Retrieve staff members associated with the team leader
        staff_members = Staff.objects.filter(team_leader=team_leader)

        for staff in staff_members:
            if date_filter != None and end_date != '':

                start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
                
                if isinstance(end_date, str):
                    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
                else:
                    end_date_dt = end_date

                end_date_dt += timedelta(days=1) - timedelta(seconds=1)

                if timezone.is_naive(end_date_dt):
                    end_date = timezone.make_aware(end_date_dt)
                else:
                    end_date = end_date_dt

                lead_filter = {'updated_date__range': [start_date, end_date]}
                lead_filter1 = {'created_date__range': [start_date, end_date]}

                leads_by_date = LeadUser.objects.filter(
                    assigned_to=staff,
                    **lead_filter
                ).aggregate(
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date1 = LeadUser.objects.filter(
                    assigned_to=staff,
                    **lead_filter1
                ).aggregate(
                    total_leads=Count('id'),
                )

            elif date_filter:
                leads_by_date = LeadUser.objects.filter(
                    assigned_to=staff,
                    updated_date__date=date_filter
                ).aggregate(
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date1 = LeadUser.objects.filter(
                    assigned_to=staff,
                    created_date__date=date_filter
                ).aggregate(
                    total_leads=Count('id'),
                )
            else:
                leads_by_date = LeadUser.objects.filter(assigned_to=staff).aggregate(
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date1 = LeadUser.objects.filter(assigned_to=staff).aggregate(
                    total_leads=Count('id')
                )

            # Ensure leads_by_date1['total_leads'] always has a value
            leads_data['total_leads'] += leads_by_date1.get('total_leads', 0)
            leads_data['interested'] += leads_by_date.get('interested', 0)
            leads_data['not_interested'] += leads_by_date.get('not_interested', 0)
            leads_data['other_location'] += leads_by_date.get('other_location', 0)
            leads_data['not_picked'] += leads_by_date.get('not_picked', 0)
            leads_data['lost'] += leads_by_date.get('lost', 0)
            leads_data['visit'] += leads_by_date.get('visit', 0)


            leads_data['total_calls'] += leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']

        visit_percentage = (leads_data['visit'] / leads_data['total_leads'] * 100) if leads_data['total_leads'] > 0 else 0
        interested_percentage = (leads_data['interested'] / leads_data['total_leads'] * 100) if leads_data['total_leads'] > 0 else 0

        staff_data.append({
            'name': team_leader.name,
            'total_leads': leads_data['total_leads'],
            'interested': leads_data['interested'],
            'not_interested': leads_data['not_interested'],
            'other_location': leads_data['other_location'],
            'not_picked': leads_data['not_picked'],
            'lost': leads_data['lost'],
            'visit': leads_data['visit'],
            'visit_percentage': round(visit_percentage, 2),
            'interested_percentage': round(interested_percentage, 2),
            'total_calls': leads_data['total_calls']
        })

        total_all_leads += leads_data['total_leads']
        total_all_interested += leads_data['interested']
        total_all_not_interested += leads_data['not_interested']
        total_all_other_location += leads_data['other_location']
        total_all_not_picked += leads_data['not_picked']
        total_all_lost += leads_data['lost']
        total_all_visit += leads_data['visit']
        total_all_calls += leads_data['total_calls']

    total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
    total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'staff_data': staff_data,
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
                             'total_staff_count': total_staffs,})
    
    admins = Admin.objects.all()
    return render(request, 'admin_dashboard/staff/my1.html', {
        'staff_data': staff_data,
        'selected_date': date_filter,
        'task_type': task_type,
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
        'admins': admins,
        'fiter': fiter,
        'template': template,
    })


def admin_productivity_view(request):
    date_filter = request.GET.get('date', None)
    end_date = request.GET.get('endDate', None)
    task_type = "admin"

    if request.user.is_superuser:
        template = 'base.html'
    elif request.user.is_staff_new:
        template = 'admin_dashboard/team_leader/base.html'
    elif request.user.is_admin:
        template = 'admin_dashboard/base.html'
    else:
        template = 'admin_dashboard/staff/base.html'

    staff_data = []

    total_all_leads = 0
    total_all_interested = 0
    total_all_not_interested = 0
    total_all_other_location = 0
    total_all_not_picked = 0
    total_all_lost = 0
    total_all_visit = 0
    total_all_calls = 0

    # Retrieve all active team leaders
    team_leaders = Admin.objects.filter(self_user__user_active=True)
    total_staffs = team_leaders.count()

    for team_leader in team_leaders:
        leads_data = {
            'total_leads': 0,
            'interested': 0,
            'not_interested': 0,
            'other_location': 0,
            'not_picked': 0,
            'lost': 0,
            'visit': 0,
            'total_calls': 0
        }

        # Retrieve staff members associated with the team leader
        staff_members = Staff.objects.filter(team_leader__admin=team_leader)

        for staff in staff_members:
            if date_filter != None and end_date != '':
                start_date = timezone.make_aware(datetime.strptime(date_filter, '%Y-%m-%d'))
                
                if isinstance(end_date, str):
                    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
                else:
                    end_date_dt = end_date

                end_date_dt += timedelta(days=1) - timedelta(seconds=1)

                if timezone.is_naive(end_date_dt):
                    end_date = timezone.make_aware(end_date_dt)
                else:
                    end_date = end_date_dt

                lead_filter = {'updated_date__range': [start_date, end_date]}
                lead_filter1 = {'created_date__range': [start_date, end_date]}

                leads_by_date = LeadUser.objects.filter(
                    assigned_to=staff,
                    **lead_filter
                ).aggregate(
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date1 = LeadUser.objects.filter(
                    assigned_to=staff,
                    **lead_filter1
                ).aggregate(
                    total_leads=Count('id'),
                )

            elif date_filter:
                leads_by_date = LeadUser.objects.filter(
                    assigned_to=staff,
                    updated_date__date=date_filter
                ).aggregate(
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date1 = LeadUser.objects.filter(
                    assigned_to=staff,
                    created_date__date=date_filter
                ).aggregate(
                    total_leads=Count('id'),
                )

            else:
                leads_by_date = LeadUser.objects.filter(assigned_to=staff).aggregate(
                    interested=Count('id', filter=Q(status='Intrested')),
                    not_interested=Count('id', filter=Q(status='Not Interested')),
                    other_location=Count('id', filter=Q(status='Other Location')),
                    not_picked=Count('id', filter=Q(status='Not Picked')),
                    lost=Count('id', filter=Q(status='Lost')),
                    visit=Count('id', filter=Q(status='Visit'))
                )
                leads_by_date1 = LeadUser.objects.filter(assigned_to=staff).aggregate(
                    total_leads=Count('id')
                )

            # Ensure leads_by_date1['total_leads'] always has a value
            leads_data['total_leads'] += leads_by_date1.get('total_leads', 0)
            leads_data['interested'] += leads_by_date.get('interested', 0)
            leads_data['not_interested'] += leads_by_date.get('not_interested', 0)
            leads_data['other_location'] += leads_by_date.get('other_location', 0)
            leads_data['not_picked'] += leads_by_date.get('not_picked', 0)
            leads_data['lost'] += leads_by_date.get('lost', 0)
            leads_data['visit'] += leads_by_date.get('visit', 0)


            leads_data['total_calls'] += leads_by_date['interested'] + leads_by_date['not_interested'] + leads_by_date['other_location'] + leads_by_date['not_picked'] + leads_by_date['lost'] + leads_by_date['visit']

        visit_percentage = (leads_data['visit'] / leads_data['total_leads'] * 100) if leads_data['total_leads'] > 0 else 0
        interested_percentage = (leads_data['interested'] / leads_data['total_leads'] * 100) if leads_data['total_leads'] > 0 else 0

        staff_data.append({
            'name': team_leader.name,
            'total_leads': leads_data['total_leads'],
            'interested': leads_data['interested'],
            'not_interested': leads_data['not_interested'],
            'other_location': leads_data['other_location'],
            'not_picked': leads_data['not_picked'],
            'lost': leads_data['lost'],
            'visit': leads_data['visit'],
            'visit_percentage': round(visit_percentage, 2),
            'interested_percentage': round(interested_percentage, 2),
            'total_calls': leads_data['total_calls']
        })

        total_all_leads += leads_data['total_leads']
        total_all_interested += leads_data['interested']
        total_all_not_interested += leads_data['not_interested']
        total_all_other_location += leads_data['other_location']
        total_all_not_picked += leads_data['not_picked']
        total_all_lost += leads_data['lost']
        total_all_visit += leads_data['visit']
        total_all_calls += leads_data['total_calls']

    total_visit_percentage = (total_all_visit / total_all_leads * 100) if total_all_leads > 0 else 0
    total_interested_percentage = (total_all_interested / total_all_leads * 100) if total_all_leads > 0 else 0

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'staff_data': staff_data,
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
                             'total_staff_count': total_staffs,})

    return render(request, 'admin_dashboard/staff/my1.html', {
        'staff_data': staff_data,
        'selected_date': date_filter,
        'task_type': task_type,
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
        'template': template,
    })


def project_list(request, tag):
    user = request.user
    if tag == "project_view":
        if request.method == "GET":
            project = Project.objects.all()
            context = {
                'project': project,
            }
            return render(request, 'project_list.html', context)
    if tag == "project_add":
        if request.method == "GET":
            return render(request, 'project_add.html',)
        if request.method == "POST":
            project_name    = request.POST['project_name']
            youtube_url     = request.POST['youtube_url']
            media_file      = request.FILES.get('media_file')
            message         = request.POST['message']

            Project.objects.create(
                user=user,
                name=project_name,
                message=message,
                youtube_link=youtube_url,
                media_file=media_file,
            )
            return redirect('project_list', 'project_view')
            # return render(request, 'project_list.html',)
    return render(request, 'project_list.html')

def project_edit(request, id):
    user = request.user
    if request.method == "GET":
        project = Project.objects.filter(id=id).last()
        context = {
            'project': project,
        }
        return render(request, 'project_edit.html', context)
    
    if request.method == "POST":
        project_name    = request.POST['project_name']
        youtube_url     = request.POST['youtube_url']
        media_file      = request.FILES.get('media_file')
        message         = request.POST['message']

        project = Project.objects.filter(id=id).last()
        project.name = project_name
        project.youtube_link = youtube_url
        if media_file:
            project.media_file = media_file
        project.message = message
        project.save()


        return redirect('project_edit', id)
    return render(request, 'project_edit.html')


def get_month_calendar(year, month):
    cal = calendar.Calendar(firstweekday=6)  
    return [week for week in cal.itermonthdays(year, month)]


# def staff_productivity_calendar_view(request, staff_id, year=None, month=None):
#     # months_list = "1 2 3 4 5 6 7 8 9 10 11 12".split()
#     months_list = [(i, month_name[i]) for i in range(1, 13)]

#     year = int(request.GET.get('year', datetime.now().year))
#     month = int(request.GET.get('month', datetime.now().month))

#     staff = Staff.objects.get(user__id=staff_id)

#     days_in_month = monthrange(year, month)[1]
#     salary_arg = staff.salary
#     if salary_arg is None:
#         salary_arg = 0
#     salary = float(salary_arg)
#     daily_salary = round(float(salary) / int(days_in_month))

#     leads_data = LeadUser.objects.filter(
#         assigned_to=staff,
#         updated_date__year=year,
#         updated_date__month=month,
#         status='Intrested'
#     ).values('updated_date__day').annotate(count=Count('id'))

#     productivity_data = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}

#     total_salary = 0

#     for lead in leads_data:
#         day = lead['updated_date__day']
#         leads_count = lead['count']
#         productivity_data[day]['leads'] = leads_count

#         if leads_count >= 10:
#             daily_earned_salary = daily_salary
#         else:
#             daily_earned_salary = round((daily_salary / 10) * leads_count, 2)

#         productivity_data[day]['salary'] = daily_earned_salary
#         total_salary += daily_earned_salary

#     calendar_data = calendar.monthcalendar(year, month)
#     print(calendar_data, 'AAAAAAAAAAAAAAAA')

#     context = {
#         'staff': staff,
#         'year': year,
#         'month': month,
#         'productivity_data': productivity_data,
#         'calendar_data': calendar_data,
#         'days_in_month': days_in_month,
#         'total_salary': round(total_salary, 2),
#         'months_list': months_list,
#     }

#     return render(request, 'staff_productivity_calendar.html', context)


# ----------------------------------

def staff_productivity_calendar_view(request, staff_id, year=None, month=None):
    if request.user.is_superuser:
        template = 'base.html'
    elif request.user.is_staff_new:
        template = 'admin_dashboard/team_leader/base.html'
    elif request.user.is_admin:
        template = 'admin_dashboard/base.html'
    else:
        template = 'admin_dashboard/staff/base.html'

    months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]

    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    if request.user.is_superuser:
        staff = Staff.objects.get(id=staff_id)
    elif request.user.is_team_leader:
        staff = Staff.objects.get(id=staff_id)
    elif request.user.is_admin:
        staff = Staff.objects.get(id=staff_id)
    else:
        staff = Staff.objects.get(user__id=staff_id)

    days_in_month = monthrange(year, month)[1]
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
    print(leads_data, 'AAAAAAAAAAAAAAAAAAAAA')

    productivity_data = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}

    total_salary = 0

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

    calendar_data = calendar.monthcalendar(year, month)

    weekdays = list(calendar.day_name)

    structured_calendar_data = []
    for week in calendar_data:
        week_data = []
        for i, day in enumerate(week):
            day_name = weekdays[i]  
            week_data.append({
                'day': day,
                'day_name': day_name
            })
        structured_calendar_data.append(week_data)

    context = {
        'staff': staff,
        'year': year,
        'month': month,
        'productivity_data': productivity_data,
        'structured_calendar_data': structured_calendar_data,  
        'days_in_month': days_in_month,
        'total_salary': round(total_salary, 2),
        'months_list': months_list,
        'monthly_salary': salary_arg,
        'template': template,
    }
    return render(request, 'staff_productivity_calendar.html', context)





# OFFICE_LAT = 37.7749
# OFFICE_LNG = -122.4194
OFFICE_LAT = 26.8925797
OFFICE_LNG = 74.74362083333334
RADIUS = 100 

def haversine(lat1, lon1, lat2, lon2):
    R = 6371e3
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)
    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c 


def check_location(request):
    if request.method == 'POST':
        user = request.user

        if user.is_superuser:
            return JsonResponse({'allowed': True})

        data = json.loads(request.body)
        user_lat = data['latitude']
        user_lng = data['longitude']
        
        distance = haversine(OFFICE_LAT, OFFICE_LNG, user_lat, user_lng)
        
        if distance <= RADIUS:
            return JsonResponse({'allowed': True})
        else:
            return JsonResponse({'allowed': False})


@csrf_exempt
def check_superuser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        
        try:
            user = User.objects.get(username=username)
            is_superuser = user.is_superuser
        except User.DoesNotExist:
            is_superuser = False

        return JsonResponse({'is_superuser': is_superuser})
    

def add_freelancer(request):
    # if request.method == "GET":
    #     return render(request, 'add_freelancer.html')
    
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        referral_code = request.POST['referral_code']

        dob = request.POST['dob']
        pancard = request.POST['pancard']
        aadharCard = request.POST['aadharCard']
        # marksheet = request.POST['marksheet']
        degree = request.POST['degree']
        account_number = request.POST['account_number']
        upi_id = request.POST['upi_id']
        bank_name = request.POST['bank_name']
        ifsc_code = request.POST['ifsc_code']
        profile_image = request.FILES.get("profile_image")
        user_type = request.POST['user_type']

        # refer = Staff.objects.filter(referral_code=referral_code).exists()
        # if not refer:
        #     messages.error(request, "Referral Code is invalid. Please register again.")
        #     return redirect('login')
        if user_type == "freelancer":
            user = User.objects.create_user(
                username=username, profile_image=profile_image, password=password, email=username, name=name, mobile=mobile, is_staff_new=True, is_freelancer=True)
        if user_type == "it_staff":
            user = User.objects.create_user(
                username=username, profile_image=profile_image, password=password, email=username, name=name, mobile=mobile, is_staff_new=True, is_it_staff=True)
        user.set_password(password)
        user.save()
        team = Team_Leader.objects.filter().last()

        staff = Staff.objects.create(
            team_leader=team,
            user=user,
            name=name,
            email=username,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            dob=dob,
            pancard=pancard,
            aadharCard=aadharCard,
            degree=degree,
            account_number=account_number,
            upi_id=upi_id,
            bank_name=bank_name,
            ifsc_code=ifsc_code,
            join_referral=referral_code,
        )
        messages.success(request, "Your profile created succesfully. Please wait we are review your profile.")
    return render(request, 'Login.html',)


def incentive_slap_staff(request, staff_id):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]

        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))

        if request.user.is_staff_new:
            user_type = request.user.is_freelancer
        else:
            staff_instance = Staff.objects.filter(id=staff_id).last()
            user_type = User.objects.filter(email=staff_instance.email).last().is_freelancer

        slab = Slab.objects.all()
        if request.user.is_superuser:
            sell_property = Sell_plot.objects.filter(
            staff=staff_id, 
            updated_date__year=year,
            updated_date__month=month,).order_by('-created_date')

            total_earn_amount = Sell_plot.objects.filter(
            staff=staff_id, 
            updated_date__year=year,
            updated_date__month=month,).aggregate(total_earn=Sum('earn_amount'))

        elif request.user.is_team_leader:
            sell_property = Sell_plot.objects.filter(
            staff=staff_id, 
            updated_date__year=year,
            updated_date__month=month,).order_by('-created_date')

            total_earn_amount = Sell_plot.objects.filter(
            staff=staff_id, 
            updated_date__year=year,
            updated_date__month=month,).aggregate(total_earn=Sum('earn_amount'))
            
        elif request.user.is_admin:
            sell_property = Sell_plot.objects.filter(
            staff=staff_id, 
            updated_date__year=year,
            updated_date__month=month,).order_by('-created_date')

            total_earn_amount = Sell_plot.objects.filter(
            staff=staff_id, 
            updated_date__year=year,
            updated_date__month=month,).aggregate(total_earn=Sum('earn_amount'))

        else:
            sell_property = Sell_plot.objects.filter(
                staff__email=request.user.email, 
                updated_date__year=year,
                updated_date__month=month,).order_by('-created_date')

            total_earn_amount = Sell_plot.objects.filter(
                staff__email=request.user.email, 
                updated_date__year=year,
                updated_date__month=month,).aggregate(total_earn=Sum('earn_amount'))
        total_earn = total_earn_amount['total_earn'] if total_earn_amount['total_earn'] else 0
    context = {
        'slab': slab,
        'sell_property': sell_property,
        'total_earn': total_earn,
        'year': year,
        'month': month,
        'months_list': months_list,
        'template': template,
        'user_type': user_type,
    }
    return render(request, 'admin_dashboard/staff/incentive_slap_staff.html', context)

# home/views.py

def add_sell_freelancer(request, id):
    if request.method == "GET":
        admins = Admin.objects.all()
        if request.user.is_team_leader:
            staffs = Staff.objects.filter(team_leader__email=request.user.email)
            context = {
                'id':id,
                'staffs':staffs,
                'admins': admins,
            }
        if request.user.is_superuser:
            context = {
                    'id':id,
                    'admins': admins,
                }
        return render(request, 'admin_dashboard/staff/add_sell.html', context)
    
    if request.method == "POST":
        
        # --- [FIX 1 & 2] ---
        # .get() ka istemal kiya aur 'plot_no' key ko theek kiya
        project_name = request.POST.get('project_name')
        project_location = request.POST.get('project_location', None)
        description = request.POST.get('description', None)
        size_in_gaj = request.POST.get('size_in_gaj')      # FIX: ['size_in_gaj'] se .get('size_in_gaj') kiya
        plot_no = request.POST.get('plot_no', None)           # FIX: 'amount_per_gaj' se 'plot_no' kiya
        date = request.POST.get('date')                   # FIX: ['date'] se .get('date') kiya
        admin_id = request.POST.get('admin', None)
        team_leader_id = request.POST.get('team_leader', None)
        staff_id = request.POST.get('staff', None)

        # --- [FIX 3] ---
        # Validation check taaki code crash na ho agar required data missing hai
        if not project_name or not size_in_gaj or not date:
            context = {'id': id, 'error': 'Project Name, Size (Gaj), and Date are required.'}
            # Template ko render karne ke liye context dobara banana padega
            admins = Admin.objects.all()
            if request.user.is_team_leader:
                context['staffs'] = Staff.objects.filter(team_leader__email=request.user.email)
            context['admins'] = admins
            return render(request, 'admin_dashboard/staff/add_sell.html', context)


        # --- [FIX 4] ---
        # Instance checks taaki code crash na ho agar koi object na mile
        user = request.user.email
        if id != 0:
            user_instance = Staff.objects.filter(id=id).last()
        else:
            user_instance = Staff.objects.filter(id=staff_id).last()

        if not user_instance:
            context = {'id': id, 'error': f'Staff not found with id {staff_id or id}.'}
            # Re-populate context...
            return render(request, 'admin_dashboard/staff/add_sell.html', context)
        
        team_leader_insatnce = user_instance.team_leader

        if not team_leader_insatnce:
            context = {'id': id, 'error': f'Team Leader not found for staff {user_instance.name}.'}
            # Re-populate context...
            return render(request, 'admin_dashboard/staff/add_sell.html', context)

        admin_instance = team_leader_insatnce.admin
        
        if not admin_instance:
            context = {'id': id, 'error': f'Admin not found for team leader {team_leader_insatnce.name}.'}
            # Re-populate context...
            return render(request, 'admin_dashboard/staff/add_sell.html', context)


        # --- [FIX 5] ---
        # int() crashes ko rokne ke liye int(variable or 0) ka istemal
        
        # Pehle size_in_gaj ko safe integer me convert karo
        size_in_gaj_int = int(size_in_gaj or 0)

        staff_slab = user_instance.achived_slab
        if staff_slab is None:
            user_instance.achived_slab = size_in_gaj_int
        else:
            update_staff_slab = int(staff_slab or 0) + size_in_gaj_int
            user_instance.achived_slab = update_staff_slab
        user_instance.save()

        team_lead_slab = team_leader_insatnce.achived_slab
        if team_lead_slab is None:
            team_leader_insatnce.achived_slab = size_in_gaj_int
        else:
            update_staff_slab1 = int(team_lead_slab or 0) + size_in_gaj_int
            team_leader_insatnce.achived_slab = update_staff_slab1
        team_leader_insatnce.save()

        admin_slab = admin_instance.achived_slab
        if admin_slab is None:
            admin_instance.achived_slab = size_in_gaj_int
        else:
            update_staff_slab2 = int(admin_slab or 0) + size_in_gaj_int
            admin_instance.achived_slab = update_staff_slab2
        admin_instance.save()
        
        current_slab = int(user_instance.achived_slab or 0)
        current_team_leader_slab = int(team_leader_insatnce.achived_slab or 0)
        current_admin_slab = int(admin_instance.achived_slab or 0)
        
        slabs = Slab.objects.all()

        # --- [FIX 6] ---
        # Variables ko loop se pehle initialize karo
        slab_amount = 0
        myslab = "N/A"
        current_slab_amount = 0

        for slab in slabs:
            start_value = int(slab.start_value or 0) # [FIX 5]

            if slab.end_value is not None:
                end_value = int(slab.end_value or 0) # [FIX 5]

                if start_value <= current_slab <= end_value:
                    slab_amount_base = int(slab.amount or 0) # [FIX 5]
                    if user_instance.user.is_freelancer:
                        slab_amount = slab_amount_base * size_in_gaj_int
                    if user_instance.user.is_staff_new:
                        slab_amount = (slab_amount_base - 100) * size_in_gaj_int
                    
                    myslab = f"{start_value}-{end_value}"
                    current_slab_amount = slab_amount_base
                    break
            else:
                if current_slab >= start_value:
                    slab_amount_base = int(slab.amount or 0) # [FIX 5]
                    if user_instance.user.is_freelancer:
                        slab_amount = slab_amount_base * size_in_gaj_int
                    if user_instance.user.is_staff_new:
                        slab_amount = (slab_amount_base - 100) * size_in_gaj_int
                    
                    myslab = f"{start_value}+"
                    current_slab_amount = slab_amount_base
                    break

        sell = Sell_plot.objects.create(
            admin = admin_instance,
            team_leader = team_leader_insatnce,
            staff = user_instance,
            project_name = project_name,
            project_location = project_location,
            description = description,
            size_in_gaj = size_in_gaj, # Model me string save kar rahe hain (original logic)
            plot_no = plot_no,
            date = date,
            earn_amount = slab_amount,
            slab = myslab,
            slab_amount = current_slab_amount,
        )
        return redirect('add_sell_freelancer', 0)
        
    return render(request, 'admin_dashboard/staff/add_sell.html', {'id':id})

def add_freelancer_super_side(request):
    if request.method == "GET":
        my_staff = Staff.objects.filter(user__is_freelancer=True)
        
        total_leads = LeadUser.objects.filter(status="Leads").count()
        total_interested_leads = LeadUser.objects.filter(status="Intrested", assigned_to__user__is_freelancer=True).count()
        total_not_interested_leads = LeadUser.objects.filter(status="Not Interested", assigned_to__user__is_freelancer=True).count()
        total_other_location_leads = LeadUser.objects.filter(status="Other Location", assigned_to__user__is_freelancer=True).count()
        total_not_picked_leads = LeadUser.objects.filter(status="Not Picked", assigned_to__user__is_freelancer=True).count()
        total_lost_leads = LeadUser.objects.filter(status="Lost", assigned_to__user__is_freelancer=True).count()
        total_visits_leads = LeadUser.objects.filter(status="Visit", assigned_to__user__is_freelancer=True).count()

        months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
        
        if request.user.is_superuser:
            staff_list = Staff.objects.all()
        
        days_in_month = monthrange(year, month)[1]
        
        total_salary_all_staff = 0
        productivity_data_all_staff = {}

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

            productivity_data = {day: {'leads': 0, 'salary': 0} for day in range(1, days_in_month + 1)}
            total_salary = 0

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

            productivity_data_all_staff[staff.id] = {
                'name': staff.name,
                'productivity_data': productivity_data,
                'total_salary': round(total_salary, 2)
            }
            
            total_salary_all_staff += total_salary

        calendar_data = calendar.monthcalendar(year, month)
        weekdays = list(calendar.day_name)

        structured_calendar_data = []
        for week in calendar_data:
            week_data = []
            for i, day in enumerate(week):
                day_name = weekdays[i]
                week_data.append({
                    'day': day,
                    'day_name': day_name
                })
            structured_calendar_data.append(week_data)

        context = {
            # 'users': users, 
            'total_interested_leads': total_interested_leads,
            'total_not_interested_leads': total_not_interested_leads,
            'total_other_location_leads': total_other_location_leads,
            'total_not_picked_leads': total_not_picked_leads,
            'total_lost_leads': total_lost_leads,
            'total_leads': total_leads,
            'total_visits_leads': total_visits_leads,
            'my_staff': my_staff,
            'total_salary_all_staff': total_salary_all_staff,
        }
    return render(request, 'add_freelancer_super.html', context)

def team_lead_leads_report(request, id, tag):
    if tag == "Intrested":
        staff_leads = LeadUser.objects.filter(team_leader=id, status='Intrested').order_by('-updated_date')
    elif tag == "Not Interested":
        staff_leads = LeadUser.objects.filter(team_leader=id, status='Not Interested').order_by('-updated_date')
    elif tag == "Other Location":
        staff_leads = LeadUser.objects.filter(team_leader=id, status='Other Location').order_by('-updated_date')
    elif tag == "Lost":
        staff_leads = LeadUser.objects.filter(team_leader=id, status='Lost').order_by('-updated_date')
    elif tag == "Visit":
        staff_leads = LeadUser.objects.filter(team_leader=id, status='Visit').order_by('-updated_date')
    else:
        staff_leads = LeadUser.objects.filter(team_leader=id).order_by('-updated_date') 
    paginator = Paginator(staff_leads, per_page=50)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # total_upload_leads = leads2.count()

    num_pages = paginator.num_pages
    page_range = []
    
    if num_pages <= 7:
        page_range = list(paginator.page_range)
    else:
        page_range = list(paginator.page_range[:3])  
        if page.number > 4:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[max(3, page.number - 2):page.number + 2]))
        if page.number < num_pages - 3:
            page_range.append('...')
        page_range.extend(list(paginator.page_range[-3:]))

    context = {
        'staff_leads': staff_leads,
        'page_range': page_range,
        'page': page,
        'staff_id': id,
    }
    return render(request, 'super_admin/team_lead_leads_report.html', context)

def get_matching_leads(request):
    current_time = localtime(now()) + timedelta(hours=5, minutes=30)
    min_time = current_time - timedelta(minutes=15)

    if request.user.is_team_leader:
        leads = LeadUser.objects.filter(
            team_leader__user=request.user,
            follow_up_date=current_time.date(),
            follow_up_time__gt=current_time.time(),
            follow_up_time__lte=(current_time + timedelta(minutes=15)).time()
        )

    elif request.user.is_superuser:
        leads = LeadUser.objects.filter(
            follow_up_date=current_time.date(),
            follow_up_time__gt=current_time.time(),
            follow_up_time__lte=(current_time + timedelta(minutes=15)).time()
        )

    elif request.user.is_staff_new:
        leads = LeadUser.objects.filter(
            assigned_to__user=request.user,
            follow_up_date=current_time.date(),
            follow_up_time__gt=current_time.time(),
            follow_up_time__lte=(current_time + timedelta(minutes=15)).time()
        )

    elif request.user.is_admin:
        leads = LeadUser.objects.filter(
            team_leader__admin__self_user=request.user,
            follow_up_date=current_time.date(),
            follow_up_time__gt=current_time.time(),
            follow_up_time__lte=(current_time + timedelta(minutes=15)).time()
        )

    if leads.exists():
        data = {'status': 'success', 'message': 'Please follow up with the customer!', 'leads': list(leads.values('name', 'id'))}
    else:
        data = {'status': 'no_lead'}

    return JsonResponse(data)

@login_required(login_url='login')
def today_interested_count(request):
    today = localtime(now()).date()

    if request.user.is_superuser:
        interested_leads = LeadUser.objects.filter(
            status='Intrested', follow_up_date=today
        )
    elif request.user.is_team_leader:
        interested_leads = LeadUser.objects.filter(
            team_leader__user=request.user,
            status='Intrested', follow_up_date=today
        )
    elif request.user.is_admin:
        interested_leads = LeadUser.objects.filter(
            team_leader__admin__self_user=request.user,
            status='Intrested', follow_up_date=today
        )
    elif request.user.is_staff_new:
        interested_leads = LeadUser.objects.filter(
            assigned_to__user=request.user,
            status='Intrested', follow_up_date=today
        )

    leads_data = list(interested_leads.values('name', 'follow_up_time'))

    data = {
        'count': interested_leads.count(),
        'leads': leads_data
    }

    return JsonResponse(data)

@login_required
def dashboard(request):
    today = date.today()

    attendance, _ = Attendance.objects.get_or_create(user=request.user, date=today)

    if request.method == 'POST':
        description = request.POST['description']
        Task.objects.create(user=request.user, description=description)

        attendance.is_present = True
        attendance.save()

        return redirect('dashboard')

    tasks = Task.objects.filter(user=request.user)
    attendance_records = Attendance.objects.filter(user=request.user)

    return render(request, 'it_dashboard/dashboard.html', {
        'tasks': tasks,
        'attendance_records': attendance_records,
    })


def get_logo(request):
    setting = Settings.objects.last()
    if setting and setting.logo:
        return JsonResponse({'logo_url': setting.logo.url})
    return JsonResponse({'logo_url': ''})

def it_staff_super_admin_side(request):
    if request.method == "GET":
        it_staff = Staff.objects.filter(user__is_it_staff=True)
    context = {
        'it_staff': it_staff,
    }
    return render(request, 'super_admin/it_staff.html', context)

def AddLeadBySelf(request):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        context = {
            'template': template,
        }
        return render(request, 'super_admin/add_lead_by_self.html', context)

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        status = request.POST['status']
        description = request.POST['description']
        if request.user.is_staff_new:
            staff_instance = Staff.objects.filter(email=request.user.email).last()
            lead = LeadUser.objects.create(
                user = request.user,
                team_leader = staff_instance.team_leader,
                assigned_to = staff_instance,
                name = name,
                email = email,
                call = mobile,
                message = description,
                status = status,
            )
            return redirect('leads')
        if request.user.is_team_leader:
            team_lead_instance = Team_Leader.objects.filter(email=request.user.email).last()
            lead = LeadUser.objects.create(
                user = request.user,
                team_leader = team_lead_instance,
                # assigned_to = staff_instance,
                name = name,
                email = email,
                call = mobile,
                message = description,
                status = status,
            )

            return redirect('lead')
        
        if request.user.is_admin:
            admin_instance = Admin.objects.filter(email=request.user.email).last()
            lead = LeadUser.objects.create(
                user = request.user,
                # team_leader__admin = admin_instance,
                # assigned_to = staff_instance,
                name = name,
                email = email,
                call = mobile,
                message = description,
                status = status,
            )

            return redirect('total_leads_admin')
        
def LeadHistory(request, id):
    if request.method == "GET":
        if request.user.is_superuser:
            template = 'base.html'
        elif request.user.is_staff_new:
            template = 'admin_dashboard/team_leader/base.html'
        elif request.user.is_admin:
            template = 'admin_dashboard/base.html'
        else:
            template = 'admin_dashboard/staff/base.html'

        lead_history = Leads_history.objects.filter(lead_id=id).order_by('-updated_date')

        context = {
            'template': template,
            'lead_history': lead_history,
        }
        return render(request, 'super_admin/lead_history.html', context)
    

@login_required
def add_inquiry(request):
    if request.method == "POST":
        # Step 1: Merchant Register Forms Data
        legal_name = request.POST.get('merchant_legal_name')
        marchant_dba_name = request.POST.get('merchant_dba_name')  
        installation_address = request.POST.get('installation_address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        contact_person = request.POST.get('contact_person_name') 
        telephone = request.POST.get('telephone_no') 
        primary_mobile = request.POST.get('primary_mobile_no')  
        secondary_mobile = request.POST.get('secondary_mobile_no') 
        email = request.POST.get('email_address')  
        pan_no = request.POST.get('pan_no')
        gst_no = request.POST.get('gst_no')
        business_type = request.POST.get('type_of_business')  
        constitution_type = request.POST.get('constitution_type')
        others = request.POST.get('other_constitution_type') 
        # Merchant Settlement Details
        beneficiary_name = request.POST.get('beneficiary_name')
        bank_account_no = request.POST.get('bank_account_no')
        bank_name = request.POST.get('bank_name')
        ifsc_code = request.POST.get('ifsc_code')
        branch_name = request.POST.get('branch_name')
        merchant_inquiry = MerchantInquiry.objects.last()
        # Create and save the MerchantFormsData instance
        merchant_form_data = MerchantFormsData.objects.create(
            legal_name=legal_name,
            marchant_dba_name=marchant_dba_name,  
            installation_address=installation_address,
            city=city,
            pincode=pincode,
            state=state,
            contact_person=contact_person,  
            telephone=telephone, 
            primary_mobile=primary_mobile, 
            secondary_mobile=secondary_mobile,  
            email=email,  
            pan_no=pan_no,
            gst_no=gst_no,
            business_type=business_type,  
            constitution_type=constitution_type,
            others=others, 
            beneficiary_name=beneficiary_name,
            bank_account_no=bank_account_no,
            bank_name=bank_name,
            ifsc_code=ifsc_code,
            branch_name=branch_name,
            merchant_inquiry = merchant_inquiry,
            submitted_by = request.user,

        )
        merchant_form_data.save()
        messages.success(request, "Your Inquiry has been submitted successfully. Please wait, the manager will review your inquiry.")
        return JsonResponse({"success": True, "message": "Data submitted successfully"})
    
    # If not POST, render the form template
    return render(request, "admin_dashboard/staff/add_inquiry.html")

@login_required
def update_inquiry_forms(request, id):
    if request.method == "GET":
        try:
            # Fetch the MerchantInquiry and related MerchantFormsData by ID
            merchant_inquiry = MerchantInquiry.objects.get(id=id)
        except MerchantInquiry.DoesNotExist:
            messages.error(request, "Merchant inquiry record not found!")
            return redirect('staff_user')  
        
        try:
            merchant_forms_data = MerchantFormsData.objects.get(merchant_inquiry=merchant_inquiry)
        except MerchantFormsData.DoesNotExist:
            messages.error(request, "No form data associated with this inquiry.")
            return redirect('staff_user')

        context = {
            'merchant_forms_data': merchant_forms_data,
            'merchant_inquiry':merchant_inquiry
        }
        return render(request, 'admin_dashboard/staff/update_inquiry_forms.html', context)

    if request.method == "POST":
        # Fetch the MerchantFormsData that needs to be updated
        try:
            merchant_inquiry = MerchantInquiry.objects.get(id=id)
            merchant_forms_data = MerchantFormsData.objects.get(merchant_inquiry=merchant_inquiry)
        except (MerchantInquiry.DoesNotExist, MerchantFormsData.DoesNotExist):
            messages.error(request, "Invalid inquiry or form data.")
            return redirect('staff_user')

        # Step 1: Merchant Register Forms Data (retrieve from POST data)
        merchant_forms_data.legal_name = request.POST.get('merchant_legal_name', merchant_forms_data.legal_name)
        merchant_forms_data.marchant_dba_name = request.POST.get('merchant_dba_name', merchant_forms_data.marchant_dba_name)  
        merchant_forms_data.installation_address = request.POST.get('installation_address', merchant_forms_data.installation_address)
        merchant_forms_data.city = request.POST.get('city', merchant_forms_data.city)
        merchant_forms_data.pincode = request.POST.get('pincode', merchant_forms_data.pincode)
        merchant_forms_data.state = request.POST.get('state', merchant_forms_data.state)
        merchant_forms_data.contact_person = request.POST.get('contact_person_name', merchant_forms_data.contact_person)  
        merchant_forms_data.telephone = request.POST.get('telephone_no', merchant_forms_data.telephone) 
        merchant_forms_data.primary_mobile = request.POST.get('primary_mobile_no', merchant_forms_data.primary_mobile)  
        merchant_forms_data.secondary_mobile = request.POST.get('secondary_mobile_no', merchant_forms_data.secondary_mobile) 
        merchant_forms_data.email = request.POST.get('email_address', merchant_forms_data.email)  
        merchant_forms_data.pan_no = request.POST.get('pan_no', merchant_forms_data.pan_no)
        merchant_forms_data.gst_no = request.POST.get('gst_no', merchant_forms_data.gst_no)
        merchant_forms_data.business_type = request.POST.get('type_of_business', merchant_forms_data.business_type)  
        merchant_forms_data.constitution_type = request.POST.get('constitution_type', merchant_forms_data.constitution_type)
        merchant_forms_data.others = request.POST.get('other_constitution_type', merchant_forms_data.others) 

        # Merchant Settlement Details
        merchant_forms_data.beneficiary_name = request.POST.get('beneficiary_name', merchant_forms_data.beneficiary_name)
        merchant_forms_data.bank_account_no = request.POST.get('bank_account_no', merchant_forms_data.bank_account_no)
        merchant_forms_data.bank_name = request.POST.get('bank_name', merchant_forms_data.bank_name)
        merchant_forms_data.ifsc_code = request.POST.get('ifsc_code', merchant_forms_data.ifsc_code)
        merchant_forms_data.branch_name = request.POST.get('branch_name', merchant_forms_data.branch_name)

        # Update the record
        merchant_forms_data.save()

        # Provide success feedback and respond with a JSON message
        messages.success(request, "Inquiry form updated successfully.")
        return JsonResponse({"success": True, "message": "Form updated successfully"})

    # If not POST, render the form template
    return render(request, "admin_dashboard/staff/update_inquiry_forms.html")
@login_required
def interested_not_interested_inquiry(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        selected_value = request.POST.get('status')
        status_check = True
        # Handle "Not Interested" status
        if selected_value == "Not Interested":
            status_check = False
            # Get dsr_manager users and count the inquiries with "New Inquiry" status assigned to them
            dsr_managers = User.objects.filter(dsr_manager=True)
            least_inquiries_dsr = None
            if dsr_managers.exists():
                least_inquiries_dsr = dsr_managers.annotate(
                    inquiry_count=Count('assigned_inquiry', filter=Q(assigned_inquiry__inquiry_status='New Inquiry'))
                ).order_by('inquiry_count').first()

            assigned_user = least_inquiries_dsr if least_inquiries_dsr else None
        # Handle "Interested" status
        elif selected_value == "Interested":
            on_boarding_managers = User.objects.filter(on_boarding_manager=True)
            least_inquiries_on_boarding = None
            if on_boarding_managers.exists():
                least_inquiries_on_boarding = on_boarding_managers.annotate(
                    inquiry_count=Count('assigned_inquiry', filter=Q(assigned_inquiry__inquiry_status='New Inquiry'))
                ).order_by('inquiry_count').first()

            assigned_user = least_inquiries_on_boarding if least_inquiries_on_boarding else None
        else:
            assigned_user = None
        MerchantInquiry.objects.create(
            full_name=full_name,
            contact_number=contact_number,
            address=address,
            is_interested=status_check,
            submitted_by=request.user,
            assigned_user=assigned_user
        )
        if request.user.is_team_leader and not status_check:
            messages.success(request, "Your Inquiry has been submitted successfully. Please wait, the manager will review your inquiry.")
            return JsonResponse({'success': True})
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def update_inquiry(request, id):
    if request.method == "GET":
        try:
            merchant_inquiry = MerchantInquiry.objects.get(id=id)
        except MerchantInquiry.DoesNotExist:
            messages.error(request, "Merchant inquiry record not found!")
            return redirect('staff_user')  
        try:
            merchant_forms_data = MerchantFormsData.objects.get(merchant_inquiry=merchant_inquiry)
        except MerchantFormsData.DoesNotExist:
            messages.error(request, "No form data associated with this inquiry.")
            return redirect('staff_user')
        context = {
            'merchant_forms_data': merchant_forms_data,
        }
        return render(request, 'admin_dashboard/staff/edit_inquiry.html', context)
    if request.method == "POST":
        try:
            # Get the specific MerchantInquiry record
            merchant_inquiry = MerchantInquiry.objects.get(id=id)
        except MerchantInquiry.DoesNotExist:
            messages.error(request, "Merchant inquiry record not found!")
            return redirect('staff_user')  
        try:
            # Get the associated MerchantFormsData record
            forms_data = MerchantFormsData.objects.get(merchant_inquiry=merchant_inquiry)
        except MerchantFormsData.DoesNotExist:
            messages.error(request, "No form data associated with this inquiry.")
            return redirect('staff_user')
        # Get data from the form
        pos_type_opted = request.POST.get('pos_type_opted')
        number_of_pos_terminals = request.POST.get('number_of_pos_terminals')
        value_added_services_required = request.POST.get('value_added_services_required') == 'on'
        emi_facility_on_credit_card = request.POST.get('emi_facility_on_credit_card') == 'on'
        sodexo = request.POST.get('sodexo') == 'on'
        amex = request.POST.get('amex') == 'on'
        operation_model = request.POST.get('operation_model')
        monthly_rental_amount = request.POST.get('monthly_rental_amount')
        fixed_cost_amount = request.POST.get('fixed_cost_amount')
        device_security_charge = request.POST.get('device_security_charge')
        setup_fee = request.POST.get('setup_fee')
        mop = request.POST.get('mop')
        mop_amount = request.POST.get('mop_amount')
        cheque_number = request.POST.get('cheque_number')
        payment_ref_number = request.POST.get('payment_ref_number')
        #save Data
        forms_data.pos_type_opted = pos_type_opted
        forms_data.number_of_pos_terminals = number_of_pos_terminals
        forms_data.value_added_services_required = value_added_services_required
        forms_data.emi_facility_on_credit_card = emi_facility_on_credit_card
        forms_data.sodexo = sodexo
        forms_data.amex = amex
        forms_data.operation_model = operation_model
        forms_data.monthly_rental_amount = monthly_rental_amount
        forms_data.fixed_cost_amount = fixed_cost_amount
        forms_data.device_security_charge = device_security_charge
        forms_data.setup_fee = setup_fee
        forms_data.mop = mop
        forms_data.mop_amount = mop_amount
        forms_data.cheque_number = cheque_number 
        forms_data.payment_ref_number = payment_ref_number
        
        assigned_delivery_user = User.objects.filter(delivery_manager=True).annotate(
            forms_count=Count('assigned_inquiry', filter=Q(assigned_inquiry__inquiry_status='Pending Delivery'))
        ).order_by('forms_count').first()
        if assigned_delivery_user:
            forms_data.assigned_delivery_user = assigned_delivery_user
        else:
            messages.error(request, "No delivery user available to assign.")
            return redirect('staff_user')
        merchant_inquiry.inquiry_status = "Pending Delivery"
        merchant_inquiry.delivery_manager = assigned_delivery_user
        merchant_inquiry.save()
        forms_data.save()
        messages.error(request, "Machine  Details add  successfully")
        return redirect('staff_user')


    # Render the template for GET requests
    return render(request, "form_template.html")

@csrf_exempt
def update_inquiry_status(request):
    if request.method == 'POST':
        inquiry_id = request.POST.get('id')
        try:
            inquiry = get_object_or_404(MerchantInquiry, id=inquiry_id)
            # Update the status logic
            if inquiry.inquiry_status ==  "Pending Delivery":
                inquiry.inquiry_status = 'Completed'
            else:
                inquiry.inquiry_status = 'Pending Delivery'
            inquiry.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def pending_inquiry_lists(request, status):
    if request.method == "GET":
        user  = request.user
        inquiries_data = []
        if user.executive_manager:
                executive_manager_inquiry_data = MerchantInquiry.objects.filter(submitted_by=user).order_by("-id")
                inquiries_data = executive_manager_inquiry_data.filter(submitted_by=user, is_interested=True).order_by('-id')
                inquiries_data = executive_manager_inquiry_data.filter(submitted_by=user, is_interested=False).order_by('-id')
                inquiries_data = executive_manager_inquiry_data.filter(submitted_by=user, inquiry_status='New Inquiry').order_by('-id')   
                if status == "pending":     
                    inquiries_data = executive_manager_inquiry_data.filter(submitted_by=user, inquiry_status='Pending Delivery').order_by('-id')
                elif status == "new_inquiry":
                    inquiries_data = executive_manager_inquiry_data.filter(submitted_by=user, inquiry_status='New Inquiry').order_by('-id')
                elif status == "completed":
                    inquiries_data = executive_manager_inquiry_data.filter(submitted_by=user, inquiry_status='Completed').order_by('-id')    
        if user.delivery_manager :
                delivery_manager_inquiry_data = MerchantInquiry.objects.filter(assigned_user=user).order_by("-id")
                if status == "pending":     
                    inquiries_data = delivery_manager_inquiry_data.filter(assigned_user = user, inquiry_status='Pending Delivery').order_by('-id')
                elif status == "new_inquiry":
                    inquiries_data = delivery_manager_inquiry_data.filter(assigned_user = user, inquiry_status='New Inquiry').order_by('-id')
                elif status == "completed":
                    inquiries_data = delivery_manager_inquiry_data.filter(assigned_user = user, inquiry_status='Completed').order_by('-id')  
        if user.on_boarding_manager:
            on_boarding_manager_manager_inquiry_data = MerchantInquiry.objects.filter(assigned_user=user).order_by("-id")
            inquiries_data = on_boarding_manager_manager_inquiry_data.filter(assigned_user = user, inquiry_status='New Inquiry').order_by('-id')
        context = {
            'inquiry_data':inquiries_data,
        }
        return render(request, "admin_dashboard/staff/inquiry_lits.html", context)