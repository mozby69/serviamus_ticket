from django.shortcuts import render
from django.core.files.storage import default_storage
from django.db import connection
from django.contrib import messages
import os
import pandas as pd
from dbfread import DBF
from myapp.models import pensioner_list, import_history
from datetime import datetime

def dbf_page(request):
    if request.method == 'POST':
        dbf_file = request.FILES.get('dbf_file')
        fpt_file = request.FILES.get('fpt_file')
        branch_name = request.user.username
        
        if not dbf_file:
            return render(request, 'myapp/import_dbf.html', {'error': 'DBF file is required.'})

        if not fpt_file:
            return render(request, 'myapp/import_dbf.html', {'error': 'FPT memo file is required.'})

        dbf_file_path = default_storage.save('temp.dbf', dbf_file)
        fpt_file_path = default_storage.save('temp.fpt', fpt_file)

        try:
            # Delete existing data for the current user
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM pensioner_list WHERE branch_name = %s', [branch_name])
                print(f"Deleted existing records for branch: {branch_name}")

            # Open the DBF file with dbfread and specify encoding
            dbf = DBF(dbf_file_path, encoding='latin-1')  # Adjust encoding if needed
            records = list(dbf)
            df = pd.DataFrame(records)

            # Remove 'REMARKS' field if it exists
            if 'REMARKS' in df.columns:
                df = df.drop(columns=['REMARKS'])
                print("Removed 'REMARKS' column from DataFrame")

            # Prepare the data for bulk creation
            pensioner_list_data = []
            for index, row in df.iterrows():
                # Handle empty or invalid dates
                birth_date = row.get('BIRTH', None)
                if isinstance(birth_date, str):
                    try:
                        # Validate the date format
                        birth_date = datetime.strptime(birth_date, '%m/%d/%Y').date()
                    except ValueError:
                        print(f"Invalid date format for row {index}: {row['BIRTH']}")
                        birth_date = None  # Set to None if the date format is invalid

                pensioner_list_data.append(
                    pensioner_list(
                        csv_id=row.get('ID', ''),
                        name=row.get('NAME', ''),
                        bank=row.get('BANK', ''),
                        add1=row.get('ADD1', ''),
                        add2=row.get('ADD2', ''),
                        birth=birth_date,  # Use as is or None
                        ptype=row.get('PYTYPE', ''),
                        status=row.get('STATUS', ''),
                        grouping=row.get('GROUPING', ''),
                        conmonth=row.get('CONMONTH', ''),
                        readyx=row.get('READYX', ''),
                        branch_name=branch_name,
                    )
                )
                print(f"Prepared data for row {index}: {row}")

            # Bulk create the records
            if pensioner_list_data:
                pensioner_list.objects.bulk_create(pensioner_list_data)
                print("Inserted new records into the database")
            else:
                print("No data to insert")

            # Record the import in the history
            import_history.objects.create(
                import_date=datetime.now().date(),
                file_name=dbf_file.name,
                branch_name=branch_name,
            )

            messages.success(request, f'Import Successfully!', extra_tags='success_import')

        except Exception as e:
            print(f"Error processing files: {str(e)}")
            return render(request, 'myapp/import_dbf.html', {'error': str(e)})

        finally:
            if os.path.isfile(dbf_file_path):
                os.remove(dbf_file_path)
            if os.path.isfile(fpt_file_path):
                os.remove(fpt_file_path)

    return render(request, 'myapp/import_dbf.html')
