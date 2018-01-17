from .base import FunctionalTest
from samireland.models import Article

class WritingPageTests(FunctionalTest):

    def test_writing_page_layout(self):
        # The user goes to the writing page
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.click(nav_links[3])

        # The page has the correct heading
        self.check_page("/writing/")
        self.check_title("Writing")
        self.check_h1("Writing")

        # There's some summary text
        summary = self.browser.find_element_by_class_name("summary")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("button")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("form")

        # There is a writing section
        articles = self.browser.find_element_by_id("articles")
        self.assertIn("no articles", articles.text)
        with self.assertRaises(self.NoElement):
            articles.find_element_by_tag_name("a")


    def test_can_change_writing_page_text(self):
        self.check_editable_text("/writing/", "summary")


    def test_writing_page_articles(self):
        Article.objects.create(
         id="article-1", title="The First Article", date="2016-01-01",
         summary="summary1", body="Line 1\n\nLine 2"
        )
        Article.objects.create(
         id="article-2", title="The Recent Article", date="2016-08-09",
         summary="summary2", body="Line 1\n\nLine 2"
        )
        Article.objects.create(
         id="article-3", title="The Middle Article", date="2016-04-12",
         summary="summary3", body="Line 1\n\nLine 2"
        )

        # They go to the page and look at the articles - there are 3
        self.get("/writing/")
        articles = self.browser.find_element_by_id("articles")
        articles = articles.find_elements_by_class_name("article")
        self.assertEqual(len(articles), 3)

        # They are in the correct order
        self.assertEqual(
         articles[0].find_element_by_class_name("article-title").text,
         "The Recent Article"
        )
        self.assertEqual(
         articles[0].find_element_by_class_name("article-date").text,
         "9 August, 2016"
        )
        self.assertEqual(
         articles[1].find_element_by_class_name("article-title").text,
         "The Middle Article"
        )
        self.assertEqual(
         articles[1].find_element_by_class_name("article-date").text,
         "12 April, 2016"
        )
        self.assertEqual(
         articles[2].find_element_by_class_name("article-title").text,
         "The First Article"
        )
        self.assertEqual(
         articles[2].find_element_by_class_name("article-date").text,
         "1 January, 2016"
        )



class ArticleAdditionTests(FunctionalTest):

    def test_can_add_article(self):
        self.login()
        self.get("/writing/")

        # There is a link to create a new article
        articles = self.browser.find_element_by_id("articles")
        link = articles.find_element_by_tag_name("a")
        self.click(link)

        # They are on the new project page
        self.check_page("/writing/new/")
        self.check_title("New Article")
        self.check_h1("New Article")

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        summary_input = form.find_elements_by_tag_name("textarea")[0]
        body_input = form.find_elements_by_tag_name("textarea")[1]

        # They enter some data and submit
        id_input.send_keys("my-first-article")
        title_input.send_keys("My First Article")
        date_input.send_keys("01-06-2017")
        summary_input.send_keys("summary")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the page for the new article
        self.check_page("/writing/my-first-article/")
        self.check_title("My First Article")
        self.check_h1("My First Article")

        # There is a date
        date = self.browser.find_element_by_class_name("date")
        self.assertEqual(date.text, "1 June, 2017")

        # There is a body
        body = self.browser.find_element_by_class_name("article-body")
        paragraphs = body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Line 1")
        self.assertEqual(paragraphs[1].text, "Line 2")

        # They go back to the writing page and the article is there too
        self.get("/writing/")
        articles = self.browser.find_element_by_id("articles")
        self.assertNotIn("no publications", articles.text)
        articles = articles.find_elements_by_class_name("article")
        self.assertEqual(len(articles), 1)
        self.assertEqual(
         articles[0].find_element_by_class_name("article-title").text,
         "My First Article"
        )
        self.assertEqual(
         articles[0].find_element_by_class_name("article-date").text,
         "1 June, 2017"
        )
        self.assertEqual(
         articles[0].find_element_by_class_name("article-summary").text,
         "summary"
        )
        self.assertEqual(
         articles[0].find_element_by_class_name("article-link").text,
         "Read More"
        )
        self.click(articles[0].find_element_by_tag_name("a"))
        self.check_page("/writing/my-first-article/")


    def test_article_id_must_be_unique(self):
        self.login()
        self.get("/writing/new/")

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        summary_input = form.find_elements_by_tag_name("textarea")[0]
        body_input = form.find_elements_by_tag_name("textarea")[1]

        # They enter some data and submit
        id_input.send_keys("my-first-article")
        title_input.send_keys("My First Article")
        date_input.send_keys("01-06-2017")
        summary_input.send_keys("summary")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They do it again
        self.get("/writing/new/")
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        summary_input = form.find_elements_by_tag_name("textarea")[0]
        body_input = form.find_elements_by_tag_name("textarea")[1]
        id_input.send_keys("my-first-article")
        title_input.send_keys("My First Article")
        date_input.send_keys("01-06-2017")
        summary_input.send_keys("summary")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the same page
        self.check_page("/writing/new/")

        # The form is still filled in
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        summary_input = form.find_elements_by_tag_name("textarea")[0]
        body_input = form.find_elements_by_tag_name("textarea")[1]
        self.assertEqual(id_input.get_attribute("value"), "my-first-article")
        self.assertEqual(title_input.get_attribute("value"), "My First Article")
        self.assertEqual(date_input.get_attribute("value"), "2017-06-01")
        self.assertEqual(summary_input.get_attribute("value"), "summary")
        self.assertEqual(body_input.get_attribute("value"), "Line 1\n\nLine 2")

        # There is an error message
        error = form.find_element_by_class_name("error-message")
        self.assertIn("already", error.text)



class ArticleEditingTests(FunctionalTest):

    def setUp(self):
        FunctionalTest.setUp(self)
        Article.objects.create(
         id="my-first-article", title="My First Article", date="2017-06-01",
         summary="summary", body="Line 1\n\nLine 2"
        )


    def test_can_edit_paper(self):
        self.login()

        # The user goes to the article page
        self.get("/writing/my-first-article/")

        # There is an edit link
        edit = self.browser.find_element_by_class_name("edit")
        self.click(edit)

        # They are on the edit page, and there is a filled in form
        self.check_page("/writing/my-first-article/edit/")
        self.check_title("Edit Article")
        self.check_h1("Edit Article")
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        summary_input = form.find_elements_by_tag_name("textarea")[0]
        body_input = form.find_elements_by_tag_name("textarea")[1]
        self.assertEqual(id_input.get_attribute("value"), "my-first-article")
        self.assertFalse(id_input.is_enabled())
        self.assertEqual(title_input.get_attribute("value"), "My First Article")
        self.assertEqual(date_input.get_attribute("value"), "2017-06-01")
        self.assertEqual(summary_input.get_attribute("value"), "summary")
        self.assertEqual(body_input.get_attribute("value"), "Line 1\n\nLine 2")

        # They make a bunch of edits and save
        title_input.send_keys("T")
        date_input.send_keys("2")
        summary_input.send_keys("S")
        body_input.send_keys("B")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the article page and it is changed
        self.check_page("/writing/my-first-article/")
        self.check_title("My First ArticleT")
        self.check_h1("My First ArticleT")

        date = self.browser.find_element_by_class_name("date")
        self.assertEqual(date.text, "2 June, 2017")
        body = self.browser.find_element_by_class_name("article-body")
        paragraphs = body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Line 1")
        self.assertEqual(paragraphs[1].text, "Line 2B")


    def test_article_deletion(self):
        # User goes to edit the article
        self.login()
        self.get("/writing/my-first-article/")
        edit = self.browser.find_element_by_class_name("edit")
        self.click(edit)
        self.check_page("/writing/my-first-article/edit/")

        # There is a deletion button
        delete_button = self.browser.find_element_by_tag_name("button")
        self.assertIn("Delete", delete_button.text)

        # They click it and a form appears
        deletion_form = self.browser.find_elements_by_tag_name("form")[1]
        self.check_invisible(deletion_form)
        self.click(delete_button)
        self.check_visible(deletion_form)

        # The form asks them if they really want to delete and they back down
        self.assertIn("sure", deletion_form.text)
        no = deletion_form.find_element_by_tag_name("button")
        self.assertIn("No", no.text)
        self.click(no)
        self.check_invisible(deletion_form)

        # They change their mind and delete
        self.click(delete_button)
        self.check_visible(deletion_form)
        yes = deletion_form.find_elements_by_tag_name("input")[-1]
        self.assertIn("Yes", yes.get_attribute("value"))
        self.click(yes)

        # They are back on the research page and the publication is gone
        self.check_page("/writing/")
        articles = self.browser.find_element_by_id("articles")
        self.assertIn("no articles", articles.text)
