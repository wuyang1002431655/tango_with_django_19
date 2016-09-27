#JQuery and Django

JQuery rocks! JQuery is a library written in Javascript that lets you access the power of Javascript without the pain. This is because a few lines of JQuery often encapsulates
hundreds of lines of Javascript. Also, JQuery provides a suite of
functionality that is mainly focused on manipulating HTML elements. In
this chapter, we will describe:

- how to incorporate JQuery within your Django Application
- explain how to interpret JQuery code
- and provide a number of small examples 

##Including JQuery in Your Django Project/Application

In your *base* template include a reference to:

{lang="html",linenos=off}
	{% load staticfiles %}
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js">
	<script src="{% static "js/rango-jquery.js" %}"></script>
	
or if you have downloaded and saved a copy to your static folder, then you can reference it as follows:

{lang="html",linenos=off}
	{% load staticfiles %}
	<script src="{% static "js/jquery.min.js" %}"></script>
	<script src="{% static "js/rango-jquery.js" %}"></script>
	
Make sure you have your static files set up (see [Chapter Templates and Static Media](#chapter-templates-static))

In the static folder create a *js* folder and plonk the JQuery
javascript file (`jquery.js`) here along with an file called
`rango-jquery.js`, which will house our Javascript code. In
`rango-jquery.js`, add the following Javascript:

{lang="javascript",linenos=off}
	$(document).ready(function() {
		// JQuery code to be added in here.
	});


This piece of JQuery, first selects the document object (with
`$(document)`), and then makes a call to `ready()`. Once the document is
ready i.e. the complete page is loaded, then the anonymous function
denoted by `function(){ }` will be executed. It is pretty typical, if
not standard, to wait until the document has been finished loading
before running the JQuery functions. Otherwise, the code my try to run,
but the HTML elements may not have been downloaded. See the [JQuery Documentation on Ready](http://api.jquery.com/ready/) for more details.

I> ### Stylistic Note
I>
I> JQuery requires you to think in a more `functional` programming style, as opposed to the typical 
I> Javascript style which is often written in a more `procedural` programming style. For all the 
I> JQuery commands they follow a similar pattern: Select and Act. Select an element, and then act on 
I> the element. So it is good to keep this in mind. There are different selection operators, and 
I> various actions that can then be performed/applied. In the next, subsections we will take a few 
I> JQuery functions that you can use to manipulate the HTML elements.



