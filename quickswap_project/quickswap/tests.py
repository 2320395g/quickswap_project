from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from quickswap.models import Trade, Pictures, Comment, UserProfile
from quickswap.views import UserTradesView
from quickswap_project.urls import MyRegistrationView
from quickswap.templatetags import quickswap_template_tags
from django.test import Client


class SimpleUrlTests(TestCase):
	def test_urls(self):

		good_response = self.client.get(reverse('home'))
		self.assertEqual(good_response.status_code, 200)

		bad_response = self.client.get('test')
		self.assertEqual(bad_response.status_code, 404)

class ModelTest(TestCase):

    #using this to test other models removes the need to manually tear down the user model
    #after each use as a variable in testing another model, as well as a way to ensure
    #unique usernames each time using for example an appended datettime. As it is also a
    #core django model it does not need tested itself.
    def create_user(self):
        user = User.objects.create(username = 'testUser', email ='testEmail@test.com')
        user.set_password('testPassword')
        user.save()
        return user

    def create_trade(self, user,
                name = 'test Trade', category = 'art', quality = 'good',
                description = 'testTradeDescription', suggested_trade = 'testTradeSuggested_Trade',
                location = [-5.28192134932531, 52.832490053801356],
                slug = 'test-Trade', date_made = timezone.now()):

        return Trade.objects.create(user = user, name = name, category = category,
                            quality = quality, description = description,
                            suggested_trade = suggested_trade, location = location,
                            slug = slug, date_made = date_made)

    def test_trade(self):
        user = self.create_user()
        trade = self.create_trade(user)
        self.assertTrue(isinstance(trade, Trade))
        self.assertEqual(trade.__str__(), trade.name)

    def create_picture(self, trade, picture = 'picture_test_image.jpg'):
        return Pictures.objects.create(picture = picture, trade = trade)

    def test_picture(self):
        user = self.create_user()
        trade = self.create_trade(user)
        picture = self.create_picture(trade)
        self.assertTrue(isinstance(picture, Pictures))

    def test_picture_admin_image(self):
        user = self.create_user()
        trade = self.create_trade(user)
        picture = self.create_picture(trade)
        self.assertEqual(picture.admin_image(), '<img src="/media/picture_test_image.jpg" />')

    def test_picture_admin_thumbnail(self):
        user = self.create_user()
        trade = self.create_trade(user)
        picture = self.create_picture(trade)
        self.assertEqual(picture.admin_thumbnail(), '<img src="/media/picture_test_image.jpg" width="48" height="48" />')

    def test_picture_admin_user(self):
        user = self.create_user()
        trade = self.create_trade(user)
        picture = self.create_picture(trade)
        self.assertEqual(picture.admin_user(), picture.trade.user)

    def create_comment(self, trade, user, text = 'testText', picture = 'comment_test_image.jpg',
                date_made = timezone.now()):

        return Comment.objects.create(trade = trade, user = user, text = text, picture = picture,
                date_made = date_made)

    def test_comment(self):
        user = self.create_user()
        trade = self.create_trade(user)
        comment = self.create_comment(trade, user)
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(comment.__str__(), 'testText - testUser')

    def test_comment_admin_thumbnail(self):
        user = self.create_user()
        trade = self.create_trade(user)
        comment = self.create_comment(trade, user)
        self.assertEqual(comment.admin_thumbnail(), '<img src="/media/comment_test_image.jpg" width="48" height="48" />')

    def test_comment_admin_image(self):
        user = self.create_user()
        trade = self.create_trade(user)
        comment = self.create_comment(trade, user)
        self.assertEqual(comment.admin_image(), '<img src="/media/comment_test_image.jpg" />')

    def create_userprofile(self, user, description = 'testDescription', picture = 'userprofile_test_image.jpg',
                trades_made = 13, comments_made = 37):
        return UserProfile.objects.create(user = user, description = description, picture = picture,
                trades_made = trades_made, comments_made = comments_made)

    def test_userprofile(self):
        user = self.create_user()
        userprofile = self.create_userprofile(user)
        self.assertTrue(isinstance(userprofile, UserProfile))
        self.assertEqual(userprofile.__str__(), 'testUser')

    def test_userprofile_admin__image(self):
        user = self.create_user()
        userprofile = self.create_userprofile(user)
        self.assertEqual(userprofile.admin_image(), '<img src="/media/userprofile_test_image.jpg" />')

    def test_userprofile_admin__thumbnail(self):
        user = self.create_user()
        userprofile = self.create_userprofile(user)
        self.assertEqual(userprofile.admin_thumbnail(), '<img src="/media/userprofile_test_image.jpg" width="48" height="48" />')

class URLSTest(TestCase):
    def create_user(self):
        return User.objects.create(username='testUser', email ='testEmail@test.com')

    def test_myregistrationview(self):
        user = self.create_user()
        response = MyRegistrationView.get_success_url(self, user)
        self.assertEqual(response, '/quickswap/register_profile/')

class TemplateTagsTest(TestCase):

    def test_getdictvalue(self):
        test_dict = {'testKey':'testValue'}
        value = quickswap_template_tags.getDictValue(test_dict, 'testKey')
        self.assertEqual(value, 'testValue')


class ViewTest(TestCase):

    def create_trade(self, user,
                name = 'test Trade', category = 'art', quality = 'good',
                description = 'testTradeDescription', suggested_trade = 'testTradeSuggested_Trade',
                location = [-5.28192134932531, 52.832490053801356],
                slug = 'test-Trade', date_made = timezone.now()):

        return Trade.objects.create(user = user, name = name, category = category,
                            quality = quality, description = description,
                            suggested_trade = suggested_trade, location = location,
                            slug = slug, date_made = date_made)

    #Password must be set in this way as otherwise it sets 'testPassword' as
    #the password hash, so when attempting to login, it compares 'testPassword'
    #with the hash value of 'testPassword', obviously preventing the login.
    def create_user(self):
        user = User.objects.create(username = 'testUser', email ='testEmail@test.com')
        user.set_password('testPassword')
        user.save()
        return user

    def create_userprofile(self, user, description = 'testDescription', picture = 'userprofile_test_image.jpg',
                trades_made = 13, comments_made = 37):
        return UserProfile.objects.create(user = user, description = description, picture = picture,
                trades_made = trades_made, comments_made = comments_made)

    def create_picture(self, trade, picture = 'test_image.jpg'):
        return Pictures.objects.create(picture = picture, trade = trade)


    def test_home_view_content_login(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/home.html','quickswap/base.html')
        self.assertContains(response, 'Welcome to Quickswap!')
        self.assertNotContains(response, 'Hello')
        self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.get(reverse('home'))
        self.assertContains(response, 'Hello')

    def test_home_view_userprofile_creation(self):
        c = Client()
        testUser = self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        self.assertFalse(UserProfile.objects.filter(user = testUser).exists())
        c.get(reverse('home'))
        self.assertTrue(UserProfile.objects.filter(user = testUser).exists())

    def test_home_view_trades_by_comments_not_equal_to_0(self):
        c = Client()
        self.assertTrue(Trade.objects.all().count() == 0)
        response = c.get(reverse('home'))
        self.assertFalse(bool(response.context['comment_num']))
        self.assertFalse(bool(response.context['pictures']))
        user = self.create_user()
        trade = self.create_trade(user)
        self.create_picture(trade)
        response = c.get(reverse('home'))
        self.assertTrue(bool(response.context['comment_num']))
        self.assertTrue(bool(response.context['pictures']))

    def test_home_view_trades_by_newest_not_equal_to_0(self):
        c = Client()
        self.assertTrue(Trade.objects.all().count() == 0)
        response = c.get(reverse('home'))
        self.assertFalse(bool(response.context['comment_num2']))
        self.assertFalse(bool(response.context['pictures2']))
        user = self.create_user()
        trade = self.create_trade(user)
        self.create_picture(trade)
        response = c.get(reverse('home'))
        self.assertTrue(bool(response.context['comment_num2']))
        self.assertTrue(bool(response.context['pictures2']))

    def test_about_view(self):
        c = Client()
        response = c.get(reverse('quickswap:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/about.html','quickswap/base.html')
        self.assertContains(response, 'All About Quickswap')

    def test_add_trade_view(self):
        c = Client()
        response = c.get(reverse('quickswap:add_trade'))
        self.assertRedirects(response, '/accounts/login/?next=/quickswap/add_trade/', 302, 200)
        self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.get(reverse('quickswap:add_trade'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/add_trade.html','quickswap/base.html')
        self.assertContains(response, 'New Trade')


    def test_register_profile_view(self):
        c = Client()
        response = c.get(reverse('quickswap:register_profile'))
        self.assertRedirects(response, '/accounts/login/?next=/quickswap/register_profile/', 302, 200)
        self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.get(reverse('quickswap:register_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/profile_registration.html','quickswap/base.html')
        self.assertContains(response, 'Almost done...')

    def test_register_profile_form(self):
        c = Client()
        self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.post(reverse('quickswap:register_profile'))
        self.assertRedirects(response, '/quickswap/', 302, 200)

    def test_user_view_redirects(self):
        c = Client()
        #Trying to acces a user page when not logged in should redirect to login
        response = c.get(reverse('quickswap:user', args=['testUser']))
        self.assertRedirects(response, '/accounts/login/?next=/quickswap/user/testUser/', 302, 200)
        #Trying to access a user page that doesn't exists when logged in should
        #redirect to home
        self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.get(reverse('quickswap:user', args=['nonExistingUser']))
        self.assertRedirects(response, '/quickswap/', 302, 200)
        #Accessing existing user when logged in should work
        response = c.get(reverse('quickswap:user', args=['testUser']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/user.html','quickswap/base.html')

    def test_user_view_user_is_current_user(self):
        c = Client()
        self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.get(reverse('quickswap:user', args=['testUser']))
        self.assertContains(response, 'Your profile')
        User.objects.create(username = 'otherTestUser')
        response = c.get(reverse('quickswap:user', args=['otherTestUser']))
        self.assertContains(response, 's Profile')

    def test_user_view_post(self):
        c = Client()
        user = self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.post(reverse('quickswap:user', args=['testUser']))
        self.assertRedirects(response, '/quickswap/user/testUser/', 302, 200)

    def test_trade_view(self):
        c = Client()
        response = c.get(reverse('quickswap:trade', args=['test-trade']))
        self.assertRedirects(response, '/quickswap/', 302, 200)
        user = self.create_user()
        self.create_trade(user)
        response = c.get(reverse('quickswap:trade', args=['test-trade']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/trade.html','quickswap/base.html')
        self.assertContains(response, 'Suggested Trade')

    def test_trade_view_post(self):
        c = Client()
        user = self.create_user()
        trade = self.create_trade(user)
        self.create_picture(trade)
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.post(reverse('quickswap:trade', args=['testTrade']))
        self.assertRedirects(response, '/quickswap/', 302, 200)

    def test_edit_trade_view(self):
        c = Client()
        response = c.get(reverse('quickswap:edit_trade', args=['test-trade']))
        self.assertRedirects(response, '/accounts/login/?next=/quickswap/edit_trade/test-trade/', 302, 200)
        user = self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.get(reverse('quickswap:edit_trade', args=['test-trade']))
        self.assertRedirects(response, '/quickswap/', 302, 200)
        trade = self.create_trade(user)
        self.create_picture(trade)
        response = c.get(reverse('quickswap:edit_trade', args=['test-trade']))
        self.assertEqual(response.status_code, 200)


    def test_user_trade_view_is_current_user(self):
        c = Client()
        response = c.get(reverse('quickswap:usertrades', args=['testUser']))
        self.assertRedirects(response, '/accounts/login/?next=/quickswap/usertrades/testUser/', 302, 200)
        user = self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        response = c.get(reverse('quickswap:user', args=['nonExistingUser']))
        self.assertRedirects(response, '/quickswap/', 302, 200)
        response = c.get(reverse('quickswap:usertrades', args=['testUser']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/usertrades.html','quickswap/base.html')
        self.assertContains(response, 'You have not made any trades')
        trade = self.create_trade(user)
        self.create_picture(trade)
        response = c.get(reverse('quickswap:usertrades', args=['testUser']))
        self.assertContains(response, 'test Trade')


    def test_user__trades_view_user_does_not_exist(self):
        c = Client()
        user = self.create_user()
        self.assertTrue(c.login(username = 'testUser', password = 'testPassword'))
        self.assertRaises(User.DoesNotExist, UserTradesView.get_user(self, 'nonExistingUser'))
        response = c.get(reverse('quickswap:usertrades', args=['nonExistingUser']))
        self.assertRedirects(response, '/quickswap/', 302, 200)
        print(response)


    def test_category_view(self):
        c = Client()
        response = c.get(reverse('quickswap:category', args=['art']))
        self.assertContains(response, 'This category has no trades.')
        user = self.create_user()
        trade = self.create_trade(user)
        self.create_picture(trade)
        response = c.get(reverse('quickswap:category', args=['art']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/category.html','quickswap/base.html')
        self.assertContains(response, 'test Trade')

    def test_categories_view(self):
        c = Client()
        response = c.get(reverse('quickswap:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/categories.html','quickswap/base.html')
        self.assertContains(response, 'Electronics')

    def test_allusers_view(self):
        c = Client()
        response = c.get(reverse('quickswap:allusers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/allusers.html','quickswap/base.html')
        self.assertContains(response, 'Quickswap has no registered users')
        user = self.create_user()
        self.create_userprofile(user)
        response = c.get(reverse('quickswap:allusers'))
        self.assertContains(response, 'testUser')

    def test_alltrades_view(self):
        c = Client()
        response = c.get(reverse('quickswap:alltrades'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/alltrades.html','quickswap/base.html')
        self.assertContains(response, 'Quickswap has no available trades')
        user = self.create_user()
        trade = self.create_trade(user)
        self.create_picture(trade)
        response = c.get(reverse('quickswap:alltrades'))
        self.assertContains(response, 'test Trade')

    def test_contact_us_view(self):
        c = Client()
        response = c.get(reverse('quickswap:contactus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/contactus.html','quickswap/base.html')
        self.assertContains(response, 'Get In Touch')

    def test_helpdesk_view(self):
        c = Client()
        response = c.get(reverse('quickswap:helpdesk'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickswap/helpdesk.html','quickswap/base.html')
        self.assertContains(response, 'Having Trouble?')
