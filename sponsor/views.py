# from django.views.generic.base import TemplateView
#
# from core.utils import next_deadline
#
#
# class SponsorRequestView(TemplateView):
#     template_name = "sponsor/sponsor-request.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(SponsorRequestView, self).get_context_data(**kwargs)
#         context["deadline"] = next_deadline()
#         return context
