from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

import datetime

from asset_manage_app.models import housekeep
from asset_manage_app.forms import MakeRecord, SignupForm, SigninForm
from asset_manage_app.graph import Plot_Graph, Plot_PieChart

# Create your views here.    

#Sign up
def record_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("record_signin"))
    else:
        form = SignupForm()
    return render(request, "record_signup.html", {"form": form})
    
#Sign in    
def record_signin(request):
    if request.method == "POST":
        form = SigninForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("record_list"))
    else:
        form = SigninForm()

    return render(request, "record_signin.html", {"form": form})

#Sign out
def record_signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("record_signin"))


# Record List #
category_list = ["Grocery", "Restaurant", "Internet", "Fashion", "Study", "Medical",
            "Subscription", "Utilities", "Other"]
year_list = [2023, 2024]
month_list = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "december"]
month_num = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
              "July": 7, "August": 8, "September": 9, "October": 10, "November": 11,
              "December": 12}
def inverse_lookup(month_num, d):
    for k, v in month_num.items():
        if v == d:
            return k
        
def adjust_for_graph(x, y):
    result = {}
    for i in range(0, len(x)):
        if y[i] in result:
            result[y[i]] += x[i]
        else:
            result[y[i]] = x[i]
    
    items = [i for i in result.keys()]
    values = [v for v in result.values()]
    return values, items

def create_graph_for_search(temp_data1, temp_data2, label, category_value):
    records_amount_for_pie, records_list_for_pie = adjust_for_graph(temp_data1, temp_data2)
    pie_chart_for_search = Plot_PieChart(records_amount_for_pie, records_list_for_pie, 
                                                label, category_value)
    return pie_chart_for_search

@login_required
def record_list(request):
    forms = MakeRecord()

    selected_year = datetime.date.today().year
    d = datetime.date.today().month
    selected_month = inverse_lookup(month_num, d)
    selected_category = ""

    #Current Month#
    current_month = inverse_lookup(month_num, d)

    current_month_base_records = housekeep.objects.filter(
            date__year = datetime.date.today().year, 
            date__month = datetime.date.today().month).order_by(
            "-date")
    per_page = 5
    paginator = Paginator(current_month_base_records, per_page)
    total_page = list(range(1, (paginator.count // per_page + 1) + 1))

    page_for_month = request.GET.get("page", 1)
    try:
        current_month_records = paginator.page(page_for_month)
    except (EmptyPage, PageNotAnInteger):
        current_month_records = paginator.page(1)

    current_total_month_amount = 0
    for record in current_month_base_records:
        current_total_month_amount += record.amount

    temp_amount = [record.amount for record in current_month_base_records]
    temp_category = [record.category for record in current_month_base_records]
    amount_data, category_data = adjust_for_graph(temp_amount, temp_category)
    current_pie_chart = Plot_PieChart(amount_data, category_data, 
                                      label = "category", category_value = current_month)
    
    date_for_bar = [x.date for x in current_month_base_records]
    amount_for_bar= [y.amount for y in current_month_base_records]
    y, x = adjust_for_graph(amount_for_bar, date_for_bar)
    current_bar_chart = Plot_Graph(x, y)

    #Current Month#

    #Search Result#
    records = []
    if request.GET.get("Year") or request.GET.get("Month") or request.GET.get("Category"):
        search = True
        
        
        if request.GET.get("Year") and request.GET.get("Month") and not request.GET.get("Category"):
            y = request.GET.get("Year")
            m = month_num[request.GET.get("Month")]
            records = housekeep.objects.filter(date__year = y, date__month = m)
            if not records:
                search = False
                pie_chart_for_search = ""
            temp_data1 = [record.amount for record in records]
            temp_data2 = [record.category for record in records]
            label = "category"
            category_value = request.GET.get("Month")
            pie_chart_for_search = create_graph_for_search(temp_data1, temp_data2, label, category_value)
        elif not request.GET.get("Month") and request.GET.get("Category"):
            records = housekeep.objects.filter(category = request.GET.get("Category"))
            if not records:
                search = False
                pie_chart_for_search = ""
            temp_data1 = [record.amount for record in records]
            temp_data2 = [inverse_lookup(month_num, record.date.month)
                           for record in records]
            label = "date"
            category_value = request.GET.get("Category")
            pie_chart_for_search = create_graph_for_search(temp_data1, temp_data2, label, category_value)
        elif request.GET.get("Year") and request.GET.get("Month") and request.GET.get("Category"):
            y = request.GET.get("Year")
            m = month_num[request.GET.get("Month")]
            records = housekeep.objects.filter(
                date__year = y,
                date__month = m,
                category = request.GET.get("Category")
            )
            pie_chart_for_search = ""
    else:
        search = False
        pie_chart_for_search = ""

    search_result_amount = 0
    for record in records:
        search_result_amount += record.amount

    search_result_per_page = 10
    search_paginator = Paginator(records, search_result_per_page)
    search_total_page = list(range(1, (search_paginator.count // search_result_per_page + 1) + 1))

    page_for_search = request.GET.get("search_page", 1)
    try:
        records = search_paginator.page(page_for_search)
    except (EmptyPage, PageNotAnInteger):
        records = search_paginator.page(1)

    params = request.GET.copy()
    if "search_page" in params:
        search_page = params["search_page"]
        del params["search_page"]
    else:
        search_page = 1

    search_params = params.urlencode()
    #Search Result#    


    return TemplateResponse(request, "record_list.html", {
                            "forms": forms,
                            "current_month": current_month,
                            "current_month_records": current_month_records,
                            "current_total_month_amount": current_total_month_amount,
                            "current_bar_chart": current_bar_chart,
                            "current_pie_chart": current_pie_chart,
                            "records": records, 
                            "selected_year": selected_year,
                            "selected_month": selected_month,                            "forms": forms,
                            "year_list": year_list,
                            "month_list": month_list,
                            "category_list": category_list,
                            "selected_category": selected_category,
                            "pie_chart_for_search": pie_chart_for_search,
                            "search": search,
                            "search_result_amount": search_result_amount,
                            "total_page": total_page,
                            "search_total_page": search_total_page,
                            "search_params": search_params})

@login_required
def record_add(request):
    forms = MakeRecord(request.POST)
    if forms.is_valid():
        forms.save()
    return HttpResponseRedirect(reverse("record_list"))

@login_required
def record_edit(request, housekeep_id):
    try:
        record = housekeep.objects.get(id = housekeep_id)
    except housekeep.DoesNotExist:
        raise Http404
    
    if request.method == "GET":
        forms = MakeRecord(instance = record)
        return TemplateResponse(request, "record_edit.html", {"record": record, "forms": forms})
    else:
        forms = MakeRecord(request.POST, instance = record)
        if forms.is_valid():
            forms.save()
        return HttpResponseRedirect(reverse("record_list"))

@login_required
@require_POST
def record_delete(request, housekeep_id):
    try:
        record = housekeep.objects.get(id = housekeep_id)
    except housekeep.DoesNotExist:
        raise Http404
    record.delete()
    return HttpResponseRedirect(reverse("record_list"))
    
