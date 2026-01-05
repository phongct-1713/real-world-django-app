from django.shortcuts import render

def index(request):
    """Render the single-page application."""
    return render(request, 'base.html')
