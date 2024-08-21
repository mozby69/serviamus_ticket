from django.shortcuts import render
from myapp.models import ticket_list
from django.http import JsonResponse


def ticket_done_page(request):
    list_pen = ticket_list.objects.all()
    context = {
        'list_pen':list_pen,
    }
    return render(request,'myapp/ticket_done.html',context)



def fetch_tickets(request):
    if request.method == 'GET':
        # Fetch ticket data from the database
        tickets = ticket_list.objects.all().values('name', 'date_issued', 'valid_until', 'endorsed_to', 'relationship')  # Select specific fields if needed

        return JsonResponse(list(tickets), safe=False)  # Consider security implications if fetching sensitive data
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)