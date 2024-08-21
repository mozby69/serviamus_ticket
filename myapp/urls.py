from . import views
from django.urls import path
from .app_views import index ,import_page,records_csv,ticket_done


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
    ]
