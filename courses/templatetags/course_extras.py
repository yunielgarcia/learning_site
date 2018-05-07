import markdown2
from django import template
from django.utils.safestring import mark_safe

from ..models import Course

register = template.Library()


@register.simple_tag  # simple bcs only returns a string
def newest_course():
    """Gets the most recent course that was added to the library"""
    return Course.objects.latest('created_at')


@register.inclusion_tag('courses/course_nav.html')
def nav_courses_list():
    """Returns dict of courses to display as navigation pane"""
    courses = Course.objects.all()
    return {'courses': courses}


@register.filter('time_estimate')
def time_estimate(word_count):
    """Estimates the # of min to complete a step based on the passed-in wordcount"""
    minutes = round(word_count/20)
    return minutes


# register.inclusion_tag('courses/course_nav.html')(nav_courses_list)

@register.filter('makdown_to_html')
def makdown_to_html(makdown_text):
    """Converts markdown text to html"""
    html_body = markdown2.markdown(makdown_text)
    return mark_safe(html_body)
