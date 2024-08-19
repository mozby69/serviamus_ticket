from django.shortcuts import render,get_object_or_404,redirect
from myapp.models import pensioner_list
from django.template.loader import get_template
from weasyprint import HTML
import io
from django.http import HttpResponse
from myapp.models import ticket_list
from django.db import transaction
from django.db import IntegrityError
from datetime import timedelta,datetime,date,time



def records_csv_page(request):
    list_pen = pensioner_list.objects.all()
    current_date = date.today()
    if request.method == 'POST':
        if 'save_family' in request.POST:
            endorsed_to = request.POST.get("endorsed_to")
            relationship = request.POST.get("relationship")
            name = request.POST.get("name")
            csv_id = request.POST.get("csv_id")

            current_date = date.today()
            valid_until = current_date + timedelta(days=30)


            try:
                ticket_list.objects.create(endorsed_to=endorsed_to, relationship=relationship,name=name,csv_id=csv_id,date_issued=current_date, valid_until=valid_until)
                return redirect('records_csv_page')
            except IntegrityError:
                return HttpResponse("Error occurred")

    context = {
        'list_pen': list_pen,
    }
    return render(request, 'myapp/records_csv.html', context)





def print_personal_ticket_page(request):
    return render(request, 'myapp/print_personal_ticket.html')

def print_family_ticket_page(request):
    return render(request, 'myapp/print_family_ticket.html')


def print_both_ticket_page(request, pk):
    list_pen = pensioner_list.objects.all()
    emp = get_object_or_404(pensioner_list, id=pk)
    context = {
        'emp':emp,
        'list_pen':list_pen,
    }
    return render(request, 'myapp/print_both_ticket.html', context)





def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HTML(string=html).write_pdf()
    return result

def pdf_view(request):
    context = {'data': 'This is a PDF example'}
    pdf = render_to_pdf('myapp/print_personal_ticket.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'
    return response