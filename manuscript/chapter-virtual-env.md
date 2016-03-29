## Virtual Environments

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

They are pretty easy to setup, once you have pip installed, and you know
the right commands. You need to install a couple of additional packages.

    $ pip install virtualenv
    $ pip install virtualenvwrapper

The first package provides you with the infrastructure to create a
virtual environment. See [a non-magical introduction to Pip and
Virtualenv for Python
Beginners](http://dabapps.com/blog/introduction-to-pip-and-virtualenv-python/)
by Jamie Matthews for details about using virtualenv. However, using
just *virtualenv* alone is rather complex. The second package provides a
wrapper to the functionality in the virtualenv package and makes life a
lot easier.

If you are using a linux/unix based OS, then to use the wrapper you need
to call the following shell script from your command line: :

    $ source virtualenvwrapper.sh

It is a good idea to add this to your bash/profile script. So you dont
have to run it each and every time you want to use virtualenvironments.

However, if you are using windows, then install the
[virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win)
package:

    $ pip install virtualenvwrapper-win

Now you should be all set to create a virtual environment:

    $ mkvirtualenv rango

You can list the virtual environments created with `lsvirtualenv`, and
you can activate a virtual environment as follows:

    $ workon rango
    (rango)$

Your prompt with change and the current virtual environment will be
displayed, i.e. rango. Now within this environment you will be able to
install all the packages you like, without interferring with your
standard or other environements. Try `pip list` to see you dont have
Django or Pillow installed in your virtual environment. You can now
install them with pip so that they exist in your virtual environment.

Later on when we go to deploy the application, we will go through a
similar process see Chapter
Deploying your Application\<virtual-environment\> and set up a virtual
environment on PythonAnywhere.

### Code Repository

We should also point out that when you develop code, you should always
house your code within a version-controlled repository such as
[SVN](http://subversion.tigris.org/) or [GIT](http://git-scm.com/). We
won't be going through this right now so that we can get stuck into
developing an application in Django. We have however provided a
crash course on GIT \<git-crash-course\>. We highly recommend that you
set up a GIT repository for your own projects. Doing so could save you
from disaster.

Exercises
---------

To get comfortable with your environment, try out the following
exercises.

-   Install Python 2.7.5+ and Pip.
-   Play around with your CLI and create a directory called `code`,
    which we use to create our projects in.
-   Install the Django and Pillow packages.
-   Setup your Virtual Environment
-   Setup your account on GitHub
-   Download and setup a Integrated Development Environemnt (like
    PyCharm)
-

    We have made the code for the book and application that you build available on GitHub, see [Tango With Django Book](https://github.com/leifos/tango_with_django_book) and [Rango Application](https://github.com/leifos/tango_with_django) .

    :   -   If you spot any errors or problem with the book, you can
            make a change request!
        -   If you have any problems with the exercises, you can check
            out the repository and see how we completed them.
