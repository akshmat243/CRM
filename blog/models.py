# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AddFloorPlans(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    property_id = models.CharField(max_length=36)
    title = models.CharField(max_length=100, blank=True, null=True)
    image_plan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'add_floor_plans'


class AdminRoleCreations(models.Model):
    role_name = models.TextField()
    role_type = models.IntegerField()
    permission_ids = models.TextField(blank=True, null=True)
    department_id = models.IntegerField()
    batch_level = models.IntegerField()
    batch_role_limit = models.BigIntegerField()
    status = models.IntegerField(db_comment='1 = Active, 2 = Inactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_role_creations'


class Advertisements(models.Model):
    id = models.CharField(max_length=36)
    user_id = models.CharField(max_length=255)
    blog_category_id = models.CharField(max_length=50)
    blog_sub_category_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    media = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'advertisements'


class AffiliatePartnerRequests(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    no_of_requests = models.BigIntegerField(blank=True, null=True)
    status = models.IntegerField(db_comment='1 = Pending, 2 = Approve, 3 = Disapprove')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affiliate_partner_requests'


class AffiliatePlanRentals(models.Model):
    plan_type_id = models.IntegerField()
    plan_name = models.CharField(max_length=100)
    expected_rent_range = models.IntegerField(blank=True, null=True)
    price_range_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_range_to = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    no_of_listing = models.IntegerField(blank=True, null=True)
    open_transaction = models.IntegerField(blank=True, null=True)
    rental_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cancellation_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit_deductable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=8, db_comment='active,inactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affiliate_plan_rentals'


class AffiliatePlanResales(models.Model):
    plan_type_id = models.IntegerField()
    plan_name = models.CharField(max_length=100)
    expected_price_range = models.IntegerField(blank=True, null=True)
    price_range_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_range_to = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    no_of_listing = models.IntegerField(blank=True, null=True)
    open_transaction = models.IntegerField(blank=True, null=True)
    resale_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resale_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cancellation_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit_deductable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=8, db_comment='active,inactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affiliate_plan_resales'


class AffiliateRentals(models.Model):
    charges_deduction_day = models.IntegerField(blank=True, null=True)
    earning_visible_day = models.IntegerField(blank=True, null=True)
    earning_release_day = models.IntegerField(blank=True, null=True)
    percentage_of_affiliate_earning = models.IntegerField(blank=True, null=True)
    listing_change = models.IntegerField(blank=True, null=True)
    security_deposit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affiliate_rentals'


class AffiliateResales(models.Model):
    charges_deduction_day = models.IntegerField(blank=True, null=True)
    earning_visible_day = models.IntegerField(blank=True, null=True)
    earning_release_day = models.IntegerField(blank=True, null=True)
    percentage_of_affiliate_earning = models.IntegerField(blank=True, null=True)
    listing_change = models.IntegerField(blank=True, null=True)
    security_deposit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affiliate_resales'


class AffiliateSettings(models.Model):
    validity_for_resale = models.IntegerField(blank=True, null=True)
    validity_for_rental = models.IntegerField(blank=True, null=True)
    validity_for_new_project = models.IntegerField(blank=True, null=True)
    new_percentage_of_affiliate_earning = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affiliate_settings'


class Amenities(models.Model):
    category_ids = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.TextField(blank=True, null=True)
    feature_type = models.SmallIntegerField(blank=True, null=True, db_comment='1=Property Feature, 2=Society/Building Feature, 3=Other Feature')
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'amenities'


class AssignAffiliateProperties(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    property_id = models.CharField(max_length=36)
    plan_id = models.CharField(max_length=36)
    plan_type = models.CharField(max_length=6)
    order_id = models.CharField(max_length=36)
    start_from = models.DateTimeField()
    end_to = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assign_affiliate_properties'


class AssignAffiliatePropertyLogs(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    property_id = models.CharField(max_length=36)
    plan_id = models.CharField(max_length=36)
    plan_type = models.CharField(max_length=6)
    order_id = models.CharField(max_length=36)
    start_from = models.DateTimeField()
    end_to = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assign_affiliate_property_logs'


class Banners(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'banners'


class Batches(models.Model):
    department_id = models.IntegerField()
    batch_number = models.BigIntegerField()
    batch_name = models.TextField()
    batch_timing = models.TimeField()
    delayed_check_in_limit = models.TextField()
    delayed_check_out_limit = models.TextField()
    batch_employee_min_limit = models.BigIntegerField()
    batch_employee_max_limit = models.BigIntegerField()
    status = models.IntegerField(db_comment='1 = Active, 2 = Inactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batches'


class BlogCategories(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    add_product = models.SmallIntegerField(blank=True, null=True, db_comment='0=No, 1=Yes')
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog_categories'


class BlogCategoryLists(models.Model):
    blog_category_name = models.TextField()
    image = models.TextField()
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blog_category_lists'


class Blogs(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    file = models.CharField(max_length=225, blank=True, null=True)
    description_type = models.CharField(max_length=225, blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blogs'


class BlogsDetails(models.Model):
    blog_category_ids = models.CharField(max_length=50)
    homepage = models.CharField(max_length=9, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255)
    image = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blogs_details'


class Boards(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'boards'


class BucketDetails(models.Model):
    user_id = models.IntegerField()
    required_for = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    category_id = models.IntegerField()
    transaction_type = models.IntegerField(blank=True, null=True)
    subcategory = models.IntegerField(blank=True, null=True)
    subcategory_type = models.IntegerField(blank=True, null=True)
    property_detail_type = models.IntegerField(blank=True, null=True)
    configuration = models.IntegerField(blank=True, null=True)
    expected_price_prefix = models.TextField(blank=True, null=True)
    expected_price = models.CharField(max_length=100, blank=True, null=True)
    expected_rent_prefix = models.TextField(blank=True, null=True)
    expected_rent = models.CharField(max_length=100, blank=True, null=True)
    expected_rent_postfix = models.TextField(blank=True, null=True)
    expected_deposit_prefix = models.TextField(blank=True, null=True)
    expected_deposit = models.CharField(max_length=100, blank=True, null=True)
    expected_heavy_deposit_prefix = models.TextField(blank=True, null=True)
    expected_heavy_deposit = models.CharField(max_length=100, blank=True, null=True)
    lock_in_year = models.IntegerField(blank=True, null=True)
    lock_in_month = models.IntegerField(blank=True, null=True)
    pincode = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    society_building = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    specification = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bucket_details'


class BucketManagers(models.Model):
    fetch_out = models.IntegerField(blank=True, null=True)
    earning_visible_day = models.IntegerField(blank=True, null=True)
    earning_release_day = models.IntegerField(blank=True, null=True)
    site_visit = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bucket_managers'


class BucketPlanManagers(models.Model):
    bucket_plan_type_id = models.IntegerField()
    plan_name = models.TextField()
    expected_price_range = models.IntegerField()
    expected_rent_range = models.IntegerField()
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit_deductable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fetch_out_possible = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fetch_out_charges = models.BigIntegerField(blank=True, null=True)
    referral_earning = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=8, db_comment="'active','inactive'")
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bucket_plan_managers'


class BucketPlanTypes(models.Model):
    plan_name = models.CharField(max_length=20)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bucket_plan_types'


class BucketPlans(models.Model):
    plan = models.CharField(max_length=50)
    expected_price_range = models.IntegerField()
    expected_rent_range = models.IntegerField()
    full_limit = models.IntegerField()
    security_deposit = models.IntegerField()
    security_deposit_deductable = models.IntegerField()
    fetch_out_charges = models.IntegerField()
    referral_earning = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bucket_plans'


class BusinessCategories(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'business_categories'


class Carriers(models.Model):
    name = models.TextField()
    phone = models.CharField(max_length=255)
    email = models.TextField()
    cv = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'carriers'


class Carts(models.Model):
    user_id = models.IntegerField()
    plan_type = models.CharField(max_length=6)
    plan_type_id = models.IntegerField()
    plan_id = models.IntegerField()
    expected_range = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carts'


class Categories(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class CategoriesOlds(models.Model):
    name = models.CharField(max_length=255)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories_olds'


class Channels(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    channel_name = models.TextField()
    image = models.TextField(blank=True, null=True)
    image_size_172_171 = models.TextField(blank=True, null=True)
    image_size_210_240 = models.TextField(blank=True, null=True)
    operate = models.IntegerField(blank=True, null=True, db_comment='1 = Online, 2 = Offline, 3 = Both')
    rera = models.IntegerField(blank=True, null=True, db_comment='1 = Yes, 2 = No')
    rera_no_type = models.IntegerField(blank=True, null=True, db_comment='1 = Individual, 2 = Company')
    rera_no = models.TextField(blank=True, null=True)
    rera_name = models.TextField(blank=True, null=True)
    instagram_name = models.TextField(blank=True, null=True)
    youtube_name = models.TextField(blank=True, null=True)
    facebook_name = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    approved_by_admin = models.IntegerField(db_comment='1 = Pending, 2 = Approve, 3 = Disapprove\t')
    status = models.IntegerField(db_comment='1 = Active, 2 = Inactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channels'


class ContentCategories(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'content_categories'


class CourseCategories(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_categories'


class Courses(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    file = models.CharField(max_length=250, blank=True, null=True)
    role = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class Currencies(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    exchange_rate = models.FloatField(blank=True, null=True)
    status = models.IntegerField()
    code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'currencies'


class CustomerReviews(models.Model):
    name = models.TextField()
    role = models.CharField(max_length=255)
    image = models.TextField()
    review = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_reviews'


class Departments(models.Model):
    name = models.TextField()
    status = models.IntegerField(db_comment='1 = Active, 2 = Inactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departments'


class Details(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    property_id = models.CharField(max_length=36)
    configuration = models.CharField(max_length=250, blank=True, null=True)
    area = models.CharField(max_length=250, blank=True, null=True)
    area_postfix = models.CharField(max_length=250, blank=True, null=True)
    personal_cabin = models.CharField(max_length=250, blank=True, null=True)
    expected_rent_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_rent = models.CharField(max_length=250, blank=True, null=True)
    expected_rent_postfix = models.CharField(max_length=250, blank=True, null=True)
    room_type = models.CharField(max_length=250, blank=True, null=True)
    no_of_bed = models.CharField(max_length=250, blank=True, null=True)
    total_no_of_beds = models.CharField(max_length=250, blank=True, null=True)
    no_of_rooms = models.CharField(max_length=250, blank=True, null=True)
    expected_price_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_price = models.CharField(max_length=250, blank=True, null=True)
    carpet_area = models.CharField(max_length=250, blank=True, null=True)
    carpet_area_postfix = models.CharField(max_length=250, blank=True, null=True)
    built_up_area = models.CharField(max_length=250, blank=True, null=True)
    built_area_postfix = models.CharField(max_length=250, blank=True, null=True)
    bathroom_type = models.CharField(max_length=250, blank=True, null=True)
    restroom_type = models.CharField(max_length=250, blank=True, null=True)
    year_built = models.CharField(max_length=250, blank=True, null=True)
    no_of_floors = models.CharField(max_length=250, blank=True, null=True)
    oc_received = models.CharField(max_length=250, blank=True, null=True)
    construction_type = models.CharField(max_length=250, blank=True, null=True)
    expected_deposit_prefix = models.CharField(max_length=250, blank=True, null=True)
    expected_deposit = models.CharField(max_length=250, blank=True, null=True)
    na_passed = models.CharField(max_length=250, blank=True, null=True)
    fencing = models.CharField(max_length=250, blank=True, null=True)
    land_type = models.CharField(max_length=250, blank=True, null=True)
    rera_register = models.CharField(max_length=250, blank=True, null=True)
    add_rera_no = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'details'


class DeveloperDetails(models.Model):
    name = models.TextField()
    detail = models.TextField()
    logo = models.TextField()
    status = models.IntegerField()
    developer_demand = models.CharField(max_length=9)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'developer_details'


class DoctorSpecialities(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(db_comment='1=Active, 2=Deactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_specialities'


class EmployeeProfiles(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    aadhar_card = models.TextField(blank=True, null=True)
    pan_card = models.TextField(blank=True, null=True)
    joining_letter = models.TextField(blank=True, null=True)
    certificates = models.TextField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True)
    account_name = models.TextField(blank=True, null=True)
    account_number = models.BigIntegerField(blank=True, null=True)
    ifsc_code = models.TextField(blank=True, null=True)
    upi_id = models.TextField(blank=True, null=True)
    basic_salary = models.TextField(blank=True, null=True)
    conveyance = models.IntegerField(blank=True, null=True)
    conveyance_limit = models.BigIntegerField(blank=True, null=True)
    conveyance_limit_postfix = models.IntegerField(blank=True, null=True)
    travel_allowance = models.IntegerField(blank=True, null=True)
    travel_allowance_limit = models.TextField(blank=True, null=True)
    travel_allowance_limit_postfix = models.IntegerField(blank=True, null=True)
    meal_allowance = models.IntegerField(blank=True, null=True)
    meal_allowance_limit = models.TextField(blank=True, null=True)
    meal_allowance_limit_postfix = models.IntegerField(blank=True, null=True)
    life_insurance = models.IntegerField(blank=True, null=True)
    life_insurance_product_name = models.TextField(blank=True, null=True)
    life_insurance_premium_amount = models.TextField(blank=True, null=True)
    life_insurance_premium_amount_postfix = models.IntegerField(blank=True, null=True)
    medical_insurance = models.IntegerField(blank=True, null=True)
    medical_insurance_product_name = models.TextField(blank=True, null=True)
    medical_insurance_premium_amount = models.TextField(blank=True, null=True)
    medical_insurance_premium_amount_postfix = models.IntegerField(blank=True, null=True)
    provident_fund = models.IntegerField(blank=True, null=True)
    provident_percentage_basic_salary = models.BigIntegerField(blank=True, null=True)
    tds_applicable = models.IntegerField(blank=True, null=True)
    tds_percentage_basic_salary = models.BigIntegerField(blank=True, null=True)
    paid_sick_leaves = models.IntegerField(blank=True, null=True)
    no_paid_sick_leaves = models.BigIntegerField(blank=True, null=True)
    no_paid_sick_leaves_postfiix = models.IntegerField(blank=True, null=True)
    house_rent_allowance = models.IntegerField(blank=True, null=True)
    house_rent_allowance_limit = models.BigIntegerField(blank=True, null=True)
    house_rent_allowance_limit_postfix = models.IntegerField(blank=True, null=True)
    incentives = models.IntegerField(blank=True, null=True)
    professional_tax = models.IntegerField(blank=True, null=True)
    professional_tax_charges = models.BigIntegerField(blank=True, null=True)
    professional_tax_charges_postfix = models.IntegerField(blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'employee_profiles'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class Faqs(models.Model):
    modules_id = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, db_comment='1= Active, 2=Deactive')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faqs'


class FavouriteProjects(models.Model):
    new_project_id = models.CharField(max_length=36)
    user_id = models.IntegerField()
    is_favourite = models.IntegerField(db_comment='1= Favourite, 2 = Not Favourite\t')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favourite_projects'


class FavouriteProperties(models.Model):
    property_id = models.CharField(max_length=36)
    user_id = models.IntegerField(blank=True, null=True)
    is_favourite = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favourite_properties'


class FloorPlans(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    property_id = models.CharField(max_length=36)
    title_site = models.CharField(max_length=250, blank=True, null=True)
    image_site = models.CharField(max_length=250, blank=True, null=True)
    title_floor = models.CharField(max_length=250, blank=True, null=True)
    image_floor = models.CharField(max_length=250, blank=True, null=True)
    image_all_floor_plan = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'floor_plans'


class LoanRates(models.Model):
    code = models.CharField(max_length=255)
    bank_name = models.TextField()
    loan_type_id = models.IntegerField()
    rate = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan_rates'


class LoanTypes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(db_comment='1=Active, 2=Deactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan_types'


class Loans(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    loan_type_id = models.IntegerField(blank=True, null=True)
    requirement = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    status = models.IntegerField(db_comment='1 = Pending , 2 = Approve, 3 = Disapprove')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loans'


class Localities(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
    property_id = models.CharField(max_length=36)
    property_room_type_id = models.CharField(max_length=36, blank=True, null=True)
    file_path = models.CharField(max_length=250, blank=True, null=True)
    media_type = models.IntegerField(blank=True, null=True, db_comment='1 = indoor, 2 = outdoor, 3=amenities , 4= outside_view ,5=land')
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class MyAffiliateLinks(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    property_id = models.CharField(max_length=36)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'my_affiliate_links'


class NewProjectAddFloorPlans(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    title = models.CharField(max_length=100, blank=True, null=True)
    image_plan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_add_floor_plans'


class NewProjectAddSchemeStructures(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    title = models.TextField(blank=True, null=True)
    image_scheme = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_add_scheme_structures'


class NewProjectApprovalLadders(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_brokerage_others_id = models.CharField(max_length=36)
    brokerage_ladder_from_book = models.IntegerField(blank=True, null=True)
    brokerage_ladder_from_others = models.IntegerField(blank=True, null=True)
    brokerage_ladder_till_book = models.IntegerField(blank=True, null=True)
    brokerage_ladder_till_others = models.IntegerField(blank=True, null=True)
    brokerage_percent_ladder = models.IntegerField(blank=True, null=True)
    brokerage_amount_ladder = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_approval_ladders'


class NewProjectApprovals(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    approval_status = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    is_visible_on_homepage = models.TextField(blank=True, null=True)
    enable_relist = models.IntegerField(blank=True, null=True)
    brokerage_type = models.TextField(blank=True, null=True)
    relisting_charges = models.TextField(blank=True, null=True)
    affiliate_charges = models.TextField(blank=True, null=True)
    new_proj_sec_deposit = models.TextField(blank=True, null=True)
    coupon_code_availability = models.TextField(blank=True, null=True)
    affiliate_bonus = models.TextField(blank=True, null=True)
    enable_scratch_card = models.TextField(blank=True, null=True)
    scratch_card_prize = models.TextField(blank=True, null=True)
    scratch_card_percent = models.TextField(blank=True, null=True)
    scratch_card_amount = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_approvals'


class NewProjectApprovedByAdmins(models.Model):
    id = models.BigAutoField(primary_key=True)
    new_project_id = models.CharField(max_length=255, db_collation='utf8mb3_general_ci')
    user_id = models.IntegerField(blank=True, null=True)
    remark = models.TextField(db_collation='utf8mb3_general_ci', blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, db_comment='0=Pending, 1=Approved, 2=Disapproved')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_approved_by_admins'


class NewProjectBrokerageOthers(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    new_project_detail_id = models.CharField(max_length=36)
    configuration = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    area_postfix = models.TextField(blank=True, null=True)
    brokerage_amount = models.FloatField(blank=True, null=True)
    brokerage_percent = models.TextField(blank=True, null=True)
    brokerage_to_show = models.TextField(blank=True, null=True)
    brokerage_release_days = models.TextField(blank=True, null=True)
    scheme_expiry = models.TextField(blank=True, null=True)
    brokerage_ladder_from = models.TextField(blank=True, null=True)
    brokerage_ladder_till = models.TextField(blank=True, null=True)
    brokerage_ladder_from_booking = models.TextField(blank=True, null=True)
    brokerage_ladder_till_booking = models.TextField(blank=True, null=True)
    brokerage_release_days_register = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_brokerage_others'


class NewProjectBrokerageOthers1(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    configuration = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    area_postfix = models.TextField(blank=True, null=True)
    brokerage_amount_flat_amount = models.TextField(blank=True, null=True)
    brokerage_percent_flat_amount = models.TextField(blank=True, null=True)
    brokerage_to_show_flat_amount = models.TextField(blank=True, null=True)
    brokerage_release_days_flat_amount = models.TextField(blank=True, null=True)
    scheme_expiry_flat_amount = models.TextField(blank=True, null=True)
    brokerage_ladder_from_ladder_amt = models.TextField(blank=True, null=True)
    brokerage_ladder_till_ladder_amt = models.TextField(blank=True, null=True)
    brokerage_amount_ladder_amount = models.TextField(blank=True, null=True)
    brokerage_percent_ladder_amount = models.TextField(blank=True, null=True)
    brokerage_to_show_ladder_amount = models.TextField(blank=True, null=True)
    brokerage_release_days_ladder_amount = models.TextField(blank=True, null=True)
    scheme_expiry_ladder_amount = models.TextField(blank=True, null=True)
    brokerage_percent_flat_percent = models.TextField(blank=True, null=True)
    brokerage_amount_flat_percent = models.TextField(blank=True, null=True)
    brokerage_to_show_flat_percent = models.TextField(blank=True, null=True)
    brokerage_release_days_flat_percent = models.TextField(blank=True, null=True)
    scheme_expiry_flat_percent = models.TextField(blank=True, null=True)
    brokerage_ladder_from_ladder_percent = models.TextField(blank=True, null=True)
    brokerage_ladder_till_ladder_percent = models.TextField(blank=True, null=True)
    brokerage_percent_ladder_amo = models.TextField(blank=True, null=True)
    brokerage_amount_ladder_percent = models.TextField(blank=True, null=True)
    brokerage_to_show_ladder_percent = models.TextField(blank=True, null=True)
    brokerage_release_days_ladder_percent = models.TextField(blank=True, null=True)
    scheme_expiry_ladder_percent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_brokerage_others_1'


class NewProjectCoupons(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_approval_id = models.CharField(max_length=36)
    coupon_visibility = models.TextField(blank=True, null=True)
    coupon_code = models.TextField(blank=True, null=True)
    coupon_discount_percent_relist = models.TextField(blank=True, null=True)
    coupon_discount_amount_relist = models.TextField(blank=True, null=True)
    coupon_discount_percent_affiliate = models.TextField(blank=True, null=True)
    coupon_discount_amount_affiliate = models.TextField(blank=True, null=True)
    coupon_discount_percent_secure = models.TextField(blank=True, null=True)
    coupon_discount_amount_secure = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_coupons'


class NewProjectDetailLadders(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_detail_id = models.CharField(max_length=36)
    brokerage_type = models.IntegerField(blank=True, null=True, db_comment='3 = Ladder Amount, 4 = Ladder Percentage')
    brokerage_ladder_from_book = models.IntegerField(blank=True, null=True)
    brokerage_ladder_from_others = models.TextField(blank=True, null=True)
    brokerage_ladder_till_book = models.IntegerField(blank=True, null=True)
    brokerage_ladder_till_others = models.TextField(blank=True, null=True)
    brokerage_percent_ladder = models.TextField(blank=True, null=True)
    brokerage_amount_ladder = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_detail_ladders'


class NewProjectDetails(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36, blank=True, null=True)
    configuration = models.TextField(blank=True, null=True)
    floor_plan = models.TextField(blank=True, null=True)
    no_of_bed = models.IntegerField(blank=True, null=True)
    no_bed_others = models.TextField(blank=True, null=True)
    total_no_of_beds = models.TextField(blank=True, null=True)
    total_no_beds_others = models.TextField(blank=True, null=True)
    no_of_rooms = models.TextField(blank=True, null=True)
    no_rooms_others = models.TextField(blank=True, null=True)
    carpet_area = models.TextField(blank=True, null=True)
    carpet_area_postfix = models.IntegerField(blank=True, null=True)
    built_up_area = models.TextField(blank=True, null=True)
    built_area_postfix = models.IntegerField(blank=True, null=True)
    super_built_up_area = models.TextField(blank=True, null=True)
    super_built_area_postfix = models.IntegerField(blank=True, null=True)
    bathroom_type = models.IntegerField(blank=True, null=True)
    restroom_type = models.IntegerField(blank=True, null=True)
    no_of_floors = models.IntegerField(blank=True, null=True)
    no_master_bedroom = models.IntegerField(blank=True, null=True)
    no_master_bedroom_others = models.TextField(blank=True, null=True)
    no_common_bedroom = models.IntegerField(blank=True, null=True)
    no_common_bedroom_others = models.TextField(blank=True, null=True)
    no_master_bathroom = models.IntegerField(blank=True, null=True)
    no_master_bathroom_others = models.TextField(blank=True, null=True)
    no_common_bathroom = models.IntegerField(blank=True, null=True)
    no_common_bathroom_others = models.TextField(blank=True, null=True)
    no_balcony = models.IntegerField(blank=True, null=True)
    no_balcony_others = models.TextField(blank=True, null=True)
    agreement_value_price_prefix = models.IntegerField(blank=True, null=True)
    agreement_value = models.FloatField(blank=True, null=True)
    gst_percentage = models.IntegerField(blank=True, null=True)
    gst_amount = models.TextField(blank=True, null=True)
    stamp_duty_price_prefix = models.IntegerField(blank=True, null=True)
    stamp_duty = models.TextField(blank=True, null=True)
    registration_price_prefix = models.IntegerField(blank=True, null=True)
    registration_charges = models.TextField(blank=True, null=True)
    paper_work_price_prefix = models.IntegerField(blank=True, null=True)
    paper_work = models.TextField(blank=True, null=True)
    society_form_price_prefix = models.IntegerField(blank=True, null=True)
    society_formation = models.TextField(blank=True, null=True)
    no_advance_maint = models.TextField(blank=True, null=True)
    inclusive_price_prefix = models.IntegerField(blank=True, null=True)
    inclusive_price = models.FloatField(blank=True, null=True)
    total_advance_maint_price_prefix = models.IntegerField(blank=True, null=True)
    total_advance_maint = models.TextField(blank=True, null=True)
    advance_maint_amt = models.FloatField(blank=True, null=True)
    brokerage_type = models.IntegerField(blank=True, null=True)
    brokerage_amount_flat = models.TextField(blank=True, null=True)
    brokerage_percent_flat = models.TextField(blank=True, null=True)
    brokerage_release_days_register = models.TextField(blank=True, null=True)
    scheme_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_details'


class NewProjectDetails1(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
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
    no_of_floors = models.CharField(max_length=250, blank=True, null=True)
    food_available = models.CharField(max_length=250, blank=True, null=True)
    food_charges = models.CharField(max_length=250, blank=True, null=True)
    food_charge_prefix = models.CharField(max_length=250, blank=True, null=True)
    add_food_charge = models.CharField(max_length=250, blank=True, null=True)
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
    price_square_prefix = models.CharField(max_length=250, blank=True, null=True)
    price_square = models.CharField(max_length=250, blank=True, null=True)
    maintenance_charges = models.CharField(max_length=250, blank=True, null=True)
    maintenance_charges_postfix = models.CharField(max_length=250, blank=True, null=True)
    membership_charges_prefix = models.IntegerField(blank=True, null=True)
    membership_charges = models.TextField(blank=True, null=True)
    annual_dues_prefix = models.IntegerField(blank=True, null=True)
    annual_dues = models.BigIntegerField(blank=True, null=True)
    expected_rental_prefix = models.IntegerField(blank=True, null=True)
    expected_rental = models.BigIntegerField(blank=True, null=True)
    price_negotiable = models.IntegerField(blank=True, null=True)
    agreement_value_price_prefix = models.IntegerField(blank=True, null=True)
    agreement_value = models.TextField(blank=True, null=True)
    gst = models.TextField(blank=True, null=True)
    stamp_duty_price_prefix = models.IntegerField(blank=True, null=True)
    stamp_duty = models.TextField(blank=True, null=True)
    registration_price_prefix = models.IntegerField(blank=True, null=True)
    registration_charges = models.TextField(blank=True, null=True)
    paper_work_price_prefix = models.IntegerField(blank=True, null=True)
    paper_work = models.TextField(blank=True, null=True)
    society_form_price_prefix = models.IntegerField(blank=True, null=True)
    society_formation = models.TextField(blank=True, null=True)
    no_advance_maint = models.TextField(blank=True, null=True)
    advance_maint_amt = models.TextField(blank=True, null=True)
    total_advance_maint_price_prefix = models.IntegerField(blank=True, null=True)
    total_advance_maint = models.TextField(blank=True, null=True)
    inclusive_price_prefix = models.IntegerField(blank=True, null=True)
    inclusive_price = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_details_1'


class NewProjectEnquiries(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    new_project_id = models.CharField(max_length=36)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_enquiries'


class NewProjectEnquiriesOld(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    new_project_id = models.CharField(max_length=36)
    name = models.TextField()
    phone = models.BigIntegerField()
    email = models.TextField()
    message = models.TextField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_enquiries_old'


class NewProjectFloorPlans(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    title_site = models.CharField(max_length=250, blank=True, null=True)
    image_site = models.CharField(max_length=250, blank=True, null=True)
    title_floor = models.CharField(max_length=250, blank=True, null=True)
    image_floor = models.CharField(max_length=250, blank=True, null=True)
    image_all_floor_plan = models.TextField(blank=True, null=True)
    image_all_payment_scheme = models.TextField(blank=True, null=True)
    image_payment_scheme_1 = models.TextField(blank=True, null=True)
    image_payment_scheme_2 = models.TextField(blank=True, null=True)
    image_project_detail_pdf = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    image_plans = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_floor_plans'


class NewProjectLocalities(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
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
        db_table = 'new_project_localities'


class NewProjectLocalityClinics(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    nearby_clinic = models.CharField(max_length=250, blank=True, null=True)
    map_clinic = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    specialist_clinic = models.CharField(max_length=250, blank=True, null=True)
    add_specialist_clinic = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_locality_clinics'


class NewProjectLocalityColleges(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    nearby_college = models.CharField(max_length=250, blank=True, null=True)
    map_college = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    stream_college = models.CharField(max_length=250, blank=True, null=True)
    stream_college_type = models.CharField(max_length=250, blank=True, null=True)
    board_college = models.CharField(max_length=250, blank=True, null=True)
    board_college_type = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_locality_colleges'


class NewProjectLocalityHospitals(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    nearby_hospital = models.CharField(max_length=250, blank=True, null=True)
    map_hospital = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    specialist_hospital = models.CharField(max_length=250, blank=True, null=True)
    add_specialist_hospital = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_locality_hospitals'


class NewProjectLocalitySchools(models.Model):
    id = models.CharField(max_length=36)
    new_project_id = models.CharField(max_length=36)
    nearby_school = models.CharField(max_length=250, blank=True, null=True)
    map_school = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    stream_school = models.CharField(max_length=250, blank=True, null=True)
    stream_school_type = models.CharField(max_length=250, blank=True, null=True)
    board_school = models.CharField(max_length=250, blank=True, null=True)
    board_school_type = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_locality_schools'


class NewProjectLocations(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    pincode = models.IntegerField(blank=True, null=True)
    country_id = models.CharField(max_length=100, blank=True, null=True)
    country_name = models.CharField(max_length=250, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.CharField(max_length=250, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    city_name = models.CharField(max_length=100, blank=True, null=True)
    society_building = models.CharField(max_length=250, blank=True, null=True)
    flat_apartment = models.TextField(blank=True, null=True)
    shop_office = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    plot_survey = models.CharField(max_length=250, blank=True, null=True)
    landmark = models.CharField(max_length=250, blank=True, null=True)
    map_location = models.CharField(max_length=250, blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_locations'


class NewProjectMedia(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    new_project_room_type_id = models.CharField(max_length=36, blank=True, null=True)
    cover_photo = models.TextField(blank=True, null=True)
    file_path = models.CharField(max_length=250, blank=True, null=True)
    image_size_610_510 = models.TextField(blank=True, null=True)
    image_size_370_240 = models.TextField(blank=True, null=True)
    image_size_270_250 = models.TextField(blank=True, null=True)
    image_size_280_240 = models.TextField(blank=True, null=True)
    media_type = models.IntegerField(blank=True, null=True, db_comment='1 = indoor, 2 = outdoor, 3=amenities , 4= outside_view ,5=land, 6= All Image, 7=Reels, 8 =Advertising, 9 = All Video, 10 = Project Detail')
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_media'


class NewProjectOtherFloorPlans(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    image_site = models.TextField(blank=True, null=True)
    image_floor = models.TextField(blank=True, null=True)
    image_all_floor_plan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_other_floor_plans'


class NewProjectParkings(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
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
    free_charge_hrs = models.CharField(max_length=250, blank=True, null=True)
    free_charge_postfix_hrs = models.CharField(max_length=250, blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_parkings'


class NewProjectPostRequestAgents(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    user_id = models.IntegerField()
    project_name = models.TextField(blank=True, null=True)
    developer_id = models.TextField(blank=True, null=True)
    relisting_charges = models.TextField(blank=True, null=True)
    affiliate_charges = models.TextField(blank=True, null=True)
    enable_scratch_card = models.TextField(blank=True, null=True)
    scratch_card_prize = models.TextField(blank=True, null=True)
    coupon_code = models.TextField(blank=True, null=True)
    new_proj_sec_deposit = models.TextField(blank=True, null=True)
    avail_new_proj_sd = models.TextField(blank=True, null=True)
    pay_new_proj_sd = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_post_request_agents'


class NewProjectRequests(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36, blank=True, null=True)
    user_id = models.IntegerField()
    developer_id = models.IntegerField(blank=True, null=True)
    project_name = models.TextField(blank=True, null=True)
    pincode = models.BigIntegerField(blank=True, null=True)
    society_building = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    landmark = models.TextField(blank=True, null=True)
    map_location = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_requests'


class NewProjectRoomTypes(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_detail_id = models.CharField(max_length=36)
    room_type_id = models.CharField(max_length=11, blank=True, null=True)
    no_of_rooms_title = models.CharField(max_length=250, blank=True, null=True)
    size_of_room = models.CharField(max_length=250, blank=True, null=True)
    room_title = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_project_room_types'


class NewProjectStructureTypes(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    new_project_id = models.CharField(max_length=36)
    total_land_parcel = models.BigIntegerField(blank=True, null=True)
    total_open_space = models.BigIntegerField(blank=True, null=True)
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
        db_table = 'new_project_structure_types'


class NewProjects(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    property_type = models.SmallIntegerField(db_comment='1=Featured ,2=Recomend ')
    developer_id = models.IntegerField(blank=True, null=True)
    developer_name = models.TextField(blank=True, null=True)
    developer_detail = models.TextField(blank=True, null=True)
    developer_logo = models.TextField(blank=True, null=True)
    project_name = models.TextField(blank=True, null=True)
    project_detail = models.TextField(blank=True, null=True)
    project_logo = models.TextField(blank=True, null=True)
    rera_register = models.TextField(blank=True, null=True)
    add_rera_no = models.TextField(blank=True, null=True)
    add_rera_link = models.TextField(blank=True, null=True)
    project_status = models.IntegerField(blank=True, null=True)
    developer_possession = models.TextField(blank=True, null=True)
    rera_possession = models.TextField(blank=True, null=True)
    possession_received_on = models.TextField(blank=True, null=True)
    oc_received = models.IntegerField(blank=True, null=True)
    ownership_type = models.IntegerField(blank=True, null=True)
    construction_type = models.IntegerField(blank=True, null=True)
    best_suitable = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField(db_comment='1=Active ,0=Inactive')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_projects'


class NoticeManagements(models.Model):
    image = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notice_managements'


class Notifications(models.Model):
    wabpay_title = models.TextField(blank=True, null=True)
    wabpay_description = models.TextField(blank=True, null=True)
    wabpay_image = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notifications'


class OauthAccessTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    client_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_access_tokens'


class OauthAuthCodes(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField()
    client_id = models.PositiveBigIntegerField()
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_auth_codes'


class OauthClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    secret = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=255, blank=True, null=True)
    redirect = models.TextField()
    personal_access_client = models.IntegerField()
    password_client = models.IntegerField()
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_clients'


class OauthPersonalAccessClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_personal_access_clients'


class OauthRefreshTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    access_token_id = models.CharField(max_length=100)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_refresh_tokens'


class OrderItems(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    order_id = models.CharField(max_length=36)
    user_id = models.IntegerField()
    quantity = models.IntegerField()
    plan_type = models.CharField(max_length=10)
    plan_type_id = models.IntegerField()
    plan_name = models.CharField(max_length=20)
    plan_id = models.IntegerField()
    expected_rent_range = models.IntegerField(blank=True, null=True)
    expected_price_range = models.IntegerField(blank=True, null=True)
    no_of_listing = models.IntegerField(blank=True, null=True)
    open_transaction = models.IntegerField(blank=True, null=True)
    rental_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resale_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resale_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cancellation_charges = models.IntegerField(blank=True, null=True)
    fetch_out_possible = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fetch_out_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    referral_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit_deductable = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    payment_status = models.CharField(max_length=7)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Parkings(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    property_id = models.CharField(max_length=36)
    type_of_vehicle = models.CharField(max_length=250, blank=True, null=True)
    number_of_parking = models.CharField(max_length=250, blank=True, null=True)
    additional_dropdown = models.CharField(max_length=250, blank=True, null=True)
    total_park_multi = models.CharField(max_length=250, blank=True, null=True)
    no_floor_multi = models.CharField(max_length=250, blank=True, null=True)
    out_park_multi = models.CharField(max_length=250, blank=True, null=True)
    total_park_separate = models.CharField(max_length=250, blank=True, null=True)
    no_floor_separate = models.CharField(max_length=250, blank=True, null=True)
    out_park_separate = models.CharField(max_length=250, blank=True, null=True)
    total_park_automate = models.CharField(max_length=250, blank=True, null=True)
    no_floor_automate = models.CharField(max_length=250, blank=True, null=True)
    out_park_automate = models.CharField(max_length=250, blank=True, null=True)
    parking_structure = models.CharField(max_length=250, blank=True, null=True)
    type_of_parking = models.CharField(max_length=250, blank=True, null=True)
    free_in_time = models.CharField(max_length=250, blank=True, null=True)
    free_in_time_prefix = models.CharField(max_length=250, blank=True, null=True)
    free_out_time = models.CharField(max_length=250, blank=True, null=True)
    free_out_time_prefix = models.CharField(max_length=250, blank=True, null=True)
    free_usage_hrs = models.CharField(max_length=250, blank=True, null=True)
    free_charge_prefix = models.CharField(max_length=250, blank=True, null=True)
    free_charge_hrs = models.CharField(max_length=250, blank=True, null=True)
    free_charge_postfix = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parkings'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class Permissions(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'permissions'


class PermissionsOld(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'permissions_old'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_access_tokens'


class PlanTypes(models.Model):
    plan_name = models.CharField(max_length=20)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'plan_types'


class PostReels(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    transaction_type = models.IntegerField(blank=True, null=True)
    subcategory = models.IntegerField(blank=True, null=True)
    subcategory_type = models.IntegerField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    country_name = models.TextField(blank=True, null=True)
    state_name = models.TextField(blank=True, null=True)
    city_name = models.TextField(blank=True, null=True)
    district_name = models.TextField(blank=True, null=True)
    society_building = models.TextField(blank=True, null=True)
    latitude = models.BigIntegerField(blank=True, null=True)
    longitude = models.IntegerField(blank=True, null=True)
    type_category = models.IntegerField(blank=True, null=True)
    configuration = models.IntegerField(blank=True, null=True)
    area = models.BigIntegerField(blank=True, null=True)
    area_postfix = models.IntegerField(blank=True, null=True)
    carpet_area = models.BigIntegerField(blank=True, null=True)
    carpet_area_postfix = models.IntegerField(blank=True, null=True)
    built_up_area = models.BigIntegerField(blank=True, null=True)
    built_area_postfix = models.IntegerField(blank=True, null=True)
    super_built_up_area = models.BigIntegerField(blank=True, null=True)
    super_built_area_postfix = models.IntegerField(blank=True, null=True)
    possession = models.IntegerField(blank=True, null=True)
    construction_status = models.IntegerField(blank=True, null=True)
    construction_status_year = models.IntegerField(blank=True, null=True)
    oc_received = models.IntegerField(blank=True, null=True)
    rera_register = models.IntegerField(blank=True, null=True)
    expected_price_prefix = models.IntegerField(blank=True, null=True)
    expected_price = models.BigIntegerField(blank=True, null=True)
    expected_rent_prefix = models.IntegerField(blank=True, null=True)
    expected_rent = models.BigIntegerField(blank=True, null=True)
    expected_rent_postfix = models.IntegerField(blank=True, null=True)
    expected_heavy_deposit_prefix = models.IntegerField(blank=True, null=True)
    expected_heavy_deposit = models.BigIntegerField(blank=True, null=True)
    lock_in_year = models.IntegerField(blank=True, null=True)
    lock_in_month = models.IntegerField(blank=True, null=True)
    reel = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_reels'


class ProductAdvertisements(models.Model):
    id = models.CharField(max_length=36)
    advertisement_id = models.CharField(max_length=36)
    product_title = models.CharField(max_length=255, blank=True, null=True)
    product_media = models.CharField(max_length=255, blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    specification_title = models.TextField(blank=True, null=True)
    specification_description = models.TextField(blank=True, null=True)
    key_highlights_logo = models.CharField(max_length=255, blank=True, null=True)
    key_highlights_title = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_advertisements'


class PromotionSocialOthers(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    promotion_id = models.CharField(max_length=36)
    social_logo = models.TextField(blank=True, null=True)
    social_link_other = models.TextField(blank=True, null=True)
    social_name_other = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'promotion_social_others'


class Promotions(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    sub_category = models.IntegerField(blank=True, null=True)
    super_sub_category = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    media = models.TextField(blank=True, null=True)
    thumbnail = models.CharField(max_length=250, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    app = models.CharField(max_length=100, blank=True, null=True)
    instagram_link = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.CharField(max_length=100, blank=True, null=True)
    youtube_link = models.CharField(max_length=100, blank=True, null=True)
    linkedin_link = models.CharField(max_length=100, blank=True, null=True)
    threads_link = models.CharField(max_length=100, blank=True, null=True)
    twitter_link = models.CharField(max_length=100, blank=True, null=True)
    social_logo = models.CharField(max_length=100, blank=True, null=True)
    social_name = models.CharField(max_length=100, blank=True, null=True)
    social_link = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, db_comment='1=Yourself, 2=Business')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'promotions'


class Properties(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    property_type = models.SmallIntegerField(db_comment='1=Featured ,2=Recomend\t')
    affiliate_plan_id = models.IntegerField(blank=True, null=True)
    affiliate_plan_type = models.CharField(max_length=6, blank=True, null=True)
    property_upload_id = models.CharField(max_length=36, blank=True, null=True)
    status = models.SmallIntegerField(db_comment='1=Active ,0=Inactive')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'properties'


class PropertiesOld(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    status = models.SmallIntegerField(db_comment='1=Active ,0=Inactive')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'properties_old'


class PropertyApprovedByAdmins(models.Model):
    id = models.BigAutoField(primary_key=True)
    property_id = models.CharField(max_length=255, db_collation='utf8mb3_general_ci')
    user_id = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, db_comment='0=Pending, 1=Approved, 2=Disapproved')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_approved_by_admins'


class PropertyDetails(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
    property_id = models.CharField(max_length=36)
    property_room_type_id = models.CharField(max_length=36, blank=True, null=True)
    file_path = models.CharField(max_length=250, blank=True, null=True)
    cover_photo = models.TextField(blank=True, null=True)
    image_size_610_510 = models.TextField(blank=True, null=True)
    image_size_370_240 = models.TextField(blank=True, null=True)
    image_size_270_250 = models.TextField(blank=True, null=True)
    media_type = models.IntegerField(blank=True, null=True, db_comment='1 = indoor, 2 = outdoor, 3=amenities , 4= outside_view ,5=land, 6= All Image, 7=Affiliate Marketing, 8 =Advertising')
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_media'


class PropertyParkings(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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
    id = models.CharField(primary_key=True, max_length=36)
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


class PushNotifications(models.Model):
    push_title = models.TextField()
    push_image = models.TextField()
    push_description = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'push_notifications'


class RaiseTickets(models.Model):
    user_id = models.IntegerField()
    title = models.TextField()
    description = models.TextField()
    image = models.TextField()
    department = models.IntegerField(blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    employee_assigned = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'raise_tickets'


class ReferralPlanAgents(models.Model):
    loan_type_id = models.IntegerField()
    percentage_disbursement_amount = models.IntegerField(blank=True, null=True)
    visible_day_disbursement = models.IntegerField(blank=True, null=True)
    release_day_disbursement = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_plan_agents'


class ReferralPlanOthers(models.Model):
    loan_type_id = models.IntegerField()
    percentage_disbursement_amount = models.IntegerField(blank=True, null=True)
    visible_day_disbursement = models.IntegerField(blank=True, null=True)
    release_day_disbursement = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_plan_others'


class ReferralPlans(models.Model):
    id = models.IntegerField(primary_key=True)
    resale_earning_per_transaction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resale_earning_visible_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resale_earning_release_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_earning_per_transaction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_earning_visible_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_earning_release_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_earning_per_transaction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_earning_visible_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_earning_release_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resale_percentage_of_affiliate_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_percentage_of_affiliate_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_percentage_of_affiliate_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_plans'


class Referrals(models.Model):
    referrer_id = models.IntegerField()
    referee_id = models.IntegerField()
    referral_code = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referrals'


class RentPayments(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    amount = models.CharField(max_length=255)
    rent_type = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=4, db_comment='"upi", "bank"')
    name = models.TextField()
    upi_id = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.BigIntegerField(blank=True, null=True)
    ifsc_code = models.CharField(max_length=255, blank=True, null=True)
    pan = models.CharField(max_length=255)
    otp = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rent_payments'


class RoomTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_ids = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.SmallIntegerField(db_comment='1=Active, 2=Deactive')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_types'


class ScratchCards(models.Model):
    name = models.TextField()
    value = models.TextField()
    gift_image = models.TextField(blank=True, null=True)
    result_image = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scratch_cards'


class Storylines(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    no_of_family_member = models.CharField(max_length=225, blank=True, null=True)
    name = models.CharField(max_length=225, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=225, blank=True, null=True)
    family_member_type = models.CharField(max_length=255, blank=True, null=True)
    workplace_address = models.CharField(max_length=255, blank=True, null=True)
    workplace_map_location = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    travels_via = models.CharField(max_length=255, blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    daytime = models.CharField(max_length=255, blank=True, null=True)
    education_grade = models.CharField(max_length=255, blank=True, null=True)
    boards_university = models.CharField(max_length=255, blank=True, null=True)
    stream = models.CharField(max_length=255, blank=True, null=True)
    university_address = models.CharField(max_length=255, blank=True, null=True)
    university_map = models.CharField(max_length=255, blank=True, null=True)
    travel_via = models.CharField(max_length=255, blank=True, null=True)
    hobbies_elder = models.CharField(max_length=255, blank=True, null=True)
    elder_daytime_sleeping = models.CharField(max_length=255, blank=True, null=True)
    medical_condition = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'storylines'


class Streams(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'streams'


class StructureTypes(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    property_id = models.CharField(max_length=36)
    no_of_tower = models.CharField(max_length=250, blank=True, null=True)
    land_type = models.CharField(max_length=250, blank=True, null=True)
    no_of_wings = models.CharField(max_length=250, blank=True, null=True)
    total_floor_structure = models.CharField(max_length=250, blank=True, null=True)
    no_floor_structure = models.CharField(max_length=250, blank=True, null=True)
    out_floor_structure = models.CharField(max_length=250, blank=True, null=True)
    no_of_flats = models.CharField(max_length=250, blank=True, null=True)
    no_of_property = models.CharField(max_length=250, blank=True, null=True)
    no_of_elevator = models.CharField(max_length=250, blank=True, null=True)
    no_of_staircase = models.CharField(max_length=250, blank=True, null=True)
    no_of_refugee_flat = models.CharField(max_length=250, blank=True, null=True)
    no_of_refugee_property = models.CharField(max_length=250, blank=True, null=True)
    nearest_refugee_flat = models.CharField(max_length=250, blank=True, null=True)
    nearest_refugee_property = models.CharField(max_length=250, blank=True, null=True)
    property_entrance_spacing = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_types'


class Subscribes(models.Model):
    channel_id = models.CharField(max_length=36)
    user_id = models.IntegerField()
    is_subscribed = models.IntegerField(db_comment='1 = Subscribe, 2 = Unsubscribed')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscribes'


class Superadmins(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'superadmins'


class Taxations(models.Model):
    id = models.IntegerField()
    plan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'taxations'


class Universities(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'universities'


class UserProfiles(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    investing_since = models.CharField(max_length=100, blank=True, null=True)
    invest_capital_prefix = models.IntegerField(blank=True, null=True)
    investment_capital = models.IntegerField(blank=True, null=True)
    invest_capital_other = models.CharField(max_length=100, blank=True, null=True)
    avail_fund_prefix = models.IntegerField(blank=True, null=True)
    available_funds = models.IntegerField(blank=True, null=True)
    avail_fund_other = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    pincode_office = models.CharField(max_length=30, blank=True, null=True)
    country_office_id = models.IntegerField(blank=True, null=True)
    country_office_name = models.TextField(blank=True, null=True)
    state_office_id = models.IntegerField(blank=True, null=True)
    state_office_name = models.TextField(blank=True, null=True)
    district_office_id = models.IntegerField(blank=True, null=True)
    district_office_name = models.TextField(blank=True, null=True)
    city_office_id = models.IntegerField(blank=True, null=True)
    city_office_name = models.TextField(blank=True, null=True)
    society_building_office = models.CharField(max_length=250, blank=True, null=True)
    shop_office = models.CharField(max_length=250, blank=True, null=True)
    landmark_office = models.CharField(max_length=250, blank=True, null=True)
    official_mobile = models.CharField(max_length=30, blank=True, null=True)
    official_mail = models.CharField(max_length=50, blank=True, null=True)
    gstin = models.IntegerField(blank=True, null=True)
    add_gstin = models.CharField(max_length=500, blank=True, null=True)
    rera = models.IntegerField(blank=True, null=True)
    firm_type = models.IntegerField(blank=True, null=True)
    firm_name = models.TextField(blank=True, null=True)
    rera_type = models.CharField(max_length=10, blank=True, null=True)
    rera_certificate = models.TextField(blank=True, null=True)
    competency_certificate = models.TextField(blank=True, null=True)
    address_proof = models.TextField(blank=True, null=True)
    add_rera = models.CharField(max_length=250, blank=True, null=True)
    date_incorporation = models.CharField(max_length=30, blank=True, null=True)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    business_category = models.IntegerField(blank=True, null=True)
    business_sub_cat = models.IntegerField(blank=True, null=True)
    business_type = models.IntegerField(blank=True, null=True)
    official_web_link = models.CharField(max_length=100, blank=True, null=True)
    official_app_link = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profiles'


class UserSocialOthers(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    social_logo = models.CharField(max_length=250, blank=True, null=True)
    social_link_other = models.CharField(max_length=100, blank=True, null=True)
    social_name_other = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_social_others'


class UserSocials(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.IntegerField()
    instagram_link = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.CharField(max_length=100, blank=True, null=True)
    youtube_link = models.CharField(max_length=100, blank=True, null=True)
    linkedin_link = models.CharField(max_length=100, blank=True, null=True)
    threads_link = models.CharField(max_length=100, blank=True, null=True)
    twitter_link = models.CharField(max_length=100, blank=True, null=True)
    social_logo = models.CharField(max_length=250, blank=True, null=True)
    social_name = models.CharField(max_length=100, blank=True, null=True)
    social_link = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_socials'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.TextField(blank=True, null=True)
    role = models.SmallIntegerField(blank=True, null=True, db_comment='0= Admin, 1=agent,2=investor,3=business,4=customer, 5=employee')
    role_type = models.IntegerField(blank=True, null=True)
    employee_type = models.TextField(blank=True, null=True)
    employee_id = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    batch_number = models.BigIntegerField(blank=True, null=True)
    assigned_reporting_manager = models.TextField(blank=True, null=True)
    batch_timing = models.TextField(blank=True, null=True)
    age = models.BigIntegerField(blank=True, null=True)
    personal_mobile = models.BigIntegerField(blank=True, null=True)
    personal_email = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True, db_comment='1=MALE ,2=FEMALE ,3=OTHERS ')
    mobile = models.BigIntegerField(blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    is_verify = models.SmallIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    two_factor_secret = models.TextField(blank=True, null=True)
    two_factor_recovery_codes = models.TextField(blank=True, null=True)
    two_factor_confirmed_at = models.DateTimeField(blank=True, null=True)
    date_birth = models.CharField(max_length=30, blank=True, null=True)
    pincode = models.CharField(max_length=30, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    country_name = models.TextField(blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    state_name = models.TextField(blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    district_name = models.TextField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    city_name = models.TextField(blank=True, null=True)
    society_building = models.CharField(max_length=250, blank=True, null=True)
    flat_apartment = models.CharField(max_length=250, blank=True, null=True)
    landmark = models.CharField(max_length=250, blank=True, null=True)
    pan_num = models.CharField(max_length=30, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    referral_code = models.TextField(unique=True, blank=True, null=True)
    referral_from = models.TextField(blank=True, null=True)
    is_approved = models.CharField(max_length=8, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class WabpayModules(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wabpay_modules'


class Wishlists(models.Model):
    property_id = models.CharField(max_length=36, blank=True, null=True)
    user_id = models.CharField(max_length=36, blank=True, null=True)
    is_like = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wishlists'
