from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

# Create your views here.

def index(request):
    #context_dict = {'boldmessage': "Crunchie, creamy, cookie, candy, cupcake!"}
    
    category_list = Category.objects.order_by('-likes')[:5]
    
    context_dict = {'categories': category_list}
    
    return render(request, 'rango/index.html', context=context_dict)
    

def about(request):

    # To complete the exercise in chapter 4, we need to remove the following line
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>View index page</a>")
    
    # and replace it with a pointer to ther about.html template using the render method
    return render(request, 'rango/about.html',{})