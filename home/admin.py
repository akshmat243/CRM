from django.contrib import admin

# Register your models here.
# from .models import LeadUser
from .models import *
import openpyxl
from django.http import HttpResponse



# @admin.register(LeadUser)
# class LeadUserAdmin(admin.ModelAdmin):
#     list_display = ('name','email', 'call', 'send', 'status')
@admin.register(LeadUser)
class LeadUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'call', 'send', 'status', 'assigned_to', 'created_date','updated_date')
    list_filter =['assigned_to', 'status', 'team_leader',]
    search_fields = ('name', 'call', 'created_date',)
    list_per_page = 100

    actions = ['download_interested_leads']

    def download_interested_leads(self, request, queryset):
        # Filter leads with status "Interested"
        interested_leads = queryset.filter(status='Intrested')

        # Create an Excel workbook and sheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Interested Leads"

        # Write the header row
        headers = ['Name', 'Phone', 'Staff Name', 'Status',]
        ws.append(headers)

        # Write data rows
        for lead in interested_leads:
            ws.append([
                lead.name,
                # lead.email,
                lead.call,
                lead.assigned_to.name if lead.assigned_to else '',
                # lead.team_leader.name if lead.team_leader else '',
                lead.status,
                # lead.created_date.strftime('%Y-%m-%d %H:%M:%S'),
                # lead.updated_date.strftime('%Y-%m-%d %H:%M:%S')
            ])

        # Prepare the response to download the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=interested_leads.xlsx'
        wb.save(response)
        return response

    download_interested_leads.short_description = "Download Interested Leads"
    
# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display= ('name', 'phone','email','last_login','action')

class AllUser(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'is_admin', 'is_team_leader', 'is_staff_new', 'login_time', 'logout_time', 'created_date','updated_date']
    search_fields = ('name',)
    
class AdminUser(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'admin_id', 'created_date', 'updated_date']
    search_fields = ('user',)
    list_filter =['user',]

class Team_LeaderUser(admin.ModelAdmin):
    list_display = ['name', 'admin','email', 'team_leader_id', 'created_date','updated_date']
    search_fields = ('name', 'call', 'created_date',)
    list_filter =['admin',]

@admin.register(Team_LeadData)
class Team_LeadData(admin.ModelAdmin):
    search_fields = ('name', 'call', 'created_date',)
    list_display = ('name', 'email', 'call', 'send', 'status','assigned_to', 'created_date','updated_date')
    list_filter =['assigned_to', 'status', 'team_leader',]
    list_per_page = 500

@admin.register(Leads_history)
class Leads_history(admin.ModelAdmin):
    search_fields = ('name', 'status',)
    list_display = ('name', 'status',)
    list_filter =['status',]

@admin.register(Slab)
class Slab(admin.ModelAdmin):
    search_fields = ('amount',)
    list_display = ('start_value', 'end_value', 'amount')

@admin.register(Sell_plot)
class Sell_plot(admin.ModelAdmin):
    search_fields = ('size_in_gaj',)
    list_display = ('size_in_gaj', 'plot_no', 'earn_amount')

@admin.register(Project)
class Project(admin.ModelAdmin):
    list_display = ('name', 'created_date','updated_date')
    list_filter =['name',]

class StaffUser(admin.ModelAdmin):
    list_display = ['name','team_leader', 'email', 'staff_id', 'created_date','updated_date']
    search_fields = ('name',)
    list_filter =['team_leader',]
# class AssignedUser(admin.ModelAdmin):
#     list_display = ['assigned_to']
    # search_fields = ('name',)

@admin.register(ActivityLog)
class ActivityLog(admin.ModelAdmin):
    list_display = ['name','team_leader', 'email', 'user_type', 'created_date','updated_date']
    search_fields = ('name',)
    list_filter =['team_leader', 'user_type',]

@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ['user','task_date', 'created_date',]
    search_fields = ('user','task_date', 'created_date',)
    list_filter =['user',]

@admin.register(Attendance)
class Attendance(admin.ModelAdmin):
    list_display = ['user','date', 'is_present',]
    search_fields = ('user','date', 'is_present',)
    readonly_fields = ('created_date', 'updated_date')
    list_filter =['user',]
    
    
admin.site.register(User, AllUser)
admin.site.register(Admin, AdminUser)
admin.site.register(Team_Leader, Team_LeaderUser)
admin.site.register(Staff, StaffUser)
# admin.site.register(ActivityLog)
admin.site.register(Marketing)
admin.site.register(Settings)
# admin.site.register(Assigned, AssignedUser)

