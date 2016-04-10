#Django Basics {#chapter-django-basics}


Let's get started with Django! In this chapter, we'll be giving you an
overview of the creation process . You'll be setting up a
new project and a new web application. By the end of this chapter, you
will have a simple Django-power webpage up and running!

##Testing your Setup

Let's start by checking that your Python and Django installations are
correct, and are at the right versions for this tutorial.
To do this, open a new terminal window and issue the following
command, which tells you what Python version you have:

```text
    $ python --version
```

The response should be something like: `2.7.10` or `3.5.1`, but any 2.7.5+ or 3.4+ versions of Python should work fine. If you need to upgrade or install Python go to the Section on installing software. 

After verifying your Python installation, check your Django installation. In your terminal window, run the Python interpreter by issuing the following command.

```text
    $ python 
	Python 2.7.10 (default, Jul 14 2015, 19:46:27) 
	[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>>
```

At the prompt, enter the following commands:

```text
	>>> import django
	>>> django.get_version()
	'1.9.5'
	>>> exit()
```	

All going well you should see the correct version of Django, and then can use `exit()` to leave the Python interpreter. If `import django` fails to import, then check that you are in your virtual environment, and check what packages are installed with `pip list` at the terminal window. 

If you have problems with installing the packages or have a different version installed, go to Chapter [System Setup](#chapter-system-setup) or consult the [Django Documentation on Installing
Django](https://docs.djangoproject.com/en/1.9/topics/install/) for more
information. 

##Creating your Django Project
To create a new Django Project, go to your `code` or `workspace` directory, and issue the following command:

```text
	$ django-admin.py startproject tango_with_django_project`
```

I> ### Windows Note
I>
I> On Windows you may have to use the full path to the django-admin.py
I> script. i.e.
I> `python c:\python27\scripts\django-admin.py startproject tango_with_django_project`
I> as suggested on
I> [StackOverflow](http://stackoverflow.com/questions/8112630/cant-create-django-project-using-command-prompt).

This command will invoke the `django-admin.py` script, which will set up
a new Django project called `tango_with_django_project` for you.
Typically, we append `_project` to the end of our Django project
directories so we know exactly what they contain - but the naming
convention is entirely up to you.

You'll now notice within your workspace is a directory set to the name
of your new project, `tango_with_django_project`. Within this newly
created directory, you should see two items:

-   another directory with the same name as your project,
    `tango_with_django_project`; and
-   a Python script called `manage.py`.

For the purposes of this tutorial, we call this nested directory called `tango_with_django_projectI` the
*project configuration directory*. Within this directory, you will find
four Python scripts. We will discuss this scripts in detail later on,
but for now you should see:

-   `__init__.py`, a blank Python script whose presence indicates to the
    Python interpreter that the directory is a Python package;
-   `settings.py`, the place to store all of your Django project's
    settings;
-   `urls.py`, a Python script to store URL patterns for your project;
    and
-   `wsgi.py`, a Python script used to help run your development server
    and deploy your project to a production environment.

I> ###Note
I>
I> The project configuration directory has been created with new Django
I> projects since version 1.4. Having two directories with the same name
I> may seem quite a bit odd, but the change was made to separate out
I> project-related components from individual applications.

In the project directory, you will see there is a file called
`manage.py`. We will be calling this script time and time again as we
develop our project. It provides you with a series of commands you
can run to maintain your Django project. For example, `manage.py` allows
you to run the built-in Django development server to test your work and
run database commands. You'll be using this script a lot throughout the
development cycle.

I> ###For Further Information on Django Admin Script
I>
I> See the Django documentation for more details about the 
I> [Admin and Manage scripts](https://docs.djangoproject.com/en/1.9/ref/django-admin/#django-admin-py-and-manage-py).

You can try using the `manage.py` script now, by issuing the following
command.

`$ python manage.py runserver`

Executing this command will instruct Django to initiate its lightweight
development server. You should see the output in your terminal window similar
to the example shown below:

```text
    $ python manage.py runserver
	
	Performing system checks...

	System check identified no issues (0 silenced).

	You have unapplied migrations; your app may not work properly until they are applied.
	Run 'python manage.py migrate' to apply them.

	April 10, 2016 - 11:07:24
	Django version 1.9.5, using settings 'tango_with_django_project.settings'
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.
```

In the output you can see a number of things. First, there are no issues. However, second there is an issue, i.e. unapplied migrations. We will talk about these in more detail when we setup our database, but for now we can ignore these. Third, and most importantly, you can see that a URL has been specified: `http://127.0.0.1:8000/`, which is the address of the Django development webserver.
   

Now open up your favourite web browser and enter the URL
<http://127.0.0.1:8000/> [\#f1]\_. You should see a webpage similar to
the one shown in [Figure](#img-ch3-django-powered-page).

![A screenshot of the initial Django page you will see when running the
development server for the first
time.](../images/ch3-django-powered-page.png){id="img-ch3-django-powered-page"}

You can stop the development server at anytime by pushing `CTRL + C` in
your terminal window. If you wish to run the development server on a
different port, or allow users from other machines to access it, you can
do so by supplying optional arguments. Consider the following command:

```
	$ python manage.py runserver <your_machines_ip_address>:5555
```
Executing this command will force the development server to respond to
incoming requests on TCP port 5555. You will need to replace
`<your_machines_ip_address>` with your computer's IP address or 127.0.0.1. 

When setting ports, it is unlikely that you will be able to use TCP port
80 or 8080 as these are traditionally reserved for HTTP traffic. Also, any port
below 1024 is considered to be
[privileged](http://www.w3.org/Daemon/User/Installation/PrivilegedPorts.html)
by your operating system. 

While you won't be using the lightweight development server to deploy
your application,  it is nice to be able to demo your
application on another machine in your network. Running the server with your
machine's IP address will enable others to enter in
`http://<your_machines_ip_address>:<port>/` and view your web
application. Of course, this will depend on how your network is
configured. There may be proxy servers or firewalls in the way which
would need to be configured before this would work. Check with the
administrator of the network you are using if you can't view the
development server remotely.

I> ###Note
I>
I> The `django-admin.py` and `manage.py` scripts provides a lot of
I> useful, time-saving functionality for you. `django-admin.py` allows
I> you to start new projects and apps, along with other commands. Within
I> your project directory, `manage.py` allows you to perform
I> administrative tasks within the scope of your project only. Simply
I> execute the relevant script name without any arguments to see what you
I> can do with each. The [official Django documentation provides a
I> detailed list and explanation of each possible
I> command](https://docs.djangoproject.com/en/1.9/ref/django-admin/) you
I> can supply for both scripts.

If you are using version control, now is be a good time to commit the
changes you have made to your workspace. Refer to the 
[crash course on GIT chapter](#chapter-git) if you can't remember the
commands and steps involved in doing this.

##Creating a Django Application

A Django project is a collection of *configurations* and *applications*
that together make up a given web application or website. One of the
intended outcomes of using this approach is to promote good software
engineering practices. By developing a small series of applications, the
idea is that you can theoretically drop an existing application into a
different Django project and have it working with minimal effort. Why
reinvent the wheel if it's already there? [1]

A Django application exists to perform a particular task. You need to
create specific applications that are responsible for providing your
site with particular kinds of functionality. For example, we could
imagine that a project might consist of several applications including a
polling app, a registration app, and a specific content related app. In
another project, we may wish to re-use the polling and registration apps, and so can include them in other projects. We will talk about this later, for now we are going to create the application for the *Rango* app.


To do this, from within your Django project directory (e.g. `<workspace>/tango_with_django_project`),
run the following command.

    $ python manage.py startapp rango

The `startapp` command creates a new directory within your project's
root. Unsurprisingly, this directory is called `rango` - and contained
within it are another five Python scripts:

-   another `__init__.py`, serving the exact same purpose as discussed
    previously;
-   `admin.py`, where you can register your models so that you can benefit
	    from some Django machinery which creates an admin interface for you.
-   `apps.py`, 
-   `models.py`, a place to store your application's data models - where
    you specify the entities and relationships between data;
-   `tests.py`, where you can store a series of functions to test your
    application's code; 
-   `views.py`, where you can store a series of functions that handle requests and return responses; and
- `migrations` directory, which stores database specific information related to your models.
    

`views.py` and `models.py` are the two files you will use for any given
application, and form part of the main architectural design pattern
employed by Django, i.e. the *Model-View-Template* pattern. You can
check out [the official Django
documentation](https://docs.djangoproject.com/en/1.9/intro/overview/) to
see how models, views and templates relate to each other in more detail.

Before you can get started with creating your own models and views, you
must first tell your Django project about your new application's
existence. To do this, you need to modify the `settings.py` file,
contained within your project's configuration directory. Open the file
and find the `INSTALLED_APPS` tuple. Add the `rango` application to the
end of the tuple, which should then look like the following example.

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rango',
)
```

Verify that Django picked up your new application by running the
development server again. If you can start the server without errors,
your application was picked up and you will be ready to proceed to the
next step.

##Creating a View


With our Rango application created, let's now create a simple view. For
our first view, let's just send some simple text back to the client - we
won't concern ourselves about using models or templates just yet.

In your favourite IDE, open the file `views.py`, located within your
newly created `rango` application directory. Remove the comment
`# Create your views here.` so that you now have a blank file.

You can now add in the following code.

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there partner!")
```

Breaking down the three lines of code, we observe the following points
about creating this simple view.

-   We first import the
    [HttpResponse](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpResponse)
    object from the `django.http` module.
-   Each view exists within the `views.py` file as a series of
    individual functions. In this instance, we only created one view -
    called `index`.
-   Each view takes in at least one argument - a
    [HttpRequest](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpRequest)
    object, which also lives in the `django.http` module. Convention
    dictates that this is named `request`, but you can rename this to
    whatever you want if you so desire.
-   Each view must return a HttpResponse object. A simple HttpResponse
    object takes a string parameter representing the content of the page
    we wish to send to the client requesting the view.

With the view created, you're only part of the way to allowing a user to
access it. For a user to see your view, you must map a [Uniform
Resources Locator
(URL)](http://en.wikipedia.org/wiki/Uniform_resource_locator) to the
view.

To create an initial mapping, open `urls.py` located in your project directory, and add the following lines of code to the `urlpatterns`:


```python

from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]
```

This maps the basic URL to the `index` view in the `rango` application. Run the development server (e.g. `python manage.py runserver`) and visit http://127.0.0.1:8000 or whatever address your development server is running on.


##Mapping URLs
Rather than directly mapping URLs from the project to the application, we can make our application more modular (and thus re-usable) by changing how we route the incoming URL to a view. To do this we first need to modify the project's `urls.py` and have it point to the application to handle any specific rango application requests. Then, we need to specify how rango deals with such requests.

First, open the project's `urls.py` file
which is located inside your project configuration directory. As a
relative path from your workspace directory, this would be the file
`<workspace>/tango_with_django_project/tango_with_django_project/urls.py`.
Update the `urlpatterns` list as shown in the example below.

```python
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include  # New import added

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^rango/', include('rango.urls')),   #maps any URLs with starting 
											  #with rango/ to be handled by
											  #the rango application
    url(r'^admin/', admin.site.urls),
]
```

You will see that the `urlpatterns` is a Python list, which is expected by the Django framework.  The added mapping looks for URL strings that match the patterns `^rango/`. When a match is made the remainder of the url string is then
passed onto and handled by `rango.urls` through the use of the  `include()` function from
within `django.conf.urls`.  

Think of this as a chain that processors the
URL string - as illustrated in Figure fig-url-chain. In this chain, the
domain is stripped out and the remainder of the url string (`rango/`) is
passed on to tango\_with\_django project, where it finds a match and
strips away `rango/` leaving and empty string to be passed on to the
application `rango`.  

Consequently, we need to create a new file called `urls.py` in the `rango` application directory, to handle the remaining URL string (and map the empty string to the `index` view):

```python
from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	]
```

This code imports the relevant Django machinery for
URL mappings and the `views` module from `rango`. This allows us to call the function `url` and point to the `index` view for the mapping in `urlpatterns`. 

The URL mapping we have created calls Django's `url()` function, where the first parameter is the regular expression `^$`,
which matches to an empty string. Any URL supplied by the user that
matches this pattern means that the view `views.index()` would be
invoked by Django. You might be thinking that matching a blank URL is pretty pointless -
what use would it serve? When the URL pattern matching takes place,
only a portion of the original URL string is considered. This is
because our Django project will first process the original URL string
(i.e. `http://www.tangowithdjango.com/rango/`). 



Once this has been
processed, it is removed, with the remained being passed for pattern
matching. In this instance, there would be nothing left - so an empty
string would match!






 The `index` view is then passed the incoming `HttpRequest` object as a
parameter, containing information about the user's request to the
server. We also make use of the optional parameter to the `url()`
function, `name`, using the string `'index'` as the associated value.


> **note**
>
> The `name` parameter is optional to the `django.conf.urls.url()`
> function. This is provided by Django to allow you to distinguish one
> mapping from another. It is entirely plausible that two separate URL
> mappings expressions could end calling the same view. `name` allows
> you to differentiate between them - something which is useful for
> *reverse URL matching.* Check out [the Official Django documentation
> on this
> topic](https://docs.djangoproject.com/en/1.9/topics/http/urls/#naming-url-patterns)
> for more information.

You may have seen that within your project configuration directory a
`urls.py` file already exists. Why make another? Technically, you can
put *all* the URLs for your project's applications within this file.
However, this is considered bad practice as it increases coupling on
your individual applications. A separate `urls.py` file for each
application allows you to set URLs for individual applications. With
minimal coupling, you can then join them up to your project's master
`urls.py` file later.

This means we need to configure the `urls.py` of our project
`tango_with_django_project` and connect up our main project with our
Rango application.






Restart the Django development server and visit
`http://127.0.0.1:8000/rango`. If all went well, you should see the text
`Rango says hey there partner!`. It should look just like the screenshot shown
in Figure fig-rango-hello-world.

![An illustration of a URL, showing how the different parts of the URL
are the responsibility of different `url.py`
files.](../images/url-chain.svg)

![A screenshot of Google Chrome displaying our first Django-powered
webpage. Hello, Rango!](../images/ch3-hey-there.png){id="img-ch3-hey-there"}

Within each application, you will create a number of URL to view
mappings. This initial mapping is quite simple. As we progress, we will
create more sophisticated mappings that using allow the URLs to be
parameterised.

It's important to have a good understanding of how URLs are handled in
Django. If you are still bit confused or would like to know more check
out the [official Django documentation on
URLs](https://docs.djangoproject.com/en/1.9/topics/http/urls/) for
further details and further examples.

> **note**
>
> The URL patterns use [regular
> expressions](http://en.wikipedia.org/wiki/Regular_expression) to
> perform the matching. It is worthwhile familiarising yourself on how
> to use regular expressions in Python. The official Python
> documentation contains a [useful guide on regular
> expressions](http://docs.python.org/2/howto/regex.html) , while
> regexcheatsheet.com provides a [neat summary of regular
> expressions](http://regexcheatsheet.com/).

##Basic Workflows


What you've just learnt in this chapter can be succinctly summarised
into a list of actions. Here, we provide these lists for the two
distinct tasks you have performed. You can use this section for a quick
reference if you need to remind yourself about particular actions.

### Creating a new Django Project

1.  To create the project run,
    `python django-admin.py startproject <name>`, where `<name>` is the
    name of the project you wish to create.

### Creating a new Django application

1.  To create a new application run,
    `$ python manage.py startapp <appname>`, where `<appname>` is the
    name of the application you wish to create.
2.  Tell your Django project about the new application by adding it to
    the `INSTALLED_APPS` tuple in your project's `settings.py` file.
3.  In your project `urls.py` file, add a mapping to the application.
4.  In your application's directory, create a `urls.py` file to direct
    incoming URL strings to views.
5.  In your application's `view.py`, create the required views ensuring
    that they return a `HttpResponse` object.

X>###Exercises
X>
X> Congratulations! You have got Rango up and running. This is a
X> significant landmark in working with Django. Creating views and mapping
X> URLs to views is the first step towards developing more complex and
X> usable web applications. Now try the following exercises to reinforce
X> what you've learnt.
X> 
X> -   Revise the procedure and make sure you follow how the URLs are
X>     mapped to views.
X> -   Now create a new view called `about` which returns the following:
X>     `Rango says here is the about page.`
X> -   Now map the this view to `/rango/about/`. For this step, you'll only
X>     need to edit the `urls.py` of the rango application.
X> -   Revise the `HttpResponse` in the `index` view to include a link to
X>     the about page.
X> -   In the `HttpResponse` in the `about` view include a link back to the
X>     main page.
X> -   If you haven't done so already, it is a good point to go off an
X>     complete part one of the official [Django
X>     Tutorial](https://docs.djangoproject.com/en/1.9/intro/tutorial01/).

### Hints

If you're struggling to get the exercises done, the following hints will
hopefully provide you with some inspiration on how to progress.

-   Your `index` view should be updated to include a link to the `about`
    view. Keep it simple for now - something like
    `Rango says: Hello world! <br/> <a href='/rango/about'>About</a>`
    will suffice. We'll be going back later to improve the presentation
    of these pages.
-   The regular expression to match `about/` is `r'^about/'` - this will
    be handy when thinking about your URL pattern.
-   The HTML to link back to the index page is
    `<a href="/rango/">Index</a>`. The link uses the same structure as
    the link to the `about` page shown above.

**Footnotes**

[1]: There are many applications available out there that you can use in your project. Take a look at
    [PyPI](https://pypi.python.org/pypi?%3Aaction=search&term=django&submit=search)
    and [Django Packages](https://www.djangopackages.com/) to search for
    reusable apps which you can drop into your projects.
