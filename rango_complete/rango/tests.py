import os,re
from django.test import TestCase
from rango.models import Category, Page
from django.urls import reverse
from django.conf import settings
from population_script import populate
import tempfile
import rango.models
from django.db import models
from django.contrib.auth.models import User
from django.forms import fields as django_fields
from django.db.models.query import QuerySet

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Olympic News Web App Test Failure =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

def create_user_object():
        """
        Helper function to create a User object.
        """
        user = User.objects.get_or_create(username='testuser',
                                        first_name='Test',
                                        last_name='User',
                                        email='test@test.com')[0]
        user.set_password('testabc123')
        user.save()
        return user

def create_ctaegory_object():
    category = Category.objects.get_or_create(name='Basketball', views=100, likes=10)
    return category

"""def create_page_object():
    category = create_ctaegory_object()
    page = Page.objects.get_or_create(category=category.,title='xxx',url='https://xxxx.com',views=1)
    return page
"""
def create_super_user_object():
    """
    Helper function to create a super user (admin) account.
    """
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file.
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str

class TestBase(TestCase):

    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file.
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str

    def test_for_links_in_base(self):
        """
        There should be three hyperlinks in base.html, as per the specification of the book.
        Check for their presence, along with correct use of URL lookups.
        """
        template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'rango', 'base.html'))

        look_for = [
            '<a class="nav-link" href="{% url \'rango:index\' %}">Home</a>',
            '<a class="nav-link" href="{% url \'rango:about\' %}">About</a>',
        ]
        
        for lookup in look_for:
            self.assertTrue(lookup in template_str, f"{FAILURE_HEADER}In base.html, we couldn't find the hyperlink '{lookup}'. Check your markup in base.html is correct and as written in the book.{FAILURE_FOOTER}")

    

    def test_mapping_exists(self):
        """
        Checks whether the about view has the correct URL mapping.
        """
        self.assertEquals(reverse('rango:about'), '/rango/about/', f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")
    
    '''def test_vote_template(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'rango')
        template_path = os.path.join(template_base_path, 'vote.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'vote.html' template in the 'templates/rango/' directory. Did you put it in the right place?{FAILURE_FOOTER}")
        '''

class TestTopViewed(TestCase):
    def test_top_viewed_page_response(self):
        response = self.client.get(reverse('rango:index'))
        #content = self.response.content.decode()
        expected_pages_order = list(Page.objects.order_by('-views')[:5])
        self.assertTrue('pages' in response.context, f"{FAILURE_HEADER}Couldn't find a 'pages' variable in the index() view's context dictionary. Check your index.html {FAILURE_FOOTER}")
        self.assertEqual(type(response.context['pages']), QuerySet, f"{FAILURE_HEADER}The 'pages' variable in the index() view's context dictionary doesn't return a QuerySet as expected.{FAILURE_FOOTER}")
        self.assertEqual(expected_pages_order, list(response.context['pages']), f"{FAILURE_HEADER}The 'pages' context dictionary variable for the index() view didn't return the QuerySet we were expectecting: got {list(response.context['pages'])}, expected {expected_pages_order}. Did you apply the correct ordering to the filtered results?{FAILURE_FOOTER}")
    
    def test_top_viewed_categories_re(self):
        response = self.client.get(reverse('rango:index'))
        self.assertTrue('categories' in response.context, f"{FAILURE_HEADER}The 'categories' variable does not exist in the context dictionary for index(). (Empty check){FAILURE_FOOTER}")
        self.assertEqual(type(response.context['categories']), QuerySet, f"{FAILURE_HEADER}The 'categories' variable in the context dictionary for index() does yield a QuerySet object. (Empty check){FAILURE_FOOTER}")
        self.assertEqual(len(response.context['categories']), 0, f"{FAILURE_HEADER}The 'categories' variable in the context dictionary for index() is not empty. (Empty check){FAILURE_FOOTER}")    

class TestUserProfile(TestCase):
    """
    Tests to check whether the UserProfile model has been created according to the specification.
    """
    
    def test_userprofile_class(self):
        """
        Does the UserProfile class exist in rango.models? If so, are all the required attributes present?
        Assertion fails if we can't assign values to all the fields required (i.e. one or more missing).
        """
        self.assertTrue('UserProfile' in dir(rango.models))

        user_profile = rango.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
            'website': 'www.google.com',
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }

        expected_types = {
            'website': models.fields.URLField,
            'picture': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        user_profile.save()

    def test_model_admin_interface_inclusion(self):
        """
        Attempts to access the UserProfile admin interface instance.
        If we don't get a HTTP 200, then we assume that the model has not been registered. Fair assumption!
        """
        super_user = create_super_user_object()
        self.client.login(username='admin', password='testpassword')

        # The following URL should be available if the UserProfile model has been registered to the admin interface.
        response = self.client.get('/admin/rango/userprofile/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When attempting to access the UserProfile in the admin interface, we didn't get a HTTP 200 status code. Did you register the new model with the admin interface?{FAILURE_FOOTER}")


class TestAdd(TestCase):
    """
    """

    def test_bad_add_page(self):
        """
        Tests to see if a page cannot be added when not logged in.
        """
        populate()
        response = self.client.get(reverse('rango:add_page', kwargs={'category_name_slug': 'python'}))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}When not logged in and attempting to add a page, we should be redirected. But we weren't. Check your add_page() implementation.{FAILURE_FOOTER}")
    
    def test_bad_add_category(self):
        """
        Tests to see if a category cannot be added when not logged in.
        """
        response = self.client.get(reverse('rango:add_category'))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}When attempting to add a category when not logged in, we weren't redirected when we should be. Check your add_category() implementation.{FAILURE_FOOTER}")

    """def test_good_add_page(self):

        Tests to see if a page can be added when logged in.

        populate()
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('rango:add_page', kwargs={'category_name_slug': 'python'}))
        
        #self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to add a page when logged in. Check your add_page() view.{FAILURE_FOOTER}")
        
        content = response.content.decode()
        self.assertTrue('Add News' in content, f"{FAILURE_HEADER}When adding a page (when logged in), we didn't see the expected page. Please check your add_page() view.{FAILURE_FOOTER}")
"""
    def test_good_add_category(self):
        """
        Tests to see if a category can be added when logged in.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('rango:add_category'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When adding a category (when logged in), we didn't get a HTTP 200 response. Please check your add_category() view.{FAILURE_FOOTER}")

        content = response.content.decode()
        self.assertTrue('Add a Sport' in content, f"{FAILURE_HEADER}When adding a category (when logged in), we didn't see the page we expected. Please check your add_category() view.{FAILURE_FOOTER}")

    def test_add_category_link(self):
        """
        Tests to see if the Add Category link only appears when logged in.
        """
        content = self.client.get(reverse('rango:index')).content.decode()

        self.assertTrue(reverse('rango:add_category') not in content, f"{FAILURE_HEADER}The Add Category link was present on Rango's homepage when a user is not logged in. This shouldn't be the case! Please check your base.html template.{FAILURE_FOOTER}")

        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('rango:index')).content.decode()

        self.assertTrue(reverse('rango:add_category') in content, f"{FAILURE_HEADER}The Add Category link was not present on Rango's homepage when the user was logged in. It should be visible! Please check base.html.{FAILURE_FOOTER}")

    """def test_add_page_link(self):
                Tests to see if the Add Page link only appears when logged in.
        
        populate()
        content = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'})).content.decode()
        
        self.assertTrue(reverse('rango:add_page', kwargs={'category_name_slug': 'python'}) not in content, f"{FAILURE_HEADER}The Add Page link was present in the show_category() response when a user was not logged in. It shouldn't be there. {FAILURE_FOOTER}")

        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'})).content.decode()

        self.assertTrue(reverse('rango:add_page', kwargs={'category_name_slug': 'python'}) in content, f"{FAILURE_HEADER}The Add Page link was not present when a user was logged in, and looking at the show_category() view. Did you make a mistake in your category.html template?{FAILURE_FOOTER}")


        #content = response.content.decode()
        #self.assertTrue('visits:' not in content.lower(), f"{FAILURE_HEADER}The index.html template should not contain any logic for displaying the number of views. Did you complete the exercises?{FAILURE_FOOTER}")
        """