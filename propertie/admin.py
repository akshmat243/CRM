from django.contrib import admin
from .models import *

@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'property_title', 'created_at', 'updated_at']
    search_fields = ['property_title', 'user_id']
    list_filter = [ 'created_at']

@admin.register(PropertiesOld)
class PropertiesOldAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'property_title', 'created_at', 'updated_at']
    search_fields = ['property_title', 'user_id']
    list_filter = [ 'created_at']

@admin.register(PropertyApprovedByAdmins)
class PropertyApprovedByAdminsAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'user_id', 'created_at']
    search_fields = ['property_id', 'user_id']
    list_filter = [ 'created_at']

@admin.register(PropertyDetails)
class PropertyDetailsAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'property_type', 'configuration', 'created_at', 'updated_at']
    search_fields = ['property_id', 'property_type']
    list_filter = ['created_at']

@admin.register(PropertyEnquiries)
class PropertyEnquiriesAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'sender_id', 'receiver_id', 'status', 'created_at']
    search_fields = ['property_id', 'sender_id']
    list_filter = ['status', 'created_at']

@admin.register(PropertyFloorPlans)
class PropertyFloorPlansAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'title_site', 'title_floor', 'created_at', 'updated_at']
    search_fields = ['property_id', 'title_site']
    list_filter = ['created_at']

@admin.register(PropertyListingEnquiries)
class PropertyListingEnquiriesAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'property_id', 'is_agent', 'when_plan']
    search_fields = ['user_id', 'property_id']
    list_filter = ['is_agent', 'when_plan']

@admin.register(PropertyLocalities)
class PropertyLocalitiesAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'nearby_highways', 'nearby_hospital', 'nearby_school', 'updated_at')
    search_fields = ('property_id', 'nearby_highways', 'nearby_hospital')


@admin.register(PropertyLocations)
class PropertyLocationsAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'property_title', 'pincode', 'city_name', 'state_name', 'country_name', 'updated_at')
    search_fields = ('property_id', 'property_title', 'pincode', 'city_name', 'state_name', 'country_name')


@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'file_path', 'created_at')
    search_fields = ('property_id', 'media_type')


@admin.register(PropertyParkings)
class PropertyParkingsAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'open_parking', 'reserved_parking', 'total_park', 'updated_at')
    search_fields = ('property_id', 'open_parking', 'reserved_parking')


@admin.register(PropertyRoomTypes)
class PropertyRoomTypesAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'room_type_id', 'no_of_rooms_title', 'size_of_room', 'updated_at')
    search_fields = ('property_id', 'room_type_id')


@admin.register(PropertyStructureTypes)
class PropertyStructureTypesAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'no_of_tower', 'no_of_wings', 'total_floor_structure', 'updated_at')
    search_fields = ('property_id', 'no_of_tower', 'no_of_wings')


@admin.register(PropertyUploadLogs)
class PropertyUploadLogsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'property_id', 'status', 'created_at', 'updated_at')
    search_fields = ('user_id', 'property_id', 'status')


@admin.register(PropertyUploads)
class PropertyUploadsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'property_id', 'status', 'created_at', 'updated_at')
    search_fields = ('user_id', 'property_id', 'status')


@admin.register(Localities)
class LocalitiesAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'nearby_highways', 'nearby_hospital', 'nearby_school', 'updated_at')
    search_fields = ('property_id', 'nearby_highways', 'nearby_hospital')

@admin.register(LocalityClinics)
class LocalityClinicsAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'nearby_clinic', 'latitude', 'longitude', 'specialist_clinic', 'updated_at')
    search_fields = ('property_id', 'nearby_clinic', 'specialist_clinic')


@admin.register(LocalityColleges)
class LocalityCollegesAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'nearby_college', 'stream_college', 'board_college', 'updated_at')
    search_fields = ('property_id', 'nearby_college', 'stream_college', 'board_college')


@admin.register(LocalityHospitals)
class LocalityHospitalsAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'nearby_hospital', 'latitude', 'longitude', 'specialist_hospital', 'updated_at')
    search_fields = ('property_id', 'nearby_hospital', 'specialist_hospital')


@admin.register(LocalitySchools)
class LocalitySchoolsAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'nearby_school', 'stream_school', 'board_school', 'updated_at')
    search_fields = ('property_id', 'nearby_school', 'stream_school', 'board_school')


@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'address', 'city_name', 'state_name', 'pincode', 'country_name', 'updated_at')
    search_fields = ('property_id', 'address', 'city_name', 'state_name', 'pincode')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'file_path', 'type', 'updated_at')
    search_fields = ('property_id', 'media_type', 'type')


@admin.register(FavouriteProperties)
class FavouritePropertiesAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'user_id', 'is_favourite', 'updated_at')
    search_fields = ('property_id', 'user_id')