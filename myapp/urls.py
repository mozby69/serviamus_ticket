from . import views
from django.urls import path
from .app_views import index ,import_page,records_csv


urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', index.index_page, name='index'),
    path('logout/', views.custom_logout, name='logout'),
    path('import/',import_page.import_page, name="import"),
    path('fetch_import_successful/', import_page.fetch_import_successful, name="fetch_import_successful"),
    path('records_csv/', records_csv.records_csv_page, name="records_csv_page"),
    path('print_personal_ticket',records_csv.print_personal_ticket_page, name="print_personal_ticket_page"),
    path('pdf_view/',records_csv.pdf_view, name="pdf_view"),
    path('print_family',records_csv.print_family_ticket_page, name="print_family_ticket_page"),
    
    
    ]
