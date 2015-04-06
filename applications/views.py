from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from core.utils import (
    get_event_page, get_applications_for_page, random_application
)
from core.models import EventPageMenu

from .decorators import organiser_only
from .models import Application, Form, Score, Question
from .forms import ApplicationForm, ScoreForm


def apply(request, city):
    page = get_event_page(city, request.user.is_authenticated(), False)
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(
            request, "event_not_live.html",
            {'city': page[0], 'past': page[1]}
        )

    try:
        form_obj = Form.objects.get(page=page)
    except Form.DoesNotExist:
        return redirect('core:event', city)

    menu = EventPageMenu.objects.filter(page=page)

    form = ApplicationForm(
        request.POST or None, questions=form_obj.question_set.all()
    )

    if form.is_valid():
        form.save(form=form_obj)

    number_of_email_questions = Question.objects.filter(question_type='email', form=form_obj).count()

    return render(request, 'apply.html', {
        'page': page,
        'menu': menu,
        'form_obj': form_obj,
        'form': form,
        'number_of_email_questions': number_of_email_questions,
    })


@organiser_only
def applications(request, city):
    """
    Display a list of applications for this city.
    If 'state' get parameter is passed, filter the list.
    If 'order' get parameter is passed, order the list.
    e.g /applications/?state=accepted&state=rejected
    """
    state = request.GET.getlist('state', None)
    page = get_event_page(city, request.user.is_authenticated(), False)
    order = request.GET.get('order', None)
    applications = get_applications_for_page(page, state, order)

    menu = [
        {'title': 'Applications', 'url': reverse('applications:applications', args=[city])},
        {'title': 'Messaging', 'url': ''}
    ]

    return render(request, 'applications.html', {
        'page': page,
        'applications': applications,
        'order': order,
        'menu': menu,
    })


@organiser_only
def application_detail(request, city, app_id):
    """
    Display the details of a single application.
    """
    application = Application.objects.get(pk=app_id)
    score, created = Score.objects.get_or_create(
        user=request.user, application=application)
    score_form = ScoreForm(instance=score)
    page = get_event_page(city, request.user.is_authenticated(), False)
    all_scores = Score.objects.filter(application=application)

    if request.POST:
        # Handle score submission.
        score_form = ScoreForm(request.POST, instance=score)
        if score_form.is_valid():
            score_form.save()

        if request.POST.get('random'):
            # Go to a new random application.
            new_app = random_application(request, page, application)
            if new_app:
                return redirect(
                    'applications:application_detail', city, new_app.id)
            return redirect('applications:applications', city)

    menu = [
        {'title': 'Applications', 'url': reverse('applications:applications', args=[city])},
        {'title': 'Messaging', 'url': ''}
    ]

    return render(request, 'application_detail.html', {
        'page': page,
        'application': application,
        'form': application.form,
        'scores': all_scores,
        'user_score': score,
        'score_form': score_form,
        'menu': menu,
    })

@organiser_only
@csrf_exempt
def change_state(request, city):
    """
    Change the state of Applicaction(s). Use it like this:
    e.g /applications/?state=accepted&application=1&application=2&application=3
    """
    state = request.POST.get('state', None)
    applications = request.POST.getlist('application', None)
    page = get_event_page(city, request.user.is_authenticated(), False)

    if not state or not applications:
        return JsonResponse({'error': 'Missing parameters'})

    applications = Application.objects.filter(id__in=applications, form__page=page)
    applications.update(state=state)

    ids = applications.values_list('id', flat=True)
    ids = [str(id) for id in ids]

    return JsonResponse({'message': 'Applications have been updated', 'updated': ids})
