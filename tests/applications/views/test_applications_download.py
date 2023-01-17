import csv
from io import StringIO

from django.urls import reverse

from applications.models import Answer, Application, Question


def test_download_applications_list(admin_client, future_event, future_event_form, applications):
    applications_url = reverse("applications:applications_csv", kwargs={"page_url": future_event.page_url})
    resp = admin_client.get(applications_url)
    assert resp.status_code == 200
    assert resp.get("Content-Disposition") == f'attachment; filename="{future_event.page_url}.csv"'
    csv_file = StringIO(resp.content.decode("utf-8"))
    reader = csv.reader(csv_file)
    csv_list = list(reader)
    assert len(csv_list) == 5
    assert len(csv_list[0]) == 18
    assert csv_list[0][0] == "Application Number"
    assert csv_list[1][1] == "submitted"
    assert csv_list[2][1] == "accepted"
    assert csv_list[3][1] == "rejected"
    assert csv_list[4][1] == "waitlisted"
    assert csv_list[1][17] == "answer to last for app 1"


def test_download_applications_list_uses_query_parameters_to_filter_applications(
    admin_client, future_event, applications
):
    applications_url = reverse("applications:applications_csv", kwargs={"page_url": future_event.page_url})
    resp = admin_client.get(applications_url + "?state=submitted&state=accepted")
    assert resp.status_code == 200
    assert resp.get("Content-Disposition") == f'attachment; filename="{future_event.page_url}.csv"'
    csv_file = StringIO(resp.content.decode("utf-8"))
    reader = csv.reader(csv_file)
    csv_list = list(reader)
    assert len(csv_list) == 3


def test_download_applications_list_with_question_added(
    admin_client, application_submitted, future_event, future_event_form, applications
):
    applications_url = reverse("applications:applications_csv", kwargs={"page_url": future_event.page_url})
    # add new question x as next to last question
    last_question = future_event_form.question_set.last()
    questionx = Question.objects.create(
        form=future_event_form, question_type=Question.TEXT, order=last_question.order + 1, title="questionx"
    )

    # now create a new application with answer to the new question
    new_application = Application.objects.create(form=future_event_form, state="submitted")
    new_application_questionx_answer = Answer.objects.create(  # NOQA
        application=new_application, question=questionx, answer="answer to questionx for app 5"
    )
    new_application_5_last_answer = Answer.objects.create(  # NOQA
        application=new_application, question=last_question, answer="answer to last for app 5"
    )

    resp = admin_client.get(applications_url)

    assert resp.status_code == 200
    assert resp.get("Content-Disposition") == f'attachment; filename="{future_event.page_url}.csv"'
    csv_file = StringIO(resp.content.decode("utf-8"))
    reader = csv.reader(csv_file)
    csv_list = list(reader)
    assert len(csv_list) == 6
    assert len(csv_list[0]) == 19

    # question x should be in next to last column
    assert csv_list[0][18] == "questionx"

    # old application should have blank for question x in next-to-last
    # column
    assert csv_list[1][17] == "answer to last for app 1"
    assert csv_list[1][18] == ""

    # new application should have answer for question x in next-to-last
    # column
    assert csv_list[5][17] == "answer to last for app 5"
    assert csv_list[5][18] == "answer to questionx for app 5"
