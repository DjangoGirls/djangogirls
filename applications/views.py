import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template.defaultfilters import striptags

from core.utils import get_event_page
from core.models import EventPageMenu
from .decorators import organiser_only
from .models import Application, Form, Score, Question, Email
from .forms import ApplicationForm, ScoreForm, EmailForm
from .utils import get_applications_for_page, get_organiser_menu, random_application


def apply(request, city):
    page = get_event_page(city, request.user.is_authenticated(), False)
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(
            request, "event_not_live.html",
            {'city': page[0], 'past': page[1]}
        )

    form_obj = Form.objects.filter(page=page).first()
    if form_obj is None:
        return redirect('core:event', city)

    organiser = request.user in page.event.team.all() or request.user.is_superuser

    if not organiser and not form_obj.application_open:
        return redirect('core:event', city)

    menu = EventPageMenu.objects.filter(page=page)

    form = ApplicationForm(
        request.POST or None, questions=form_obj.question_set.all()
    )

    if form.is_valid():
        form.save(form=form_obj)
        messages.success(request, "Yay! Your application has been saved. You'll hear from us soon!")

        return render(request, 'apply.html', {
            'page': page,
            'menu': menu,
            'form_obj': form_obj,
        })

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
    rsvp_status = request.GET.getlist('rsvp_status', None)
    page = get_event_page(city, request.user.is_authenticated(), False)
    order = request.GET.get('order', None)
    try:
        applications = get_applications_for_page(page, state, rsvp_status, order)
    except:
        return redirect('core:event', city=city)

    return render(request, 'applications.html', {
        'page': page,
        'applications': applications,
        'all_applications_count': Application.objects.filter(form__page=page).count(),
        'order': order,
        'menu': get_organiser_menu(city),
    })


@organiser_only
def applications_csv(request, city):
    """
    Download a csv of applications for this city.
    """
    page = get_event_page(city, request.user.is_authenticated(), False)
    try:
        applications = get_applications_for_page(page, None, None, None)
    except:
        return redirect('core:event', city=city)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = u'attachment; filename="{}.csv"'.format(city)
    writer = csv.writer(response)
    csv_header = ["Application Number", "Application State", "RSVP Status", "Average Score"]
    questions = page.form_set.first().question_set.values_list('title', flat=True)
    csv_header.extend(map(striptags, questions))
    writer.writerow(csv_header)
    for app in applications:
        score = app.average_score if app.is_scored_by_user(request.user) else '(hidden)'
        app_info = [app.number, app.state, app.rsvp_status, score]
        app_info.extend(app.answer_set.values_list('answer', flat=True))
        writer.writerow(app_info)
    return response


@organiser_only
def application_detail(request, city, app_id):
    """
    Display the details of a single application.
    """
    application = Application.objects.get(pk=app_id)
    try:
        score = Score.objects.get(
            user=request.user, application=application)
    except Score.DoesNotExist:
        score = None
    score_form = ScoreForm(instance=score)
    page = get_event_page(city, request.user.is_authenticated(), False)
    all_scores = Score.objects.filter(application=application)

    if request.POST:
        # Handle score submission.
        score_form = ScoreForm(request.POST, instance=score)
        if score_form.is_valid():
            score = score_form.save(commit=False)
            score.user = request.user
            score.application = application
            score.save()

        if request.POST.get('random'):
            # Go to a new random application.
            new_app = random_application(request, page, application)
            if new_app:
                return redirect(
                    'applications:application_detail', city, new_app.id)
            return redirect('applications:applications', city)

    return render(request, 'application_detail.html', {
        'page': page,
        'application': application,
        'form': application.form,
        'scores': all_scores,
        'user_score': score,
        'score_form': score_form,
        'menu': get_organiser_menu(city),
    })


@organiser_only
def communication(request, city):
    """
    Send emails to applicants and attendees
    """
    page = get_event_page(city, request.user.is_authenticated(), False)

    emails = Email.objects.filter(form__page=page).order_by('-created')

    return render(request, 'communication.html', {
        'page': page,
        'menu': get_organiser_menu(city),
        'emails': emails,
    })


@organiser_only
def compose_email(request, city, email_id=None):
    """
    Create new email or update email to applicants and attendees
    """
    page = get_event_page(city, request.user.is_authenticated(), False)
    form_obj = get_object_or_404(Form, page=page)
    emailmsg = None if not email_id else get_object_or_404(Email, form__page=page, id=email_id)

    form = EmailForm(request.POST or None, instance=emailmsg, initial={
        'author': request.user, 'form': form_obj
    })
    if form.is_valid() and request.method == 'POST':
        obj = form.save(commit=False)
        obj.author = request.user
        obj.form = form_obj
        obj.save()
        if request.POST.get('send'):
            obj.send()
        return redirect('applications:communication', city)

    return render(request, 'compose_email.html', {
        'page': page,
        'menu': get_organiser_menu(city),
        'form': form,
        'email': emailmsg,
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


@organiser_only
@csrf_exempt
def change_rsvp(request, city):
    """
    Change the rsvp_status of Applicaction(s). Use it like this:
    e.g /applications/?rsvp=yes&application=1&application=2&application=3
    """
    rsvp_status = request.POST.get('rsvp_status', None)
    applications = request.POST.getlist('application', None)
    page = get_event_page(city, request.user.is_authenticated(), False)

    if not rsvp_status or not applications:
        return JsonResponse({'error': 'Missing parameters'})

    applications = Application.objects.filter(id__in=applications, form__page=page)
    applications.update(rsvp_status=rsvp_status)

    ids = applications.values_list('id', flat=True)
    ids = [str(id) for id in ids]

    return JsonResponse({'message': 'Applications have been updated', 'updated': ids})


def rsvp(request, city, code):
    page = get_event_page(city, request.user.is_authenticated(), False)
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(
            request, "event_not_live.html",
            {'city': page[0], 'past': page[1]}
        )

    application, rsvp = Application.get_by_rsvp_code(code, page)
    if not application:
        return redirect('/{}/'.format(page.url))

    application.rsvp_status = rsvp
    application.save()

    if rsvp == 'yes':
        message = "Your answer has been saved, your participation in the workshop has been confirmed! We can't wait to meet you. We will be in touch with details soon."
    else:
        message = "Your answer has been saved, thanks for letting us know. Your spot will be assigned to another person on the waiting list."
    messages.success(request, message)

    menu = EventPageMenu.objects.filter(page=page)

    return render(request, 'apply.html', {
        'page': page,
        'menu': menu,
    })
