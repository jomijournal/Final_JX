from django.shortcuts import render
from models import det_ax, cli_ax
from webform import orgform, commentform
import netaddr
import string

def home(request):
    form = orgform()
    textform = commentform()
    return render(request, 'jaxapp/index.html', {'dropdownform': form, 'anotherform': textform})

def detail(request):
    if request.method == 'POST':
        form =  orgform(request.POST)

    if form.is_valid():
        org_id = form.cleaned_data['organization']
        orgname = cli_ax.objects.filter(id=org_id)[0].org
        detail_data = det_ax.objects.filter(org=orgname).order_by('-time')
        count_data = det_ax.objects.filter(org=orgname).count()

    return render(request, 'jaxapp/detail_view.html', {'detail_form' : detail_data, 'ip_name' : orgname,'count' : count_data})

def summary(request):
    if request.method == 'POST':
        form = orgform(request.POST)

    if form.is_valid():
      org_id = form.cleaned_data['organization']
      orgname = cli_ax.objects.filter(id=org_id)[0].org
      monthly = det_ax.objects.values("month").distinct()
      yearly = det_ax.objects.values("year").distinct()

      newdict = []
      for y in monthly:
        for z in yearly:
            a = det_ax.objects.filter(org=orgname).filter(month=y["month"]).filter(year=z["year"]).count()
            b = det_ax.objects.filter(org=orgname).filter(month=y["month"]).filter(year=z["year"]).values('ip').distinct()
            if a > 0:
                newdict.append([y["month"], " ", z["year"], " => ", " Unique: IPs: ", len(b), "/ Session IDs:  ", a])

            dm = {'Jan':12,'Feb':11,'Mar':10,'Apr':9,'May':8,'Jun':7,'Jul':6,'Aug':5,'Sep':4,'Oct':3,'Nov':2,'Dec':1}
            dy = {'2017':1,'2016':2,'2015':3}

            newdict.sort(key=lambda x: (dy[x[2]], dm[x[0]]))
            print newdict
    return render(request, 'jaxapp/summary_view.html', {"sum_dict" : newdict, 'ip_name' : orgname})

def ip_add(request):
    if request.method == 'POST':
        form = orgform(request.POST)

    if form.is_valid():
        org_id = form.cleaned_data['organization']
        orgname = cli_ax.objects.filter(id=org_id)[0].org
        ip_data = det_ax.objects.filter(org=orgname).values('ip').distinct()
        count_data = det_ax.objects.filter(org=orgname).values('ip').distinct().count()

    return render(request, 'jaxapp/ip_add.html', ({'ip_details' : ip_data, 'ip_name' : orgname, 'count' : count_data}))

def ip_check(request):
    if request.method == 'POST':
        form_class = commentform(request.POST)

    if form_class.is_valid():
        raw_input = form_class.cleaned_data['content']

    # print "running script for ip addresses"
    cleaned_input = raw_input.encode('utf8')
    # print type(cleaned_input)
    formatted_string = cleaned_input.replace(",", "-").replace("|", ",")


    print "PRINTING FORMATTED STRING"
    # print formatted_string
    formatted_array = formatted_string.split(",")
    print formatted_array
    ipa = []
    for x in formatted_array:
        if "-" in x:
            y = x.split("-")
            a = y[0].replace('.','')
            fa = float(a)
            while fa < 10**11:
                fa = fa *10
            print fa
            b = y[1].replace('.','')
            fb = float(b)
            while fb < 10**11:
                fb = fb *10
            print fb
            ipa.append([fa,fb])

        else:
            a = x.replace('.','',)
            fa = float(a)
            while fa < 10**11:
                fa = fa *10
            print fa
            ipa.append([fa,fa])
        print ipa

    monthly = det_ax.objects.values("month").distinct()
    yearly = det_ax.objects.values("year").distinct()

    newdict = []
    for y in monthly:
        for z in yearly:
            sum_count = []
            for s in ipa:
                a = det_ax.objects.filter(ip_float__range=(s[0],s[1])).filter(month=y["month"]).filter(year=z["year"]).count()
                sum_count.append(a)
                # b = det_ax.objects.filter(ip__in=s).filter(month=y["month"]).filter(year=z["year"]).values('ip').distinct()
            if sum(sum_count) > 0:
                newdict.append([y["month"], " ", z["year"], " => ", " Session IDs:  ", sum(sum_count)])
                # print newdict

        dm = {'Jan':12,'Feb':11,'Mar':10,'Apr':9,'May':8,'Jun':7,'Jul':6,'Aug':5,'Sep':4,'Oct':3,'Nov':2,'Dec':1}
        dy = {'2017':1,'2016':2,'2015':3}

        newdict.sort(key=lambda x: (dy[x[2]], dm[x[0]]))
        print newdict
    return render(request, 'jaxapp/ip_check.html', {"sum_dict" : newdict, "ip_array" : formatted_array})
