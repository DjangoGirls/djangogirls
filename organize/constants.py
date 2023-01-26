from django.utils.translation import gettext_lazy as _

INVOLVEMENT_CHOICES = (
    ("newcomer", _("I've never been to a Django Girls event")),
    ("attendee", _("I'm a former attendee")),
    ("coach", _("I'm a former coach")),
    ("organizer", _("I'm a former organizer")),
    ("contributor", _("I contributed to the tutorial or translations")),
)


NEW = "new"  # event is freshly submitted by user
IN_REVIEW = "in_review"  # admin started triaging the event
ON_HOLD = "on_hold"  # event is temporarily on hold (i.e. date is not definite)
ACCEPTED = "accepted"
REJECTED = "rejected"
DEPLOYED = "deployed"

APPLICATION_STATUS = (
    (NEW, _("New")),
    (IN_REVIEW, _("In review")),
    (ON_HOLD, _("On hold")),
    (ACCEPTED, _("Accepted")),
    (REJECTED, _("Rejected")),
    (DEPLOYED, _("Deployed")),
)
