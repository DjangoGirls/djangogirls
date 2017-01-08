INVOLVEMENT_CHOICES = (
    ("newcomer", "I’ve never been to a Django Girls event"),
    ("attendee", "I’m a former attendee"),
    ("coach", "I’m a former coach"),
    ("organizer", "I’m a former organizer"),
    ("contributor", "I contributed to the tutorial or translations"))


NEW = "new"  # event is freshly submitted by user
IN_REVIEW = "in_review"  # admin started triaging the event
ON_HOLD = "on_hold"  # event is temporarily on hold (i.e. date is not definite)
ACCEPTED = "accepted"
REJECTED = "rejected"
DEPLOYED = "deployed"

APPLICATION_STATUS = (
    (NEW, "New"),
    (IN_REVIEW, "In review"),
    (ON_HOLD, "On hold"),
    (ACCEPTED, "Accepted"),
    (REJECTED, "Rejected"),
    (DEPLOYED, "Deployed"),
)
