import uuid,base64
from profiles.models import Profile
from customers.models import Customer
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn 
def generate_transaction_id():
    transaction_id=str(uuid.uuid4()).replace("-","").upper()[:12]
    return transaction_id

def get_salesguy(id):
    sales_guy=Profile.objects.get(id=id)
    return sales_guy.get_full_name
def get_customer(id):
    customer=Customer.objects.get(id=id)
    return customer.name

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode("utf-8")
    buffer.close()
    return graph
def get_key(group_by):
    if group_by == 'date':
        key = 'created_on'
    elif group_by == 'transactions':
        key = 'transaction_id'
    return key

def get_chart(chart_type , data,group_by, **kwargs):
    print("daaaaaaaaaata",group_by)
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(5,4))
    key = get_key(group_by)
    cooked_data = data.groupby(key, as_index=False)['total_price'].agg('sum')
    if chart_type=="pie":
        plt.pie(data=cooked_data,x='total_price',labels=cooked_data[key].values)
    elif chart_type=="line":
        labels=kwargs.get('labels')
        plt.plot(cooked_data[key],cooked_data['total_price'],color="#687ae8",marker="o")
        print("Line chart")
    elif chart_type=="bar":
        # plt.bar(data['transaction_id'],data['total_price'])
        seaborn.barplot(x=key,y='total_price',data=cooked_data)
        print("Bar chart")
    else:
        print("OOOps, try another chart")
    plt.tight_layout()
    chart=get_graph()
    return chart
