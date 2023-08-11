import csv

from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import striptags
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from core.models import EventPageMenu
from core.utils import get_event

from .decorators import organiser_only
from .forms import ApplicationForm, EmailForm, ScoreForm
from .models import Application, Email, Form, Question, Score
from .questions import get_organiser_menu
from .services import get_applications_for_event, get_random_application


def apply(request, page_url):
    event = get_event(page_url, request.user.is_authenticated, False)
    if not event:
        raise Http404
    elif isinstance(event, tuple):
        return render(request, "applications/event_not_live.html", {"city": event[0], "past": event[1]})

    form_obj = Form.objects.filter(event=event).first()
    if form_obj is None:
        return redirect("core:event", page_url)

    organiser = request.user in event.team.all() or request.user.is_superuser

    if not organiser and not form_obj.application_open:
        return redirect("core:event", page_url)

    menu = EventPageMenu.objects.filter(event=event)

    form = ApplicationForm(request.POST or None, form=form_obj)

    if form.is_valid():
        form.save()
        messages.success(request, _("Yay! Your application has been saved. You'll hear from us soon!"))

        return render(
            request,
            "applications/apply.html",
            {
                "event": event,
                "menu": menu,
                "form_obj": form_obj,
            },
        )

    number_of_email_questions = Question.objects.filter(question_type="email", form=form_obj).count()

    return render(
        request,
        "applications/apply.html",
        {
            "event": event,
            "menu": menu,
            "form_obj": form_obj,
            "form": form,
            "number_of_email_questions": number_of_email_questions,
        },
    )


@organiser_only
def application_list(request, page_url):
    """
    Display a list of applications for this city.
    If 'state' get parameter is passed, filter the list.
    If 'order' get parameter is passed, order the list.
    e.g /applications/?state=accepted&state=rejected
    """
    state = request.GET.getlist("state", None)
    rsvp_status = request.GET.getlist("rsvp_status", None)
    event = get_event(page_url, request.user.is_authenticated, False)
    order = request.GET.get("order", None)
    active_query_string = "?" + request.META.get("QUERY_STRING", "")

    try:
        applications = get_applications_for_event(event, state, rsvp_status, order, user=request.user)
    except Application.DoesNotExist:
        return redirect("core:event", page_url=page_url)

    return render(
        request,
        "applications/applications.html",
        {
            "event": event,
            "applications": applications,
            "all_applications_count": Application.objects.filter(form__event=event).count(),
            "active_query_string": active_query_string,
            "order": order,
            "menu": get_organiser_menu(page_url),
        },
    )


@organiser_only
def applications_csv(request, page_url):
    """
    Download a csv of applications for this city, respecting filter and
    order parameters from url.
    """
    state = request.GET.getlist("state", None)
    rsvp_status = request.GET.getlist("rsvp_status", None)
    event = get_event(page_url, request.user.is_authenticated, False)
    order = request.GET.get("order", None)
    try:
        applications = get_applications_for_event(event, state, rsvp_status, order)
    except:  # TODO: what's the exception here?
        return redirect("core:event", page_url=page_url)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{page_url}.csv"'
    writer = csv.writer(response)
    csv_header = [_("Application Number"), _("Application State"), _("RSVP Status"), _("Average Score")]
    question_set = event.form.question_set

    question_titles = question_set.values_list("title", flat=True)
    csv_header.extend(map(striptags, question_titles))
    writer.writerow(csv_header)
    question_ids = question_set.values_list("id", flat=True)
    for app in applications:
        score = app.average_score if app.is_scored_by_user(request.user) else "(hidden)"
        app_info = [app.number, app.state, app.rsvp_status, score]
        # get all answers for the application
        answer_dict = {a.question_id: a.answer for a in app.answer_set.all()}
        # find the answer corresponding to a question or empty string if not found
        # this keeps the csv columns correct if some applications have less
        # questions than others
        answers = [answer_dict.get(q_id, "") for q_id in question_ids]
        app_info.extend(answers)
        writer.writerow(app_info)
    return response


@organiser_only
def application_detail(request, page_url, app_number):
    """
    Display the details of a single application.
    """
    application = (
        Application.objects.filter(number=app_number)
        .filter(form__event__page_url=page_url)
        .order_by("-created")
        .first()
    )
    try:
        score = Score.objects.get(user=request.user, application=application)
    except Score.DoesNotExist:
        score = None
    score_form = ScoreForm(instance=score)
    event = get_event(page_url, request.user.is_authenticated, False)
    all_scores = Score.objects.filter(application=application)

    if request.POST:
        # Handle score submission.
        score_form = ScoreForm(request.POST, instance=score)
        if score_form.is_valid():
            score = score_form.save(commit=False)
            score.user = request.user
            score.application = application
            score.save()

        if request.POST.get("random"):
            # Go to a new random application.
            new_app = get_random_application(request.user, event, application)
            if new_app:
                return redirect("applications:application_detail", page_url, new_app.number)
            return redirect("applications:applications", page_url)

    return render(
        request,
        "applications/application_detail.html",
        {
            "event": event,
            "application": application,
            "form": application.form,
            "scores": all_scores,
            "user_score": score,
            "score_form": score_form,
            "menu": get_organiser_menu(page_url),
        },
    )


@organiser_only
def communication(request, page_url):
    """
    Send emails to applicants and attendees
    """
    event = get_event(page_url, request.user.is_authenticated, False)

    emails = Email.objects.filter(form__event=event).order_by("-created")

    return render(
        request,
        "applications/communication.html",
        {
            "event": event,
            "menu": get_organiser_menu(page_url),
            "emails": emails,
        },
    )


@organiser_only
def compose_email(request, page_url, email_id=None):
    """
    Create new email or update email to applicants and attendees
    """
    event = get_event(page_url, request.user.is_authenticated, False)
    form_obj = get_object_or_404(Form, event=event)
    emailmsg = None if not email_id else get_object_or_404(Email, form__event=event, id=email_id)

    form = EmailForm(request.POST or None, instance=emailmsg, initial={"author": request.user, "form": form_obj})
    if form.is_valid() and request.method == "POST":
        obj = form.save(commit=False)
        obj.author = request.user
        obj.form = form_obj
        obj.save()
        if request.POST.get("send"):
            obj.send()
        return redirect("applications:communication", page_url)

    return render(
        request,
        "applications/compose_email.html",
        {
            "event": event,
            "menu": get_organiser_menu(page_url),
            "form": form,
            "email": emailmsg,
        },
    )


@organiser_only
@csrf_exempt
def change_state(request, page_url):
    """
    Change the state of Application(s). Use it like this:
    e.g /applications/?state=accepted&application=1&application=2&application=3
    """
    state = request.POST.get("state", None)
    applications = request.POST.getlist("application", None)
    event = get_event(page_url, request.user.is_authenticated, False)

    if not state or not applications:
        return JsonResponse({"error": _("Missing parameters")})

    # cleanup applications so we don't put something unwated in the db
    applications = [value for value in applications if value.isdigit()]

    applications = Application.objects.filter(id__in=applications, form__event=event)
    applications.update(state=state)

    ids = applications.values_list("id", flat=True)
    ids = [str(_id) for _id in ids]

    return JsonResponse({"message": _("Applications have been updated"), "updated": ids})


@organiser_only
@csrf_exempt
def change_rsvp(request, page_url):
    """
    Change the rsvp_status of Application(s). Use it like this:
    e.g /applications/?rsvp=yes&application=1&application=2&application=3
    """
    rsvp_status = request.POST.get("rsvp_status", None)
    applications = request.POST.getlist("application", None)
    event = get_event(page_url, request.user.is_authenticated, False)

    if not rsvp_status or not applications:
        return JsonResponse({"error": _("Missing parameters")})

    applications = Application.objects.filter(id__in=applications, form__event=event)
    applications.update(rsvp_status=rsvp_status)

    ids = applications.values_list("id", flat=True)
    ids = [str(_id) for _id in ids]

    return JsonResponse({"message": _("Applications have been updated"), "updated": ids})


def rsvp(request, page_url, code):
    event = get_event(page_url, request.user.is_authenticated, False)
    if not event:
        raise Http404
    elif isinstance(event, tuple):
        return render(request, "applications/event_not_live.html", {"city": event[0], "past": event[1]})

    application, rsvp = Application.get_by_rsvp_code(code, event)
    if not application:
        return redirect(f"/{event.page_url}/")

    if application.rsvp_status != Application.RSVP_WAITING:
        messages.error(
            request,
            _("Something went wrong with your RSVP link. Please contact us at " "%(email)s with your name.")
            % {"email": event.email},
        )
        return redirect(f"/{event.page_url}/")

    application.rsvp_status = rsvp
    application.save()

    if rsvp == Application.RSVP_YES:
        message = _(
            "Your participation in the workshop has been confirmed! "
            "We can't wait to meet you. We will be in "
            "touch with details soon."
        )
    else:
        message = _(
            "Your answer has been saved, thanks for letting us know. Your "
            "spot will be assigned to another person on the waiting list."
        )

    menu = EventPageMenu.objects.filter(event=event)

    return render(request, "applications/rsvp.html", {"event": event, "menu": menu, "message": message})
