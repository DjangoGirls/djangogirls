from django.shortcuts import render, redirect
from django.http import Http404

from core.utils import get_event_page, get_applications_for_page
from core.models import EventPageMenu

from .decorators import organiser_only
from .models import Application, Form
from .forms import ApplicationForm


def apply(request, city):
    page = get_event_page(city, request.user.is_authenticated(), False)
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(request, "event_not_live.html",
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

    return render(request, 'apply.html', {
        'page': page,
        'menu': menu,
        'form_obj': form_obj,
        'form': form,
    })


@organiser_only
def applications(request, city):
    """
    Display a list of applications for this city.
    If 'state' get parameter is passed, filter the list.
    e.g /applications/?state=accepted&state=rejected
    """
    state = request.GET.getlist('state', None)
    page = get_event_page(city, request.user.is_authenticated(), False)
    applications = get_applications_for_page(page, state)

    return render(request, 'applications.html', {
        'page': page,
        'applications': applications,
    })


@organiser_only
def application_detail(request, city, app_id):
    """
    Display the details of a single application.
    """
    page = get_event_page(city, request.user.is_authenticated(), False)
    application = Application.objects.get(pk=app_id)
    
    return render(request, 'application_detail.html', {
        'page': page,
        'application': application,
        'form': application.form,
    })
