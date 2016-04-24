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
        # Check if there is the message 'Rango Says'
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertIn('Rango says', response.content)
         
    def test_index_using_template(self):
        # Check the template used to render index page
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_rango_picture_displayed(self):
        # Check if is there an image called 'rango.jpg' on the index page
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertIn('img src="/static/images/rango.jpg', response.content)
    
    def test_index_has_title(self):
        # Check to make sure that the title tag has been used
        # And that the template contains the HTML from Chapter 4 
        response = self.client.get(reverse('index'))
        self.assertIn('<title>', response.content)
        self.assertIn('</title>', response.content)


class AboutPageTests(TestCase):
        
    def test_about_contains_create_message(self):
        # Check if in the about page is there - and contains the specified message
        # Exercise from Chapter 4
        response = self.client.get(reverse('about'))
        self.assertIn('This tutorial has been put together by', response.content)
        
        
    def test_about_contain_image(self):
        # Check if is there an image on the about page
        # Chapter 4
        response = self.client.get(reverse('about'))
        self.assertIn('img src="/static/images/', response.content)
        
    def test_about_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4 
        response = self.client.get(reverse('about'))

        self.assertTemplateUsed(response, 'rango/about.html')
        
        
        
class ModelTests(TestCase):

    def setUp(self):
        
        from populate_rango import populate
        populate()
        
    def get_category(self, name):
        from rango.models import Category
        
        try:
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:    
            cat = None
        return cat
        
    def test_python_cat_added(self):
        cat = self.get_category('Python')  
        self.assertIsNotNone(cat)
         
    def test_python_cat_with_views(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.views, 128)
        
    def test_python_cat_with_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)
        
        