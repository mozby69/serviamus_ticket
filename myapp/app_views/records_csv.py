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

# def verify_ticket_page(request):
#     csv_id = request.POST.get('csv_id')
#     done_ticket = request.POST.get('done_ticket')

#     try:
#         datalist = pensioner_list.objects.get(csv_id=csv_id)
#         data = {
#             "success": True,
#             "csv_id": datalist.csv_id,
#             "endorsed_to":done_ticket,
    
#         }
#         return JsonResponse(data)
#     except ObjectDoesNotExist:
#         return JsonResponse({'success': False, 'message': 'No records found'})


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
    ticket_record = ticket_list.objects.all()
    current_date = date.today()
    if request.method == 'POST':
        if 'save_family' in request.POST:
            category = request.POST.get("category")
            endorsed_to = request.POST.get("endorsed_to")
            relationship = request.POST.get("relationship")
            name = request.POST.get("name")
            csv_id = request.POST.get("csv_id")
            valid_until = current_date + timedelta(days=30)

            if category == "consultation":
                last_ticket = ticket_list.objects.filter(ticket_family_consult__isnull=False).order_by('ticket_family_consult').last()
                if last_ticket:
                    next_ticket_number = last_ticket.ticket_family_consult + 1
                else:
                    next_ticket_number = 10
                try:
                    x = ticket_list.objects.create(
                        name=name,
                        csv_id=csv_id,
                        date_issued=current_date,
                        valid_until=valid_until,
                        ticket_family_consult=next_ticket_number,
                        ticket_family_lab=None,
                        checkup_type="consultation",
                        endorsed_to=endorsed_to,
                        relationship=relationship,
                        recepient_type="family",
                    )
                    # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                except IntegrityError:
                    return HttpResponse("Error occurred. Please try again.")

            elif category == "laboratory":
                last_ticket2 = ticket_list.objects.filter(ticket_family_lab__isnull=False).order_by('ticket_family_lab').last()
                if last_ticket2:
                    next_ticket_number = last_ticket2.ticket_family_lab + 1
                else:
                    next_ticket_number = 20
                try:
                    x = ticket_list.objects.create(
                        name=name,
                        csv_id=csv_id,
                        date_issued=current_date,
                        valid_until=valid_until,
                        ticket_family_consult=None,
                        ticket_family_lab=next_ticket_number,
                        checkup_type="laboratory",
                        endorsed_to=endorsed_to,
                        relationship=relationship,
                        recepient_type="family",
                    )
                    # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                except IntegrityError:
                    return HttpResponse("Error occurred. Please try again.")
            
            elif category == "both":
         
                last_consultation_ticket = ticket_list.objects.filter(ticket_family_consult__isnull=False).order_by('ticket_family_consult').last()
                if last_consultation_ticket:
                    consultation_ticket_number = last_consultation_ticket.ticket_family_consult + 1
                else:
                    consultation_ticket_number = 10

                last_laboratory_ticket = ticket_list.objects.filter(ticket_family_lab__isnull=False).order_by('ticket_family_lab').last()
                if last_laboratory_ticket:
                    laboratory_ticket_number = last_laboratory_ticket.ticket_family_lab + 1
                else:
                    laboratory_ticket_number = 20

                try:
                    x = ticket_list.objects.create(
                        name=name,
                        csv_id=csv_id,
                        date_issued=current_date,
                        valid_until=valid_until,
                        ticket_family_consult=consultation_ticket_number,
                        ticket_family_lab=laboratory_ticket_number,
                        checkup_type="both",
                        endorsed_to=endorsed_to,
                        relationship=relationship,
                        recepient_type="family",
                    )
                    # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                except IntegrityError:
                    return HttpResponse("Error occurred. Please try again.")


        
        elif 'save_ssp' in request.POST:
            category = request.POST.get("category")
            name = request.POST.get("name")
            csv_id = request.POST.get("csv_id")
            valid_until = current_date + timedelta(days=30)

            # Separate logic for consultation and laboratory tickets
            if category == "consultation":
                last_ticket = ticket_list.objects.filter(ticket_ssp_consult__isnull=False).order_by('ticket_ssp_consult').last()
                if last_ticket:
                    next_ticket_number = last_ticket.ticket_ssp_consult + 1
                else:
                    next_ticket_number = 10
                try:
                    x = ticket_list.objects.create(
                        name=name,
                        csv_id=csv_id,
                        date_issued=current_date,
                        valid_until=valid_until,
                        ticket_ssp_consult=next_ticket_number,
                        ticket_ssp_lab=None,
                        checkup_type="consultation",
                        recepient_type="personal",
                    )
                    # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                except IntegrityError:
                    return HttpResponse("Error occurred. Please try again.")

            elif category == "laboratory":
                last_ticket2 = ticket_list.objects.filter(ticket_ssp_lab__isnull=False).order_by('ticket_ssp_lab').last()
                if last_ticket2:
                    next_ticket_number = last_ticket2.ticket_ssp_lab + 1
                else:
                    next_ticket_number = 20
                try:
                    x = ticket_list.objects.create(
                        name=name,
                        csv_id=csv_id,
                        date_issued=current_date,
                        valid_until=valid_until,
                        # Set ticket_ssp_consult to None for laboratory
                        ticket_ssp_consult=None,
                        ticket_ssp_lab=next_ticket_number,
                        checkup_type="laboratory",
                        recepient_type="personal",
                    )
                    # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                except IntegrityError:
                    return HttpResponse("Error occurred. Please try again.")
            
            
            elif category == "both":
         
                last_consultation_ticket = ticket_list.objects.filter(ticket_ssp_consult__isnull=False).order_by('ticket_ssp_consult').last()
                if last_consultation_ticket:
                    consultation_ticket_number = last_consultation_ticket.ticket_ssp_consult + 1
                else:
                    consultation_ticket_number = 10

                last_laboratory_ticket = ticket_list.objects.filter(ticket_ssp_lab__isnull=False).order_by('ticket_ssp_lab').last()
                if last_laboratory_ticket:
                    laboratory_ticket_number = last_laboratory_ticket.ticket_ssp_lab + 1
                else:
                    laboratory_ticket_number = 20

                try:
                    x = ticket_list.objects.create(
                        name=name,
                        csv_id=csv_id,
                        date_issued=current_date,
                        valid_until=valid_until,
                        ticket_ssp_consult=consultation_ticket_number,
                        ticket_ssp_lab=laboratory_ticket_number,
                        checkup_type="both",
                        recepient_type="personal",
                    )
                    # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                except IntegrityError:
                    return HttpResponse("Error occurred. Please try again.")

            else:
      
                return HttpResponse("Invalid category selected.")
                    


    context = {
        'list_pen': list_pen,
        'ticket_record':ticket_record,
        # 'next_ticket_number': next_ticket_number,
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

def ticket_print(request, pk):
    current_date = date.today()
    current_month = current_date.month
    
    list_ticket = ticket_list.objects.filter(csv_id=pk,date_issued__month=current_month)
  
    if not list_ticket.exists():
        return render(request, 'myapp/ticket_print_display.html', context={'error': 'Ticket not found.'})


    context = {
        'tickets': list_ticket,
        'current_date': current_date.strftime('%b %d %Y'),  # Format date for display
    }

    return render(request, 'myapp/ticket_print_display.html', context)



def ticket_print_fam(request, pk):
    current_date = date.today()
    current_month = current_date.month
    
    list_ticket = ticket_list.objects.filter(csv_id=pk,date_issued__month=current_month)
 
    if not list_ticket.exists():
        return render(request, 'myapp/ticket_print_fam.html', context={'error': 'Ticket not found.'})


    context = {
        'tickets': list_ticket,
        'current_date': current_date.strftime('%b %d %Y'),  # Format date for display
    }

    return render(request, 'myapp/ticket_print_fam.html', context)



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