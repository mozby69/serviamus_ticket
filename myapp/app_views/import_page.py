from django.shortcuts import render
import csv
from myapp.forms import CSVUploadForm
from myapp.models import pensioner_list
from datetime import datetime
import codecs
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from myapp.models import import_history
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


fs = FileSystemStorage(location='tmp/')

def import_page(request):
    import_list = import_history.objects.all().order_by('-import_date')
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Save the file temporarily
            content = csv_file.read()  # these are bytes
            file_content = ContentFile(content)
            file_name = fs.save("_tmp.csv", file_content)
            tmp_file = fs.path(file_name)

            # Truncate the table before importing new data
            branch_name = request.user.username
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM pensioner_list WHERE branch_name = %s', [branch_name])

            # Open and decode the CSV file into a text stream
            with open(tmp_file, 'r', encoding='utf-8', errors="ignore") as file:
                reader = csv.DictReader(file, delimiter=",")

                # Prepare the data for bulk creation
                pensioner_list_data = []
     
                for row in reader:
                    birth_date = None
                    if row['BIRTH']:
                        try:
                            birth_date = datetime.strptime(row['BIRTH'], '%m/%d/%Y').date()
                        except ValueError:
                            pass  # Handle invalid date formats

                    pensioner_list_data.append(
                        pensioner_list(
                            csv_id=row['ID'],  
                            name=row['NAME'],
                            bank=row['BANK'],
                            add1=row['ADD1'],
                            add2=row['ADD2'],
                            birth=birth_date,
                            ptype=row['PTYPE'],
                            status=row['STATUS'],
                            grouping=row['GROUPING'],
                            conmonth=row['CONMONTH'],
                            readyx=row['READYX'].strip().upper() == 'TRUE',
                            branch_name=branch_name,
                        )
                    )

                # Bulk create the records
                pensioner_list.objects.bulk_create(pensioner_list_data)

                import_history.objects.create(
                    import_date=datetime.now().date(),
                    file_name=csv_file.name,
                    branch_name=branch_name,
                )

            messages.success(request, f'Import Successfully!', extra_tags='success_import')

    else:
        form = CSVUploadForm()

    context = {
        'form': form,
        'import_list': import_list,
    }    
    if not request.user.is_authenticated:
        return custom_logout(request)

    return render(request, 'myapp/import.html', context)



def custom_logout(request):
    if request.method in ['POST', 'GET']: 
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))  # Redirect to login page after logout
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def fetch_import_successful(request):
    messages = get_messages(request)
    filtered_messages = [
        {'text': message.message, 'tags': message.tags} for message in messages if 'success_import' in message.tags
        or 'breakout' in message.tags or 'breakin' in message.tags or 'timeout' in message.tags
       
    ]

    return JsonResponse({'messages': filtered_messages})



def ajax_import_table(request):
    if request.method == 'GET':
        page_number = request.GET.get('page', 1)
        items_per_page = request.GET.get('items_per_page', 8)
        branch_name = request.user.username
        history_list = import_history.objects.filter(branch_name=branch_name).order_by('-id').values('import_date', 'file_name')
        paginator = Paginator(history_list, items_per_page)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Get page range with ellipsis
        if paginator.num_pages > 10:
            if page_obj.number <= 5:
                page_range = list(range(1, 6)) + ['...'] + [paginator.num_pages]
            elif page_obj.number >= paginator.num_pages - 4:
                page_range = [1, '...'] + list(range(paginator.num_pages - 4, paginator.num_pages + 1))
            else:
                page_range = [1, '...'] + list(range(page_obj.number - 2, page_obj.number + 3)) + ['...'] + [paginator.num_pages]
        else:
            page_range = list(paginator.page_range)

        data = {
            'data': list(page_obj.object_list),
            'page_number': page_obj.number,
            'num_pages': paginator.num_pages,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_range': page_range,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)