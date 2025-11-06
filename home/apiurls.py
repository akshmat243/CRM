from django.urls import path
from .api import *
from . import api
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # path('', views.login, name='login'),
    # path('update-password/', views.update_password, name='update_password'),
    path('apilogin/', LoginApiView.as_view(), name='apilogin'),
    path('staff_assigned_leads/', staff_assigned_leads.as_view(), name='staff_assigned_leads'),
    path('status-update/', StatusUpdateAPIView.as_view(), name='status-update'),
    path('auto-assign-leads/', AutoAssignLeadsAPIView.as_view(), name='auto-assign-leads'),
    path('leads-report-staff/', LeadsReportAPIView.as_view(), name='leads-report-staff'),
    path('leads-history/', LeadHistoryAPIView.as_view(), name='leads-report-staff'),
    path('self-lead-add/', AddLeadBySelfAPI.as_view(), name='self-lead-add'),
    path('profile-view/', StaffProfileAPIView.as_view(), name='profile-view'),
    path('api/marketing/edit/<str:source>/', EditRecordAPIView.as_view(), name='edit_record'),
    path('api/marketing/update/', UpdateRecordAPIView.as_view(), name='update_record'),
    path('api/activitylogs/', ActivityLogsAPIView.as_view(), name='activity_logs'),
    path('api/incentive-slab-staff/<int:staff_id>/', IncentiveSlabStaffView.as_view(), name='incentive_slab_staff_api'),
    path('staff/<int:staff_id>/productivity/', StaffProductivityCalendarAPIView.as_view(), name='staff_productivity_calendar'),
    path('dashboard/super-admin/', api.SuperAdminDashboardAPIView.as_view(), name='api-super-admin-dashboard'),

    path('dashboard/super-user/', api.SuperUserDashboardAPIView.as_view(), name='api-super-user-dashboard'),
    path('admin-leads/<str:tag>/', api.AdminSideLeadsRecordAPIView.as_view(), name='api-admin-leads-record'),

    path('leads/upload-excel/', api.ExcelUploadAPIView.as_view(), name='api-excel-upload'),

   

    path('users/it-staff/', api.ITStaffListAPIView.as_view(), name='api-it-staff-list'),
    path('attendance/<int:id>/', api.AttendanceCalendarAPIView.as_view(), name='api-attendance-calendar'),
    path('productivity/staff/', api.StaffProductivityAPIView.as_view(), name='api-staff-productivity'),
    path('productivity/team-leader/', api.TeamLeaderProductivityAPIView.as_view(), name='api-teamleader-productivity'),
    path('productivity/admin/', api.AdminProductivityAPIView.as_view(), name='api-admin-productivity'),
    path('productivity/freelancer/', api.FreelancerProductivityAPIView.as_view(), name='api-freelancer-productivity-stats'),


    path('users/admin/add/', api.AdminAddAPIView.as_view(), name='api-admin-add'),
    path('users/admin/edit/<int:id>/', api.AdminEditAPIView.as_view(), name='api-admin-edit'),
    path('leads/customer/<str:tag>/', api.TeamCustomerLeadsAPIView.as_view(), name='api-team-customer-leads'),
    path('users/toggle-active/', api.ToggleUserActiveAPIView.as_view(), name='api-toggle-user-active'),

    

    path('users/team-leader/add-new/', api.TeamLeaderAddAPIView.as_view(), name='api-team-leader-add-new'),
    path('users/team-leader/edit/<int:id>/', api.TeamLeaderEditAPIView.as_view(), name='api-teamleader-edit'),
    path('api/reports/team-leader-leads/<int:id>/<str:tag>/', api.TeamLeadLeadsReportAPIView.as_view(), name='api_team_leader_leads_report'),

    path('superuser/staff-leads/<str:tag>/', api.SuperUserStaffLeadsAPIView.as_view(), name='api-superuser-staff-leads'),



    path('users/staff/add/', api.StaffAddAPIView.as_view(), name='api-staff-add'),
    path('users/staff/edit/<int:id>/', api.StaffEditAPIView.as_view(), name='api-staff-edit'),




    path('report/incentive-slab/<int:staff_id>/', api.IncentiveSlabStaffAPIView.as_view(), name='api-incentive-slab'),
    path('staff/<int:staff_id>/calendar/', api.StaffProductivityCalendarAPIView.as_view(), name='staff_productivity_calendar'),
   
    path('leads/staff/<int:id>/<str:tag>/', api.TeamLeaderParticularLeadsAPIView.as_view(), name='api-staff-particular-leads'),
    path('api/lead/update/<int:id>/', api.update_lead_user_api, name='api_lead_update_detail'),


    path('associates/dashboard/', api.FreelancerDashboardAPIView.as_view(), name='api-freelancer-dashboard'),
    path('api/add-sell-freelancer/<int:id>/', api.AddSellPlotAPIView.as_view(), name='api_add_sell_freelancer'),
 
    path('api/dashboard/team-leader/', api.get_team_leader_dashboard_api, name='api_team_leader_dashboard'),


    path('api/team-customer/<str:tag>/', api.TeamCustomerLeadsAPIView.as_view(), name='api_team_customer_leads'), 
    path('api/export/staff-leads/', api.ExportLeadsStatusWiseAPIView.as_view(), name='api_export_leads'),
    path('api/leads/visit/', api.VisitLeadsAPIView.as_view(), name='api_visit_leads'),


    path('api/projects/', api.ProjectListCreateAPIView.as_view(), name='api_project_list_create'),

    path('api/activitylogs/', api.ActivityLogsAPIView.as_view(), name='api_activity_logs'),





    path('api/admin/team-leader-report/', api.AdminTeamLeaderReportAPIView.as_view(), name='api_admin_team_leader_report'),
    





















   ]   

