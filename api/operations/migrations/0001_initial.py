# Generated by Django 2.2.6 on 2021-06-28 06:39

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetLocationAssetListServiceHistories',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('service_history_type', models.CharField(blank=True, max_length=100)),
                ('effective_datetime', models.DateTimeField(auto_now=True)),
                ('start_date_time', models.DateTimeField(null=True)),
                ('end_date_time', models.DateTimeField(null=True)),
                ('comments', models.CharField(blank=True, max_length=100)),
                ('failure_type', models.CharField(blank=True, max_length=100)),
                ('failure_mode', models.CharField(blank=True, max_length=100)),
                ('failure_repair', models.CharField(blank=True, max_length=100)),
                ('failure_component', models.CharField(blank=True, max_length=100)),
                ('failure_root_cause', models.CharField(blank=True, max_length=100)),
                ('svc_hist_type_req_fl', models.CharField(blank=True, max_length=100)),
                ('downtime_reason', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetLocationAssetListServiceHistoriesInbound',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activityid', models.CharField(blank=True, max_length=100)),
                ('service_history_type', models.CharField(blank=True, max_length=100)),
                ('effective_datetime', models.DateTimeField(auto_now=True)),
                ('asset_id', models.CharField(blank=True, max_length=12)),
                ('start_date_time', models.DateTimeField(null=True)),
                ('end_date_time', models.DateTimeField(null=True)),
                ('comments', models.CharField(blank=True, max_length=100)),
                ('failure_type', models.CharField(blank=True, max_length=100)),
                ('failure_mode', models.CharField(blank=True, max_length=100)),
                ('failure_repair', models.CharField(blank=True, max_length=100)),
                ('failure_component', models.CharField(blank=True, max_length=100)),
                ('failure_root_cause', models.CharField(blank=True, max_length=100)),
                ('svc_hist_type_req_fl', models.CharField(blank=True, max_length=100)),
                ('downtime_reason', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='NA', max_length=100)),
                ('description', models.CharField(default='NA', max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-record_date'],
            },
        ),
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('costCenter', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('function', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='NA', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location_type', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('Bo', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MainOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('main_operation', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('serial_num', models.CharField(default='NA', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceManager',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('maintenance_manager', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('user_id', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('measurement_identifier', models.CharField(default='NA', max_length=100)),
                ('measurement_type', models.CharField(default='NA', max_length=100)),
                ('description', models.CharField(default='NA', max_length=255)),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-record_date'],
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('operation', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperationalReading',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('asset_id', models.CharField(blank=True, max_length=12)),
                ('badge_number', models.CharField(blank=True, max_length=100)),
                ('current_value', models.CharField(blank=True, max_length=100)),
                ('measurent_identifier', models.CharField(blank=True, max_length=100)),
                ('measurent_type', models.CharField(blank=True, max_length=100)),
                ('initial_value_flag', models.CharField(blank=True, max_length=100)),
                ('owning_organization', models.CharField(blank=True, max_length=100)),
                ('reading_datetime', models.DateTimeField(blank=True, null=True)),
                ('submitted_datetime', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OwningOrganization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='NA', max_length=100)),
                ('description', models.CharField(default='NA', max_length=255)),
                ('detail_description', models.TextField(default='NA')),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-record_date'],
            },
        ),
        migrations.CreateModel(
            name='Planner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('planner', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('user_id', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsValidValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('seq_valid', models.CharField(blank=True, max_length=100)),
                ('code_valid', models.CharField(blank=True, max_length=100)),
                ('short_text_valid', models.CharField(blank=True, max_length=100)),
                ('text_valid', models.CharField(blank=True, max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceHistoriesQuestions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('seq', models.CharField(blank=True, max_length=100)),
                ('code', models.CharField(blank=True, max_length=100)),
                ('short_text', models.CharField(blank=True, max_length=100)),
                ('text', models.CharField(blank=True, max_length=100)),
                ('style', models.CharField(blank=True, max_length=100)),
                ('respone', models.CharField(blank=True, max_length=100)),
                ('response_check_box', models.CharField(blank=True, max_length=100)),
                ('response_radio', models.CharField(blank=True, max_length=100)),
                ('responseDate', models.DateField(null=True)),
                ('response_datetime', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('service_hist_type', models.CharField(blank=True, max_length=100)),
                ('service_hist_desc', models.CharField(blank=True, max_length=225)),
                ('service_hist_bo', models.CharField(blank=True, max_length=100)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('service_hist_subclass', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceHistoryQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_seq', models.CharField(blank=True, max_length=100)),
                ('question_cd', models.CharField(blank=True, max_length=225)),
                ('question_desc', models.CharField(blank=True, max_length=225)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceHistoryQuestionValidValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer_seq', models.CharField(blank=True, max_length=100)),
                ('answer_cd', models.CharField(blank=True, max_length=225)),
                ('answer_desc', models.CharField(blank=True, max_length=225)),
                ('answer_text', models.CharField(blank=True, max_length=225)),
                ('point_value', models.CharField(blank=True, max_length=100)),
                ('style', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubFunction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sub_function', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkActivity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bo_status', models.CharField(default='NA', max_length=100)),
                ('required_by_date', models.DateField(default=datetime.date.today)),
                ('parent_location', models.CharField(default='NA', max_length=100)),
                ('activity_id', models.CharField(default='NA', max_length=50)),
                ('work_class', models.CharField(default='NA', max_length=100)),
                ('work_category', models.CharField(default='NA', max_length=100)),
                ('description', models.TextField(default='NA')),
                ('completion_date_time', models.DateTimeField(blank=True, null=True)),
                ('node_id', models.CharField(default='NA', max_length=12)),
                ('asset_id', models.CharField(default='NA', max_length=12)),
                ('asset_type', models.CharField(default='NA', max_length=50)),
                ('badge_number', models.CharField(default='NA', max_length=50)),
                ('serial_number', models.CharField(default='NA', max_length=50)),
                ('detailed_description', models.TextField(default='NA')),
                ('participation', models.CharField(default='NA', max_length=50)),
                ('service_history_type_dt', models.CharField(blank=True, default='NA', max_length=50)),
                ('effective_date_time_dt', models.DateTimeField(blank=True, null=True)),
                ('comments_dt', models.TextField(blank=True, default='NA')),
                ('start_date_time', models.DateTimeField(blank=True, null=True)),
                ('end_date_time', models.DateTimeField(blank=True, null=True)),
                ('downtime_reason', models.CharField(default='NA', max_length=50)),
                ('service_history_type_f', models.CharField(blank=True, default='NA', max_length=50)),
                ('effective_date_time_f', models.DateTimeField(blank=True, null=True)),
                ('comments_f', models.TextField(blank=True, default='NA')),
                ('failure_type', models.CharField(blank=True, default='NA', max_length=50)),
                ('failure_mode', models.CharField(blank=True, default='NA', max_length=50)),
                ('failure_repair', models.CharField(blank=True, default='NA', max_length=50)),
                ('failure_component', models.CharField(blank=True, default='NA', max_length=50)),
                ('failure_root_cause', models.TextField(blank=True, default='NA')),
                ('service_history_type_pm', models.CharField(default='NA', max_length=50)),
                ('effective_date_time_pm', models.DateTimeField(blank=True, null=True)),
                ('comments_pm', models.TextField(default='NA')),
                ('answer_1', models.CharField(blank=True, max_length=100)),
                ('answer_2', models.CharField(blank=True, max_length=100)),
                ('answer_3', models.CharField(blank=True, max_length=100)),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkActivityEmployee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkActivityTeam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('work_category', models.CharField(default='NA', max_length=100)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='WorkClass',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='NA', max_length=100)),
                ('description', models.CharField(default='NA', max_length=255)),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-record_date'],
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('wams_id', models.CharField(default='NA', max_length=100)),
                ('work_order_description', models.CharField(default='NA', max_length=100)),
                ('planner_cd', models.CharField(default='NA', max_length=100)),
                ('planner_name', models.CharField(default='NA', max_length=100)),
                ('work_order_no', models.CharField(default='NA', max_length=100)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrderActivityCompletion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activityid', models.CharField(blank=True, max_length=100)),
                ('completiondatetime', models.DateTimeField(auto_now=True)),
                ('bo_status_cd', models.CharField(blank=True, max_length=100)),
                ('user_id_1', models.CharField(blank=True, max_length=100)),
                ('act_type_cd', models.CharField(blank=True, max_length=100)),
                ('wo_id', models.CharField(blank=True, max_length=100)),
                ('act_dpos_flg', models.CharField(blank=True, max_length=100)),
                ('service_class_cd', models.CharField(blank=True, max_length=100)),
                ('requestor_id', models.CharField(blank=True, max_length=100)),
                ('required_by_dt', models.CharField(blank=True, max_length=100)),
                ('work_priority_flg', models.CharField(blank=True, max_length=100)),
                ('descr100', models.CharField(blank=True, max_length=225)),
                ('descrlong', models.CharField(blank=True, max_length=225)),
                ('w1_descr100_upr', models.CharField(blank=True, max_length=225)),
                ('held_for_parts_flg', models.CharField(blank=True, max_length=100)),
                ('anniversary_value', models.CharField(blank=True, max_length=100)),
                ('emergency_flg', models.CharField(blank=True, max_length=100)),
                ('act_num', models.CharField(blank=True, max_length=100)),
                ('planner_cd', models.CharField(blank=True, max_length=100)),
                ('total_priority', models.CharField(blank=True, max_length=100)),
                ('total_priority_src_flg', models.CharField(blank=True, max_length=100)),
                ('node_id_1', models.CharField(blank=True, max_length=12)),
                ('asset_id_1', models.CharField(blank=True, max_length=12)),
                ('percentage', models.CharField(blank=True, max_length=100)),
                ('seqno', models.CharField(blank=True, max_length=100)),
                ('participation_flg', models.CharField(blank=True, max_length=100)),
                ('cost_center_cd', models.CharField(blank=True, max_length=100)),
                ('percentage_2', models.CharField(blank=True, max_length=100)),
                ('act_resrc_reqmt_id', models.CharField(blank=True, max_length=100)),
                ('descrlong_1', models.CharField(blank=True, max_length=100)),
                ('resrc_src_flg', models.CharField(blank=True, max_length=100)),
                ('resrc_type_id', models.CharField(blank=True, max_length=100)),
                ('w1_quantity', models.CharField(blank=True, max_length=100)),
                ('unit_price', models.CharField(blank=True, max_length=100)),
                ('w1_duration', models.CharField(blank=True, max_length=100)),
                ('crew_shift_id', models.CharField(blank=True, max_length=100)),
                ('sched_duration', models.CharField(blank=True, max_length=100)),
                ('break_in_dttm', models.CharField(blank=True, max_length=100)),
                ('actvn_dttm', models.CharField(blank=True, max_length=100)),
                ('tmpl_act_id', models.CharField(blank=True, max_length=100)),
                ('maint_sched_id', models.CharField(blank=True, max_length=100)),
                ('maint_trigger_id', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('owning_organization', models.CharField(blank=True, max_length=100)),
                ('field_1', models.CharField(blank=True, max_length=100)),
                ('field_2', models.CharField(blank=True, max_length=100)),
                ('submitted_datetime', models.DateTimeField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrderActivityCompletionAssetLocationAssetList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('node_id', models.CharField(blank=True, max_length=12)),
                ('asset_id', models.CharField(blank=True, max_length=12)),
                ('participation', models.CharField(blank=True, max_length=100)),
                ('measurent_type', models.CharField(blank=True, max_length=100)),
                ('reading_type', models.CharField(blank=True, max_length=100)),
                ('current_value', models.CharField(blank=True, max_length=100)),
                ('asset_description', models.CharField(blank=True, max_length=100)),
                ('asset_type', models.CharField(blank=True, max_length=100)),
                ('reading_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrderActivityCompletionAssetLocationAssetListInbound',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('node_id', models.CharField(blank=True, max_length=12)),
                ('activityid', models.CharField(blank=True, max_length=100)),
                ('asset_id', models.CharField(blank=True, max_length=12)),
                ('participation', models.CharField(blank=True, max_length=100)),
                ('measurent_type', models.CharField(blank=True, max_length=100)),
                ('reading_type', models.CharField(blank=True, max_length=100)),
                ('current_value', models.CharField(blank=True, max_length=100)),
                ('asset_description', models.CharField(blank=True, max_length=100)),
                ('asset_type', models.CharField(blank=True, max_length=100)),
                ('reading_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('long_description', models.CharField(blank=True, max_length=250)),
                ('required_by_date', models.CharField(blank=True, max_length=100)),
                ('approval_profile', models.CharField(blank=True, max_length=100)),
                ('bo', models.CharField(blank=True, max_length=100)),
                ('creation_datetime', models.CharField(blank=True, max_length=100)),
                ('creation_user', models.CharField(blank=True, max_length=100)),
                ('downtime_start', models.CharField(blank=True, max_length=100)),
                ('planner', models.CharField(blank=True, max_length=100)),
                ('work_class', models.CharField(blank=True, max_length=100)),
                ('work_category', models.CharField(blank=True, max_length=100)),
                ('work_priority', models.CharField(blank=True, max_length=100)),
                ('requestor', models.CharField(blank=True, max_length=100)),
                ('owning_access_group', models.CharField(blank=True, max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('primary_phone', models.CharField(blank=True, max_length=100)),
                ('mobile_phone', models.CharField(blank=True, max_length=100)),
                ('home_phone', models.CharField(blank=True, max_length=100)),
                ('node_id', models.CharField(blank=True, max_length=12)),
                ('asset_id', models.CharField(blank=True, max_length=12)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('int10_type', models.CharField(blank=True, max_length=100)),
                ('work_request_id', models.CharField(blank=True, max_length=100)),
                ('work_request_status', models.CharField(blank=True, max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkRequestStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('work_request_id', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-record_date'],
            },
        ),
    ]
