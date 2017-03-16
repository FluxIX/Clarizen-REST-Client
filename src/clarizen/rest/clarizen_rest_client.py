from enum import Enum
import json
import requests

from .exceptions import ApiConnectionError, ApiServerError, AuthenticationError, LocationError
from .queries.condition.condition import ConditionFormat
from .queries.utils import QueryUtilities
from .utils import url_join

class _ApiUrls( Enum ):
   GetServerDefinition = "authentication/getServerDefinition"
   GetSessionInformation = "authentication/getSessionInfo"
   Login = "authentication/login"
   Logout = "authentication/logout"
   Metadata_GetEntities = "metadata/listEntities"
   Metadata_DescribeEntities = "metadata/describeEntities"
   Metadata_DescribeEntityRelations = "metadata/describeEntityRelations"
   Metadata_DescribeMetadata = "metadata/describeMetadata"
   Metadata_GetSystemSettingsValues = "metadata/getSystemSettingsValues"
   Metadata_SetSystemSettingsValues = "metadata/setSystemSettingsValues"
   EntityQuery = "data/entityQuery"
   Objects = "data/objects"
   UserQuery = "data/findUserQuery"
   ChangeEntityState = "data/changeState"
   ExpenseQuery = "data/expenseQuery"
   TimesheetQuery = "data/timesheetQuery"
   FileDownload = "files/download"

class Locations( object ):
   def __init__( self, server_location, app_location ):
      self._server_location = server_location
      self._app_location = app_location

   @property
   def server_location( self ):
      return self._server_location

   @property
   def app_location( self ):
      return self._app_location

class ClarizenRestClient( object ):
   class FieldSelection( Enum ):
      All = 0

   def __init__( self, username, password, base_api_directory_url = "https://api.clarizen.com/v2.0/services/", **kwargs ):
      self._base_apt_directory_url = base_api_directory_url

      self._clear()

      self._username = username
      self._password = password

   def __enter__( self ):
      return self

   def __exit__( self, type, value, traceback ):
      if self.logged_in:
         self.logout()

   @property
   def locations( self ):
      return self._locations

   @property
   def has_locations( self ):
      return self.locations is not None

   @property
   def username( self ):
      return self._username

   @property
   def session_id( self ):
      return self._session_id

   @property
   def user_id( self ):
      return self._user_id

   @property
   def organization_id( self ):
      return self._organization_id

   @property
   def license_type( self ):
      return self._license_type

   @property
   def logged_in( self ):
      return self.session_id is not None

   @property
   def _session_header( self ):
      if self.logged_in:
         result = { "Authorization": "Session {}".format( self.session_id ) }
      else:
         result = {}

      return result

   def _clear( self ):
      self._locations = None
      self._session_id = None
      self._user_id = None
      self._organization_id = None
      self._license_type = None

   def _append_session_header( self, **kwargs ):
      if "headers" not in kwargs:
         kwargs[ "headers" ] = self._session_header

      return kwargs

   def _get_api_result( self, response ):
      if response.status_code == 200:
         return json.loads( response.text )
      elif response.status_code >= 500:
         raise ApiServerError( response.text )
      else:
         raise ApiConnectionError( response.status_code )

   def get_type_fields( self, entity ):
      desc = self.meta__describe_entities( entity )[ 0 ]

      result = [ field[ "name" ] for field in desc[ "fields" ] if "name" in field ]

      return result

   def get_server_definition( self, **kwargs ):
      login_data = { "userName": self.username, "password": self._password }
      response = requests.post( url_join( self._base_apt_directory_url, _ApiUrls.GetServerDefinition.value ), data = login_data, **kwargs )

      result = response.status_code == 200
      if result:
         payload = json.loads( response.text )

         self._locations = Locations( payload[ "serverLocation" ], payload[ "appLocation" ] )

      return result

   def login( self, **kwargs ):
      if self.has_locations or self.get_server_definition():
         login_data = { "userName": self.username, "password": self._password }
         response = requests.post( url_join( self.locations.server_location, _ApiUrls.Login.value ), data = login_data, **kwargs )

         result = response.status_code == 200
         if result:
            payload = json.loads( response.text )

            self._session_id = payload[ "sessionId" ]
            self._user_id = payload[ "userId" ]
            self._organization_id = payload[ "organizationId" ]
            self._license_type = payload[ "licenseType" ]

         return result
      else:
         raise LocationError()

   def logout( self, **kwargs ):
      if self.logged_in:
         kwargs = self._append_session_header( **kwargs )
         response = requests.get( url_join( self.locations.server_location, _ApiUrls.Logout.value ), **kwargs )

         result = response.status_code == 200
         if result:
            self._clear()
      else:
         result = True

      return result

   def get_session_information( self, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         kwargs = self._append_session_header( **kwargs )
         response = requests.post( url_join( self.locations.server_location, _ApiUrls.GetSessionInformation.value ), **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

   def meta__get_entities( self, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         kwargs = self._append_session_header( **kwargs )
         response = requests.get( url_join( self.locations.server_location, _ApiUrls.Metadata_GetEntities.value ), **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

      # Example response text: '{"typeNames":["Note","Post","Email","Comment","Template","PushNotification","Data","WorkByDay","ResourceCalendarExceptionAbsolute","ResourceCalendarExceptionRelative","ResourceCalendarException","ReportShortcutLink","ReportsHierarchyLink","ReportsFolderContentLink","FolderContentLink","Dashboard","Report","ReportAndDashboard","FolderForReport","FoldersAndReports","DependencyLink","IntegrationsRegistry","TopicDocumentLink","TopicDiscussionLink","TopicGroupLink","TopicExpenseEntryLink","TopicExpenseSheetLink","TopicCustomerLink","TopicCaseLink","TopicWorkItemLink","TopicLink","Milestone","Task","RecurringTask","GenericTask","PlanningComponent","Project","WorkItem","Topic","Following","Like","ReportDiscussionLink","UserReportDiscussionLink","SystemReportDiscussionLink","ExpenseEntryDiscussionLink","ExpenseSheetDiscussionLink","CustomerDiscussionLink","CaseDiscussionLink","WorkItemDiscussionLink","DiscussionLink","DiscussionReply","DiscussionPost","DiscussionMessage","GroupTaskLink","GroupProjectLink","GroupCaseLink","GroupCustomerLink","GroupLink","Document","RecycleBinItems","Stopwatch","ProfileLink","SubGroupHierarchyLink","GroupMembershipLink","GroupHierarchyLink","SkillLink","MembershipLink","WorkItemAttachmentLink","DashboardAttachmentLink","ReportAttachmentLink","UserAttachmentLink","ExpenseSheetAttachmentLink","CustomerAttachmentLink","DiscussionMessageAttachmentLink","ResourceGroupEntityAttachmentLink","IssueAttachmentLink","ExpenseEntryAttachmentLink","AttachmentLink","AdditionalManagerLink","OwnerLink","ManagerResourceLink","RegularResourceLink","ReviewerLink","WorkItemTeamLink","JobTitleRateLink","ResourceLink","ProgressImpactLink","RealWorkItemHierarchyLink","ShortcutLink","BaseWorkItemHierarchyLink","WorkItemHierarchyLink","SchedulingType","CurrencyType","TrackStatus","GeographicalRegion","ResourceUtilizationCategory","InvestmentType","PackagedObjectCategory","NotifyUsers","EditorsMode","ManagerRole","DataObjectType","NumericFormat","Role","DashboardStatus","UserShortcut","IntegrationAuthenticationType","AuthorizationGroup","CustomIcon","ProofAlert","ProofRole","TriggeredBy","SyncStatus","ReplyMarkedType","CompanySize","CustomerSuccessStatus","Industry","Tier","AccountStatus","LicenseType","StorageType","ProjectSize","PostState","PostType","DiscussionEmailNotifications","CompletenessRole","SpecialRole","FileType","WidgetType","CreatorType","StopwatchAggregateState","CommentType","StopwatchState","MilestoneType","Region","Phase","Package","CaseBusinessImpact","State","TaskReportingPolicy","CaseState","ChargedType","RequestType","RiskImpact","RisksRate","BusinessImpact","ExceptionType","ObjectAccessType","Months","WeekDays","RiskState","DependencyType","Pending","Severity","WorkPolicy","DocumentType","RecipientType","TaskType","RateType","ResourceRole","Importance","Language","RecurrenceType","CommitLevel","CountryState","ReportExtensionType","ProjectType","BudgetStatus","Countries","ImportedFrom","TimeZone","Widget","CaseCustomerLink","IssueTeamMembers","RelatedWork","EnhancementRequest","Bug","Risk","Issue","Case","Expense","ExpenseSheet","CurrencyExchangeRate","EmailRecipient","CustomerLink","ContactPerson","Customer","Rate","Timesheet","User","Profile","DiscussionGroup","UserGroup","Group","Skill","JobTitle","ResourceGroupEntity","ResourceEntity","Organization","ExpenseCategory","C_ProjectBb7_Status","C_ProjectProposal_Status","C_ProjectProject_review_state","C_ProjectOddsofCaptureList","C_ProjectProjectScale","C_WorkItemCLZ_TeamBoardState_CLZ","C_WorkItemCLZ_TeamTaskColor_CLZ","C_WorkItemCLZ_TeamBoardType_CLZ","C_WorkItemCLZ_TeamBoardStatusIcon_CLZ","C_OrganizationCustomTimesheetReminderPreference","C_ProjectProductClass","C_UserGroupName","C_UserIn","C_UserRecieveTextMessages","C_UserCarrier","C_ProjectClientTier"]}'

   def meta__describe_entities( self, *entity_types, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         entities_type_parameter = QueryUtilities.get_list_parameter( *entity_types )

         kwargs = self._append_session_header( **kwargs )
         response = requests.get( url_join( self.locations.server_location, _ApiUrls.Metadata_DescribeEntities.value ), params = { "typeNames": entities_type_parameter }, **kwargs )
         result = self._get_api_result( response )[ "entityDescriptions" ]

         return result
      else:
         raise AuthenticationError( self.username )

      # Example response text: '{"entityDescriptions":[{"typeName":"Report","fields":[{"referencedEntities":["User"],"name":"CreatedBy","type":"Entity","presentationType":"ReferenceToObject","label":"Created By","defaultValue":{"id":"/User/e676545a-606f-41c2-86a0-447513714402","DisplayName":"Chris Herrick"},"system":true,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"EntityFieldDescription"},{"name":"CreatedOn","type":"DateTime","presentationType":"Date","label":"Created On","system":true,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"FieldDescription"},{"referencedEntities":["User"],"name":"LastUpdatedBy","type":"Entity","presentationType":"ReferenceToObject","label":"Last Updated By","defaultValue":{"id":"/User/e676545a-606f-41c2-86a0-447513714402","DisplayName":"Chris Herrick"},"system":true,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"EntityFieldDescription"},{"name":"LastUpdatedOn","type":"DateTime","presentationType":"Date","label":"Last Updated On","system":true,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"FieldDescription"},{"name":"LastUpdatedBySystemOn","type":"DateTime","presentationType":"Date","label":"System Last Updated On","system":true,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"referencedEntities":[],"name":"EntityType","type":"Entity","presentationType":"ReferenceToObject","label":"Entity Type","system":true,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"EntityFieldDescription"},{"name":"Name","type":"String","presentationType":"Text","label":"Name","system":false,"calculated":false,"nullable":false,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"maxLength":256,"_type":"FieldDescription"},{"name":"Description","type":"String","presentationType":"TextArea","label":"Description","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":false,"maxLength":512,"_type":"FieldDescription"},{"name":"ExternalID","type":"String","presentationType":"Text","label":"External ID","defaultValue":"52addh2r837x66lsoixv1lbgm1817","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"maxLength":40,"_type":"FieldDescription"},{"name":"ImageUrl","type":"String","presentationType":"Text","label":"ImageUrl","defaultValue":"https://app2.clarizen.com/Clarizen/Media/35.1495384.0-6B0014B2C5FBC03B4E6FAD28D9A4B488E5AA9D0C/Image.gif","system":true,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":false,"maxLength":256,"_type":"FieldDescription"},{"name":"SYSID","type":"String","presentationType":"Text","label":"ID","system":false,"calculated":true,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"maxLength":40,"_type":"FieldDescription"},{"referencedEntities":["User"],"name":"EntityOwner","type":"Entity","presentationType":"ReferenceToObject","label":"Entity Owner","system":false,"calculated":false,"nullable":false,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"EntityFieldDescription"},{"name":"AttachmentsCount","type":"Integer","presentationType":"Other","label":"# of Attachments","defaultValue":0,"system":false,"calculated":true,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"FieldDescription"},{"name":"Scheduled","type":"Boolean","presentationType":"Checkbox","label":"Scheduled","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"FieldDescription"},{"name":"SchedulerPreferredTime","type":"Integer","presentationType":"Numeric","label":"Scheduler Preferred Time","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"SchedulerNotificationType","type":"Integer","presentationType":"Numeric","label":"Scheduler Notification Type","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"SchedulerTo","type":"String","presentationType":"TextArea","label":"Scheduler To","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":false,"maxLength":-1,"_type":"FieldDescription"},{"name":"SchedulerCc","type":"String","presentationType":"TextArea","label":"Scheduler Cc","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":false,"maxLength":-1,"_type":"FieldDescription"},{"name":"SchedulerNotificationSubject","type":"String","presentationType":"Text","label":"Scheduler Notification Subject","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"maxLength":256,"_type":"FieldDescription"},{"name":"SchedulerNotificationBody","type":"String","presentationType":"RichText","label":"Scheduler Notification Body","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"maxLength":-1,"_type":"FieldDescription"},{"name":"SchedulerPostTopics","type":"String","presentationType":"Text","label":"Scheduler Post Topics","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"maxLength":256,"_type":"FieldDescription"},{"name":"SchedulerPostNotifiers","type":"String","presentationType":"Text","label":"Scheduler Post Notifiers","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"maxLength":256,"_type":"FieldDescription"},{"name":"SchedulerSaveExportedData","type":"Boolean","presentationType":"Checkbox","label":"Scheduler Save Exported Data","defaultValue":false,"system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"FieldDescription"},{"referencedEntities":["ReportExtensionType"],"name":"SchedulerExportAs","type":"Entity","presentationType":"PickList","label":"Scheduler Export As","defaultValue":{"id":"/ReportExtensionType/CSV","Name":"CSV"},"system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":false,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"EntityFieldDescription"},{"referencedEntities":["RecurrenceType"],"name":"RecurrenceType","type":"Entity","presentationType":"PickList","label":"Recurrence","defaultValue":{"id":"/RecurrenceType/Not recurring","Name":"Not recurring"},"system":false,"calculated":false,"nullable":false,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"EntityFieldDescription"},{"name":"RecurrenceInterval","type":"Integer","presentationType":"Numeric","label":"Period of Recurrence","defaultValue":1,"system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"WorkdaysOnly","type":"Boolean","presentationType":"Checkbox","label":"Daily Recurrence - Working days","defaultValue":false,"system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"WeekDays","type":"Integer","presentationType":"Numeric","label":"Weekly Recurrence at Days","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"RecurrenceDayOfMonth","type":"Integer","presentationType":"Numeric","label":"Recurrence at Date","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"referencedEntities":["Months"],"name":"RecurrenceMonthOfYear","type":"Entity","presentationType":"PickList","label":"Month","defaultValue":{"id":"/Months/January","Name":"January"},"system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"EntityFieldDescription"},{"name":"RecurrenceStartDate","type":"Date","presentationType":"Date","label":"Start date","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"RecurrenceEndDate","type":"Date","presentationType":"Date","label":"End date","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"OccurenceDuration","type":"Duration","presentationType":"Duration","label":"Occurence Duration","defaultValue":{"unit":"Days","value":1.0},"system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"Occurrences","type":"Integer","presentationType":"Numeric","label":"Occurrences","system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":true,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":false,"sortable":true,"_type":"FieldDescription"},{"name":"EmailsCount","type":"Integer","presentationType":"Other","label":"# of Emails","defaultValue":0,"system":false,"calculated":true,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"FieldDescription"},{"name":"Editable","type":"Boolean","presentationType":"Checkbox","label":"Configurable","defaultValue":true,"system":false,"calculated":false,"nullable":true,"createOnly":false,"updateable":false,"internal":false,"custom":false,"visible":true,"decimalPlaces":0,"filterable":true,"sortable":true,"_type":"FieldDescription"}],"validStates":[],"label":"Report","labelPlural":"Reports","parentEntity":"ReportAndDashboard","displayField":"Name"}]}'

   def meta__describe_entity_relations( self, *entity_types, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         entities_type_parameter = QueryUtilities.get_list_parameter( *entity_types )

         kwargs = self._append_session_header( **kwargs )
         response = requests.post( url_join( self.locations.server_location, _ApiUrls.Metadata_DescribeEntityRelations.value ), data = { "typeNames": entities_type_parameter }, **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

   def meta__describe_metadata( self, *entity_types, flags = [], **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         entities_type_parameter = QueryUtilities.get_list_parameter( *entity_types )
         flags_parameter = QueryUtilities.get_list_parameter( *flags )

         kwargs = self._append_session_header( **kwargs )
         response = requests.get( url_join( self.locations.server_location, _ApiUrls.Metadata_DescribeEntityRelations.value ), params = { "typeNames": entities_type_parameter, "flags": flags_parameter }, **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

   def meta__get_system_settings_values( self, *entity_types, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         entities_type_parameter = QueryUtilities.get_list_parameter( *entity_types )

         kwargs = self._append_session_header( **kwargs )
         response = requests.get( url_join( self.locations.server_location, _ApiUrls.Metadata_GetSystemSettingsValues.value ), params = { "typeNames": entities_type_parameter }, **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

   def meta__set_system_settings_values( self, fields = None, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         data = {}
         if fields is not None and len( fields ) > 0:
            data[ "settings" ] = QueryUtilities.get_list_parameter( [ "{}:{}".format( key, fields[ key ] ) for key in fields ] )

         kwargs = self._append_session_header( **kwargs )
         response = requests.post( url_join( self.locations.server_location, _ApiUrls.Metadata_SetSystemSettingsValues.value ), data = data, **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

   def query_entities( self, entity_type, fields = None, order_by = None, where = None, relations = None, deleted = False, paging = None, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         parameters = { "typeName": entity_type }

         if fields is not None:
            if fields == ClarizenRestClient.FieldSelection.All:
               fields = self.get_type_fields( entity_type )

            param = QueryUtilities.get_fields_parameter( fields )
            if param is not None:
               parameters[ "fields" ] = param

         if order_by is not None and len( order_by ) > 0:
            parameters[ "orders" ] = [ { "fieldName": key, "order": value } for key, value in order_by ]

         if where is not None:
            parameters[ "where" ] = where.to_json( ConditionFormat.Json_bin )

         if relations is not None and len( relations ) > 0:
            parameters[ "relations" ] = [ relation.to_json() for relation in relations ]

         parameters[ "deleted" ] = deleted

         retrieve_all_records = paging is None or len( paging ) == 0
         if not retrieve_all_records:
            parameters[ "paging" ] = paging

         kwargs = self._append_session_header( **kwargs )

         records = []
         has_more_records = True
         while has_more_records:
            response = requests.get( url_join( self.locations.server_location, _ApiUrls.EntityQuery.value ), params = parameters, **kwargs )
            api_result = self._get_api_result( response )

            records.extend( api_result[ "entities" ] )

            result_paging = api_result[ "paging" ]
            has_more_records = retrieve_all_records and result_paging[ "hasMore" ]
            if has_more_records:
               parameters[ "paging" ] = result_paging

         return records
      else:
         raise AuthenticationError( self.username )

   def query_users( self, *fields, first_name = None, last_name = None, email_address = None, fuzzy_search = False, include_suspended = False, order_by = None, paging = None, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         parameters = { "fuzzySearchUserName": fuzzy_search, "includeSuspendedUsers": include_suspended }

         if first_name is not None and len( first_name ) > 0:
            parameters[ "firstName" ] = first_name

         if last_name is not None and len( last_name ) > 0:
            parameters[ "lastName" ] = last_name

         if email_address is not None and len( email_address ) > 0:
            parameters[ "eMail" ] = email_address

         if fields is not None:
            param = QueryUtilities.get_fields_parameter( fields )
            if param is not None:
               parameters[ "fields" ] = param

         if order_by is not None and len( order_by ) > 0:
            parameters[ "orders" ] = [ { "fieldName": key, "order": value } for key, value in order_by ]

         retrieve_all_records = paging is None or len( paging ) == 0
         if not retrieve_all_records:
            parameters[ "paging" ] = paging

         kwargs = self._append_session_header( **kwargs )

         records = []
         has_more_records = True
         while has_more_records:
            response = requests.post( url_join( self.locations.server_location, _ApiUrls.UserQuery.value ), data = parameters, **kwargs )
            api_result = self._get_api_result( response )

            records.extend( api_result[ "entities" ] )

            result_paging = api_result[ "paging" ]
            has_more_records = retrieve_all_records and result_paging[ "hasMore" ]
            if has_more_records:
               parameters[ "paging" ] = result_paging

         return records
      else:
         raise AuthenticationError( self.username )

   def query_expenses( self, entity_type, project_id = None, customer_id = None, fields = None, order_by = None, where = None, relations = None, deleted = False, paging = None, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         parameters = { "typeName": entity_type }

         if project_id is not None:
            parameters[ "projectId" ] = project_id

         if customer_id is not None:
            parameters[ "customerId" ] = customer_id

         if fields is not None:
            if fields == ClarizenRestClient.FieldSelection.All:
               fields = self.get_type_fields( entity_type )

            param = QueryUtilities.get_fields_parameter( fields )
            if param is not None:
               parameters[ "fields" ] = param

         if order_by is not None and len( order_by ) > 0:
            parameters[ "orders" ] = [ { "fieldName": key, "order": value } for key, value in order_by ]

         if where is not None:
            parameters[ "where" ] = where.to_json( ConditionFormat.Json_bin )

         if relations is not None and len( relations ) > 0:
            parameters[ "relations" ] = [ relation.to_json() for relation in relations ]

         parameters[ "deleted" ] = deleted

         retrieve_all_records = paging is None or len( paging ) == 0
         if not retrieve_all_records:
            parameters[ "paging" ] = paging

         kwargs = self._append_session_header( **kwargs )

         records = []
         has_more_records = True
         while has_more_records:
            response = requests.get( url_join( self.locations.server_location, _ApiUrls.ExpenseQuery.value ), params = parameters, **kwargs )
            api_result = self._get_api_result( response )

            records.extend( api_result[ "entities" ] )

            result_paging = api_result[ "paging" ]
            has_more_records = retrieve_all_records and result_paging[ "hasMore" ]
            if has_more_records:
               parameters[ "paging" ] = result_paging

         return records
      else:
         raise AuthenticationError( self.username )

   def query_timesheet( self, entity_type, project_id = None, customer_id = None, user_is_approver = False, work_item_ids = None, timesheet_state = None, fields = None, order_by = None, where = None, relations = None, deleted = False, paging = None, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         parameters = { "typeName": entity_type, "iAmTheApprover": user_is_approver }

         if project_id is not None:
            parameters[ "projectId" ] = project_id

         if customer_id is not None:
            parameters[ "customerId" ] = customer_id

         if work_item_ids is not None and len( work_item_ids ) > 0:
            parameters[ "workItems" ] = work_item_ids

         if timesheet_state is not None:
            parameters[ "timesheetState" ] = timesheet_state.value

         if fields is not None:
            if fields == ClarizenRestClient.FieldSelection.All:
               fields = self.get_type_fields( entity_type )

            param = QueryUtilities.get_fields_parameter( fields )
            if param is not None:
               parameters[ "fields" ] = param

         if order_by is not None and len( order_by ) > 0:
            parameters[ "orders" ] = [ { "fieldName": key, "order": value } for key, value in order_by ]

         if where is not None:
            parameters[ "where" ] = where.to_json( ConditionFormat.Json_bin )

         if relations is not None and len( relations ) > 0:
            parameters[ "relations" ] = [ relation.to_json() for relation in relations ]

         parameters[ "deleted" ] = deleted

         retrieve_all_records = paging is None or len( paging ) == 0
         if not retrieve_all_records:
            parameters[ "paging" ] = paging

         kwargs = self._append_session_header( **kwargs )

         records = []
         has_more_records = True
         while has_more_records:
            response = requests.get( url_join( self.locations.server_location, _ApiUrls.TimesheetQuery.value ), params = parameters, **kwargs )
            api_result = self._get_api_result( response )

            records.extend( api_result[ "entities" ] )

            result_paging = api_result[ "paging" ]
            has_more_records = retrieve_all_records and result_paging[ "hasMore" ]
            if has_more_records:
               parameters[ "paging" ] = result_paging

         return records
      else:
         raise AuthenticationError( self.username )

   def get_object( self, entity_id, fields = None, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         parameters = {}

         if fields is not None:
            param = QueryUtilities.get_fields_parameter( fields )
            if param is not None:
               parameters[ "fields" ] = param

         kwargs = self._append_session_header( **kwargs )
         response = requests.get( url_join( self.locations.server_location, _ApiUrls.Objects.value, entity_id ), params = parameters, **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

   def get_download_file_information( self, entity_id, redirect = False, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         parameters = { "documentId": entity_id, "redirect": redirect }

         kwargs = self._append_session_header( **kwargs )
         response = requests.get( url_join( self.locations.server_location, _ApiUrls.FileDownload.value ), params = parameters, **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )

   def change_entity_state( self, new_state, *entity_ids, **kwargs ):
      if not self.logged_in:
         self.login()

      if self.logged_in:
         parameters = { "ids": entity_ids, "state": new_state }

         kwargs = self._append_session_header( **kwargs )
         response = requests.post( url_join( self.locations.server_location, _ApiUrls.ChangeEntityState.value ), data = parameters, **kwargs )
         result = self._get_api_result( response )

         return result
      else:
         raise AuthenticationError( self.username )
