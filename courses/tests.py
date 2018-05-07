from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Course, Step


# Create your tests here.
class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write regular expressions in python"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)


class CourseViewsTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python testing",
            description="Learn to write tests"
        )
        self.course2 = Course.objects.create(
            title="New Course",
            description="Course 2 description"
        )
        self.step = Step.objects.create(
            title="Intro to Doctests",
            description="test in your docstrings",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('course:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse("course:detail", kwargs={
            'pk': self.course.pk
        }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])

    def test_step_detail(self):
        resp = self.client.get(reverse('course:step', kwargs={
            'course_pk': self.course.pk,
            'step_pk': self.step.pk
        }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])