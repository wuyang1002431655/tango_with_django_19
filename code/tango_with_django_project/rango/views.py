from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    context_dict = {'boldmessage': "Crunch, creamy, cookie, candy, cupcake!"}
    
    return render(request, 'rango/index.html', context=context_dict)

def about(request):

    # To complete the exercise in chapter 4, we need to remove the following line
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>View index page</a>")
    
    # and replace it with a pointer to ther about.html template using the render method
    return render(request, 'rango/about.html',{})