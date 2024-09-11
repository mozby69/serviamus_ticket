from . import views
from django.urls import path
from .app_views import index ,import_page,records_csv,ticket_done,summary_report,import_dbf


urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', index.index_page, name='index'),
    path('logout/', views.custom_logout, name='logout'),
    path('import/',import_page.import_page, name="import"),
    path('fetch_import_successful/', import_page.fetch_import_successful, name="fetch_import_successful"),
    path('records_csv/', records_csv.records_csv_page, name="records_csv_page"),
    path('pdf_view/',records_csv.pdf_view, name="pdf_view"),
    path('print_family/<int:pk>/',records_csv.print_family_ticket_page, name="print_family_ticket_page"),
    path('print_ssp_ticket_page/<int:pk>/',records_csv.print_ssp_ticket_page,name="print_ssp_ticket_page"),
    path('view_ssp/',records_csv.view_ssp, name="view_ssp"),
    path('add_ssp/', records_csv.add_ssp, name="add_ssp"),
    path('add_family/', records_csv.add_family, name="add_family"),
    path('fetch_tickets/',ticket_done.fetch_tickets, name="fetch_tickets"),
    path('ticket_done_page/',ticket_done.ticket_done_page, name="ticket_done_page"),
    path('ticket_print/<int:pk>/<str:branch_name>/',records_csv.ticket_print, name="ticket_print"),
    path('ticket_print_fam/<int:pk>/',records_csv.ticket_print_fam,name="ticket_print_fam"),
    path('save_checkup_status/',ticket_done.save_checkup_status, name="save_checkup_status"),
    path('fetch_add_successfully/',records_csv.fetch_add_successfully,name="fetch_add_successfully"),
    path('pensioner_lists/',records_csv.pensioner_lists,name="pensioner_lists"),
    path('summary_page/',summary_report.summary_page, name="summary_page"),
    path('pensioner_lists_summary/',summary_report.pensioner_lists_summary,name="pensioner_lists_summary"),
    path('table_modal/',records_csv.table_modal, name="table_modal"),
    path('ajax_import_table/',import_page.ajax_import_table,name="ajax_import_table"),
    path('ticket_modal_lists/',records_csv.ticket_modal_lists,name="ticket_modal_lists"),
    path('update_table_modal/',records_csv.update_table_modal,name="update_table_modal"),
    path('dbf_page/',import_dbf.dbf_page,name="dbf_page"),
    path('ajax_import_table_dbf/',import_dbf.ajax_import_table_dbf,name="ajax_import_table_dbf"),
    path('table_modal_batch_print/',records_csv.table_modal_batch_print,name="table_modal_batch_print"),
    path('ticket_print_batch/', records_csv.ticket_print_batch, name='ticket_print_batch'),
   
    ]
