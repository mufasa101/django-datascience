from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView
from .models import Sale
from .utils import get_customer,get_salesguy,get_chart
from reports.forms import ReportForm
from django.http import JsonResponse

import pandas
import random

from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
import csv
import datetime
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    sales_df=None
    positions_df=None
    merged_df=None
    grouped_df=None
    chart=None
    chart_type=None
    no_data=None
    position_data=[]
    report_form=ReportForm()
    
    if request.method=='POST':
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date_to')
        chart_type=request.POST.get('chart_type')
        group_type=request.POST.get('group_type')
        sales_qs = Sale.objects.filter(created_on__date__lte=date_to, created_on__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df=pandas.DataFrame(sales_qs.values())
            sales_df['sales_guy_id']=sales_df['sales_guy_id'].apply(get_salesguy)
            sales_df['customer_id']=sales_df['customer_id'].apply(get_customer)
            sales_df['created_on']=sales_df['created_on'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated_on']=sales_df['updated_on'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({"customer_id":"customer","sales_guy_id":"sales guy","id":"sales_id"},axis=1,inplace=True)
            for sale in sales_qs:
                for pos in sale.get_positions():
                    print("sales id",pos.get_sales_id())
        
                    obj={
                        'ID':pos.id,
                        'Product':pos.product.name,
                        'Quantity':pos.quantity,
                        'price':pos.price,
                        'sales_id':pos.get_sales_id(),
                    }
                position_data.append(obj)
            positions_df=pandas.DataFrame(position_data)
            positions_df.rename({"ID":"Positions id"},axis=1,inplace=True)
            merged_df=pandas.merge(sales_df,positions_df , on='sales_id')
            grouped_df=merged_df.groupby('transaction_id',as_index=False)['total_price'].agg('sum')
            # chart=get_chart(chart_type,grouped_df,labels=grouped_df['transaction_id'].values)
            chart=get_chart(chart_type,sales_df,group_type)
            sales_df=sales_df.to_html()
            positions_df=positions_df.to_html()
            merged_df=merged_df.to_html()
            grouped_df=grouped_df.to_html()
            
        else:
            no_data=f" there was no data available \n from ({date_from}) to ({date_to})"
   
        
    context={
        'report_form':report_form,
        'sales_table':sales_df,
        'positions_table':positions_df,
        'merged_table':merged_df,
        'grouped_table':grouped_df,
        'chart_type':chart_type,
        'chart':chart,
        'no_data':no_data,
        }
    return render(request,"sales/home.html",context)


class SalesListView(LoginRequiredMixin,ListView):
    model=Sale
    template_name="sales/list.html"
    context_object_name="sales"
    
class SalesDetilView(LoginRequiredMixin,DetailView):
    model=Sale
    template_name="sales/detail.html"
class UploadTemplateView(LoginRequiredMixin,TemplateView):
    template_name = 'sales/upload_csv.html'
    
@login_required 
def csv_upload_view(request):

    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        n = random.randint(0,300)
        csv_file_name=str(n) + csv_file_name  
        print("random",n)
        print("new name",csv_file_name)
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.sales_file = csv_file
            obj.save()
            with open(obj.sales_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for data in reader:
                    if data[1]:
                        transaction_id = data[0]
                        product = data[1]
                        quantity = int(data[2])
                        customer = data[3]
                        
                        date = parse_date(datetime.datetime.strptime(data[4], '%m/%d/%Y').strftime('%Y-%m-%d'))
                        print("thiiiiiiiiiiiiiiiiii the date",date)
                        try:
                            product_obj = Product.objects.get(name__iexact=product)
                        except Product.DoesNotExist:
                            product_obj = None
                        print(product_obj)
                        if product_obj is not None:
                            customer_obj, _ = Customer.objects.get_or_create(name=customer) 
                            salesman_obj = Profile.objects.get(user=request.user)
                            position_obj = Position.objects.create(product=product_obj, quantity=quantity, created_on=date)

                            sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, sales_guy=salesman_obj, created_on=date)
                            sale_obj.positions.add(position_obj)
                            sale_obj.save()
                return JsonResponse({'ex': False})
        else:
            return JsonResponse({'ex': True})

    return HttpResponse()