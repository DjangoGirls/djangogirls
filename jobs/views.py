from django.shortcuts import render

def jobs(request):

    return render(request, 'jobs/jobs.html', {})
