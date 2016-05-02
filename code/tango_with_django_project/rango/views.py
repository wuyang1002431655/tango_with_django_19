from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

# Create your views here.

def index(request):
    #context_dict = {'boldmessage': "Crunchie, creamy, cookie, candy, cupcake!"}
    
    category_list = Category.objects.order_by('-likes')[:5]
    
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {'categories': category_list, 'pages': page_list}
    
    return render(request, 'rango/index.html', context=context_dict)
    

def about(request):

    # To complete the exercise in chapter 4, we need to remove the following line
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>View index page</a>")
    
    # and replace it with a pointer to ther about.html template using the render method
    return render(request, 'rango/about.html',{})
    
def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    
    try:
        # Can we find a category name slug with the given name?
    	# If we can't, the .get() method raises a DoesNotExist exception.
    	# So the .get() method returns one model instance or raises an exception.
    	category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # Note that filter returns a list of page objects or and empty list
        pages = Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
	
    	# We get here if we didn't find the specified category.
    	# Don't do anything -
		# the template will display the "no category" message for us.        
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
	# Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)
    
    
    
    
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            category = form.save(commit=True)
            print(category, category.slug)
            # Now that the category is saved
            # We could give a confirmation message
            # But instead since the most recent catergory added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Will handle the bad form (or form details), new form or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})
    
    
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                # probably better to use a redirect here.
            return show_category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)
