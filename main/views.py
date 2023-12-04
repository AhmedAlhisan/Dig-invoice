from django.shortcuts import render ,redirect
from transformers import pipeline
from django.db.models import F
from django.contrib import messages
from django.http import HttpRequest , HttpResponse
import pytesseract
from PIL import Image
from django.core.files.storage import FileSystemStorage
import io
from datetime import datetime
from .models import DepartmentBudget , Invoice , DepartmentDescription
import pandas as pd
from django.db.models import Sum
import json
from decimal import Decimal
from django.db.models.functions import TruncMonth
import PyPDF2
import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma



# Create your views here.
dateFinal : datetime=0
dpartmentFinale:str
FinalTotal:float
FinalVat:float
FinalPoNumber:str
FinalInvType:str
def style_test(request:HttpRequest):
    department_sums = Invoice.objects.values('department').annotate(total_sum=Sum('total_value'))

    for dept in department_sums:
 # Aggregate the data
        department_sums = Invoice.objects.values('department').annotate(total_sum=Sum('total_value'))

        # Convert to dictionary for easier access in the template
        department_totals = {dept['department']: dept['total_sum'] for dept in department_sums}

    # Pass the data to the template
    context = {
        'department_totals': department_totals
    }

    return render(request, 'main/base.html', context)


from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
from transformers import pipeline
from datetime import datetime
from .models import Invoice, DepartmentBudget  # Import your models
from django.contrib import messages
from django.shortcuts import render
from django.db.models import F



def upload_invoice(request):
    
    if request.method == 'POST':
        
        action = request.POST.get('action')
        
        if action == 'show_data':
            uploaded_file = request.FILES['img']

            # Check if uploaded file is a PDF
            if uploaded_file.name.lower().endswith('.pdf'):
                # Convert PDF to image
                images = convert_from_bytes(uploaded_file.read())
                # Assuming you want the first page of the PDF
                image = images[0]
                # Optionally, save the image if needed
                image_io = BytesIO()
                image.save(image_io, format='JPEG')
                image_io.seek(0)
                uploaded_file = InMemoryUploadedFile(
                    file=image_io,
                    field_name='img',
                    name='converted_image.jpg',  # You can dynamically set a name here
                    content_type='image/jpeg',
                    size=image_io.tell(),
                    charset=None
                )
            else:
                image = Image.open(uploaded_file) 
            
            image = Image.open(uploaded_file)
            department_selected = request.POST['department']
            department_option = None
            if department_selected == 'IT':
                department_option = request.POST.get('itOption')
            elif department_selected == 'Marketing':
                department_option = request.POST.get('marketingOption')
            elif department_selected == 'Sales':
                department_option = request.POST.get('salesOption')

            
        

            # Initialize the transformers pipeline
            pipe = pipeline("document-question-answering", model="impira/layoutlm-invoices")
        
            # Process the file
            result_date = pipe(image, "Date (Gregorian)?") 
            #first try
            result_Total_first_try = pipe(image, "Total Trade Items Price?") 
            result_VAT_first_try = pipe(image, "Total Trade Items VAT?")  
            #second try
            result_Total_second_try = pipe(image, "Total Value") 
            result_VAT_second = pipe(image, "VAT?")  
            result_po_number = pipe(image,"NUPCO PO?") 
            #for validation check
            test = pipe(image,"C.R.") 
            rem = pipe(image,"%") 
            
            #not added Yet
            print(test)
            print(rem)


            print(result_date)
            #first check
            
            print('First Try')
            print(result_Total_first_try)
            print(result_VAT_first_try)
            #second check
            print('Second Try')
            print(result_Total_second_try)
            print(result_VAT_second)
            print('__')
            print(result_po_number)
            if float(result_Total_first_try[0]['score']) > float(result_Total_second_try[0]['score']):
                result_Total = result_Total_first_try
            else:
                result_Total = result_Total_second_try    
            if float(result_VAT_first_try[0]['score']) > float(result_VAT_second[0]['score']):
                result_VAT = result_VAT_first_try
            else:
                result_VAT = result_VAT_second    
            

            # Save the file
            fs = FileSystemStorage()
            if isinstance(uploaded_file, InMemoryUploadedFile):
                # Save the converted image
                filename = fs.save(uploaded_file.name, ContentFile(uploaded_file.read()))
            else:
                # Save the original uploaded file
                filename = fs.save(uploaded_file.name, uploaded_file)
            # Return the result
            request.session['uploaded_file_url'] = fs.url(filename)
            resultdateFinal=datetime.strptime(result_date[0]['answer'], '%d/%m/%Y')
            request.session['result_Total']=result_Total[0]['answer']
            request.session['result_VAT']=result_VAT[0]['answer']
            request.session['result_po_number']=result_po_number[0]['answer']
            request.session['result_date']=result_date[0]['answer']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            request.session['uploaded_file_url'] = fs.url(filename)
            
            request.session['department_selected']=department_selected
            request.session['department_option']=department_option
            #dateFinal =resultdateFinal.strftime('%Y-%m-%d')
            print(dateFinal)
        if action == 'confirm_data':
             # Retrieve values from the session
            department = request.session.get('department_selected')
            print(department)
            invoice_number = request.session.get('result_po_number')
            print(invoice_number)
            total_value = request.session.get('result_Total')
          
            total_value = Decimal(total_value.replace(',',''))
            print(total_value)
            vat = request.session.get('result_VAT')
            vat = Decimal(vat.replace(',',''))
            print(vat)
            date = request.session.get('result_date')
            print(date)
            invoice_type = request.session.get('department_option')
            print(invoice_type)

            # Retrieve the path of the uploaded file from the session
            uploaded_file_url = request.session.get('uploaded_file_url')
            date_obj = datetime.strptime(date, '%d/%m/%Y').date()
            formatted_date = date_obj.strftime('%Y-%m-%d')
            # Create a new Invoice record using the values from the session
            new_record = Invoice(
                department=department,
                invoice_number=invoice_number,
                total_value=total_value,
                vat=vat,
                date=formatted_date,
                invoice_image=uploaded_file_url,  # Assuming you are storing a file path or identifier
                invoice_type=invoice_type
            )
            new_record.save()
            messages.success(request , 'Invoice added successfully')
            department_budget = DepartmentBudget.objects.get(department_name=department)
            department_budget.available_budget = F('available_budget') - total_value
            department_budget.save()
            
            return render(request , 'main/base.html')
        return render(request, 'main/result.html',{'result_Total':result_Total[0]['answer'] ,'result_VAT':result_VAT[0]['answer'] , 'result_po_number':result_po_number[0]['answer'] , 'result_date': result_date[0]['answer'] ,'department_selected':department_selected ,'department_option':department_option , 'imgpo':uploaded_file} )
        

    return render(request, 'main/invoice_upload.html')
#{'result_date': result_date[0]['answer'] ,,'VAT':result_VAT[0]['answer'] , 'result_po_number':result_po_number[0]['answer'] ,'department_selected':department_selected  }




class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)
def dashBoard(request : HttpRequest):
    invoices = Invoice.objects.values('department', 'invoice_number')
    
    
    df = pd.DataFrame(list(invoices))

    invoice_counts = df.groupby('department').count()

    invoice_counts_dict = invoice_counts['invoice_number'].to_dict()
    #firstchart
    data = Invoice.objects.values('department').annotate(total_spending=Sum('total_value'))
    departments = [item['department'] for item in data]
    spendings = [item['total_spending'] for item in data]
    departments_json = json.dumps(departments, cls=DecimalEncoder)
    spendings_json = json.dumps(spendings, cls=DecimalEncoder)
    #chartEnd
    #itchart
    try:
        it_budget = DepartmentBudget.objects.get(department_name='IT')
        budget_data = {
            'Spent Budget': float(it_budget.budget - it_budget.available_budget),
            'Available Budget': float(it_budget.available_budget)
        }
    except DepartmentBudget.DoesNotExist:
        budget_data = {}

    budget_data_json = json.dumps(budget_data)
    #endchart
    #MarkitingChart
    try:
        marketing_budget = DepartmentBudget.objects.get(department_name='Marketing')
        budget_data_mrkt = {
            'Spent Budget': float(marketing_budget.budget - marketing_budget.available_budget),
            'Available Budget': float(marketing_budget.available_budget)
    }
    except DepartmentBudget.DoesNotExist:
        budget_data_mrkt = {}

    budget_data_json_MRKT = json.dumps(budget_data_mrkt)
    #EndMarkett
    #salestart
    try:
        sales_budget = DepartmentBudget.objects.get(department_name='Sales')
        budget_data_sales = {
            'Spent Budget': float(sales_budget.budget - sales_budget.available_budget),
            'Available Budget': float(sales_budget.available_budget)
        }
    except DepartmentBudget.DoesNotExist:
        budget_data_sales = {}

    budget_data_sales_json = json.dumps(budget_data_sales)
    

    return render(request,'main/dashBoard.html',{'budget_data_sales_json':budget_data_sales_json,'budget_data_json_MRKT':budget_data_json_MRKT,'budget_data_json':budget_data_json,'invoice_counts': invoice_counts_dict,'departments': departments_json, 'spendings': spendings_json})
def t2(request:HttpRequest):
    describe_department_spending(request)
    #itchart
    try:
        it_budget = DepartmentBudget.objects.get(department_name='IT')
        budget_data = {
            'Spent Budget': float(it_budget.budget - it_budget.available_budget),
            'Available Budget': float(it_budget.available_budget)
        }
    except DepartmentBudget.DoesNotExist:
        budget_data = {}

    budget_data_json = json.dumps(budget_data)
    #endchart

    #MarkitingChart
    try:
        marketing_budget = DepartmentBudget.objects.get(department_name='Marketing')
        budget_data_mrkt = {
            'Spent Budget': float(marketing_budget.budget - marketing_budget.available_budget),
            'Available Budget': float(marketing_budget.available_budget)
    }
    except DepartmentBudget.DoesNotExist:
        budget_data_mrkt = {}

    budget_data_json_MRKT = json.dumps(budget_data_mrkt)
    #EndMarkett
    #salestart
    try:
        sales_budget = DepartmentBudget.objects.get(department_name='Sales')
        budget_data_sales = {
            'Spent Budget': float(sales_budget.budget - sales_budget.available_budget),
            'Available Budget': float(sales_budget.available_budget)
        }
    except DepartmentBudget.DoesNotExist:
        budget_data_sales = {}

    budget_data_sales_json = json.dumps(budget_data_sales)
    #end
    data = Invoice.objects.annotate(
        month=TruncMonth('date')
    ).values(
        'month', 'department'
    ).annotate(
        total=Sum('total_value')
    ).order_by('month')

    # Convert to a suitable structure for the front end
    chart_data = {}
    for entry in data:
        month = entry['month'].strftime("%B")
        department = entry['department']
        total = float(entry['total'])
        if month not in chart_data:
            chart_data[month] = {}
        chart_data[month][department] = total
    departments_json = json.dumps(chart_data, cls=DecimalEncoder)    
    print(chart_data)
    total_invoices_count = Invoice.objects.count()

    # Count of each invoice type for each department
    invoice_counts = Invoice.objects.values('department', 'invoice_type').annotate(total=Count('invoice_number'))

    # Organize the counts in a usable format
    department_invoice_info = {}
    for entry in invoice_counts:
        department = entry['department']
        if department not in department_invoice_info:
            department_invoice_info[department] = {'total': 0, 'types': {}}
        department_invoice_info[department]['types'][entry['invoice_type']] = entry['total']
        department_invoice_info[department]['total'] += entry['total']

    # Pass data to the template
    context = {
        'total_invoices_count': total_invoices_count,
        'department_invoice_info': department_invoice_info
    }
    all_departments = DepartmentDescription.objects.all()

    return render(request , 'main/t2.html',{'all_departments':all_departments,'total_invoices_count':total_invoices_count,'department_invoice_info':department_invoice_info,'budget_data_json':budget_data_json ,'budget_data_json_MRKT':budget_data_json_MRKT ,'budget_data_sales_json':budget_data_sales_json,'departments_json': departments_json})

#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
import openai
from django.http import JsonResponse
from .models import Invoice
from django.db.models import Sum, Count

def describe_department_spending(request):
    
    openai.api_key = 'test'
    
#

    departments = ['IT', 'Marketing', 'Sales']  # Update as per your DEPARTMENT_CHOICES
    descriptions = {}

    try:
        for department in departments:
           
            total_spent = Invoice.objects.filter(department=department).aggregate(Sum('total_value'))['total_value__sum']
            most_common_invoice_type = Invoice.objects.filter(department=department).values('invoice_type').annotate(count=Count('invoice_type')).order_by('-count').first()

            if most_common_invoice_type:
                invoice_type_desc = most_common_invoice_type['invoice_type']
            else:
                invoice_type_desc = 'No common type'

            
            prompt = f"Describe the spending pattern for the {department} department, which has spent a total of {total_spent}. The most common type of invoice is {invoice_type_desc}."
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150
                
            )

            descriptions[department] = response.choices[0].text.strip()
            DepartmentDescription.objects.update_or_create(
                department=department, 
                defaults={'description': response.choices[0].text.strip()}
            )
        print(descriptions)

        return JsonResponse(descriptions)
    except Exception as e:
        return JsonResponse({'error': str(e)})


