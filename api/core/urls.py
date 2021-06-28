from datetime import datetime, timedelta

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.gis import admin

from django.urls import path

from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin

from django.views.generic import TemplateView, RedirectView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from users.views import (
    MyTokenObtainPairView,
    ActivateAccount
)

class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass

router = NestedDefaultRouter()

# Asset
from assets.views import (
    AssetViewSet,
    AssetRegistrationViewSet,AssetRegistrationBkViewSet,
    AssetGroupViewSet,
    AssetTypeViewSet,
    RfidViewSet,
    AssetBadgeFormatViewSet,
    AssetAttributeViewSet,
    AssetAttributeColumnViewSet,
    AssetLocationViewSet,
    AssetMeasurementTypeViewSet,
    AssetLocationSyncViewSet,
    AssetAttributeFieldViewSet,
    AssetMeasurementTypeInboundViewSet,
    AssetAttributeInboundViewSet,
    AssetServiceHistoryViewSet,
    AssetMaintenanceSpecViewSet,
    AssetAttributeReferenceViewSet,
    AssetAttributePredefineViewSet
)

assets_router = router.register(
    'assets', AssetViewSet
)

assets_badge_format_router = router.register(
    'asset-badge-format', AssetBadgeFormatViewSet
)
assets_attribute_router = router.register( 'asset-attribute', AssetAttributeViewSet)
asset_groups_router = router.register(
    'asset-groups', AssetGroupViewSet
)

asset_types_router = router.register(
    'asset-types', AssetTypeViewSet
)

rfids_router = router.register(
    'rfids', RfidViewSet
)

assets_registration_router = router.register(
    'asset-registration', AssetRegistrationViewSet
)

assets_registration_bk_router = router.register(
    'asset-registration-bk', AssetRegistrationBkViewSet
)

assets_attribute_column_router = router.register(
    'asset-attribute-column', AssetAttributeColumnViewSet
)

assets_location_router = router.register(
    'asset-location', AssetLocationViewSet
)

assets_measurement_type_router = router.register(
    'asset-measurement-type', AssetMeasurementTypeViewSet
)

asset_location_sync_router = router.register(
    'asset-location-sync', AssetLocationSyncViewSet
)

asset_attribute_field_router = router.register(
    'asset-attribute-field', AssetAttributeFieldViewSet
)

asset_measurement_type_inbound_router = router.register(
    'asset-measurement-type-inbound',AssetMeasurementTypeInboundViewSet
)

asset_attribute_inbound_router = router.register(
    'asset-attribute-inbound', AssetAttributeInboundViewSet
)

asset_service_history = router.register(
    'asset-service-history', AssetServiceHistoryViewSet
)

asset_maintenance_spec = router.register(
    'asset-maintenance-spec', AssetMaintenanceSpecViewSet
)

asset_attribute_reference = router.register(
    'asset-attribute-reference', AssetAttributeReferenceViewSet
)

asset_attribute_predefine = router.register(
    'asset-attribute-predefine', AssetAttributePredefineViewSet
)



# Locations app
from locations.views import (
    RegionViewSet,
    StoreViewSet,
    LocationViewSet,
    StateViewSet
)

regions_router = router.register(
    'regions', RegionViewSet
)

stores_router = router.register(
    'stores', StoreViewSet
)

locations_router = router.register(
    'locations', LocationViewSet
)

states_router = router.register(
    'states', StateViewSet
)

# Medias app
from medias.views import (
    MediaViewSet
)

medias_router = router.register(
    'medias', MediaViewSet
)

# Notifications app
from notifications.views import (
    NotificationViewSet
)

notifications_router = router.register(
    'notifications', NotificationViewSet
)

# Operations app
from operations.views import (
    OwningOrganizationViewSet,
    BoViewSet,
    IssueTypeViewSet,
    MaintenanceViewSet,
    OperationalReadingViewSet,
    WorkOrderViewSet,
    WorkActivityViewSet,
    WorkActivityTeamViewSet,
    WorkClassViewSet,
    WorkCategoryViewSet,
    WorkRequestViewSet,
    WorkRequestStatusViewSet,
    MeasurementTypeViewSet,
    WorkOrderActivityCompletionAssetLocationAssetListViewSet,
    AssetLocationAssetListServiceHistoriesViewSet,
    ServiceHistoriesQuestionsViewSet,
    QuestionsValidValueViewSet,
    WorkOrderActivityCompletionViewSet,
    ServiceHistoryViewSet,ServiceHistoryQuestionViewSet,ServiceHistoryQuestionValidValueViewSet,
    PlannerViewSet,MaintenanceManagerViewSet,WorkRequestViewSet,MainOperationViewSet,FunctionViewSet,LocationTypeViewSet,
    SubFunctionViewSet,CostCenterViewSet,OperationViewSet,WorkActivityEmployeeViewSet,
    WorkOrderActivityCompletionAssetLocationAssetListInboundViewSet,
    AssetLocationAssetListServiceHistoriesInboundViewSet,
    # WorkOrderActivityCompletionPipeViewSet,
    OperationalReadingPipeViewSet,
    WorkRequestPipeViewSet
)

service_history_router = router.register(
    'service-history', ServiceHistoryViewSet
)
service_history_question_router = router.register(
    'service-history-question', ServiceHistoryQuestionViewSet
)
service_history_question_valid_value_router = router.register(
    'service-history-question-valid-value', ServiceHistoryQuestionValidValueViewSet
)
planner_router = router.register(
    'planner', PlannerViewSet
)
maintenance_manager_router = router.register(
    'maintenance-manager', MaintenanceManagerViewSet
)
work_request_router = router.register(
    'work-request', WorkRequestViewSet
)
work_requests_pipe_router = router.register(
    'work-request-pipe', WorkRequestPipeViewSet
)
main_operation_router = router.register(
    'main-operation-organizations', MainOperationViewSet
)
function_router = router.register(
    'function', FunctionViewSet
)
location_type_router = router.register(
    'location-type', LocationTypeViewSet
)
sub_function_router = router.register(
    'sub-function', SubFunctionViewSet
)
cost_center_router = router.register(
    'cost-center', CostCenterViewSet
)
operation_router = router.register(
    'operation', OperationViewSet
)


owning_organizations_router = router.register(
    'owning-organizations', OwningOrganizationViewSet
)

bos_router = router.register(
    'bos', BoViewSet
)

issue_types_router = router.register(
    'issue-types', IssueTypeViewSet
)

maintenances_router = router.register(
    'maintenances', MaintenanceViewSet
)

operational_readings_router = router.register(
    'operational-readings', OperationalReadingViewSet
)

operational_readings_pipe_router = router.register(
    'operational-readings-pipe', OperationalReadingPipeViewSet
)

work_orders_router = router.register(
    'work-orders', WorkOrderViewSet
)

work_activities_router = router.register(
    'work-activities', WorkActivityViewSet
)

work_activity_teams_router = router.register(
    'work-activity-teams', WorkActivityTeamViewSet
)

work_classes_router = router.register(
    'work-classes', WorkClassViewSet
)

work_categories_router = router.register(
    'work-categories', WorkCategoryViewSet
)

work_requests_router = router.register(
    'work-requests', WorkRequestViewSet
)

work_request_statuses_router = router.register(
    'work-request-statuses', WorkRequestStatusViewSet
)
measurement_types_router = router.register(
    'measurement-types', MeasurementTypeViewSet
)
work_activity_employee_router = router.register(
    'work-activity-employee', WorkActivityEmployeeViewSet
)


#### dopied from dev aoi

work_order_activity_completion_router = router.register(
    'work-order-activity-completion', WorkOrderActivityCompletionViewSet
)

# work_order_activity_completion_pipe_router = router.register(
#     'work-order-activity-completion-pipe', WorkOrderActivityCompletionPipeViewSet
# )

work_order_activity_completion_asset_location_asset_list_router = router.register(
    'work-order-activity-completion-asset-location-asset-list', WorkOrderActivityCompletionAssetLocationAssetListViewSet
)

asset_location_asset_list_service_histories_router = router.register(
    'asset-location-asset-list-service-histories', AssetLocationAssetListServiceHistoriesViewSet
)

work_order_activity_completion_asset_location_asset_list_inbound_router = router.register(
    'work-order-activity-completion-asset-location-asset-list-inbound', WorkOrderActivityCompletionAssetLocationAssetListInboundViewSet
)

asset_location_asset_list_service_histories_inbound_router = router.register(
    'asset-location-asset-list-service-histories-inbound', AssetLocationAssetListServiceHistoriesInboundViewSet
)

service_histories_questions_router = router.register(
    'service-histories-questions', ServiceHistoriesQuestionsViewSet
)

questions_valid_value_router = router.register(
    'questions-value-valid', QuestionsValidValueViewSet
)

# Organisations app
from organisations.views import (
    OrganisationViewSet
)

organisations_router = router.register(
    'organisations', OrganisationViewSet
)

# Stock
from stocks.views import (
    StockViewSet,
    ReceiveViewSet,
    IssuanceViewSet,
    ReturnViewSet,
    PurchaseViewSet,
    DisposeViewSet,
    ReversalViewSet,
    TransferViewSet,
    CountViewSet
)

stocks_router = router.register(
    'stocks', StockViewSet
)

receives_router = router.register(
    'stock-receives', ReceiveViewSet
)

issuances_router = router.register(
    'stock-issuances', IssuanceViewSet
)

returns_router = router.register(
    'stock-returns', ReturnViewSet
)

purchases_router = router.register(
    'stock-purchases', PurchaseViewSet
)

disposes_router = router.register(
    'stock-disposes', DisposeViewSet
)

reversals_router = router.register(
    'stock-reversals', ReversalViewSet
)

transfers_router = router.register(
    'stock-transfers', TransferViewSet
)

counts_router = router.register(
    'stock-counts', CountViewSet
)

# Users app
from users.views import (
    CustomUserViewSet
)

users_router = router.register(
    'users', CustomUserViewSet
)

# Wams app
from wams.views import (
    WamsViewSet
)

wams_router = router.register(
    'wams', WamsViewSet
)

# inventory app
from inventory.views import (
    InventoryItemViewSet,
    # InventoryItemUomIntraViewSet,
    # InventoryItemUomInterViewSet,
    InventoryPurchaseOrderViewSet,
    InventoryGrnViewSet,
    InventoryTransactionViewSet,
    InventoryMaterialViewSet
)

item_router = router.register(
    'inventory-item', InventoryItemViewSet
)

# item_intra_router = router.register(
#     'inventory-item-intra', InventoryItemUomIntraViewSet
# )

# item_inter_router = router.register(
#     'inventory-item-inter', InventoryItemUomInterViewSet
# )

purchase_order_router = router.register(
    'inventory-purchase-order', InventoryPurchaseOrderViewSet
)

grn_router = router.register(
    'inventory-grn', InventoryGrnViewSet
)

transaction_router = router.register(
    'inventory-transaction', InventoryTransactionViewSet
)

material_request_router = router.register(
    'inventory-material-request', InventoryMaterialViewSet
)

## employee app
from employee.views import (
    EmployeeViewSet,FailureProfileViewSet,ApprovalProfileViewSet,ContactInformationViewSet
)

employee_router = router.register(
    'employee', EmployeeViewSet
)

failure_profile_router = router.register(
    'failure-profile', FailureProfileViewSet
)

approval_profile_router = router.register(
    'approval-profile', ApprovalProfileViewSet
)

contact_information_router = router.register(
    'contact-information', ContactInformationViewSet
)


## audit_trail app
from audit_trail.views import (
    AuditTrailViewSet,
)

audit_trail_router = router.register(
    'audit_trail', AuditTrailViewSet,
)

############################################# url

urlpatterns = [
    url(r'^email-verification/$',
        TemplateView.as_view(template_name="email_verification.html"),
        name='email-verification'), # Tukar sini
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'
    ),
    url(r'v1/', include(router.urls)),
    url(r'auth/', include('rest_auth.urls')),
    url(r'auth/registration/', include('rest_auth.registration.urls')),

    url('auth/obtain/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # url for account activation via token
    #path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    #url('activate_account/<slug:uidb64>/<slug:token>/', ActivateAccount.as_view(), name='activate_account')
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                ActivateAccount.as_view(), name='activate'),

]
