#Forms {#chapter-forms}

So far we have only presented data, in this chapter we will run through how to capture
data through web forms. Django comes with some neat form handling
functionality, making it a pretty straightforward process to gather
information from users and send it back to your web application.
According to [Django's documentation on
forms](https://docs.djangoproject.com/en/1.9/topics/forms/), the form
handling functionality allows you to:

1.  display an HTML form with automatically generated *form widgets*
    (like a text field or date picker);
2.  check submitted data against a set of validation rules;
3.  redisplay a form in case of validation errors; and
4.  convert submitted form data to the relevant Python data types.

One of the major advantages of using Django's forms functionality is
that it can save you a lot of time and HTML hassle. This part of the
tutorial will look at how to implement the necessary infrastructure that
will allow users of Rango to add categories and pages to the database
via forms.

##Basic Workflow

The basic steps involved in creating a form and handling user input is as follows.

1.  If you haven't already got one, create a `forms.py` file within your
    Django application's directory to store form-related classes.
2.  Create a `ModelForm` class for each model that you wish to represent
    as a form.
3.  Customise the forms as you desire.
4.  Create or update a view to handle the form - including *displaying*
    the form, *saving* the form data, and *flagging up errors* which may
    occur when the user enters incorrect data (or no data at all) in the
    form.
5.  Create or update a template to display the form.
6.  Add a `urlpattern` to map to the new view (if you created a new
    one).

This workflow is a bit more complicated than previous workflows, and the
views that we have to construct have a lot more complexity as well.
However, once you undertake the process a few times it will be pretty
clear how everything pieces together.

##Page and Category Forms

First, create a file called `forms.py` within the `rango` application
directory. While this step is not absolutely necessary, as you could put
the forms in the `models.py`, this makes the codebase tidier and easier to work with.

### Creating `ModelForm` Classes

Within Rango's `forms.py` module, we will be creating a number of
classes that inherit from Django's `ModelForm`. In essence, [a
ModelForm](https://docs.djangoproject.com/en/1.9/topics/forms/modelforms/#modelform)
is a *helper class* that allows you to create a Django `Form` from a
pre-existing model. As we've already got two models defined for Rango
(`Category` and `Page`), we'll create `ModelForms` for both.

In `rango/forms.py` add the following code.

{lang="python",linenos=on}
	from django import forms
	from rango.models import Page, Category

	class CategoryForm(forms.ModelForm):
	    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
	    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	    # An inline class to provide additional information on the form.
	    class Meta:
	        # Provide an association between the ModelForm and a model
	        model = Category
	        fields = ('name',)


	class PageForm(forms.ModelForm):
	    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
	    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
	    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	    class Meta:
	        # Provide an association between the ModelForm and a model
	        model = Page

	        # What fields do we want to include in our form?
	        # This way we don't need every field in the model present.
	        # Some fields may allow NULL values, so we may not want to include them...
	        # Here, we are hiding the foreign key.
	        # we can either exclude the category field from the form,
	        exclude = ('category',)
	        #or specify the fields to include (i.e. not include the category field)
	        #fields = ('title', 'url', 'views')


We need to specify which fields that are included on the form, via `fields`, or specify the fields that
are to be excluded, via `exclude`.

Django provides us with a number of ways to customise the forms that are
created on our behalf. In the code sample above, we've specified the
widgets that we wish to use for each field to be displayed. For example,
in our `PageForm` class, we've defined `forms.CharField` for the `title`
field, and `forms.URLField` for `url` field. Both fields provide text
entry for users. Note the `max_length` parameters we supply to our
fields - the lengths that we specify are identical to the maximum length
of each field we specified in the underlying data models. Go back to
Chapter model-label to check for yourself, or have a look at Rango's
`models.py` file.

You will also notice that we have included several `IntegerField`
entries for the views and likes fields in each form. Note that we have
set the widget to be hidden with the parameter setting
`widget=forms.HiddenInput()`, and then set the value to zero with
`initial=0`. This is one way to set the field to zero without giving the
control to the user as the field will be hidden, yet the form will
provide the value to the model. However, as you can see in the
`PageForm`, despite the fact that we have a hidden field, we still need
to include the field in the form. If in `fields` we excluded `views`,
then the form would not contain that field (despite it being specified)
and so the form would not return the value zero for that field. This may
raise an error depending on how the model has been set up. If in the
models we specified that the `default=0` for these fields then we can
rely on the model to automatically populate field with the default
value - and thus avoid a `not null` error. In this case, it would not be
necessary to have these hidden fields. We have also included the field
`slug` in the form, and set it to use the`widget=forms.HiddenInput()`,
but rather than specifying an initial or default value, we have said the
field is not required by the form. This is because our model will be
responsible on `save()` to populating this field. Essentially, you need
to be careful when you define your models and forms to make sure that
form is going to contain and pass on all the data that is required to
populate your model correctly.

Besides the `CharField` and `IntegerField` widget, many more are
available for use. As an example, Django provides `EmailField` (for
e-mail address entry), `ChoiceField` (for radio input buttons), and
`DateField` (for date/time entry). There are many other field types you
can use, which perform error checking for you (e.g. *is the value
provided a valid integer?*). We highly recommend you have a look at the
[official Django documentation on
widgets](https://docs.djangoproject.com/en/1.9/ref/forms/widgets/) to
see what components exist and the arguments you can provide to customise
them.

Perhaps the most important aspect of a class inheriting from `ModelForm`
is the need to define *which model we're wanting to provide a form for.*
We take care of this through our nested `Meta` class. Set the `model`
attribute of the nested `Meta` class to the model you wish to use. For
example, our `CategoryForm` class has a reference to the `Category`
model. This is a crucial step enabling Django to take care of creating a
form in the image of the specified model. It will also help in handling
flagging up any errors along with saving and displaying the data in the
form.

We also use the `Meta` class to specify which fields that we wish to
include in our form through the `fields` tuple. Use a tuple of field
names to specify the fields you wish to include.

I> More about Forms
I>
I> Check out the [official Django documentation
I> on forms](https://docs.djangoproject.com/en/1.9/ref/forms/) for
I> further information about how to customise them.

### Creating an *Add Category* View

With our `CategoryForm` class now defined, we're now ready to create a
new view to display the form and handle the posting of form data. To do
this, add the following code to `rango/views.py`.

{lang="python",linenos=off}
	from rango.forms import CategoryForm

	def add_category(request):
	    # A HTTP POST?
	    if request.method == 'POST':
	        form = CategoryForm(request.POST)

	        # Have we been provided with a valid form?
	        if form.is_valid():
	            # Save the new category to the database.
	            form.save(commit=True)

	            # Now call the index() view.
	            # The user will be shown the homepage.
	            return index(request)
	        else:
	            # The supplied form contained errors - just print them to the terminal.
	            print form.errors
	    else:
	        # If the request was not a POST, display the form to enter details.
	        form = CategoryForm()

	    # Bad form (or form details), no form supplied...
	    # Render the form with error messages (if any).
	    return render(request, 'rango/add_category.html', {'form': form})

The new `add_category()` view adds several key pieces of functionality
for handling forms. First, we check the HTTP request method, to
determine if it was a HTTP `GET` or `POST`. We can then handle different
requests methods appropriately - i.e. whether we want to show a form (if
it is a `GET`), or process form data (if it is a `POST`) - all from the
same URL. The `add_category()` view function can handle three different
scenarios:

-   showing a new, blank form for adding a category;
-   saving form data provided by the user to the associated model, and
    rendering the Rango homepage; and
-   if there are errors, redisplay the form with error messages.

I> ### Get and Post
I>
I> What do we mean by `GET` and `POST`? They are two different types of
I> *HTTP requests*.
I>
I> -   A HTTP `GET` is used to *request a representation of the specified
I>     resource.* In other words, we use a HTTP `GET` to retrieve a
I>     particular resource, whether it is a webpage, image or other file.
I> -   In contrast, a HTTP `POST` *submits data from the client's web
I>     browser to be processed.* This type of request is used for example
I>     when submitting the contents of a HTML form.
I> -   Ultimately, a HTTP `POST` may end up being programmed to create a
I>     new resource (e.g. a new database entry) on the server. This can
I>     later be accessed through a HTTP `GET` request.

Django's form handling machinery processes the data returned from a
user's browser via a HTTP `POST` request. It not only handles the saving
of form data into the chosen model, but will also automatically generate
any error messages for each form field (if any are required). This means
that Django will not store any submitted forms with missing information
which could potentially cause problems for your database's referential
integrity. For example, supplying no value in the category name field
will return an error, as the field cannot be blank.

You'll notice from the line in which we call `render()` that we refer to
a new template called `add_category.html` which will contain the
relevant Django template code and HTML for the form and page.

### Creating the *Add Category* Template

Create the file `templates/rango/add_category.html`. Within the file,
add the following HTML markup and Django template code.

{lang="python",linenos=off}
	<!DOCTYPE html>
	<html>
	    <head>
	        <title>Rango</title>
	    </head>

	    <body>
	        <h1>Add a Category</h1>

	        <form id="category_form" method="post" action="/rango/add_category/">

	            {% csrf_token %}
	            {% for hidden in form.hidden_fields %}
	                {{ hidden }}
	            {% endfor %}

	            {% for field in form.visible_fields %}
	                {{ field.errors }}
	                {{ field.help_text }}
	                {{ field }}
	            {% endfor %}

	            <input type="submit" name="submit" value="Create Category" />
	        </form>
	    </body>

	</html>

Now, what does this code do? You can see that within the `<body>` of the
HTML page that we place a `<form>` element. Looking at the attributes
for the `<form>` element, you can see that all data captured within this
form is sent to the URL `/rango/add_category/` as a HTTP `POST` request
(the `method` attribute is case insensitive, so you can do `POST` or
`post` - both provide the same functionality). Within the form, we have
two for loops - one controlling *hidden* form fields, the other
*visible* form fields - with visible fields controlled by the `fields`
attribute of your `ModelForm` `Meta` class. These loops produce HTML
markup for each form element. For visible form fields, we also add in
any errors that may be present with a particular field and help text
which can be used to explain to the user what he or she needs to enter.

I> ### Hidden Fields
I>
I> The need for hidden as well as visible form fields is necessitated by
I> the fact that HTTP is a stateless protocol. You can't persist state
I> between different HTTP requests which can make certain parts of web
I> applications difficult to implement. To overcome this limitation,
I> hidden HTML form fields were created which allow web applications to
I> pass important information to a client (which cannot be seen on the
I> rendered page) in a HTML form, only to be sent back to the originating
I> server when the user submits the form.

You should also take note of the code snippet `{% csrf_token %}`. This
is a *Cross-Site Request Forgery (CSRF) token*, which helps to protect
and secure the HTTP `POST` action that is initiated on the subsequent
submission of a form. *The CSRF token is required by the Django
framework. If you forget to include a CSRF token in your forms, a user
may encounter errors when he or she submits the form.* Check out the
[official Django documentation on CSRF
tokens](https://docs.djangoproject.com/en/1.9/ref/contrib/csrf/) for
more information about this.

### Mapping the *Add Category* View

Now we need to map the `add_category()` view to a URL. In the template
we have used the URL `/rango/add_category/` in the form's submit
attribute. So we will need to follow suit in `rango/urls.py` and modify
the `urlpatterns` as follows.

{lang="python",linenos=off}
	urlpatterns = patterns('',
    	url(r'^$', views.index, name='index'),
    	url(r'^about/$', views.about, name='about'),
    	url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
    	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),)


Ordering doesn't necessarily matter in this instance. However, take a
look at the [official Django documentation on how Django process a
request](https://docs.djangoproject.com/en/1.9/topics/http/urls/#how-django-processes-a-request)
for more information. Our new URL for adding a category is
`/rango/add_category/`.

### Modifying the Index Page View

As a final step let's put a link on the index page so that we can easily
add categories. Edit the template `rango/index.html` and add the
following HTML hyperlink just before the `</body>` closing tag.

{lang="html",linenos=off}
	<a href="/rango/add_category/">Add a New Category</a><br />


### Demo

Now let's try it out! Run your Django development server, and navigate
to `http://127.0.0.1:8000/rango/`. Use your new link to jump to the add
category page, and try adding a category. Figure fig-rango-form-steps
shows screenshots of the of the Add Category and Index Pages.

![Adding a new category to Rango with our new form. The diagram
illustrates the steps involved.](../images/rango-form-steps.png)

I> ### Note
I>
I> If you add a number of categories, they will not always appear on the
I> index page, that is because we are only showing the top 5 categories
I> on the index page. If you log into the Admin interface you should be
I> able to view all the categories that you have entered. To see what is
I> happening as you entered them in `rango/views.py` in `add_category()`,
I> you can get the reference to the category model object created from
I> `form.save()`, with `cat = form.save(commit=True)` and then print to
I> console the category and slug, with `print cat, cat.slug` to see what
I> is being created.

### Cleaner Forms

Recall that our `Page` model has a `url` attribute set to an instance of
the `URLField` type. In a corresponding HTML form, Django would
reasonably expect any text entered into a `url` field to be a
well-formed, complete URL. However, users can find entering something
like `http://www.url.com` to be cumbersome - indeed, users [may not even
know what forms a correct
URL](https://support.google.com/webmasters/answer/76329?hl=en)!

In scenarios where user input may not be entirely correct, we can
*override* the `clean()` method implemented in `ModelForm`. This method
is called upon before saving form data to a new model instance, and thus
provides us with a logical place to insert code which can verify - and
even fix - any form data the user inputs. In our example above, we can
check if the value of `url` field entered by the user starts with
`http://` - and if it doesn't, we can prepend `http://` to the user's
input.

{lang="python",linenos=off}
	class PageForm(forms.ModelForm):

	    ...

	    def clean(self):
	        cleaned_data = self.cleaned_data
	        url = cleaned_data.get('url')

	        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
	        if url and not url.startswith('http://'):
	            url = 'http://' + url
	            cleaned_data['url'] = url

	            return cleaned_data


Within the `clean()` method, a simple pattern is observed which you can
replicate in your own Django form handling code.

1.  Form data is obtained from the `ModelForm` dictionary attribute
    `cleaned_data`.
2.  Form fields that you wish to check can then be taken from the
    `cleaned_data` dictionary. Use the `.get()` method provided by the
    dictionary object to obtain the form's values. If a user does not
    enter a value into a form field, its entry will not exist in the
    `cleaned_data` dictionary. In this instance, `.get()` would return
    `None` rather than raise a `KeyError` exception. This helps your
    code look that little bit cleaner!
3.  For each form field that you wish to process, check that a value was
    retrieved. If something was entered, check what the value was. If it
    isn't what you expect, you can then add some logic to fix this issue
    before *reassigning* the value in the `cleaned_data` dictionary for
    the given field.
4.  You *must* always end the `clean()` method by returning the
    reference to the `cleaned_data` dictionary. If you don't, you'll get
    some really frustrating errors!

This trivial example shows how we can clean the data being passed
through the form before being stored. This is pretty handy, especially
when particular fields need to have default values - or data within the
form is missing, and we need to handle such data entry problems.

I> ### Clean Overrides
I>
I> Overriding methods implemented as part of the Django framework can
I> provide you with an elegant way to add that extra bit of functionality
I> for your application. There are many methods which you can safely
I> override for your benefit, just like the `clean()` method in
I> `ModelForm` as shown above. Check out [the Official Django
I> Documentation on
I> Models](https://docs.djangoproject.com/en/1.9/topics/db/models/#overriding-predefined-model-methods)
I> for more examples on how you can override default functionality to
I> slot your own in.


X> ###Exercises
X>
X> Now that you've worked through the chapter, try these exercises to
X> solidify your knowledge on Django's form functionality.
X> 
X> -   What happens when you don't enter in a category name on the add category form?
X> -   What happens when you try to add a category that already exists?
X> -   What happens when you visit a category that does not exist?
X> -   How could you gracefully handle when a user visits a category that does not exist?
X> -   Undertake the [part four of the official Django Tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial04/)
X>     if you have not done so already to reinforce what you have learnt here.

### Creating an *Add Pages* View, Template and URL Mapping

A next logical step would be to allow users to add pages to a given
category. To do this, repeat the same workflow above for Pages - create
a new view (`add_page()`), a new template (`rango/add_page.html`), URL
mapping and then add a link from the category page. To get you started,
here's the view logic for you.

{lang="python",linenos=off}
	from rango.forms import PageForm

	def add_page(request, category_name_slug):

	    try:
	        cat = Category.objects.get(slug=category_name_slug)
	    except Category.DoesNotExist:
	            cat = None

	    if request.method == 'POST':
	        form = PageForm(request.POST)
	        if form.is_valid():
	            if cat:
	                page = form.save(commit=False)
	                page.category = cat
	                page.views = 0
	                page.save()
	                # probably better to use a redirect here.
	                return category(request, category_name_slug)
	        else:
	            print form.errors
	    else:
	        form = PageForm()

	    context_dict = {'form':form, 'category': cat}

	    return render(request, 'rango/add_page.html', context_dict)


T> ### Hints
T> 
T> To help you with the exercises above, the following hints may be of some use to you.
T>
T> -   Update the `category()` view to pass `category_name_slug` by inserting it to the view's `context_dict` dictionary.
T> -   Update the `category.html` with a link to  `/rango/category/<category_name_url>/add_page/`.
T> -   Ensure that the link only appears when *the requested category
T>    exists* - with or without pages. i.e. in the template check with
T>    `{% if category %} .... {% else %} A category by this name does not exist {% endif %}`.
T> -   Update `rango/urls.py` with a URL mapping to handle the above link.