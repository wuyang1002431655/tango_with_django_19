from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.
class Chapter4ViewTests(TestCase):
        
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

    def test_about_contains_create_message(self):
        # Check if in the about page is there a message
        response = self.client.get(reverse('about'))
        self.assertIn('This tutorial has been put together by', response.content)
        
    def test_about_using_template(self):
        response = self.client.get(reverse('about'))

        # Check the template used to render index page
        self.assertTemplateUsed(response, 'rango/about.html')
        
        

        
        