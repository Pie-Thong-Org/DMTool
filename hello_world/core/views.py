from django.shortcuts import render

def index(request):
    context = {
        "title": "DM Tool ß",
    }
    return render(request, "index.html", context)
