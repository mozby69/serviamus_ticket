from django.shortcuts import render
from myapp.models import ticket_list
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def ticket_done_page(request):
    list_pen = ticket_list.objects.all()
    context = {
        'list_pen':list_pen,
    }
    return render(request,'myapp/ticket_done.html',context)



def fetch_tickets(request):
    if request.method == 'GET':
        # Fetch ticket data from the database
        tickets = ticket_list.objects.all().values('name', 'date_issued', 'valid_until', 'endorsed_to', 'relationship','csv_id','checkup_status','ticket_ssp_consult','ticket_ssp_lab','ticket_family_consult','ticket_family_lab')  # Select specific fields if needed

        return JsonResponse(list(tickets), safe=False)  # Consider security implications if fetching sensitive data
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    


def save_checkup_status(request):
    csv_id = request.POST.get('x')

    try:
        update_ticket = ticket_list.objects.get(csv_id=csv_id)
        update_ticket.checkup_status = "DONE CHECKUP"
        # messages.success(request, f'STATUS CHANGE SUCCESSFULLY!')
        update_ticket.save()

     
        return JsonResponse({'success':True ,'message':'Status Successfully Change!'})
    except ObjectDoesNotExist:

        return JsonResponse({'success': False, 'message': 'No records found'})