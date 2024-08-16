from django.shortcuts import render
from myapp.models import pensioner_list
from django.template.loader import get_template
from weasyprint import HTML
import io
from django.http import HttpResponse


def records_csv_page(request):
    list_pen = pensioner_list.objects.all()

    context = {
        'list_pen':list_pen,

    }
    return render(request,'myapp/records_csv.html',context)




def print_personal_ticket_page(request):
    return render(request, 'myapp/print_personal_ticket.html')

def print_family_ticket_page(request):
    return render(request, 'myapp/print_family_ticket.html')









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