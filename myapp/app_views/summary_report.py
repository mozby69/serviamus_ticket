from django.shortcuts import render
from django.core.serializers import serialize
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from myapp.models import ticket_list
from django.db.models import Case, When, Value, CharField

#   tickets = ticket_list.objects.all().values('name', 'csv_id', 'endorsed_to', 'relationship',)
def summary_page(request):
    return render(request,"myapp/summary_report.html")


def pensioner_lists_summary(request):
        if request.method == 'GET':
            date_issued = request.GET.get('date', None)
            if date_issued:
                tickets = ticket_list.objects.filter(date_issued=date_issued).annotate(
                    # Determine which consultation ticket value to display
                    consultation_ticket=Case(
                        When(ticket_ssp_consult__isnull=False, then='ticket_ssp_consult'),
                        When(ticket_family_consult__isnull=False, then='ticket_family_consult'),
                        default=Value(''),
                        output_field=CharField()
                    ),
                    # Determine which laboratory ticket value to display
                    laboratory_ticket=Case(
                        When(ticket_ssp_lab__isnull=False, then='ticket_ssp_lab'),
                        When(ticket_family_lab__isnull=False, then='ticket_family_lab'),
                        default=Value(''),
                        output_field=CharField()
                    )
                ).values(
                    'csv_id', 'name', 'date_issued', 'valid_until', 'endorsed_to', 'relationship',
                    'checkup_status', 'checkup_type', 'recepient_type', 'counter_name',
                    'consultation_ticket', 'laboratory_ticket'
                )
                return JsonResponse(list(tickets), safe=False)
            else:
                return JsonResponse({'error': 'Date not provided'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)