from django.shortcuts import render
from myapp.models import ticket_list
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import logout


def ticket_done_page(request):
    list_pen = ticket_list.objects.all()
    context = {
        'list_pen':list_pen,
    }

    if not request.user.is_authenticated:
        return custom_logout(request)


    return render(request,'myapp/ticket_done.html',context)

def custom_logout(request):
    if request.method in ['POST', 'GET']: 
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))  # Redirect to login page after logout
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def fetch_tickets(request):
    if request.method == 'GET':
        # Fetch ticket data from the database
        tickets = ticket_list.objects.all().order_by('-id').values('branch_name','id','name', 'date_issued', 'valid_until', 'endorsed_to', 'relationship','checkup_type','recepient_type','csv_id','checkup_status','ticket_ssp_consult','ticket_ssp_lab','ticket_family_consult','ticket_family_lab')  # Select specific fields if needed

        return JsonResponse(list(tickets), safe=False)  # Consider security implications if fetching sensitive data
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    




def save_checkup_status(request):
    ids = request.POST.get('id')
 
    try:
        # Filter instead of get to handle multiple records
        tickets = ticket_list.objects.filter(id=ids)
        
        if not tickets.exists():
            return JsonResponse({'success': False, 'message': 'No records found'})
        
        if tickets.filter(checkup_status="DONE CHECKUP").exists():
            return JsonResponse({'warning': True, 'message': 'DONE ALREADY!'})
        
        tickets.update(checkup_status="DONE CHECKUP")

        return JsonResponse({'success': True, 'message': 'Status Successfully Changed!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# def save_checkup_status(request):
#     csv_id = request.POST.get('x')

#     try:
#         update_ticket = ticket_list.objects.get(csv_id=csv_id)
#         update_ticket.checkup_status = "DONE CHECKUP"
#         # messages.success(request, f'STATUS CHANGE SUCCESSFULLY!')
#         update_ticket.save()

     
#         return JsonResponse({'success':True ,'message':'Status Successfully Change!'})
#     except ObjectDoesNotExist:

#         return JsonResponse({'success': False, 'message': 'No records found'})