from django.shortcuts import render
from agents.models import FaqPage, FaqCategory, FaqPageTag
from wagtail.contrib.search_promotions.models import Query


def faq_filter(request):
    categories = request.GET.getlist("categories")
    tags = request.GET.get("tags")
    if tags:
        tags = tags.split(",")

    # Tri des FAQ par catégorie
    faqs = FaqPage.objects.all().order_by("category__slug")

    if categories:
        faqs = faqs.filter(category__slug__in=categories)

    if tags:
        for tag in tags:
            faqs = faqs.filter(tags__name=tag)

    print(str(faqs.query))

    return render(request, "agents/widgets/faq_list.html", {"faqs": faqs})


def faq_search(request):
    search_query = request.GET.get("query", None)
    if search_query:
        faqs = FaqPage.objects.live().search(search_query)
        Query.get(search_query).add_hit()
    else:
        faqs = FaqPage.objects.live()

    return render(
        request,
        "agents/widgets/faq_list.html",
        {
            "faqs": faqs,
        },
    )

def faq_by_category(request, category_slug=None):
    # Si un slug de catégorie est fourni, filtrez les FAQs par catégorie
    if category_slug:
        faqs = FaqPage.objects.filter(category__slug=category_slug)
        category = FaqCategory.objects.get(slug=category_slug)
    else:
        # Sinon, affichez toutes les FAQs
        faqs = FaqPage.objects.all()
        category = None

    return render(request, 'agents/faq_by_category.html', {
        'faqs': faqs,
        'selected_category': category
    })