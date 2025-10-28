from django.db import models



class Properties(models.Model):
    user_id = models.BigIntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    transaction_type = models.IntegerField(blank=True, null=True)
    subcategory = models.IntegerField(blank=True, null=True)
    subcategory_type = models.CharField(max_length=100, blank=True, null=True)
    property_title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    usp_of_property = models.TextField(blank=True, null=True)
    do_you_offer = models.IntegerField(blank=True, null=True)
    offer_description = models.TextField(blank=True, null=True)
    offer_valid_date = models.CharField(max_length=250, blank=True, null=True)
    offer_price_prefix = models.CharField(max_length=250, blank=True, null=True)
    offer_price = models.FloatField(blank=True, null=True)
    offer_price_postfix = models.CharField(max_length=250, blank=True, null=True)
    offer_image = models.CharField(max_length=250, blank=True, null=True)
    amenities = models.CharField(max_length=250, blank=True, null=True)
    other_amenities = models.TextField(blank=True, null=True)
    water_source = models.CharField(max_length=250, blank=True, null=True)
    overlooking = models.CharField(max_length=250, blank=True, null=True)
    power_backup = models.CharField(max_length=250, blank=True, null=True)
    property_facing = models.CharField(max_length=250, blank=True, null=True)
    width_road = models.CharField(max_length=250, blank=True, null=True)
    width_area = models.IntegerField(blank=True, null=True)
    width_road_postfix = models.IntegerField(blank=True, null=True)
    flooring = models.BigIntegerField(blank=True, null=True)
    furnishing = models.CharField(max_length=250, blank=True, null=True)
    light = models.CharField(max_length=250, blank=True, null=True)
    fan = models.CharField(max_length=250, blank=True, null=True)
    ac = models.CharField(max_length=250, blank=True, null=True)
    tv = models.CharField(max_length=250, blank=True, null=True)
    bed = models.CharField(max_length=250, blank=True, null=True)
    wardrobe = models.CharField(max_length=250, blank=True, null=True)
    geyser = models.CharField(max_length=250, blank=True, null=True)
    furnishing_checkbox = models.CharField(max_length=250, blank=True, null=True)
    # property_type = models.SmallIntegerField(db_comment='1=Featured ,2=Recomend\t')
    affiliate_plan_id = models.IntegerField(blank=True, null=True)
    affiliate_plan_type = models.CharField(max_length=6, blank=True, null=True)
    property_upload_id = models.CharField(max_length=36, blank=True, null=True)
    # status = models.SmallIntegerField(db_comment='1=Active ,0=Inactive')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'properties'


class PropertiesOld(models.Model):
    user_id = models.BigIntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    transaction_type = models.IntegerField(blank=True, null=True)
    subcategory = models.IntegerField(blank=True, null=True)
    subcategory_type = models.CharField(max_length=100, blank=True, null=True)
    property_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    maintenance_charges = models.CharField(max_length=250, blank=True, null=True)
    offer_description = models.CharField(max_length=250, blank=True, null=True)
    offer_valid_date = models.CharField(max_length=250, blank=True, null=True)
    offer_price_prefix = models.CharField(max_length=250, blank=True, null=True)
    offer_price = models.CharField(max_length=250, blank=True, null=True)
    offer_price_postfix = models.CharField(max_length=250, blank=True, null=True)
    offer_image = models.CharField(max_length=250, blank=True, null=True)
    usp_of_property = models.CharField(max_length=250, blank=True, null=True)
    amenities = models.CharField(max_length=250, blank=True, null=True)
    other_amenities = models.TextField(blank=True, null=True)
    # status = models.SmallIntegerField(db_comment='1=Active ,0=Inactive')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'properties_old'


class PropertyApprovedByAdmins(models.Model):
    property_id = models.CharField(max_length=255, db_collation='utf8mb3_general_ci')
    user_id = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)
    # status = models.SmallIntegerField(blank=True, null=True, db_comment='0=Pending, 1=Approved, 2=Disapproved')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_approved_by_admins'


class PropertyDetails(models.Model):
    property_id = models.CharField(max_length=36)
    property_type = models.TextField(blank=True, null=True)
    type_category = models.CharField(max_length=250, blank=True, null=True)
    configuration = models.CharField(max_length=250, blank=True, null=True)
    area = models.CharField(max_length=250, blank=True, null=True)
    area_postfix = models.CharField(max_length=250, blank=True, null=True)
    room_type = models.CharField(max_length=250, blank=True, null=True)
    no_of_bed = models.CharField(max_length=250, blank=True, null=True)
    no_bed_others = models.CharField(max_length=250, blank=True, null=True)
    total_no_of_beds = models.CharField(max_length=250, blank=True, null=True)
    total_no_beds_others = models.CharField(max_length=250, blank=True, null=True)
    no_of_rooms = models.CharField(max_length=250, blank=True, null=True)
    no_rooms_others = models.CharField(max_length=250, blank=True, null=True)
    carpet_area = models.CharField(max_length=250, blank=True, null=True)
    carpet_area_postfix = models.IntegerField(blank=True, null=True)
    built_up_area = models.CharField(max_length=250, blank=True, null=True)
    built_area_postfix = models.IntegerField(blank=True, null=True)
    super_built_up_area = models.CharField(max_length=250, blank=True, null=True)
    super_built_area_postfix = models.IntegerField(blank=True, null=True)
    bathroom_type = models.CharField(max_length=250, blank=True, null=True)
    restroom_type = models.CharField(max_length=250, blank=True, null=True)
    available_from = models.CharField(max_length=250, blank=True, null=True)
    willing_to_rent = models.CharField(max_length=250, blank=True, null=True)
    duration_agreement = models.CharField(max_length=250, blank=True, null=True)
    month_notice = models.CharField(max_length=250, blank=True, null=True)
    availability = models.CharField(max_length=250, blank=True, null=True)
    age_property = models.CharField(max_length=250, blank=True, null=True)
    expected_by = models.CharField(max_length=250, blank=True, null=True)
    selected_month = models.CharField(max_length=250, blank=True, null=True)
    best_suitable = models.CharField(max_length=250, blank=True, null=True)
    available_for = models.CharField(max_length=250, blank=True, null=True)
    oc_received = models.CharField(max_length=250, blank=True, null=True)
    on_rent = models.TextField(blank=True, null=True)
    construction_type = models.CharField(max_length=250, blank=True, null=True)
    ownership_type = models.CharField(max_length=250, blank=True, null=True)
    no_of_floors = models.CharField(max_length=250, blank=True, null=True)
    food_available = models.CharField(max_length=250, blank=True, null=True)
    food_charges = models.CharField(max_length=250, blank=True, null=True)
    food_charge_prefix = models.CharField(max_length=250, blank=True, null=True)
    add_food_charge = models.CharField(max_length=250, blank=True, null=True)
    rera_register = models.CharField(max_length=250, blank=True, null=True)
    add_rera_no = models.CharField(max_length=250, blank=True, null=True)
    add_rera_link = models.CharField(max_length=250, blank=True, null=True)
    no_master_bedroom = models.CharField(max_length=250, blank=True, null=True)
    no_master_bedroom_others = models.CharField(max_length=250, blank=True, null=True)
    no_common_bedroom = models.CharField(max_length=250, blank=True, null=True)
    no_common_bedroom_others = models.CharField(max_length=250, blank=True, null=True)
    no_master_bathroom = models.CharField(max_length=250, blank=True, null=True)
    no_master_bathroom_others = models.CharField(max_length=250, blank=True, null=True)
    no_common_bathroom = models.CharField(max_length=250, blank=True, null=True)
    no_common_bathroom_others = models.CharField(max_length=250, blank=True, null=True)
    no_balcony = models.CharField(max_length=250, blank=True, null=True)
    no_balcony_others = models.CharField(max_length=250, blank=True, null=True)
    na_passed = models.CharField(max_length=250, blank=True, null=True)
    expected_price_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_price = models.FloatField(blank=True, null=True)
    expected_rent_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_rent = models.FloatField(blank=True, null=True)
    expected_rent_postfix = models.CharField(max_length=250, blank=True, null=True)
    expected_deposit_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_deposit = models.FloatField(blank=True, null=True)
    expected_heavy_deposit_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_heavy_deposit = models.CharField(max_length=250, blank=True, null=True)
    price_square_prefix = models.CharField(max_length=250, blank=True, null=True)
    price_square = models.CharField(max_length=250, blank=True, null=True)
    maintenance_charges_prefix = models.IntegerField(blank=True, null=True)
    maintenance_charges = models.CharField(max_length=250, blank=True, null=True)
    maintenance_charges_postfix = models.CharField(max_length=250, blank=True, null=True)
    membership_charges_prefix = models.IntegerField(blank=True, null=True)
    membership_charges = models.FloatField(blank=True, null=True)
    annual_dues_prefix = models.CharField(max_length=250, blank=True, null=True)
    annual_dues = models.FloatField(blank=True, null=True)
    expected_rental_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_rental = models.FloatField(blank=True, null=True)
    price_negotiable = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_details'


class PropertyEnquiries(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    property_id = models.CharField(max_length=36)
    name = models.TextField()
    phone = models.BigIntegerField()
    email = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'property_enquiries'


class PropertyFloorPlans(models.Model):
    property_id = models.CharField(max_length=36)
    title_site = models.CharField(max_length=250, blank=True, null=True)
    image_site = models.CharField(max_length=250, blank=True, null=True)
    title_floor = models.CharField(max_length=250, blank=True, null=True)
    image_floor = models.CharField(max_length=250, blank=True, null=True)
    image_all_floor_plan = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    image_plans = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_floor_plans'


class PropertyListingEnquiries(models.Model):
    user_id = models.CharField(max_length=255, blank=True, null=True)
    property_id = models.CharField(max_length=255, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    is_agent = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    mobile = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    when_plan = models.IntegerField(blank=True, null=True)
    interested_in = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_listing_enquiries'


class PropertyLocalities(models.Model):
    property_id = models.CharField(max_length=36)
    nearby_highways = models.TextField(blank=True, null=True)
    nearby_railway = models.TextField(blank=True, null=True)
    nearby_metro = models.TextField(blank=True, null=True)
    nearby_mono = models.TextField(blank=True, null=True)
    nearby_airport = models.TextField(blank=True, null=True)
    nearby_bus_station = models.TextField(blank=True, null=True)
    nearby_hospital = models.TextField(blank=True, null=True)
    nearby_clinic = models.TextField(blank=True, null=True)
    nearby_playgroup = models.TextField(blank=True, null=True)
    nearby_school = models.TextField(blank=True, null=True)
    nearby_college = models.TextField(blank=True, null=True)
    nearby_qsr = models.TextField(blank=True, null=True)
    nearby_cafe = models.TextField(blank=True, null=True)
    nearby_grocery = models.TextField(blank=True, null=True)
    nearby_restaurant = models.TextField(blank=True, null=True)
    nearby_business_hub = models.TextField(blank=True, null=True)
    nearby_office_center = models.TextField(blank=True, null=True)
    nearby_place_visit = models.TextField(blank=True, null=True)
    nearby_mall = models.TextField(blank=True, null=True)
    nearby_theater = models.TextField(blank=True, null=True)
    nearby_gym = models.TextField(blank=True, null=True)
    nearby_yoga = models.TextField(blank=True, null=True)
    nearby_zumba = models.TextField(blank=True, null=True)
    nearby_beauty_salon = models.TextField(blank=True, null=True)
    nearby_spa = models.TextField(blank=True, null=True)
    nearby_car_repair = models.TextField(blank=True, null=True)
    nearby_laundry = models.TextField(blank=True, null=True)
    nearby_gas_station = models.TextField(blank=True, null=True)
    nearby_pathology = models.TextField(blank=True, null=True)
    nearby_atm = models.TextField(blank=True, null=True)
    nearby_bank = models.TextField(blank=True, null=True)
    nearby_temple = models.TextField(blank=True, null=True)
    nearby_mosque = models.TextField(blank=True, null=True)
    nearby_church = models.TextField(blank=True, null=True)
    nearby_night_club = models.TextField(blank=True, null=True)
    nearby_pub = models.TextField(blank=True, null=True)
    nearby_lounge = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_localities'


class PropertyLocations(models.Model):
    property_id = models.CharField(max_length=36)
    property_title = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    country_id = models.CharField(max_length=100, blank=True, null=True)
    country_name = models.CharField(max_length=250, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=250, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    city_name = models.CharField(max_length=250, blank=True, null=True)
    district_name = models.TextField(blank=True, null=True)
    society_building = models.CharField(max_length=250, blank=True, null=True)
    flat_apartment = models.CharField(max_length=250, blank=True, null=True)
    shop_office = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    plot_survey = models.CharField(max_length=250, blank=True, null=True)
    landmark = models.CharField(max_length=250, blank=True, null=True)
    map_location = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_locations'


class PropertyMedia(models.Model):
    property_id = models.CharField(max_length=36)
    property_room_type_id = models.CharField(max_length=36, blank=True, null=True)
    file_path = models.CharField(max_length=250, blank=True, null=True)
    cover_photo = models.TextField(blank=True, null=True)
    image_size_610_510 = models.TextField(blank=True, null=True)
    image_size_370_240 = models.TextField(blank=True, null=True)
    image_size_270_250 = models.TextField(blank=True, null=True)
    # media_type = models.IntegerField(blank=True, null=True, db_comment='1 = indoor, 2 = outdoor, 3=amenities , 4= outside_view ,5=land, 6= All Image, 7=Affiliate Marketing, 8 =Advertising')
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_media'


class PropertyParkings(models.Model):
    property_id = models.CharField(max_length=36)
    open_parking = models.CharField(max_length=250, blank=True, null=True)
    reserved_parking = models.CharField(max_length=250, blank=True, null=True)
    parking_structure = models.CharField(max_length=250, blank=True, null=True)
    additional_dropdown = models.CharField(max_length=250, blank=True, null=True)
    total_park = models.CharField(max_length=250, blank=True, null=True)
    no_floor = models.CharField(max_length=250, blank=True, null=True)
    guest_parking = models.CharField(max_length=250, blank=True, null=True)
    parking_structure_guest = models.CharField(max_length=250, blank=True, null=True)
    additional_dropdown_guest = models.CharField(max_length=250, blank=True, null=True)
    total_park_guest = models.CharField(max_length=250, blank=True, null=True)
    no_floor_guest = models.CharField(max_length=250, blank=True, null=True)
    type_of_guest_park = models.CharField(max_length=250, blank=True, null=True)
    free_in_time = models.CharField(max_length=250, blank=True, null=True)
    free_out_time = models.CharField(max_length=250, blank=True, null=True)
    free_charge_prefix_time = models.CharField(max_length=250, blank=True, null=True)
    free_charge_time = models.CharField(max_length=250, blank=True, null=True)
    free_charge_postfix_time = models.CharField(max_length=250, blank=True, null=True)
    free_usage_hrs = models.CharField(max_length=250, blank=True, null=True)
    add_hours = models.CharField(max_length=250, blank=True, null=True)
    free_charge_prefix_hrs = models.CharField(max_length=250, blank=True, null=True)
    free_charge_hrs = models.FloatField(blank=True, null=True)
    free_charge_postfix_hrs = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_parkings'


class PropertyRoomTypes(models.Model):
    property_id = models.CharField(max_length=36)
    room_type_id = models.CharField(max_length=11, blank=True, null=True)
    no_of_rooms_title = models.CharField(max_length=250, blank=True, null=True)
    size_of_room = models.CharField(max_length=250, blank=True, null=True)
    room_title = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_room_types'


class PropertyStructureTypes(models.Model):
    property_id = models.CharField(max_length=36)
    no_of_tower = models.CharField(max_length=250, blank=True, null=True)
    no_of_tower_others = models.CharField(max_length=250, blank=True, null=True)
    no_of_wings = models.CharField(max_length=250, blank=True, null=True)
    no_of_wings_others = models.CharField(max_length=250, blank=True, null=True)
    total_floor_structure = models.CharField(max_length=250, blank=True, null=True)
    no_floor_structure = models.CharField(max_length=250, blank=True, null=True)
    no_of_flats = models.CharField(max_length=250, blank=True, null=True)
    no_of_flats_others = models.CharField(max_length=250, blank=True, null=True)
    no_of_property = models.CharField(max_length=250, blank=True, null=True)
    no_of_property_others = models.CharField(max_length=250, blank=True, null=True)
    no_of_elevator = models.CharField(max_length=250, blank=True, null=True)
    no_of_elevator_others = models.CharField(max_length=250, blank=True, null=True)
    no_of_staircase = models.CharField(max_length=250, blank=True, null=True)
    no_of_staircase_others = models.CharField(max_length=250, blank=True, null=True)
    no_of_refugee_flat = models.CharField(max_length=250, blank=True, null=True)
    no_of_refugee_flat_others = models.CharField(max_length=250, blank=True, null=True)
    no_of_refugee_property = models.CharField(max_length=250, blank=True, null=True)
    no_of_refugee_property_others = models.CharField(max_length=250, blank=True, null=True)
    nearest_refugee_flat = models.CharField(max_length=250, blank=True, null=True)
    nearest_refugee_property = models.CharField(max_length=250, blank=True, null=True)
    land_type = models.CharField(max_length=250, blank=True, null=True)
    fencing = models.CharField(max_length=250, blank=True, null=True)
    no_elevator_property = models.CharField(max_length=250, blank=True, null=True)
    no_elevator_property_others = models.CharField(max_length=250, blank=True, null=True)
    no_stair_property = models.CharField(max_length=250, blank=True, null=True)
    no_stair_property_others = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_structure_types'


class PropertyUploadLogs(models.Model):
    user_id = models.IntegerField()
    action_by = models.IntegerField(blank=True, null=True)
    order_id = models.CharField(max_length=36)
    property_id = models.CharField(max_length=36)
    media_file = models.CharField(max_length=150)
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_upload_logs'


class PropertyUploads(models.Model):
    user_id = models.IntegerField()
    order_id = models.CharField(max_length=36)
    property_id = models.CharField(max_length=36)
    media_file = models.CharField(max_length=150)
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_uploads'


# location for properties

class Localities(models.Model):
    property_id = models.CharField(max_length=36)
    nearby_highways = models.CharField(max_length=250, blank=True, null=True)
    nearby_railway = models.CharField(max_length=250, blank=True, null=True)
    nearby_metro = models.CharField(max_length=250, blank=True, null=True)
    nearby_mono = models.CharField(max_length=250, blank=True, null=True)
    nearby_airport = models.CharField(max_length=250, blank=True, null=True)
    nearby_bus_station = models.CharField(max_length=250, blank=True, null=True)
    nearby_hospital = models.CharField(max_length=250, blank=True, null=True)
    nearby_clinic = models.CharField(max_length=250, blank=True, null=True)
    nearby_playgroup = models.CharField(max_length=250, blank=True, null=True)
    nearby_school = models.CharField(max_length=250, blank=True, null=True)
    nearby_college = models.CharField(max_length=250, blank=True, null=True)
    nearby_qsr = models.CharField(max_length=250, blank=True, null=True)
    nearby_cafe = models.CharField(max_length=250, blank=True, null=True)
    nearby_grocery = models.CharField(max_length=250, blank=True, null=True)
    nearby_restaurant = models.CharField(max_length=250, blank=True, null=True)
    nearby_business_hub = models.CharField(max_length=250, blank=True, null=True)
    nearby_office_center = models.CharField(max_length=250, blank=True, null=True)
    nearby_place_visit = models.CharField(max_length=250, blank=True, null=True)
    nearby_mall = models.CharField(max_length=250, blank=True, null=True)
    nearby_theater = models.CharField(max_length=250, blank=True, null=True)
    nearby_gym = models.CharField(max_length=250, blank=True, null=True)
    nearby_yoga = models.CharField(max_length=250, blank=True, null=True)
    nearby_zumba = models.CharField(max_length=250, blank=True, null=True)
    nearby_beauty_salon = models.CharField(max_length=250, blank=True, null=True)
    nearby_spa = models.CharField(max_length=250, blank=True, null=True)
    nearby_car_repair = models.CharField(max_length=250, blank=True, null=True)
    nearby_laundry = models.CharField(max_length=250, blank=True, null=True)
    nearby_gas_station = models.CharField(max_length=250, blank=True, null=True)
    nearby_pathology = models.CharField(max_length=250, blank=True, null=True)
    nearby_atm = models.CharField(max_length=250, blank=True, null=True)
    nearby_bank = models.CharField(max_length=250, blank=True, null=True)
    nearby_temple = models.CharField(max_length=250, blank=True, null=True)
    nearby_mosque = models.CharField(max_length=250, blank=True, null=True)
    nearby_church = models.CharField(max_length=250, blank=True, null=True)
    nearby_night_club = models.CharField(max_length=250, blank=True, null=True)
    nearby_pub = models.CharField(max_length=250, blank=True, null=True)
    nearby_lounge = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localities'


class LocalityClinics(models.Model):
    property_id = models.CharField(max_length=36)
    nearby_clinic = models.CharField(max_length=250, blank=True, null=True)
    map_clinic = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    specialist_clinic = models.CharField(max_length=250, blank=True, null=True)
    add_specialist_clinic = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locality_clinics'


class LocalityColleges(models.Model):
    property_id = models.CharField(max_length=36)
    nearby_college = models.CharField(max_length=250, blank=True, null=True)
    map_college = models.CharField(max_length=250, blank=True, null=True)
    stream_college = models.CharField(max_length=250, blank=True, null=True)
    stream_college_type = models.CharField(max_length=250, blank=True, null=True)
    board_college = models.CharField(max_length=250, blank=True, null=True)
    board_college_type = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locality_colleges'


class LocalityHospitals(models.Model):
    property_id = models.CharField(max_length=36)
    nearby_hospital = models.CharField(max_length=250, blank=True, null=True)
    map_hospital = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.CharField(max_length=250, blank=True, null=True)
    longitude = models.CharField(max_length=250, blank=True, null=True)
    specialist_hospital = models.CharField(max_length=250, blank=True, null=True)
    add_specialist_hospital = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locality_hospitals'


class LocalitySchools(models.Model):
    property_id = models.CharField(max_length=36)
    nearby_school = models.CharField(max_length=250, blank=True, null=True)
    map_school = models.CharField(max_length=250, blank=True, null=True)
    stream_school = models.CharField(max_length=250, blank=True, null=True)
    stream_school_type = models.CharField(max_length=250, blank=True, null=True)
    board_school = models.CharField(max_length=250, blank=True, null=True)
    board_school_type = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locality_schools'


class Locations(models.Model):
    property_id = models.CharField(max_length=36)
    address = models.CharField(max_length=250, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=250, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    city_name = models.CharField(max_length=11, blank=True, null=True)
    landmark = models.CharField(max_length=250, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    country_id = models.CharField(max_length=100, blank=True, null=True)
    country_name = models.CharField(max_length=250, blank=True, null=True)
    map_location = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'


class Media(models.Model):
    property_id = models.CharField(max_length=36)
    property_room_type_id = models.CharField(max_length=36, blank=True, null=True)
    file_path = models.CharField(max_length=250, blank=True, null=True)
    # media_type = models.IntegerField(blank=True, null=True, db_comment='1 = indoor, 2 = outdoor, 3=amenities , 4= outside_view ,5=land')
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media'


class FavouriteProperties(models.Model):
    property_id = models.CharField(max_length=36)
    user_id = models.IntegerField(blank=True, null=True)
    is_favourite = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favourite_properties'
