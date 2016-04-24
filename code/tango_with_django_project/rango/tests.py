from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders

# Create your tests here.
class GeneralTests(TestCase):
    def test_serving_static_files(self):
        # If using static media properly result is not NONE once it finds rango.jpg
        result = finders.find('images/rango.jpg')
        self.assertIsNotNone(result)


class IndexPageTests(TestCase):
        
    def test_index_contains_hello_message(self):
        # Check if there is the message 'hello world!'
        response = self.client.get(reverse('index'))
        self.assertIn('Rango says', response.content)
         
    def test_index_using_template(self):
        response = self.client.get(reverse('index'))

        # Check the template used to render index page
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_rango_picture_displayed(self):
        response = self.client.get(reverse('index'))

        # Check if is there an image in index page
        self.assertIn('img src="/static/images/rango.jpg', response.content)
    
    def test_index_has_title(self):
        response = self.client.get(reverse('index'))
        #Check to make sure that the title tag has been used 
        self.assertIn('<title>', response.content)
        self.assertIn('</title>', response.content)


class AboutPageTests(TestCase):
        
    def test_about_contains_create_message(self):
        # Check if in the about page is there a message
        response = self.client.get(reverse('about'))
        self.assertIn('This tutorial has been put together by', response.content)
        
    def test_about_using_template(self):
        response = self.client.get(reverse('about'))

        # Check the template used to render index page
        self.assertTemplateUsed(response, 'rango/about.html')