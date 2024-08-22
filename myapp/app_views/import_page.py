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
                        )
                    )

                # Bulk create the records
                pensioner_list.objects.bulk_create(pensioner_list_data)

                import_history.objects.create(
                    import_date=datetime.now().date(),
                    file_name=csv_file.name
                )

            messages.success(request, f'Import Sucessfully!', extra_tags='success_import')

            

    else:
        form = CSVUploadForm()

    context = {
        'form':form,
        'import_list': import_list,
    }    
    
    return render(request, 'myapp/import.html', context)


def fetch_import_successful(request):
    messages = get_messages(request)
    filtered_messages = [
        {'text': message.message, 'tags': message.tags} for message in messages if 'success_import' in message.tags
        or 'breakout' in message.tags or 'breakin' in message.tags or 'timeout' in message.tags
       
    ]

    return JsonResponse({'messages': filtered_messages})
