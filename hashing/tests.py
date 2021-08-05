from hashing.forms import HashForm
from django.test import TestCase
from selenium import webdriver
import hashlib
from .models import Hash

class FunctionalTestCase(TestCase):

    # setup
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    # block
    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter hash here:', self.browser.page_source)
        
    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',
                      self.browser.page_source)
        
    # close
    def tearDown(self):
        self.browser.quit()

class UnitTestCase(TestCase):
        
    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')
        
    def test_hash_form(self):
        data = {
            'text': 'hello'
        }
        form = HashForm(data=data)
        self.assertTrue(form.is_valid())
        
    def test_hash_func_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual(text_hash, 
                         '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
    
    def test_hash_object(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash.save()
        
        pulled_hash = Hash.objects.get(hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(hash.text, pulled_hash.text)
        
    def test_viewing_hash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash.save()
        
        response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertContains(response, 'hello')
