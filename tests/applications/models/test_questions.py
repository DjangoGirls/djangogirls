import pytest

from applications.models import Question


def test_get_choices_as_list(form):
    # correctly return choices of a choices field
    question = Question.objects.filter(question_type="choices")[:1].get()
    assert sorted(question.get_choices_as_list()) == sorted(question.choices.split(";"))

    # return TypeError if field is not a choices field
    question = Question.objects.filter(question_type="paragraph")[:1].get()
    with pytest.raises(TypeError):
        question.get_choices_as_list()
