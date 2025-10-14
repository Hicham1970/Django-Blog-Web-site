from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'dashboard/dash.html')



def blogpost(request):
    return render(request, 'dashboard/blogpost.html' )


def comments(request):
    return render(request, 'dashboard/comments.html' )

def charts(request):
    return render(request, 'dashboard/charts.html' )


def pages(request):
    return render(request, 'dashboard/pages.html' )


