# Webhose Search {#chapter-webhose}
Now that our Rango app is looking good and most of the core functionality has been implemented, we can move onto some of the more advanced functionality. In this chapter, we will connect Rango up to the *Webhose API* so that users can also search for pages, rather than simply browse categories. Before we do so, we need to set up an account with Webhose, and write a [wrapper](https://en.wikipedia.org/wiki/Adapter_pattern) to query and obtain results from their API.

## The Webhose API
The Webhose API provides you with the ability to programmatically query *Webhose*, an online service that collates information from a variety of online sources in real-time. Through a straightforward interface, you can request results for a query in JSON. The returned data can then be interpreted by a JSON parser, with the results then rendered as part of a template within you app.

Although Webhose allows you to obtain results for information that has been recently [crawled](https://en.wikipedia.org/wiki/Web_crawler), we'll be focusing on returning content ranked by its *relevancy* to the query that a user of Rango provides. To use the Webhose API, you'll need an *API key*. The key provides you with 1,000 free queries per month -- more than enough for our purposes.

I> ### What is an Application Programming Interface (API)?
I> An [Application Programming Interface](http://en.wikipedia.org/wiki/Application_programming_interface) specifies how software components should interact with one another. In the context of web applications, an API is considered as a set of HTTP requests along with a definition of the structures of response messages that each request can return. Any meaningful service that can be offered over the Internet can have its own API - we aren't limited to web search. For more information on web APIs, [Luis Rei provides an excellent tutorial on APIs](http://blog.luisrei.com/articles/rest.html).

### Registering for a Webhose API Key
To obtain a Webhose API key, you must first register for a free Webhose account. Head over to [`https://www.webhose.io`](https://www.webhose.io) in your Web browser, and sign up by clicking *'Use it for free'* at the top right of the page. You don't need to provide a company name -- and in company e-mail, simply provide a valid e-mail address.

Once you have created your account, you'll be taken to the Webhose *Dashboard*, [as can be seen below](#fig-webhose-dashboard). From the dashboard, you can see a count of how many queries you have issued over the past month, and how many free queries you have remaining. There's also a neat little graph which demonstrates the rate at which you issue queries to Webhose over time. Scroll down the page, and you'll find a section called *Active API Key*. **Take a note of the key shown here by copying it into a blank text file -- you'll be needing this later on.** This is your unique key, that when sent with a request to the Webhose API, will identify you to their servers.

{id="fig-webhose-dashboard"}
![The Webhose dashboard, showing where the API key is displayed on the page. You'll most likely have to scroll down to see it. In the screenshot, the API key has been obscured. Keep your key safe and secure!
](images/ch14-webhose-dashboard.png)

Once you have your API key, scroll back up to the top of the Webhose dashboard, and click the [*Get live data* button](https://webhose.io/api), which is in blue. You'll then be taken to the API page, which allows you to play around with the Webhose API interface. Try it out!

1. In the box under *Return posts containing the following keywords*, enter a query.
2. In the *Sort by* dropdown box, choose *Relevancy*.
3. You can then choose a value for *Return posts crawled since*, but leaving it at the 3 day default should be fine.
3. Click *Test the Query*, and you'll then be presented with a series of results to the query you entered. [The screenshot below shows example output for the query *Glasgow*.](#fig-webhose-query)

{id="fig-webhose-query"}
![A sample response from the Webhose API for the query *Glasgow*. Shown is the *Visual Glimpse*; you can also see the raw JSON response from the server by clicking the *JSON* tab. 
](images/ch14-webhose-query.png)

Have a look at what you get back, and also have a look at the raw JSON response that is returned by the Webhose API. You can do this by clicking on the *JSON* tab. You can try copying and pasting the JSON response in to an online [JSON pretty printer](http://jsonprettyprint.com/) to see how it's structured if you want. Close the response by clicking the *X* to the right of the *Output Stream* title, and you'll be returned the API page. You can now scroll down to find the *Integration Examples* section. Make sure the *Endpoint* tab is selected, and have a look at the URL that you are shown. This is the URL that your Rango app will be communicating with to obtain search results -- or, in other words, the *endpoint URL*. We'll be making use of it later. An example of the Webhose API endpoint URL -- for a given configuration, with the API key and query redacted -- is shown below.

`http://webhose.io/search?token=<KEY>&format=json&q=<QUERY>&sort=relevancy`

## Adding Search Functionality
Now you've got your Webhose API key, you're ready to implement functionality in Python that issues queries to the Webhose API. Create a new module (file) in the `rango` app directory called `webhose_search.py`, and add the following code -- picking the correct one for your Python version. As mentioned earlier in the book, it's better you go through and type the code out -- you'll be thinking about how it works as you type (and understanding what's going on), rather than blindly copying and pasting.

I> ### Python 2 and 3 Differences
I> In [Python 3, the `urllib` package was refactored](http://stackoverflow.com/a/2792652), so the way that we connect and work with external web resources has changed from Python 2.7+. Below we have two versions of the code, one for Python 2.7+ and one for Python 3+. Make sure you use the correct one for your environment.

### Python 2 Version
{lang="python",linenos=on}
	import json
	import urllib
	import urllib2
	
	def read_webhose_key():
	    """
	    Reads the Webhose API key from a file called 'webhose.key'.
	    Returns either None (no key found), or a string representing the key.
	    Remember: put webhose.key in your .gitignore file to avoid committing it!
	    """
	    # See Python Anti-Patterns - it's an awesome resource!
	    # Here we are using "with" when opening files.
	    # http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
	    webhose_api_key = None
	
	    try:
	        with open('webhose.key', 'r') as f:
	            webhose_api_key = f.readline()
	    except:
	        raise IOError('webhose.key file not found')
	
	    return webhose_api_key
	
	def run_query(search_terms, size=10):
	    """
	    Given a string containing search terms (query), and a number of results to
	    return (default of 10), returns a list of results from the Webhose API,
	    with each result consisting of a title, link and summary.
	    """
	    webhose_api_key = read_webhose_key()
	
	    if not webhose_api_key:
	        raise KeyError('Webhose key not found')
	
	    # What's the base URL for the Webhose API?
	    root_url = 'http://webhose.io/search'
	
	    # Format the query string - escape special characters.
	    query_string = urllib.quote(search_terms)
	
	    # Use string formatting to construct the complete API URL.
	    # search_url is a string split over multiple lines.
	    search_url = ('{root_url}?token={key}&format=json&q={query}'
	                  '&sort=relevancy&size={size}').format(
	                    root_url=root_url,
	                    key=webhose_api_key,
	                    query=query_string,
	                    size=size)
	
	    results = []
	
	    try:
	        # Connect to the Webhose API, and convert the response to a
	        # Python dictionary.
	        response = urllib2.urlopen(search_url).read()
	        json_response = json.loads(response)
    
	        # Loop through the posts, appendng each to the results list
	        # as a dictionary.
	        for post in json_response['posts']:
	            results.append({'title': post['title'],
	                            'link': post['url'],
	                            'summary': post['text'][:200]})
	    except:
	        print("Error when querying the Webhose API")
	
	    # Return the list of results to the calling function.
	    return results

### Python 3 Version
{lang="python",linenos=on}
	import json
	import urllib.parse  # Py3
	import urllib.request  # Py3
	
	def read_webhose_key():
	    """
	    Reads the Webhose API key from a file called 'webhose.key'.
	    Returns either None (no key found), or a string representing the key.
	    Remember: put webhose.key in your .gitignore file to avoid committing it!
	    """
	    # See Python Anti-Patterns - it's an awesome resource!
	    # Here we are using "with" when opening files.
	    # http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
	    webhose_api_key = None
	
	    try:
	        with open('webhose.key', 'r') as f:
	            webhose_api_key = f.readline()
	    except:
	        raise IOError('webhose.key file not found')
	
	    return webhose_api_key
	
	def run_query(search_terms, size=10):
	    """
	    Given a string containing search terms (query), and a number of results to
	    return (default of 10), returns a list of results from the Webhose API,
	    with each result consisting of a title, link and summary.
	    """
	    webhose_api_key = read_webhose_key()
	
	    if not webhose_api_key:
	        raise KeyError('Webhose key not found')
	
	    # What's the base URL for the Webhose API?
	    root_url = 'http://webhose.io/search'
	
	    # Format the query string - escape special characters.
	    query_string = urllib.parse.quote(search_terms)  # Py3
	
	    # Use string formatting to construct the complete API URL.
	    # search_url is a string split over multiple lines.
	    search_url = ('{root_url}?token={key}&format=json&q={query}'
	                  '&sort=relevancy&size={size}').format(
	                    root_url=root_url,
	                    key=webhose_api_key,
	                    query=query_string,
	                    size=size)
	
	    results = []
	
	    try:
	        # Connect to the Webhose API, and convert the response to a
	        # Python dictionary.
	        response = urllib.request.urlopen(search_url).read().decode('utf-8')
	        json_response = json.loads(response)
	    
	        # Loop through the posts, appendng each to the results list as
	        # a dictionary.
	        for post in json_response['posts']:
	            results.append({'title': post['title'],
	                            'link': post['url'],
	                            'summary': post['text'][:200]})
	    except:
	        print("Error when querying the Webhose API")
	
	    # Return the list of results to the calling function.
	    return results

In the code samples above, we have implemented two functions: one to retrieve your Webhose API key from a local file (through function `read_webhose_key()`), and another to issue a query to the Webhose API and return results (`run_query()`). Below, we discuss how both of the functions work.

### `read_webhose_key()` -- Reading the Webhose API Key

### `run_query()` -- Executing the Query

## Putting Search into Rango

### Adding a Search Template

### Adding the View

