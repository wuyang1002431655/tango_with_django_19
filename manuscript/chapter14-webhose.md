# Webhose Search {#chapter-webhose}
Now that our Rango app is looking good and most of the core functionality has been implemented, we can move onto some of the more advanced functionality. In this chapter, we will connect Rango up to the *Webhose API* so that users can also search for pages, rather than simply browse categories. Before we do so, we need to set up an account with Webhose, and write a [wrapper](https://en.wikipedia.org/wiki/Adapter_pattern) to query and obtain results from their API.

## The Webhose API
The Webhose API provides you with the ability to programmatically query *Webhose*, an online service that collates information from a variety of online sources in real-time. Through a straightforward interface, you can request results for a query in JSON. The returned data can then be interpreted by a JSON parser, with the results then rendered as part of a template within you app.

Although Webhose allows you to obtain results for information that has been recently [crawled](https://en.wikipedia.org/wiki/Web_crawler), we'll be focusing on returning content ranked by its *relevancy* to the query that a user of Rango provides. To use the Webhose API, you'll need an *API key*. The key provides you with 1,000 free queries per month -- more than enough for our purposes.

I> ### Application Programming Interface (API)
I> An [Application Programming Interface](http://en.wikipedia.org/wiki/Application_programming_interface) specifies how software components should interact with one another. In the context of web applications, an API is considered as a set of HTTP requests along with a definition of the structures of response messages that each request can return. Any meaningful service that can be offered over the Internet can have its own API - we aren't limited to web search. For more information on web APIs, [Luis Rei provides an excellent tutorial on APIs](http://blog.luisrei.com/articles/rest.html).

### Registering for a Webhose API Key
To obtain a Webhose API key, you must first register for a free Webhose account. Head over to [`https://www.webhose.io`](https://www.webhose.io) in your Web browser, and sign up by clicking `Use it for free` at the top right of the page. You don't need to provide a company name -- and in company e-mail, simply provide a valid e-mail address.

Once you have created your account, you'll be taken to the Webhose *Dashboard*, as can be seen below. From the dashboard, you can see a count of how many queries you have issued over the past month, and how many free queries you have remaining. There's also a neat little graph which demonstrates the rate at which you issue queries to Webhose over time.

{id="fig-webhose-dashboard"}
![The Webhose dashboard, showing where the API key is displayed on the page. You'll most likely have to scroll down to see it.
](images/ch14-webhose-dashboard.png)

## Adding Search Functionality

### Python 2 Version

### Python 3 Version

### `read_webhose_key()` -- Reading the Webhose API Key

### `run_query()` -- Executing the Query

## Putting Search into Rango

### Adding a Search Template

### Adding the View

