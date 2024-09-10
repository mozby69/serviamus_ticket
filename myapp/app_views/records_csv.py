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
from django.contrib.messages import get_messages
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import logout
from django.db.models import Count
from django.urls import reverse_lazy


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
    branch_name = request.POST.get('branch_name')


    try:
        datalist = pensioner_list.objects.get(csv_id=csv_id,branch_name=branch_name)
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
    branch_name = request.POST.get('branch_name')


    print("result llll", csv_id)
    try:
        datalist = pensioner_list.objects.get(csv_id=csv_id,branch_name=branch_name)
        data = {
            "success": True,
            "name": datalist.name,
            "csv_id":datalist.csv_id,
        }
        return JsonResponse(data)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message': 'No records found'})


def add_weekdays(start_date, num_days):
    """Add weekdays to a start date, excluding weekends."""
    current_date = start_date
    while num_days > 0:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # 0-4 are weekdays (Monday to Friday)
            num_days -= 1
    return current_date



STARTING_NUMBERS_CONSULT = {
    'admin': 223,
    'RLC_SINGCANG': 100,
    'FCH-BACOLOD': 50,
}

def get_starting_number_consult(username):
    return STARTING_NUMBERS_CONSULT.get(username, 223)


STARTING_NUMBERS_LAB = {
    'admin': 223,
    'RLC_SINGCANG': 120,
    'FCH-BACOLOD': 60,
}

def get_starting_number_lab(username):
    return STARTING_NUMBERS_LAB.get(username, 1)


@transaction.atomic
def records_csv_page(request):
    list_pen = pensioner_list.objects.all()
    ticket_record = ticket_list.objects.all()
    current_date = date.today()
    branch_name = request.user.username
    current_month = current_date.month
    current_year = current_date.year

    if request.method == 'POST':

        if 'save_family' in request.POST:
            category = request.POST.get("category")
            endorsed_to = request.POST.get("endorsed_to")
            relationship = request.POST.get("relationship")
            name = request.POST.get("name")
            csv_id = request.POST.get("csv_id")
            valid_until = add_weekdays(current_date, 4) 


            duplicates = ticket_list.objects.filter(
                csv_id=csv_id,
                branch_name=branch_name,
                date_issued__year=current_year,
                date_issued__month=current_month
            )

            starting_number_consult = get_starting_number_consult(branch_name)
            starting_number_lab = get_starting_number_lab(branch_name)

            if category == "consultation":
                last_ticket = ticket_list.objects.filter(ticket_family_consult__isnull=False, branch_name=branch_name).order_by('ticket_family_consult').last()
                next_ticket_number = last_ticket.ticket_family_consult + 1 if last_ticket else starting_number_consult

                if duplicates.exists():
                    messages.error(request, f'This account already has a ticket for this date!',extra_tags='duplicate')
                    return redirect('records_csv_page')
                
                else:
                    # Create the new ticket
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
                        branch_name=branch_name,
                    )
                    messages.success(request, f'Ticket Successfully Added!', extra_tags='added')
                    return redirect('records_csv_page')

            elif category == "laboratory":
                last_ticket2 = ticket_list.objects.filter(ticket_family_lab__isnull=False, branch_name=branch_name).order_by('ticket_family_lab').last()
                next_ticket_number = last_ticket2.ticket_family_lab + 1 if last_ticket2 else starting_number_lab

                if duplicates.exists():
                    messages.error(request, f'This account already has a ticket for this date!',extra_tags='duplicate')
                    return redirect('records_csv_page')
                else:
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
                            branch_name=branch_name,
                        )
                        messages.success(request, f'Ticket Successfully Added!', extra_tags='added')
                        return redirect('records_csv_page')
                        # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                    except IntegrityError:
                        return HttpResponse("Error occurred. Please try again.")
            
            elif category == "both":
         
                last_ticket3 = ticket_list.objects.filter(ticket_family_consult__isnull=False, branch_name=branch_name).order_by('ticket_family_consult').last()
                consultation_ticket_number = last_ticket3.ticket_family_consult + 1 if last_ticket3 else starting_number_consult

                last_ticket4 = ticket_list.objects.filter(ticket_family_lab__isnull=False, branch_name=branch_name).order_by('ticket_family_lab').last()
                laboratory_ticket_number = last_ticket4.ticket_family_lab + 1 if last_ticket4 else starting_number_lab


                if duplicates.exists():
                    messages.error(request, f'This account already has a ticket for this date!',extra_tags='duplicate')
                    return redirect('records_csv_page')
                else:

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
                            branch_name=branch_name,
                        )
                        messages.success(request, f'Ticket Successfully Added!', extra_tags='added')
                        return redirect('records_csv_page')
                        # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                    except IntegrityError:
                        return HttpResponse("Error occurred. Please try again.")


        
        elif 'save_ssp' in request.POST:
            category = request.POST.get("category")
            name = request.POST.get("name")
            csv_id = request.POST.get("csv_id")
            valid_until = current_date + timedelta(days=30)


            starting_number_consult = get_starting_number_consult(branch_name)
            starting_number_lab = get_starting_number_lab(branch_name)

            duplicates = ticket_list.objects.filter(
                csv_id=csv_id,
                branch_name=branch_name,
                date_issued__year=current_year,
                date_issued__month=current_month
            )

            # Separate logic for consultation and laboratory tickets
            if category == "consultation":
              
                last_ticket = ticket_list.objects.filter(ticket_ssp_consult__isnull=False, branch_name=branch_name).order_by('ticket_ssp_consult').last()
                next_ticket_number = last_ticket.ticket_ssp_consult + 1 if last_ticket else starting_number_consult
                
                if duplicates.exists():
                    messages.error(request, f'This account already has a ticket for this date!',extra_tags='duplicate')
                    return redirect('records_csv_page')
                
                else:
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
                            branch_name=branch_name,
                        )
                        messages.success(request, f'Ticket Successfully Added!', extra_tags='added')
                        return redirect('records_csv_page')
                        # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                    except IntegrityError:
                        return HttpResponse("Error occurred. Please try again.")

            elif category == "laboratory":
                last_ticket2 = ticket_list.objects.filter(ticket_ssp_lab__isnull=False, branch_name=branch_name).order_by('ticket_ssp_lab').last()
                next_ticket_number = last_ticket2.ticket_ssp_lab + 1 if last_ticket2 else starting_number_lab

                if duplicates.exists():
                    messages.error(request, f'This account already has a ticket for this date!',extra_tags='duplicate')
                    return redirect('records_csv_page')
                
                else:
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
                            branch_name=branch_name,
                        )
                        messages.success(request, f'Ticket Successfully Added!', extra_tags='added')
                        return redirect('records_csv_page')
                        # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                    except IntegrityError:
                        return HttpResponse("Error occurred. Please try again.")
            
            
            elif category == "both":
         
                last_ticket_consult = ticket_list.objects.filter(ticket_ssp_consult__isnull=False, branch_name=branch_name).order_by('ticket_ssp_consult').last()
                consultation_ticket_number = last_ticket_consult.ticket_ssp_consult + 1 if last_ticket_consult else starting_number_consult

                last_ticket_lab = ticket_list.objects.filter(ticket_ssp_lab__isnull=False, branch_name=branch_name).order_by('ticket_ssp_lab').last()
                laboratory_ticket_number = last_ticket_lab.ticket_ssp_lab + 1 if last_ticket_lab else starting_number_lab

                if duplicates.exists():
                    messages.error(request, f'This account already has a ticket for this date!',extra_tags='duplicate')
                    return redirect('records_csv_page')
                
                else:

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
                            branch_name=branch_name,
                        )
                        messages.success(request, f'Ticket Successfully Added!', extra_tags='added')
                        return redirect('records_csv_page')
                        # return redirect('print_ssp_ticket_page', pk=x.csv_id)
                    except IntegrityError:
                        return HttpResponse("Error occurred. Please try again.")

            else:
      
                return HttpResponse("Invalid category selected.")
                    


    context = {
        'list_pen': list_pen,
        'ticket_record':ticket_record,
        'branch_name':branch_name,
        # 'next_ticket_number': next_ticket_number,
    }
    
    if not request.user.is_authenticated:
        return custom_logout(request)

    return render(request, 'myapp/records_csv.html', context)

@csrf_exempt
def custom_logout(request):
    if request.method in ['POST', 'GET']: 
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))  # Redirect to login page after logout
    else:
        return HttpResponseRedirect(reverse_lazy('login'))





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
    current_year = current_date.year
    
    list_ticket = ticket_list.objects.filter(csv_id=pk,date_issued__month=current_month,date_issued__year=current_year)
  
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




def fetch_add_successfully(request):
    messages = get_messages(request)
    filtered_messages = [
        {'text': message.message, 'tags': message.tags} for message in messages if 'added' in message.tags
        or 'breakout' in message.tags or 'breakin' in message.tags or 'duplicate' in message.tags
       
    ]

    return JsonResponse({'messages': filtered_messages})













def pensioner_lists(request):
    if request.method == 'GET':
        branch_name = request.user.username
        # Fetch ticket data from the database
        tickets = pensioner_list.objects.filter(branch_name=branch_name).values('id', 'name', 'bank', 'ptype', 'grouping', 'csv_id','branch_name')

        return JsonResponse(list(tickets), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)





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


def table_modal(request):
    branch_name = request.user.username
    current_date = date.today()
    current_month = current_date.month
    current_year = current_date.year

    attendances = ticket_list.objects.filter(branch_name=branch_name,date_issued__month=current_month,date_issued__year=current_year).order_by('-id').values('id','name', 'date_issued', 'valid_until','ticket_ssp_consult','ticket_ssp_lab','ticket_family_consult','ticket_family_lab')

    # Set the number of items per page
    paginator = Paginator(attendances, 5)  # 5 items per page

    # Get the page number from the request
    page = request.GET.get('page', 1)

    try:
        attendances_page = paginator.page(page)
    except PageNotAnInteger:
        attendances_page = paginator.page(1)  # If page is not an integer, deliver the first page
    except EmptyPage:
        attendances_page = paginator.page(paginator.num_pages)  # If page is out of range, deliver the last page

    # Convert the page object to a list of dictionaries
    data = list(attendances_page)

    # Prepare pagination data
    pagination_data = {
        'attendances': data,
        'has_previous': attendances_page.has_previous(),
        'has_next': attendances_page.has_next(),
        'page_number': attendances_page.number,
        'num_pages': paginator.num_pages,
        'page_range': list(paginator.get_elided_page_range(number=attendances_page.number, on_each_side=2, on_ends=1)),
    }

    return JsonResponse(pagination_data)




def ticket_modal_lists(request):
    ID = request.POST.get('data_table_modal_id')
    try:
        datalist = ticket_list.objects.get(id=ID)
        data = {
            "success": True,
            'id':datalist.id,
            "name": datalist.name,
            "endorsed_to": datalist.endorsed_to,
            "relationship": datalist.relationship,
            "date_issued": datalist.date_issued,
            "valid_until":datalist.valid_until,
            "checkup_status":datalist.checkup_status,
            "recepient_type":datalist.recepient_type,
            "counter_name":datalist.counter_name,
            "ticket_ssp_consult":datalist.ticket_ssp_consult,
            "ticket_ssp_lab":datalist.ticket_ssp_lab,
            "ticket_family_consult":datalist.ticket_family_consult,
            "ticket_family_lab":datalist.ticket_family_lab,
     
        }
        return JsonResponse(data)
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message': 'No records found'})
    



def update_table_modal(request):
    if request.method == "POST":
        id = request.POST.get("edit_id")
        name = request.POST.get("edit_names")
        endorsed_to = request.POST.get("edit_endorsed_to")
        relationship = request.POST.get("edit_relationship")
     

        try:
            ticket_list_save = ticket_list.objects.get(id=id)
            ticket_list_save.name = name
            ticket_list_save.endorsed_to = endorsed_to
            ticket_list_save.relationship = relationship
        

            ticket_list_save.save()
            return JsonResponse({'success': True})
        except ticket_list.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': f"does not exist."})
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})
