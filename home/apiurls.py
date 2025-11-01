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

    path('associates/dashboard/', api.FreelancerDashboardAPIView.as_view(), name='api-freelancer-dashboard'),

    path('users/it-staff/', api.ITStaffListAPIView.as_view(), name='api-it-staff-list'),
    path('attendance/<int:id>/', api.AttendanceCalendarAPIView.as_view(), name='api-attendance-calendar'),
    path('productivity/staff/', api.StaffProductivityAPIView.as_view(), name='api-staff-productivity'),
    path('productivity/team-leader/', api.TeamLeaderProductivityAPIView.as_view(), name='api-teamleader-productivity'),


    path('users/admin/add/', api.AdminAddAPIView.as_view(), name='api-admin-add'),
    path('users/admin/edit/<int:id>/', api.AdminEditAPIView.as_view(), name='api-admin-edit'),
    path('leads/customer/<str:tag>/', api.TeamCustomerLeadsAPIView.as_view(), name='api-team-customer-leads'),
    path('users/toggle-active/', api.ToggleUserActiveAPIView.as_view(), name='api-toggle-user-active'),









]   
