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
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt



def view_ssp(request):
    past_ssp_id = request.POST.get('past_ssp_id')
    try:
        datalist = pensioner_list.objects.get(id=past_ssp_id)
        data = {
            "success": True,
            "name": datalist.name,
            "csv_id": datalist.csv_id,
            "bank": datalist.bank,
            "add1": datalist.add1,
            "add2": datalist.add2,
            "birth": datalist.birth,
            "ptype": datalist.ptype,
            "status": datalist.status,
            "grouping": datalist.grouping,
            "conmonth": datalist.conmonth,
        }
        return JsonResponse(data)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message': 'No records found'})


def add_ssp(request):
    csv_id = request.POST.get('csv_id')
    endorsed_to = request.POST.get('endorsed_to')
    relationship = request.POST.get('relationship')

    try:
        datalist = pensioner_list.objects.get(csv_id=csv_id)
        data = {
            "success": True,
            "name": datalist.name,
            "csv_id": datalist.csv_id,
            "endorsed_to":endorsed_to,
            "relationship":relationship,
        }
        return JsonResponse(data)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message': 'No records found'})


@csrf_exempt
def add_family(request):
    csv_id = request.POST.get('csv_id')
    print("result llll", csv_id)
    try:
        datalist = pensioner_list.objects.get(csv_id=csv_id)
        data = {
            "success": True,
            "name": datalist.name,
            "csv_id":datalist.csv_id,
        }
        return JsonResponse(data)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message': 'No records found'})


def records_csv_page(request):
    list_pen = pensioner_list.objects.all()

    # Determine the next ticket number for SSP
    last_ticket = ticket_list.objects.filter(ticket_num_family__isnull=False).order_by('ticket_num_family').last()
    if last_ticket:
        next_ticket_number = last_ticket.ticket_num_family + 1
    else:
        next_ticket_number = 10  # Start from 10 if no ticket exists


    last_ticket_ssp = ticket_list.objects.filter(ticket_num_ssp__isnull=False).order_by('ticket_num_ssp').last()
    if last_ticket_ssp:
        next_ticket_number_ssp = last_ticket_ssp.ticket_num_ssp + 1
    else:
        next_ticket_number_ssp = 10  # Start from 10 if no ticket exists

    current_date = date.today()
    if request.method == 'POST':
        if 'save_family' in request.POST:
            endorsed_to = request.POST.get("endorsed_to")
            relationship = request.POST.get("relationship")
            name = request.POST.get("name")
            csv_id = request.POST.get("csv_id")
            valid_until = current_date + timedelta(days=30)

            try:
                x = ticket_list.objects.create(
                    endorsed_to=endorsed_to,
                    relationship=relationship,
                    name=name,
                    csv_id=csv_id,
                    date_issued=current_date,
                    valid_until=valid_until,
                    ticket_num_family=next_ticket_number  # Incrementing SSP ticket number
                )
                return redirect('print_family_ticket_page', pk=x.csv_id)
            except IntegrityError:
                return HttpResponse("Error occurred. Please try again.")
        
        elif 'save_ssp' in request.POST:
    
            name = request.POST.get("name")
            csv_id = request.POST.get("csv_id")
            valid_until = current_date + timedelta(days=30)

            try:
                x = ticket_list.objects.create(
                    name=name,
                    csv_id=csv_id,
                    date_issued=current_date,
                    valid_until=valid_until,
                    ticket_num_ssp=next_ticket_number_ssp  # Incrementing SSP ticket number
                )
                return redirect('print_ssp_ticket_page', pk=x.csv_id)
            except IntegrityError:
                return HttpResponse("Error occurred. Please try again.")


    context = {
        'list_pen': list_pen,
        'next_ticket_number': next_ticket_number,
    }

    return render(request, 'myapp/records_csv.html', context)







def print_family_ticket_page(request,pk):
    emp = get_object_or_404(pensioner_list, csv_id=pk)
    current_date = date.today()
    list_ticket = ticket_list.objects.filter(csv_id=pk,date_issued=current_date)
   

    context = {
        'emp':emp,
        'list_ticket':list_ticket,
      
    }


    return render(request, 'myapp/print_family_ticket.html',context)


def print_ssp_ticket_page(request, pk):
    current_date = date.today()
    list_pen = pensioner_list.objects.all()
    emp = get_object_or_404(pensioner_list, csv_id=pk)
    list_ticket = ticket_list.objects.filter(csv_id=pk,date_issued=current_date)

    context = {
        'emp':emp,
        'list_pen':list_pen,
        'list_ticket':list_ticket,
    }
    return render(request, 'myapp/print_ssp_ticket.html', context)





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