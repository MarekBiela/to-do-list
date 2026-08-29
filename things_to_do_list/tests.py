from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Task, Tag


class TaskViewTests(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name="home")
        self.task1 = Task.objects.create(
            name="Test1",
            is_done=True,
        )
        self.task2 = Task.objects.create(
            name="Test2",
            is_done=False,
        )
        self.task1.tags.add(self.tag)
        self.task2.tags.add(self.tag)

    def test_task_list_view(self):
        response = self.client.get(reverse("things_to_do_list:index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all()),
        )

        self.assertTemplateUsed(
            response,
            "things_to_do_list/task_list.html",
        )

    def test_task_create_view(self):
        response = self.client.post(
            reverse("things_to_do_list:create"),
            {
                "name": "Task test",
                "is_done": False,
                "tags": [self.tag.pk],
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.count(), 3)

    def test_task_update_view(self):
        response = self.client.post(
            reverse(
                "things_to_do_list:update",
                args=[self.task1.pk],
            ),
            {
                "name": "Updated task",
                "deadline": "",
                "is_done": False,
                "tags": [self.tag.pk],
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, "Updated task")
        self.assertFalse(self.task1.is_done)

    def test_task_delete_view(self):
        response = self.client.post(
            reverse(
                "things_to_do_list:delete",
                args=[self.task1.pk],
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_toggle_complete_undo_task(self):
        response = self.client.get(
            reverse(
                "things_to_do_list:toggle-complete-undo",
                args=[self.task1.pk],
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.is_done)


class TagViewTests(TestCase):

    def setUp(self):
        self.tag1 = Tag.objects.create(name="home")
        self.tag2 = Tag.objects.create(name="work")

    def test_tag_list_view(self):
        response = self.client.get(reverse("things_to_do_list:tag-list"))

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertEqual(
            list(response.context["tag_list"]),
            list(Tag.objects.all()),
        )

        self.assertTemplateUsed(
            response,
            "things_to_do_list/tag_list.html",
        )

    def test_tag_create_view(self):
        response = self.client.post(
            reverse("things_to_do_list:tag-create"),
            {
                "name": "test tag",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Tag.objects.count(), 3)

    def test_tag_update_view(self):
        response = self.client.post(
            reverse(
                "things_to_do_list:tag-update",
                args=[self.tag1.pk],
            ),
            {
                "name": "Updated tag",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.name, "Updated tag")

    def test_tag_delete_view(self):
        response = self.client.post(
            reverse(
                "things_to_do_list:tag-delete",
                args=[self.tag1.pk],
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Task.objects.filter(pk=self.tag1.pk).exists())
