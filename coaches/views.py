import csv
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import striptags
from django.views.decorators.csrf import csrf_exempt
from core.utils import get_event_page
from core.models import EventPageMenu
from applications.decorators import organiser_only
from .models import CoachApplication, CoachForm, Question, CoachEmail
from .forms import CoachApplicationForm, EmailForm
from .utils import get_coach_applications_for_page
from applications.utils import get_organiser_menu


def register(request, city):
    page = get_event_page(city, request.user.is_authenticated(), False)
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(
            request, "event_not_live.html",
            {'city': page[0], 'past': page[1]}
        )

    form_obj = CoachForm.objects.filter(page=page).first()
    if form_obj is None:
        return redirect('core:event', city)

    organiser = request.user in page.event.team.all() or request.user.is_superuser

    if not organiser and not form_obj.coach_application_open:
        return redirect('core:event', city)

    menu = EventPageMenu.objects.filter(page=page)

    form = CoachApplicationForm(
        request.POST or None, questions=form_obj.question_set.all()
    )

    if form.is_valid():
        form.save(form=form_obj)
        messages.success(request, "Yay! Your registration has been saved. You'll hear from us soon!")

        return render(request, 'coach_apply.html', {
            'page': page,
            'menu': menu,
            'form_obj': form_obj,
        })

    number_of_email_questions = Question.objects.filter(question_type='email', form=form_obj).count()

    return render(request, 'coach_apply.html', {
        'page': page,
        'menu': menu,
        'form_obj': form_obj,
        'form': form,
        'number_of_email_questions': number_of_email_questions,
    })


@organiser_only
def coach_applications(request, city):
    """
    Display a list of coach applications for this city.
    If 'state' get parameter is passed, filter the list.
    If 'order' get parameter is passed, order the list.
    e.g /coach_applications/?state=accepted&state=rejected
    """
    state = request.GET.getlist('state', None)
    page = get_event_page(city, request.user.is_authenticated(), False)
    order = request.GET.get('order', None)
    active_query_string = '?' + request.META.get('QUERY_STRING') if request.META.get('QUERY_STRING') else ''
    try:
        applications = get_coach_applications_for_page(page, state, order)
    except:
        return redirect('core:event', city=city)

    return render(request, 'coach_applications.html', {
        'page': page,
        'applications': applications,
        'all_applications_count': CoachApplication.objects.filter(form__page=page).count(),
        'active_query_string': active_query_string,
        'order': order,
        'menu': get_organiser_menu(city),
    })


@organiser_only
def applications_csv(request, city):
    """
    Download a csv of applications for this city, respecting filter and order parameters from url.
    """
    state = request.GET.getlist('state', None)
    page = get_event_page(city, request.user.is_authenticated(), False)
    order = request.GET.get('order', None)
    try:
        applications = get_coach_applications_for_page(page, state, order).prefetch_related('answer_set')
    except:
        return redirect('core:event', city=city)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = u'attachment; filename="{}.csv"'.format(city)
    writer = csv.writer(response)
    csv_header = ["Application Number", "Application State"]
    question_titles = page.coachform_set.first().question_set.values_list('title', flat=True)
    csv_header.extend(map(striptags, question_titles))
    writer.writerow(csv_header)
    question_ids = page.coachform_set.first().question_set.values_list('id', flat=True)
    for app in applications:
        app_info = [app.number, app.state]
        # get all answers for the application
        answer_dict = dict([(a.question_id, a.answer)for a in app.answer_set.all()])
        # find the answer corresponding to a question or empty string if not found
        # this keeps the csv columns correct if some applications have less questions than others
        answers = [answer_dict.get(q_id, '') for q_id in question_ids]
        app_info.extend(answers)
        writer.writerow(app_info)
    return response


@organiser_only
def coach_application_detail(request, city, coach_app_id):
    """
    Display the details of a single coach application.
    Redirect to list of coach applications if requested application doesn't exist.
    """
    application = None
    page = get_event_page(city, request.user.is_authenticated(), False)
    try:
        application = CoachApplication.objects.get(pk=coach_app_id)
    finally:
        if application:
            return render(request, 'coach_application_detail.html', {
                'page': page,
                'application': application,
                'form': application.form,
                'menu': get_organiser_menu(city),
            })
        return redirect('coaches:coach_applications', city=city)


@organiser_only
def communication(request, city):
    """
    Send emails to applicants and attendees
    """
    page = get_event_page(city, request.user.is_authenticated(), False)

    emails = CoachEmail.objects.filter(form__page=page).order_by('-created')

    return render(request, 'coach_communication.html', {
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
    form_obj = get_object_or_404(CoachForm, page=page)
    emailmsg = None if not email_id else get_object_or_404(CoachEmail, form__page=page, id=email_id)

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
        return redirect('coaches:coach_communication', city)

    return render(request, 'compose_coach_email.html', {
        'page': page,
        'menu': get_organiser_menu(city),
        'form': form,
        'email': emailmsg,
    })


@organiser_only
@csrf_exempt
def change_state(request, city):
    """
    Change the state of CoachApplicaction(s). Use it like this:
    e.g /coach_applications/?state=accepted&application=1&application=2&application=3
    """
    state = request.POST.get('state', None)
    applications = request.POST.getlist('application', None)
    page = get_event_page(city, request.user.is_authenticated(), False)

    if not state or not applications:
        return JsonResponse({'error': 'Missing parameters'})

    applications = CoachApplication.objects.filter(id__in=applications, form__page=page)
    applications.update(state=state)

    ids = applications.values_list('id', flat=True)
    ids = [str(id) for id in ids]

    return JsonResponse({'message': 'Applications have been updated', 'updated': ids})

