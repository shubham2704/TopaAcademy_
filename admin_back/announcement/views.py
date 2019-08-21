from django.shortcuts import render

# Create your views here.

def announcement_view(request):
    
    return render(request, "admin_html/announcement.html")
