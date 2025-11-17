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
    path('api/admin-leads/<str:tag>/', api.AdminSideLeadsRecordAPIView.as_view(), name='api-admin-leads-record'),

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



        #lead  lead lead
    path('api/superuser/unassigned-leads/', api.SuperUserUnassignedLeadsAPIView.as_view(), name='api_superuser_unassigned_leads'),

    #associates dashboard cards api url
    path('api/superuser/freelancer-leads/<str:tag>/', api.SuperUserFreelancerLeadsAPIView.as_view(), name='api_superuser_freelancer_leads'),

    #teamleader cards api 
    path('api/superuser/team-leader-leads/<str:tag>/',api.SuperUserTeamLeaderLeadsAPIView.as_view(),name='api_superuser_team_leader_leads'),



    path('report/incentive-slab/<int:staff_id>/', api.IncentiveSlabStaffAPIView.as_view(), name='api-incentive-slab'),
    path('staff/<int:staff_id>/calendar/', api.StaffProductivityCalendarAPIView.as_view(), name='staff_productivity_calendar'),
   #staff associates view api 
    path('leads/staff/<int:id>/<str:tag>/', api.TeamLeaderParticularLeadsAPIView.as_view(), name='api-staff-particular-leads'),
    path('api/lead/update/<int:id>/', api.update_lead_user_api, name='api_lead_update_detail'),


    path('associates/dashboard/', api.FreelancerDashboardAPIView.as_view(), name='api-freelancer-dashboard'),
    path('api/add-sell-freelancer/<int:id>/', api.AddSellPlotAPIView.as_view(), name='api_add_sell_freelancer'),
        #EXTRAAAA
    path('api/dashboard/team-leader/', api.get_team_leader_dashboard_api, name='api_team_leader_dashboard'),

        #LEADS REPORT
    path('api/team-customer/<str:tag>/', api.TeamCustomerLeadsAPIView.as_view(), name='api_team_customer_leads'), 
    path('api/export/staff-leads/', api.ExportLeadsStatusWiseAPIView.as_view(), name='api_export_leads'),
    path('api/leads/visit/', api.VisitLeadsAPIView.as_view(), name='api_visit_leads'),

        #project
    path('api/projects/', api.ProjectListCreateAPIView.as_view(), name='api_project_list_create'),
    path('api/superuser/project/edit/<int:id>/', api.ProjectEditAPIView.as_view(), name='api_superuser_project_edit'),

    path('api/activitylogs/', api.ActivityLogsAPIView.as_view(), name='api_activity_logs'),


    #team leader dashbord supeuserside
    path('api/superuser/team-leader-dashboard/', api.SuperUserTeamLeaderDashboardAPIView.as_view(), name='api_superuser_team_leader_dashboard'),

    # for staff dashbord  
    path('api/superuser/staff-report/', api.SuperUserStaffReportAPIView.as_view(), name='api_superuser_staff_report'),

            #ADMIN DASHBOARD
    path('api/admin/team-leader-report/', api.AdminTeamLeaderReportAPIView.as_view(), name='api_admin_team_leader_report'),
    path('api/admin/add-team-leader/', api.TeamLeaderAddAPIView.as_view(), name='api_admin_add_team_leader'),
  

    # 1. Superuser waali line
    path('api/superuser/staff-leads/<str:tag>/', api.SuperUserStaffLeadsAPIView.as_view(), name='api-superuser-staff-leads'),
    
    # 2. Admin waali cards  line ke liye 
    path('api/admin/staff-leads/<str:tag>/', api.AdminStaffLeadsAPIView.as_view(), name='api-admin-staff-leads'),

    path('api/admin/staff-report/', api.StaffReportAPIView.as_view(), name='api_admin_staff_report'),
    path('api/admin/add-staff/', api.AdminStaffAddAPIView.as_view(), name='api_admin_add_staff'),
    
    #teamleader superuserside list SUPERUSERDASHBOARD
    path('api/superuser/get-team-leaders/', api.SuperUserTeamLeaderListAPIView.as_view(), name='api_superuser_get_team_leaders'),
    



    #ADMINDASHBOARDAPI 2ND PART


    #edit team leader admin side 
    path('api/admin/team-leader/edit/<int:id>/', api.AdminTeamLeaderEditAPIView.as_view(), name='api_admin_team_leader_edit'),

    #staff edit admin dashboard
    path('api/admin/staff/edit/<int:id>/', api.AdminStaffEditAPIView.as_view(), name='api_admin_staff_edit'),

    #staff incentive
    path('api/admin/staff-incentive/<int:staff_id>/', api.AdminStaffIncentiveAPIView.as_view(), name='api_admin_staff_incentive'),

    #staffearn calender
    path('api/admin/staff-calendar/<int:staff_id>/', api.AdminStaffProductivityCalendarAPIView.as_view(), name='api_admin_staff_calendar'),

    #satff view admin dash board
    path('api/admin/staff-leads/by-staff/<int:id>/<str:tag>/', api.AdminStaffParticularLeadsAPIView.as_view(), name='api_admin_staff_particular_leads'),


    #ADMINDASHBOARDAPI 3rd HARSHITSHARMA
    

    #staff dasboard  
    path('api/staff/dashboard/', api.StaffDashboardAPIView.as_view(), name='api_staff_dashboard'),

    #add new  lead
    path('api/staff/add-self-lead/', api.StaffAddSelfLeadAPIView.as_view(), name='api_staff_add_self_lead'),

    # change status
    path('api/staff/update-lead/<int:id>/', api.StaffUpdateLeadAPIView.as_view(), name='api_staff_update_lead'),

    # project select 
    path('api/staff/update-lead-project/', api.UpdateLeadProjectAPIView.as_view(), name='api_staff_update_lead_project'),

    #interseted, today, tomoorow, pending followups
    path('api/staff/interested-leads/<str:tag>/', api.StaffInterestedLeadsAPIView.as_view(), name='api_staff_interested_leads'),

    #not interested
    path('api/staff/not-interested-leads/', api.StaffNotInterestedLeadsAPIView.as_view(), name='api_staff_not_interested_leads'),



    














   ]   

