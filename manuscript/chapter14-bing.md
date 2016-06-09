#Bing Search 
Now that our Rango application is looking good and most of the core functionality has been implemented, we can move on some of the more advanced functionality. In this chapter, we will connect Rango up to Bing's Search API so that users can also search for pages, rather than just use the categories. Before we can do so, we need to set up an account to use Bing's Search API and write a wrapper to call Bing's web search functionality.

##The Bing Search API
The Bing Search API provides you with the ability to embed search results from the Bing search engine within your own applications. Through a straightforward interface, you can request results from Bing's servers to be returned in either XML or JSON. The data returned can then be interpreted by a XML or JSON parser, with the results then rendered as part of a template within your application.

Although the Bing API can handle requests for different kinds of content, we'll be focusing on web search only for this tutorial - as well as handling JSON responses. To use the Bing Search API, you will need to sign up for an *API key*. The key currently provides subscribers with access to 5000 queries per month, which should be more than enough for our purposes.

###Registering for a Bing API Key
To register for a Bing API key, you must first register for a free Microsoft account. The account provides you with access to a wide range of Microsoft services. If you already have a Hotmail account, you already have one! Otherwise, you can create a free account at (https://account.windowsazure.com)[https://account.windowsazure.com].

When your account has been created, go to the (Windows Azure Marketplace Bing Search API page)[ https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44>] and login.

<!-->. At the top of the screen, you may first need to click the *Sign In* button - if you have already signed into your Microsoft account, you won't need to provide your account details again. If the text says *Sign Out*, you're already logged in.
-->
On the right hand side of the page you should see a list of transactions per month. At the bottom of the list is *5,000 Transactions/month*. Click the sign up button to the right - subscribe for the free service.

<!--> Once you've read the *Publisher Offer Terms*, agreed and click *Sign Up* to continue. You will  then be presented with a page confirming that you have successfully signed up.-->

Once you've signed up, click the *Data* link at the top of the page. From there, you should be presented with a list of data sources available through the Windows Azure Marketplace. At the top of the list should be *Bing Search API* - it should also say that you are *subscribed* to the data source. Click the *use* link associated with the Bing Search API located on the right of the page. You will then be presented with a screen similar to that shown in Figure :num:`fig-bing-explore`.


{id="fig-bing-explore"}
![The Bing Search API service explorer page. In this screenshot, the *Primary Account Key* is deliberately obscured. You should make sure you keep your key secret, too!
](images/images/bing-explore.png)

	
This page allows you to try out the Bing Search API by filling out the boxes to the left. For example, the *Query* box allows you to specify a query to send to the API. Ensure that at the bottom of the screen you select *Web* for web search results only. Note the URL provided in the blue box at the top of the page changes as you alter the settings within the webpage. Take a note of the Web search URL. We'll be using part of this URL within our code later on. The following example is a URL to perform a web search using the query *rango*.

{lang="text",linenos=off}
	https://api.datamarket.azure.com/Bing/Search/v1/Web?Query=%27rango%27


Assuming this all works take a copy of your API key. We will need this when we make requests as part of the authentication process. To obtain your key, locate the text *Primary Account Key* at the top of the page and click the *Show* link next to it. Your key will then be shown.   We'll be using it later, so take a note of it - and keep it safe!  The Bing API Service Explorer keeps a tab of how many queries you have left of your monthly quota. So if someone obtains your key, they'll be able to use your quota.  

##Adding Search Functionality
To add search functionality to Rango, we need to write a couple of additional functions: (1) to read in your Bing API key, and (2) to query the Bing API. 


###Read Bing Key



###Issue Queries

This code should take in the request from a particular user and return to the calling function a list of results. Any errors that occur during the API querying phase should also be handled gracefully within the function. Spinning off search functionality into an additional function also provides a nice abstraction between Django-related code and search functionality code.

To start, let's create a new Python module called ``bing_search.py`` within our ``rango`` application directory. Add the following code into the file. Check out the inline commentary for a description of what's going on throughout the function.




{lang="python",linenos=off}
	import json
	import urllib, urllib2

	# Add your BING_API_KEY 

	BING_API_KEY = '<insert_bing_api_key>'

	def run_query(search_terms):
		# Specify the base
		root_url = 'https://api.datamarket.azure.com/Bing/Search/'
		source = 'Web'

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
			source,
			results_per_page,
			offset,
			query)

		# Setup authentication with the Bing servers.
		# The username MUST be a blank string, and put in your API key!
		username = ''


		# Create a 'password manager' which handles authentication for us.
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, search_url, username, BING_API_KEY)

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

				# Catch a URLError exception - something went wrong when connecting!		
		except urllib2.URLError as e:
			print "Error when querying the Bing API: ", e

		# Return the list of results to the calling function.
		return results

The logic of the function above can be broadly split into six main tasks:

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
I>If you're interested in seeing how to tailor your results, check out the (Bing Search API Migration Guide and FAQ)[http://datamarket.azure.com/dataset/bing/search].


##Storing your API KEY safely

If you are putting your code into a public repository on GitHub or the like, then you should take some pre-cautions about sharing your API Key. One solution is to create a new file call, `keys.py` which has a variable  `BING_API_KEY`. Then import the `BING_API_KEY` into `bing_search.py`.  Update your `.gitignore` file to include `keys.py`, so that `keys.py` is not added to the repository. This way the key will only be stored locally.


X> ###Exercises
X>
X> Taking the basic Bing Search API function we added above as a baseline, try out the following exercises.
X> - If using a public repository, refactor the code so that your API key is not publicly accessible
X> - Add a main() function to the `bing_search.py` to test out the BING Search API 



T> Hint: add the following code, so that when you run `python bing_search.py` it calls the `main()` function:
T> 	
T> {lang="python",linenos=off}
T>	def main():
T>	
T>		#insert your code here
T>
T>	if __name__ == '__main__':
T>		main()
T>	
T>
T> - The main function should ask a user for a query (from the command line), and then issue the query to the BING API via the run_query method and print out the top ten results returned. 
T> - Print out the rank, title and URL for each result.



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


