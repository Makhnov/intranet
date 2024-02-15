from termcolor import colored
from django.shortcuts import render
from django.utils.timezone import datetime
from wagtail.contrib.search_promotions.models import Query

from utils.auth import check_page_access
from administration.models import AdministrationIndexPage, ConvocationPage, CompteRenduPage

def administration_search(request):
    user = request.user
    search_query = request.GET.get('query', None)
    # print(colored(f"search_query: {search_query}", "yellow"))
    start_date = request.GET.get('start_date', None)
    # print(colored(f"start_date: {start_date}", "yellow"))
    end_date = request.GET.get('end_date', None)    
    # print(colored(f"end_date: {end_date}", "yellow"))
    pages = AdministrationIndexPage.objects.first().get_children().live().specific()
    
    convocations, comptes_rendus = cv_cr_filter(user, pages, search_query, start_date, end_date)
    
    return render(
        request,
        "widgets/search/admin_results.html",
        {
            "convocations": convocations,
            "comptes_rendus": comptes_rendus,
            "search_query": search_query,
            "start_date": start_date,
            "end_date": end_date,
        },
    )

# Filtre de recherche pour les convocations et comptes rendus
def cv_cr_filter(user, pages, search_query=None, start_date=None, end_date=None):
    convocations = ConvocationPage.objects.none()
    comptes_rendus = CompteRenduPage.objects.none() 
    
    for page in pages:
        if check_page_access(user, page, False):
            convocations = convocations | ConvocationPage.objects.live().descendant_of(page).order_by('date')
            comptes_rendus = comptes_rendus | CompteRenduPage.objects.live().descendant_of(page).order_by('date')

    if start_date == "single":
        date = datetime.now().date()
        convocations = convocations.filter(date__gte=date).first()
        comptes_rendus = comptes_rendus.filter(date__lte=date).last()
    else:
        if start_date:
            convocations = convocations.filter(date__gte=start_date)
            comptes_rendus = comptes_rendus.filter(date__gte=start_date)
        if end_date:
            convocations = convocations.filter(date__lte=end_date)
            comptes_rendus = comptes_rendus.filter(date__lte=end_date)

    # print(colored(f"convocations: {convocations}", "white", "on_blue"))
    # print(colored(f"comptes_rendus: {comptes_rendus}", "white", "on_blue"))   
    
    if search_query:                       
        convocations = convocations.search(search_query)
        comptes_rendus = comptes_rendus.search(search_query)
        Query.get(search_query).add_hit()
        
    return convocations, comptes_rendus