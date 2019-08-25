from django.shortcuts import render

# Create your views here.


def monitor_exam(request, exam_id):
    
    
    return render(request, "admin_html/monitor-exam.html")

def exam_report(request):
        
    return render(request, "admin_html/exam-report.html")