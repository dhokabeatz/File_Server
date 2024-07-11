from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from backend.models import Document, CustomUser
from backend.forms import CustomUserCreationForm
from django.test import SimpleTestCase
from django.utils.cache import add_never_cache_headers
from django.http import HttpResponse
from backend.views import *
from django.contrib.auth.models import AnonymousUser
from backend.middleware import NoCacheMiddleware
from backend.views import *

class AuthTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="A!s2d#f4G%h"
        )
        self.client.login(username="testuser", password="A!s2d#f4G%h")

    def test_login_view(self):
        self.client.logout()
        response = self.client.post(
            reverse("login"),
            {"username": "test@example.com", "password": "A!s2d#f4G%h"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userDashboard"))

    def test_logout_view(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("landing_page"))

    def test_access_user_dashboard_authenticated(self):
        response = self.client.get(reverse("userDashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userdashboard_page.html")

    def test_access_user_dashboard_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("userDashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('userDashboard')}"
        )


class MiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="A!s2d#f4G%h"
        )

    def test_middleware_with_authenticated_user(self):
        request = self.factory.get(reverse("userDashboard"))
        request.user = self.user
        middleware = NoCacheMiddleware(lambda req: HttpResponse("OK"))
        response = middleware(request)
        self.assertEqual(response.status_code, 200)
        if request.user.is_authenticated:
            self.assertIn("Cache-Control", response)
            self.assertIn("no-store", response["Cache-Control"])

    def test_middleware_with_anonymous_user(self):
        request = self.factory.get(reverse("userDashboard"))
        request.user = AnonymousUser()
        middleware = NoCacheMiddleware(lambda req: HttpResponse("OK"))
        response = middleware(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache-Control", response)
        self.assertIn("no-cache", response["Cache-Control"])


class URLTests(SimpleTestCase):
    def test_add_file_url_is_resolved(self):
        url = reverse("add_file")
        self.assertEqual(resolve(url).func, add_file)

    def test_admin_dashboard_url_is_resolved(self):
        url = reverse("admin_dashboard")
        self.assertEqual(resolve(url).func, admin_dashboard)

    def test_edit_file_url_is_resolved(self):
        url = reverse("edit_file", args=[1])
        self.assertEqual(resolve(url).func, edit_file)

    def test_delete_file_url_is_resolved(self):
        url = reverse("delete_file", args=[1])
        self.assertEqual(resolve(url).func, delete_file)

    def test_download_multiple_files_url_is_resolved(self):
        url = reverse("download_multiple")
        self.assertEqual(resolve(url).func, download_multiple_files)

    def test_email_form_view_url_is_resolved(self):
        url = reverse("email_form", args=[1])
        self.assertEqual(resolve(url).func, email_form_view)

    def test_landing_page_url_is_resolved(self):
        url = reverse("landing_page")
        self.assertEqual(resolve(url).func, landing_page)

    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func, login)

    def test_signup_url_is_resolved(self):
        url = reverse("signUp")
        self.assertEqual(resolve(url).func, signUp)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, logout)

    def test_user_dashboard_url_is_resolved(self):
        url = reverse("userDashboard")
        self.assertEqual(resolve(url).func, userDashboard)


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "A!s2d#f4G%h",
                "password2": "A!s2d#f4G%h",
            }
        )
        if not form.is_valid():
            print(form.errors)  # Debugging: print form errors
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CustomUserCreationForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "A!s2d#f4G%h",
                "password2": "wrongpassword",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["password2"], ["The two password fields didn’t match."]
        )

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            username="existinguser", email="test@example.com", password="A!s2d#f4G%h"
        )
        form = CustomUserCreationForm(
            data={
                "username": "newuser",
                "email": "test@example.com",
                "password1": "A!s2d#f4G%h",
                "password2": "A!s2d#f4G%h",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Email already exists"])


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.admin_user = get_user_model().objects.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpassword123"
        )
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        cls.document = Document.objects.create(
            title="Test Document",
            description="This is a test document",
            file="testfile.txt",
            uploaded_by=cls.user,
        )

    def setUp(self):
        self.client = Client()

    def test_admin_dashboard_template(self):
        self.client.force_login(self.admin_user)  # Log in as admin user
        url = reverse("admin_dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.templates)  # Debug: Print the templates used
        self.assertTemplateUsed(response, "adminDashboard.html")

    def test_add_file_view(self):
        self.client.force_login(self.admin_user)  # Ensure admin is logged in
        url = reverse("add_file")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_file.html")

    def test_delete_file_view(self):
        self.client.force_login(self.admin_user)  # Ensure admin is logged in
        url = reverse("delete_file", args=[self.document.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_file.html")

    def test_edit_file_view(self):
        self.client.force_login(self.admin_user)  # Ensure admin is logged in
        url = reverse("edit_file", args=[self.document.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_file.html")

    def test_email_form_view(self):
        self.client.force_login(self.user)  # Log in as regular user for this test
        url = reverse("email_form", args=[self.document.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "email_form.html")

    def test_download_multiple_files_view(self):
        self.client.force_login(self.user)  # Log in as regular user for this test
        url = reverse("download_multiple")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)  # POST method not allowed


class DocumentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        Document.objects.create(
            title="Test Document",
            description="This is a test document",
            file="testfile.txt",
            uploaded_by=user,
        )

    def test_document_title(self):
        document = Document.objects.get(id=1)
        expected_title = f"{document.title}"
        self.assertEqual(expected_title, "Test Document")

    def test_document_description(self):
        document = Document.objects.get(id=1)
        expected_description = f"{document.description}"
        self.assertEqual(expected_description, "This is a test document")

    # Add more tests as needed for other fields and methods

    def test_document_str_method(self):
        document = Document.objects.get(id=1)
        self.assertEqual(str(document), document.title)
