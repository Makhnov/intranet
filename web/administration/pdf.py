from django_weasyprint import WeasyTemplateResponseMixin
from django.http import request
from wagtail_pdf_view.mixins import PdfViewPageMixin
from django.views.generic.detail import DetailView
from .models import ConvocationPage, CompteRenduPage

class ConvocationPDFView(WeasyTemplateResponseMixin, DetailView):
    model = ConvocationPage
    template_name = 'administration/convocation_page.html'
    pdf_filename = 'convocation.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_pdf'] = 'pdf' in self.request.path
        return context


class CompteRenduPDFView(WeasyTemplateResponseMixin, DetailView):
    model = CompteRenduPage
    template_name = 'administration/compte_rendu_page.html'
    pdf_filename = 'compte_rendu.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_pdf'] = 'pdf' in self.request.path
        return context