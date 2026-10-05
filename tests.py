from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Task

User = get_user_model()


class TaskCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pass12345!")
        self.other = User.objects.create_user("bob", password="pass12345!")
        self.client.login(username="alice", password="pass12345!")

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get(reverse("task-list"))
        self.assertEqual(resp.status_code, 302)

    def test_create(self):
        resp = self.client.post(reverse("task-create"), {"title": "Write tests", "status": "todo", "priority": 2})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Task.objects.get().owner, self.user)

    def test_update(self):
        t = Task.objects.create(owner=self.user, title="Old")
        self.client.post(reverse("task-update", args=[t.pk]), {"title": "New", "status": "done", "priority": 1})
        t.refresh_from_db()
        self.assertEqual((t.title, t.status), ("New", "done"))

    def test_delete(self):
        t = Task.objects.create(owner=self.user, title="Bye")
        self.client.post(reverse("task-delete", args=[t.pk]))
        self.assertFalse(Task.objects.exists())

    def test_cannot_access_others_tasks(self):
        t = Task.objects.create(owner=self.other, title="Secret")
        self.assertEqual(self.client.get(reverse("task-detail", args=[t.pk])).status_code, 404)

    def test_search(self):
        Task.objects.create(owner=self.user, title="Buy milk")
        Task.objects.create(owner=self.user, title="Walk dog")
        resp = self.client.get(reverse("task-list"), {"q": "milk"})
        self.assertEqual(len(resp.context["tasks"]), 1)
