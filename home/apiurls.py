from django.urls import path
from .api import *
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


] 
