#Making Rango Tango! Code and Hints {#chapter-hints}

Hopefully, you will have been able to complete the exercises given the workflows we provided. If not, or if you need a little help, have a look at the potential solutions we have provided below, and use them within your version of Rango.

I> ### Got a different solution?
I> The solutions provided in this chapter address one potential way to solve each problem. There are more than likely many different ways in which the problems can be solved. If you find a different way to solve them, let us know!

## Track Page Click Throughs

Currently, Rango provides a direct link to external pages. This is not very good if you want to track the number of times each page is clicked and viewed. To count the number of times a page is viewed via Rango, you'll need to perform the following steps.

### Creating a URL Tracking View

Create a new view called `track_url()` in `/rango/views.py` which takes
a parameterised HTTP `GET` request (i.e. `rango/goto/?page_id=1`) and
updates the number of views for the page. The view should then redirect
to the actual URL.

{lang="python",linenos=off}
	from django.shortcuts import redirect
	
	def track_url(request):
		page_id = None
		url = '/rango/'
		if request.method == 'GET':
			if 'page_id' in request.GET:
				page_id = request.GET['page_id']
				try:
					page = Page.objects.get(id=page_id)
					page.views = page.views + 1
					page.save()
					url = page.url
					except:
					pass
		return redirect(url)


Be sure that you import the `redirect()` function to `views.py` if it
isn't included already!

{lang="python",linenos=off}
	from django.shortcuts import redirect


### Mapping URL

In `/rango/urls.py` add the following code to the `urlpatterns` tuple.

{lang="python",linenos=off}
	url(r'^goto/$', views.track_url, name='goto'),


### Updating the Category Template

Update the `category.html` template so that it uses
`rango/goto/?page_id=XXX` instead of providing the direct URL for users
to click.

{lang="python",linenos=off}
	{% for page in pages %}
	<li>
		<a href="{% url 'goto' %}?page_id={{page.id}}">{{ page.title }}</a>
		{% if page.views > 1 %}
			({{ page.views }} views)
		{% elif page.views == 1 %}
			({{ page.views }} view)
		{% endif %}
	</li>
	{% endfor %}


Here you can see that in the template we have added some control
statements to display `view`, `views` or nothing depending on the value
of `page.views`.

### Updating Category View

Since we are tracking the number of click throughs you can now update
the `category()` view so that you order the pages by the number of
views, i.e:

{lang="python",linenos=off}
	pages = Page.objects.filter(category=category).order_by('-views')

Now, confirm it all works, by clicking on links, and then going back to
the category page. Don't forget to refresh or click to another category
to see the updated page.

## Searching Within a Category Page

Rango aims to provide users with a helpful directory of page links. At
the moment, the search functionality is essentially independent of the
categories. It would be nicer however to have search integrated into
category browsing. Let's assume that a user will first browse their
category of interest first. If they can't find the page that they want,
they can then search for it. If they find a page that is suitable, then
they can add it to the category that they are in. Let's tackle the first
part of this description here.

We first need to remove the global search functionality and only let
users search within a category. This will mean that we essentially
decommission the current search page and search view. After this, we'll
need to perform the following.

### Decommissioning Generic Search

Remove the generic *Search* link from the menu bar by editing the
`base.html` template. You can also remove or comment out the URL mapping
in `rango/urls.py`.

### Creating a Search Form Template

After the categories add in a new `div` at the bottom of the template in `category.html`, and add in the search form.
This is very similar to the template code in the `search.html`, but we have updated the action to point to the `show_category` page. We also pass through a variable called `query`, so that the user can see what query has been issued.

{lang="html",linenos=off}
	<form class="form-inline" id="user_form"
		method="post" action="{% url 'show_category'  category.slug %}">
		{% csrf_token %}
		<div class="form-group">
			<input class="form-control" type="text" size="50"
				name="query" value="{{ query }}" id="query" />
		</div>
		<button class="btn btn-primary" type="submit" name="submit"
			value="Search">Search</button>
	</form>

After the search form, we need to provide a space where the results are rendered. Again, this code is similar to the template code in `search.html`.

{lang="html",linenos=off}
	<div>
	{% if result_list %}
		<h3>Results</h3>
		<!-- Display search results in an ordered list -->
		<div class="list-group">
		{% for result in result_list %}
			<div class="list-group-item">
				<h4 class="list-group-item-heading">
					<a href="{{ result.link }}">{{ result.title }}</a>
				</h4>
				<p class="list-group-item-text">{{ result.summary }}</p>
			</div>
		{% endfor %}
		</div>
	{% endif %}
	</div>
	

Remember to wrap the search form and search results with `{% if user.authenticated %}` and `{% endif %}`, so that only authenticated users can search. You don't want random users to be wasting your Bing Search budget!

### Updating the Category View
Update the category view to handle a HTTP `POST` request (i.e. when the
user submits a search) and inject the results list into the context. The
following code demonstrates this new functionality.

{lang="python",linenos=off}
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
		# Note that filter() returns a list of page objects or an empty list
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
		
		
		# New code added here to handle a POST request
		
		# create a default query based on the category name
		# to be shown in the search box
		context_dict['query'] = category.name
		
		result_list = []
		if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
		# Run our Bing function to get the results list!
		result_list = run_query(query)
		context_dict['query'] = query
		context_dict['result_list'] = result_list
		
		
		# Go render the response and return it to the client.
		return render(request, 'rango/category.html', context_dict)

Notice that in the `context_dict` that we pass through, now includes
the `result_list` and `query`, and if there is no query, we provide a
default query, i.e. the category name. The query box then displays this
value.

## Creating and Viewing Profiles {#section-hints-profiles}
This section provides a solution for creating Rango `UserProfile` accounts, and provides the necessary infrastructure to allow users of Rango to view these profiles. Recall that the standard Django `auth` `User` object contains a variety of standard information regarding an individual user, such as a username and password. We however chose to implement an additional `UserProfile` model to store additional information such as a user's Website and a profile picture. Here, we'll go through how you can implement this, using the following steps.

- Create a `profile_registration.html` which will display the `UserProfileForm`.
- Create a `UserProfileForm` `ModelForm` class to handle the new form.
- Create a `register_profile()` view to capture the profile details.
- Map the view to a URL, i.e. `rango/register_profile/`.
- In the `MyRegistrationView` defined in the [Django `registration-redux` chapter](#section-redux-templates-flow), update the `get_success_url()` to point to `rango/add_profile/`.


The basic flow for a registering user here would be:

- clicking the `Register` link;
- filling out the initial Django `registration-redux` form (and thus registering);
- filling out the new `UserProfileForm` form; and
- completing the registration.

This therefore assumes that a user will be registered with Rango *before* the profile form is saved.

### Creating a Profile Registration Template
First, let's create a template that'll provide the necessary markup for displaying an additional registration form. In this solution, we're going to keep the Django Registration-Redux form separate from our Profile Registration form - just to delineate between the two. If you can think of a neat way to mix both forms together, why not try it?

Create a template in Rango's templates directory called `profile_registration.html`. Within this new template, add the following markup and Django template code.

{lang="html",linenos=off}
	{% extends "rango/base.html" %}
	
	{% block title_block %}
	    Registration - Step 2
	{% endblock %}
	
	{% block body_block %}
	    <h1>Registration - Step 2</h1>
	    <form method="post" action=".">
	        {% csrf_token %}
	        {{ form.as_p }}
	        <input type="submit" value="Submit" />
	    </form>
	{% endblock %}

Much like the previous Django Registration-Redux form that we [created previously](#section-redux-templates-login), this template inherits from our `base.html` template, which incorporates the basic layout for our Rango app. We also create an HTML `form` inside the `body_block` block. This will be populated with fields from a `form` object that we'll be passing into the template from the corresponding view (see below).

### Creating the `UserProfileForm` Class
Looking at Rango's `models.py` module, you should see a `UserProfile` model that you implemented previously. We've included it below to remind you of what it contains - a reference to a Django `contrib.auth.User` object, and fields for storing a Website and profile image.

{lang="python",linenos=off}
	class UserProfile(models.Model):
	    # This line is required. Links UserProfile to a User model instance.
	    user = models.OneToOneField(User)
	    # The additional attributes we wish to include.
	    website = models.URLField(blank=True)
	    picture = models.ImageField(upload_to='profile_images', blank=True)
	    
	    # Override the __unicode__() method to return out something meaningful!
	    def __str__(self):
	        return self.user.username

In order to provide the necessary HTML markup on the fly for this model, we need to implement a Django `ModelForm` class, based upon our `UserProfile` model. Looking back to the [chapter detailing Django forms](#chapter-forms), we can implement a `ModelForm` for our `UserProfile` as shown in the example below. Perhaps unsurprisingly, we call this new class `UserProfileForm`.

{lang="python",linenos=off}
	class UserProfileForm(forms.ModelForm):
	    website = forms.URLField(required=False)
	    picture = forms.ImageField(required=False)
	    
	    class Meta:
	        model = UserProfile
	        exclude = ('user',)

Note the inclusion of optional (through `required=False`) `website` and `picture` HTML form fields - and the nested `Meta` class that associates the `UserProfileForm` with the `UserProfile` model. The `exclude` attribute instructs the Django form machinery to *not* produce a form field for the `user` model attribute. As the newly registered user doesn't have reference to their `User` object, we'll have to manually associate this with their new `UserProfile` instance when we create it later.

### Creating a Profile Registration View
Next, we need to create the corresponding view to handle the processing of a `UserProfileForm` form, the subsequent creation of a new `UserProfile` instance, and instructing Django to render any response with our new `profile_registration.html` template. By now, this should be pretty straightforward to implement. Handling a form means being able to handle a request to render the form (via a HTTP `GET`), and being able to process any entered information (via a HTTP `POST`). A possible implementation for this view is shown below.

{lang="python",linenos=off}
	@login_required
	def register_profile(request):
	    form = UserProfileForm()
	    
	    if request.method == 'POST':
	        form = UserProfileForm(request.POST)
	        if form.is_valid():
	            user_profile = form.save(commit=False)
	            user_profile.user = request.user
	            user_profile.save()
	            
	            return redirect('index')
	        else:
	            print(form.errors)
	
	    context_dict = {'form':form}
	    
	    return render(request, 'rango/profile_registration.html', context_dict)

Upon creating a new `UserProfileForm` instance, we then check our `request` object to determine if a `GET` or `POST` was made. If the request was a `POST`, we then recreate the `UserProfileForm`, using data gathered from the `POST` request. We then check if the submitted form was valid - meaning that form fields were filled out correctly. In this case, we only really need to check if the URL supplied is valid - since the URL and profile picture fields are marked as optional.

With a valid `UserProfileForm`, we can then create a new instance of the `UserProfile` model with the line `user_profile = form.save(commit=False)`. Setting `commit=False` gives us time to manipulate the `UserProfile` instance before we commit it to the database. This is where can then add in the necessary step to associate the new `UserProfile` instance with the newly created `User` object that has been just created (refer to the [flow at the top of this section](#section-hints-profiles) to refresh your memory). After successfully saving the new `UserProfile` instance, we then redirect the newly created user to Rango's `index` view, using the URL pattern name. If form validation failed for any reason, errors are simply printed to the console. You will probably in your own code want to make the handling of errors more robust.

If the request sent was a HTTP `GET`, the user simply wants to request a blank form to fill out - so we respond by `render`ing the `profile_registration.html` template created above with a blank instance of the `UserProfileForm`, passed to the rendering context dictionary as `form` - thus satisfying the requirement we created in our template. This solution should therefore handle all required scenarios for creating, parsing and saving data from a `UserProfileForm` form.

E> ### Can't find `login_required`?
E> Remember, once a newly registered user hits this view, they will have had a new account created for them - so we can safely assume that he or she is now logged into Rango. This is why we are using the neat `@login_required` decorator at the top of our view to prevent individuals from accessing the view when they are unauthorised to do so.
E> 
E> If you are receiving an error stating that the `login_required()` function (used as a decorator to our new view) cannot be located, ensure that you have the following `import` statement at the top of your `view.py` module.
E>
E> {lang="python",linenos=off}
E> 	from django.contrib.auth.decorators import login_required

### Mapping the View to a URL
Now that our template, `ModelForm` and corresponding view have all been implemented, a seasoned Djangoer should now be thinking: *map it!* We need to map our new view to a URL, so that users can access the newly created content. This can be easily achieved by opening up Rango's `urls.py` module, and adding the following line to the `urlpatterns` list.

{lang="python",linenos=off}
	url(r'^register_profile/$', views.register_profile, name='register_profile'),

This maps our new `register_profile()` view to the URL `/rango/register_profile/`. Remember, the `/rango/` part of the URL comes from your project's `urls.py` module - the remainder of the URL is then handled by the Rango app's `urls.py` module.

### Modifying Registration Flow
Now that everything is (almost) working, we need to tweak the process that users undertake when registering. Back in the [Django `registration-redux` chapter](#section-redux-templates-flow), we created a new class-based view called `MyRegistrationView` that changes the URL that users are redirected to upon a successful registration. This needs to be changes from redirecting a user to the Rango homepage (with URL name `index`) to our new user profile registration URL. From the previous section, we gave this the name `register_profile`. This therefore means simply changing the `MyRegistrationView` class to look like the following example.

{lang="python",linenos=off}
	class MyRegistrationView(RegistrationView):
	    def get_success_url(self,request, user):
	        return url('register_profile')

Now when a user registers, they should be then redirected to the profile registration form - and upon successful completion of that - be redirected to the Rango homepage. It's easy when you know how...