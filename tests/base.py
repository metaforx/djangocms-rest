from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth import get_user_model


class RESTTestCase(CMSTestCase):
    prefix = "http://testserver"

class BaseCMSRestTestCase(RESTTestCase):
    @classmethod
    def _create_pages(cls, page_list, parent=None):
        new_pages = [
            create_page(f"page {i}", language="en", template="INHERIT", parent=parent)
            for i in range(page_list if isinstance(page_list, int) else len(page_list))
        ]

        if isinstance(page_list, list):
            for i, page in enumerate(new_pages):
                cls._create_pages(page_list[i], page)
        else:
            cls.pages = new_pages

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        User = get_user_model()
        cls.user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass",
            is_staff=True,
            is_superuser=True
        )

        cls._create_pages([2, (3, 1), 2])
        # homepage = cls.pages[0]
        # homepage.set_as_homepage()
        # homepage.refresh_from_db()
        # publish_page(homepage, user=cls.user, language="en")

    @classmethod
    def tearDownClass(cls):
        from cms.models import Page
        Page.objects.all().delete()
        super().tearDownClass()

