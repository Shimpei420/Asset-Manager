import matplotlib.pyplot as plt
import base64
from io import BytesIO
import datetime
import calendar
import numpy as np

def MonthNumberToMonthName(date):
    if date == "":
        return
    else:
        return date.strftime("%B")

def Output_Graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph

def Plot_Graph(x, y):
    today = datetime.date.today()
    end_day = calendar.monthrange(today.year, today.month)[1]
    first_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month, end_day)
    month_in_english = MonthNumberToMonthName(today)
    plt.switch_backend("AGG")     
    plt.figure(figsize=(10,5))    
    plt.bar(x, y, align = "edge")                 
    plt.xticks(np.arange(first_date, end_date, np.timedelta64(1,'D')), rotation=45)       
    plt.xlim(first_date, end_date, 10)
    plt.title(f"Daily Spend in {month_in_english}", fontsize = 20) 
    plt.xlabel("Date")            
    plt.ylabel("Amount")
    plt.tight_layout()            
    graph = Output_Graph() 
    return graph  


def Plot_PieChart(p,l, label, category_value):
    plt.rcParams['font.family'] = 'Yu Gothic'
    c = ["skyblue", 'powderblue', 'lightcyan', 'cadetblue',"cornflowerblue"]
    plt.switch_backend("AGG")
    plt.figure(figsize=(4,4))
    if label == "category":
        plt.pie(p, autopct="%d%%", labels = l, colors = c, counterclock=False, startangle=90, radius=0.8, center=(0, 0))
        plt.title(f'How to spend in {category_value}', fontsize=15)
    elif label == "date":
        plt.pie(p, autopct="%d%%", labels = l, colors = c, counterclock=False, startangle=90, radius=0.8, center=(0, 0))
        plt.title(f'When to spend for {category_value}', fontsize=15)
    
    graph = Output_Graph()
    return graph