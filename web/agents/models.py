import uuid
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey

from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail.blocks import PageChooserBlock

# Widgets et fonctions
from utils.faq import SimpleAnswerBlock, ChoiceAnswerBlock, StepAnswerBlock, FaqLaw

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Wagtail /home Médias, MenuPage, Panels, etc.
from home.views import custom_content_panels, custom_promote_panels
from utils.widgets import PiecesJointes as PJBlock

# Tags
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager

# Snippets
from wagtail.snippets.models import register_snippet

# API
from wagtail.api import APIField

# Traduction
from django.utils.translation import gettext_lazy as _

# Recherche et Tri
from wagtail.search import index
from itertools import groupby

# Slugs
from django.utils.text import slugify

# Formulaire
from wagtailstreamforms.blocks import WagtailFormBlock

##################
## PAGE DE MENU ##
################## 

# Index de la section pour les agents (tri par catégories)
class FaqIndexPage(MenuPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["agents.FaqPage", "agents.FaqFormPage"]
    save = menu_page_save("agents")
    
    def get_all_categories(self):
        return FaqCategory.objects.all()

    def get_all_tags(self):
        return FaqPageTag.objects.all()
    
    def get_popular_tags(self, limit=10):
        tags = FaqPageTag.objects.annotate(num_times=models.Count("tag")).order_by("-num_times")[:limit]
        return tags

    def get_sorted_faqs(self):
        return FaqPage.objects.child_of(self).order_by("category__slug")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        faqs = FaqPage.objects.child_of(self).live().select_related('category')
        category_slug = request.GET.get('category')
        tags = request.GET.getlist('tag')
        tags = tags if tags != [''] else None
        query = request.GET.get('query')
        
        if category_slug and category_slug != "*":                         
                faqs = faqs.filter(category__slug=category_slug)
        if tags:
            # faqs = faqs.filter(tags__slug__in=tags).distinct()
            for tag in tags:
                faqs = faqs.filter(tags__slug=tag)
                
        if query:
            faqs = faqs.search(query)
            faqs = sorted(faqs, key=lambda x: (x.category.title.lower(), x.category.slug.lower()))
        else:
            faqs = faqs.order_by('category__title', 'category__slug')

        # Grouper les faq
        grouped_faqs = {k: list(v) for k, v in groupby(faqs, lambda x: x.category)}

        is_root = not (category_slug or tags or query)
        
        context.update({
            'faqs': grouped_faqs,
            'categories': self.get_all_categories(),
            'tags': self.get_all_tags(),
            'popular_tags': self.get_popular_tags(),
            'selected_category': category_slug,
            'selected_tags': tags,
            'is_root': is_root,
            'query': query,
            'section': 'agents',
            'fields': ['category', 'tags'],
        })
        
        return context

######################
##   PAGES DE FAQ   ##
###################### 

# La page de création des Q/R (une grande partie de la logique se trouve dans /utils/faq.py)
class FaqPage(Page):
    parent_page_types = ["agents.FaqIndexPage"]
    subpage_types = []
    
    category = models.ForeignKey(
        'FaqCategory',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="+",
        verbose_name=_("Category"),
    )
    question = models.CharField(max_length=255, verbose_name=_("Question"))
    answer = StreamField(
        [
            ("single_answer", SimpleAnswerBlock(label=_("Simple answer"))),
            ("multiple_answer", ChoiceAnswerBlock()),
            ("step_answer", StepAnswerBlock()),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Answer(s)"),
        help_text=_(
            "Click on the ⊕ below to add an answer. You can add simple answer(s), conditional answer(s) or step answer(s). You can either imbriqued conditional answer(s) or step answer(s) inside any answer."
        ),
    )
    related = StreamField(
        [
            ('related_faq', PageChooserBlock(target_model='agents.FaqPage', label=_("Related FAQ"))),
        ],
        use_json_field=True,
        null=True, 
        blank=True, 
        verbose_name=_("Similar themes"), 
        help_text=_("You can click on the ⊕ below to add related FAQ to this one. Users will see it in the 'Go further' section"),
    )
    law_texts = StreamField(
        [
            ('law_text', FaqLaw(label=_("Law text"))),
        ],
        use_json_field=True,
        null=True,
        blank=True,
        verbose_name=_("Law texts"),
        help_text=_("You can click on the ⊕ below to add law texts related to this FAQ."),
    )
    tags = ClusterTaggableManager(
        through='FaqPageTag',
        blank=True,
        verbose_name=_("Faq Tags"),
    )

    content_panels = custom_content_panels(["title"]) + [
        FieldPanel("category"),
        FieldPanel("question", icon="question"),
        FieldPanel("answer", icon="answer"),
        FieldPanel("related", icon="related"),
        FieldPanel("law_texts", icon="law"),
        FieldPanel("tags"),
    ]

    promote_panels = custom_promote_panels(["slug"])

    # Fields for search
    search_fields = Page.search_fields + [
        index.AutocompleteField("title"),
        index.SearchField("question"),
        index.SearchField("category"),
        index.FilterField("answer"),
        index.FilterField("slug"),
    ]

    # Fields for API
    api_fields = [
        APIField("question"),
        APIField("answer"),
        APIField("category"),
        APIField("tags"),
    ]

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = "Question pour FAQ"
        if not self.slug:
            unique_suffix = uuid.uuid4().hex[:6]
            self.slug = f"faqslug-{unique_suffix}"
        super().save(*args, **kwargs)

# Page pour les enquêtes, les formulaires, etc.
class FaqFormPage(MenuPage):
    template = "agents/formulaires/questionnaire.html"
    parent_page_types = ["agents.FaqIndexPage"]
    subpage_types = []
    save = menu_page_save("formulaire-agents")
    
    introduction = RichTextField(
        blank=True,
        null=True,
        verbose_name=_("Introduction"),
        help_text=_("Here you can explain how the gathering works..."),
    )
    form = StreamField(
        [
            ('form_field', WagtailFormBlock(icon="form", label=_("Form field"))),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Question form"),
        help_text=_("The main form for to gather informations from the agents."),
    )
    date_from = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("From"),
        help_text=_("Start date of the survey."),
    )
    date_to = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("To"),
        help_text=_("End date of the survey."),
    )
    
    # Panneau de contenu
    content_panels = MenuPage.content_panels + [
        FieldPanel("introduction", heading=_("Introduction")),
        FieldPanel("form", heading=_("Form"), classname="collapsible"),
        MultiFieldPanel([
                FieldPanel("date_from", classname="col6"),
                FieldPanel("date_to", classname="col6"),
            ],
            heading=_("Survey period"),
            classname="collapsible",
        ),
        InlinePanel(
            "agents_documents",
            label=_("Document"),
            heading=_("Attachments"),
        ),
    ]    
           
    search_fields = MenuPage.search_fields + [
        index.SearchField("introduction"),
    ]
    
    class Meta:
        verbose_name = _("Agents Form page (survey, form, etc.)")
        verbose_name_plural = _("Form pages")
        
###############
##  WIDGETS  ##
############### 

@register_snippet
class FaqCategory(models.Model):
    title = models.CharField(
        max_length=255, 
        verbose_name=_("Title"),
        help_text=_("Visible title on the FAQ index page."),
    )
    slug = models.SlugField(unique=True, editable=False, default="")
    tooltip = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Tooltip"),
        help_text=_("Tooltip displayed on the index pages. Visible when user mouse over the logo icon."),
    )
    logo = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
        help_text=_("Visible icon on index pages. Ideal size: 1/1 (square or round). Format :⚠️SVG⚠️"),
        
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("tooltip"),
        FieldPanel("logo"),
    ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("one category")
        verbose_name_plural = _("categories")

# Les tags pour la FAQ
class FaqPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "FaqPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )

# Liste de documents (GenericPage)
class AmicalePieceJointe(PJBlock):
    """Modèle de pièce jointe spécifique à la page enquête/formulaire des agents"""

    page = ParentalKey(
        FaqFormPage,
        on_delete=models.CASCADE,
        related_name="agents_documents",
    )
   
## FONCTIONS ET AUTRES WIDGETS ##
# /utils/faq.py