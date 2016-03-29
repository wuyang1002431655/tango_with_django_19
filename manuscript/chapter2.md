Getting Ready to Tango
======================
Now that you're ready to go, let's get set up so that you can *Tango with Django!* You'll need to ensure that you have everything you need installed on your computer, and that you have a sound understanding of your development environment. 

This chapter outlines the five different components that you need to get setup. These are listed below.

* Get your *Python* installation setup and working.
* Setup your *virtual environment* and get to grips with *pip*.
* Get *Django* installed and ready to go.
* Setup an *Integrated Development Environment (IDE)*, if you choose to do so.
* Understand how to use the *Git* version control system to store your code.

Once you're familiar with all of these technologies, you're ready to go!

Python
------
Tango with Django requires you to have installed on your computer a copy of the Python programming language. Any version from the `2.7` family (e.g. `2.7.11`) or version `3.5` will do. If you're not sure how to install Python and would like some assistance, have a look at **the chapter dealing with installing components**.

I> ### Not sure how to use Python?
I>
I> If you haven't used Python before or you simply wish to brush up on your skills, then we highly recommend that you check out and work through one or more of the following guides:
I> - [**Learn Python in 10 Minutes**](http://www.korokithakis.net/tutorials/python/) by Stavros;
I> - [**The Official Python Tutorial**](http://docs.python.org/2/tutorial/);
I> - [**Think Python: How to Think like a Computer Scientist**](http://www.greenteapress.com/thinkpython/) by Allen B. Downey; or
I> - [**Learn to Program**](https://www.coursera.org/course/programming1) by Jennifer Campbell and Paul Gries.


Virtual Environments
---------------------

We're almost all set to go! However, before we continue, it's worth
pointing out that while this setup is fine to begin with, there are some
drawbacks. What if you had another Python application that requires a
different version to run? Or you wanted to switch to the new version of
Django, but still wanted to maintain your Django 1.7 project?

The solution to this is to use [virtual
environments](http://simononsoftware.com/virtualenv-tutorial/). Virtual
environments allow multiple installations of Python and their relevant
packages to exist in harmony. This is the generally accepted approach to
configuring a Python setup nowadays.

Pip
---

Pip is the python package manager.....

Django
------

-   Django version 1.9

As Django is a web application framework written in the Python
programming language, you will be required to have a working knowledge
of Python. 


Integrated Development Environment
----------------------------------

While not absolutely necessary, a good Python-based integrated
development environment (IDE) can be very helpful to you during the
development process. Several exist, with perhaps JetBrains'
[*PyCharm*](http://www.jetbrains.com/pycharm/) and *PyDev* (a plugin of
the [Eclipse IDE](http://www.eclipse.org/downloads/)) standing out as
popular choices. The [Python
Wiki](http://wiki.python.org/moin/IntegratedDevelopmentEnvironments)
provides an up-to-date list of Python IDEs.

Research which one is right for you, and be aware that some may require
you to purchase a licence. Ideally, you'll want to select an IDE that
supports integration with Django. PyCharm and PyDev both support Django
integration out of the box - though you will have to point the IDE to
the version of Python that you are using.

Git - Code Repository
---------------------
We should also point out that when you develop code, you should always
house your code within a version-controlled repository such as
[SVN](http://subversion.tigris.org/) or [GIT](http://git-scm.com/). We
won't be going through this right now so that we can get stuck into
developing an application in Django. We have however provided a
crash course on GIT \<git-crash-course\>. We highly recommend that you
set up a GIT repository for your own projects. Doing so could save you
from disaster.

X> Exercises
X> ---------
X> To get comfortable with your environment, try out the following exercises.
X> 
X> -   Install Python 2.7.5+/3.0+ and Pip.
X> -   Play around with your CLI and create a directory called `code`,    which we use to create our projects in.
X>  -   Install the Django and Pillow packages.
X>  -   Setup your Virtual Environment
X>  -   Setup your account on GitHub
X>  -   Download and setup a Integrated Development Environment (like
    PyCharm)
X> -
X> 
X>     We have made the code for the book and application that you build available on GitHub, see [Tango With Django 
X>  Book](https://github.com/leifos/tango_with_django_19) .
X> 
X>    -   If you spot any errors or problem with the book, you can
X>             make a change request!
X>         -   If you have any problems with the exercises, you can check
X>             out the repository and see how we completed them.
X> 

