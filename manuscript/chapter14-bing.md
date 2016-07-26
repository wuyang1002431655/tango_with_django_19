#Bing Search 
Now that our Rango application is looking good and most of the core functionality has been implemented, we can move on some of the more advanced functionality. In this chapter, we will connect Rango up to Bing's Search API so that users can also search for pages, rather than just use the categories. Before we can do so, we need to set up an account to use Bing's Search API and write a wrapper to call Bing's web search functionality.

##The Bing Search API
The Bing Search API provides you with the ability to embed search results from the Bing search engine within your own applications. Through a straightforward interface, you can request results from Bing's servers to be returned in either XML or JSON. The data returned can then be interpreted by a XML or JSON parser, with the results then rendered as part of a template within your application.

Although the Bing API can handle requests for different kinds of content, we'll be focusing on web search only for this tutorial - as well as handling JSON responses. To use the Bing Search API, you will need to sign up for an *API key*. The key currently provides subscribers with access to 5000 queries per month, which should be more than enough for our purposes.

###Registering for a Bing API Key
To register for a Bing API key, you must first register for a free Microsoft account. The account provides you with access to a wide range of Microsoft services. If you already have a Hotmail account, you already have one! Otherwise, you can create a free account at [https://account.windowsazure.com](https://account.windowsazure.com).

When your account has been created, go to the [Windows Azure Marketplace Bing Search API page](https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44) and login.

<!-->. At the top of the screen, you may first need to click the *Sign In* button - if you have already signed into your Microsoft account, you won't need to provide your account details again. If the text says *Sign Out*, you're already logged in.
-->
On the right hand side of the page you should see a list of transactions per month. At the bottom of the list is *5,000 Transactions/month*. Click the sign up button to the right - subscribe for the free service.

{id="fig-bing-search"}
![The Bing Search API services - sign up for the 5000 transactions/month for free.
](images/images/ch14-bing-search-api.png)

<!--> Once you've read the *Publisher Offer Terms*, agreed and click *Sign Up* to continue. You will  then be presented with a page confirming that you have successfully signed up.-->

Once you've signed up, click the *Data* link at the top of the page. From there, you should be presented with a list of data sources available through the Windows Azure Marketplace. At the top of the list should be *Bing Search API* - it should also say that you are *subscribed* to the data source. Click the *use* link associated with the Bing Search API located on the right of the page. 


{id="fig-bing-explore"}
![The Account Information Page. In this screenshot, the *Primary Account Key* is deliberately obscured. You should make sure you keep your key secret, too!
](images/images/ch14-bing-account.png)

	
This page allows you to try out the Bing Search API by filling out the boxes to the left. For example, the *Query* box allows you to specify a query to send to the API. Ensure that at the bottom of the screen you select *Web* for web search results only. Note the URL provided in the blue box at the top of the page changes as you alter the settings within the webpage. Take a note of the Web search URL. We'll be using part of this URL within our code later on. The following example is a URL to perform a web search using the query *rango*.

{lang="text",linenos=off}
	https://api.datamarket.azure.com/Bing/Search/v1/Web?Query=%27rango%27


Assuming this all works take a copy of your API key. We will need this when we make requests as part of the authentication process. To obtain your key, locate the text *Primary Account Key* at the top of the page and click the *Show* link next to it. Your key will then be shown.   We'll be using it later, so take a note of it - and keep it safe!  The Bing API Service Explorer keeps a tab of how many queries you have left of your monthly quota. So if someone obtains your key, they'll be able to use your quota.  

##Adding Search Functionality
Below we have provided the code which we can use to issued queries to the Bing search service. Create a file called `rango/bing_search.py` and import the following code.


{lang="python",linenos=on}
	import json
	import urllib, urllib2

	# Add your Microsoft Account Key to a file called bing.key

	def read_bing_key():
		"""
		reads the BING API key from a file called 'bing.key'
		returns: a string which is either None, i.e. no key found, or with a key
		remember to put bing.key in your .gitignore file 
		to avoid committing it to the repo.
		"""
	
		# See Python Anti-Patterns - 
		#it is an awesome resource to improve your python code
		# Here we using "with" when opening documents
		# See http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
		# and visit the link "Not using with to open files"
		
		bing_api_key = None
		try:
			with open('bing.key','r') as f:
				bing_api_key = f.readline()
		except:
			raise IOError('bing.key file not found')
		return bing_api_key
	
	def run_query(search_terms):
		bing_api_key = read_bing_key()
		if not bing_api_key:
			raise KeyError('Bing Key Not Found')
			
		# Specify the base url and the service (Bing Search API 2.0)
		root_url = 'https://api.datamarket.azure.com/Bing/Search/'
		service = 'Web'

		# Specify how many results we wish to be returned per page.
		# Offset specifies where in the results list to start from.
		# With results_per_page = 10 and offset = 11, this would start from page 2.
		results_per_page = 10
		offset = 0

		# Wrap quotes around our query terms as required by the Bing API.
		# The query we will then use is stored within variable query.
		query = "'{0}'".format(search_terms)
		query = urllib.quote(query)

		# Construct the latter part of our request's URL.
		# Sets the format of the response to JSON and sets other properties.
		search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
			root_url,
			service,
			results_per_page,
			offset,
			query)

		# Setup authentication with the Bing servers.
		# The username MUST be a blank string, and put in your API key!
		username = ''

		# headers = {'Authorization': 'Basic {0}'.format( b64encode(bing_api_key) )}
		# Create a 'password manager' which handles authentication for us.
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, search_url, username, bing_api_key)

		# Create our results list which we'll populate.
		results = []
		try:
			# Prepare for connecting to Bing's servers.
			handler = urllib2.HTTPBasicAuthHandler(password_mgr)
			opener = urllib2.build_opener(handler)
			urllib2.install_opener(opener)
			
			# Connect to the server and read the response generated.
			response = urllib2.urlopen(search_url).read()
			
			# Convert the string response to a Python dictionary object.
			json_response = json.loads(response)
			
			# Loop through each page returned, populating out results list.
			for result in json_response['d']['results']:
				results.append({
					'title': result['Title'],
					'link': result['Url'],
					'summary': result['Description']})
					
		except urllib2.URLError as e:
			print "Error when querying the Bing API: ", e
			
		# Return the list of results to the calling function.
		return results



As you can see we have written two functions. The first reads in your Bing API key, and the second issues the query.

###Read Bing Key
The `read_bing_key()` function reads in your key from a file called, `bing.key` in the `rango` directory. We have created this function because if you are putting your code into a public repository on GitHub, for example, then you should take some pre-cautions to avoid sharing your API Key publicly. 

One  solution is to store the  *Account Key* in a file called, `rango/bing.key`, which we don't commit to the Git repo. To make sure that we don't accidentally add it, update your `.gitignore` file to exclude `key` files, by adding `*.key`. This way the key will only be stored locally and you wont have someone else using your quota.


###Run Query
The `run_query()` function takes a query as a string, and returns the top ten results from Bing in a list that contains dictionary of the result items (`title`, `link`, `summary`). If you are interested, the inline commentary describes how the request is created and then issued to the Bing API.

Briefly, though, the logic of the function above can be broadly split into six main tasks:

* First, the function prepares for connecting to Bing by preparing the URL that we'll be requesting.
* The function then prepares authentication, making use of your Bing API key. Make sure you replace ``<api_key>`` with your actual Bing API key, otherwise you'll be going nowhere!
* We then connect to the Bing API through the command ``urllib2.urlopen(search_url)``. The results from the server are read and saved as a string.
* This string is then parsed into a Python dictionary object using the ``json`` Python package.
* We loop through each of the returned results, populating a ``results`` dictionary. For each result, we take the ``title`` of the page, the ``link`` or URL and a short ``summary`` of each returned result.
* The dictionary is returned by the function.

Notice that results are passed from Bing's servers as JSON. This is because we explicitly specify to use JSON in our initial request - check out the ``search_url`` variable which we define. If an error occurs when attempting to connect to Bing's servers, the error is printed to the terminal via the ``print`` statement within the ``except`` block.



I> ###Bing it on!
I>
I> There are many different parameters that the Bing Search API can handle which we don't cover here. 
I> If you want to know more about the API  check out the [Bing Search API Migration Guide and FAQ](http://datamarket.azure.com/dataset/bing/search).


X> ###Exercises
X>
X> - Add a `main()` function to the `bing_search.py`, so that you can run the module independently i.e. `python bing_search.py`
X> - Prompt the user to enter a query, i.e. use `raw_input()`
X> - Issue the query via `run_query()` and print the results


T> ### Hint
T>
T> Add the following code, so that when you run `python bing_search.py` it calls the `main()` function:
T> 	
T> {lang="python",linenos=off}
T>	def main():
T>	
T>			#insert your code here
T>
T>	if __name__ == '__main__':
T>			main()
T>	
T>
T> When you run the module explicitly via `python bing_search.py` then the `bing_search` module is treated as the `__main__` module, and thus triggers `main()`.
T> However, when the module is imported by another module, then `__name__` will not equal `__main__`, and so the `main()` function not be called. This way you can import it with your application without running `main()`.

##Putting Search into Rango
To add external search functionality, we will need to perform the following steps.

-  We must first create a ``search.html`` template which extends from our ``base.html`` template. The ``search.html`` template will include a HTML ``<form>`` to capture the user's query as well as template code to present any results.
- We then create a view to handle the rendering of the ``search.html`` template for us, as well as calling the ``run_query()`` function we defined above.

###Adding a Search Template
Let's first create our ``search.html`` template. Add the following HTML markup and Django template code.

{lang="html",linenos=off}
	{% extends "base.html" %}
	{% load staticfiles %}
	{% block title %} Search {% endblock %}
	{% block body_block %}
	<div class="page-header">
		<h1>Search with Rango</h1>
	</div>
	<div class="row">
		<div class="panel panel-primary">
			<br/>
			<form class="form-inline" id="user_form" method="post" action="{% url 'search' %}">
				{% csrf_token %}
				<!-- Display the search form elements here -->
				<input class="form-control" type="text" size="50" name="query" value="" id="query" />
				<input class="btn btn-primary" type="submit" name="submit" value="Search" />
				<br />
			</form>
			<div class="panel">
			{% if result_list %}
				<div class="panel-heading">
					<h3 class="panel-title">Results</h3>
					<!-- Display search results in an ordered list -->
					<div class="panel-body">
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
					</div>
				</div>
			{% endif %}
			
		</div>
	</div>
	{% endblock %}


The template code above performs two key tasks:

- In all scenarios, the template presents a search box and a search buttons within a HTML ``<form>`` for users to enter and submit their search queries.
- If a ``results_list`` object is passed to the template's context when being rendered, the template then iterates through the object displaying the results contained within.
	
To style the html we have made use of Bootstrap: panels, http://getbootstrap.com/components/#panels, list groups, http://getbootstrap.com/components/#list-group, and inline forms, http://getbootstrap.com/css/#forms-inline.

As you will see from our corresponding view code shortly, a ``results_list`` will only be passed to the template engine when there are results to return. There won't be results for example when a user lands on the search page for the first time - they wouldn't have posed a query yet!

###Adding the View
With our search template added, we can then add the view which prompts the rendering of our template. Add the following ``search()`` view to Rango's ``views.py`` module.

{lang="python",linenos=off}	
	def search(request):
		result_list = []
		if request.method == 'POST':
			query = request.POST['query'].strip()
			if query:
				# Run our Bing function to get the results list!
				result_list = run_query(query)
		return render(request, 'rango/search.html', {'result_list': result_list})
		
		
By now, the code should be pretty self explanatory to you. The only major addition is the calling of the ``run_query()`` function we defined earlier in this chapter. To call it, we are required to also import the ``bing_search.py`` module, too. Ensure that before you run the script that you add the following import statement at the top of the ``views.py`` module.

{lang="python",linenos=off}
	from rango.bing_search import run_query

You'll also need to ensure you do the following, too.

- Add a mapping between your ``search()`` view and the ``/rango/search/`` URL calling it ``name='search'``
- Update the ``base.html`` navigation bar to include a link to the search page. Remember to use the ``url`` template tag to reference the link.


I> Application Programming Interface
I>
I> According to the (relevant article on Wikipedia)[ http://en.wikipedia.org/wiki/Application_programming_interface>], an *Application Programming Interface (API)* specifies how software components should interact with one another.
I> In the context of web applications, an API is considered as a set of HTTP requests along with a definition of the structures of response messages that each request can return. 
I> Any meaningful service that can be offered over the Internet can have its own API - we aren't limited to web search. For more information on web APIs, (Luis Rei provides an excellent tutorial on APIs)[ http://blog.luisrei.com/articles/rest.html].


