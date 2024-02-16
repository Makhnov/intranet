from termcolor import colored
from django.db import models
from django.utils.text import slugify
from wagtail import blocks

from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

# Blocks (Images, Documents, Embeds)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

# Wagtail /home Médias, MenuPage, Panels, etc.
from home.models import (
    MediaBlock as MediaBlock,
    CustomLinkBlock as LinkBlock,
    CustomEmbedBlock as EmbedBlock,
)

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Clefs
from modelcluster.fields import ParentalKey

# Tables
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock

# Wagtail /home Médias, MenuPage, Panels, etc.
from home.views import custom_content_panels, custom_promote_panels

# Tags
from taggit.models import TaggedItemBase, Tag
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


class FaqPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "FaqPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class FaqIndexPage(MenuPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["agents.FaqPage"]
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

        # Tri par catégories
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
        })

        print(colored(f"category_slug: {category_slug}", "white", "on_blue"))
        print(colored(f"tag_slug: {tags}", "white", "on_blue"))
        print(colored(f"query: {query}", "white", "on_blue"))
        print(colored(f"faqs: {faqs}", "white", "on_blue"))
        print(colored(f"Page racine: {is_root}", "white", "on_blue"))
        
        return context

    
class FaqLaw(blocks.StructBlock):
    text_name = blocks.CharBlock(required=True, max_length=255, label=_("Law text reference"))
    text_link = blocks.URLBlock(required=True, label=_("Law text link"))
        
# ("table", TypedTableBlock([
#     ('text', blocks.CharBlock()),
#     ('numeric', blocks.FloatBlock()),
#     ('rich_text', blocks.RichTextBlock()),
#     ('image', ImageChooserBlock()),
# ], icon="table")),

def faq_simple_answer():
    return blocks.StreamBlock(        
        [
            ("heading", blocks.CharBlock(classname="title", icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="pilcrow")),
            ("media", MediaBlock(icon="media")),
            ("image", ImageChooserBlock(icon="image")),
            ("document", DocumentChooserBlock(icon="doc-full")),
            ("link", LinkBlock(icon="link")),
            ("embed", EmbedBlock(icon="media")),
            ("list", blocks.ListBlock(blocks.CharBlock(icon="list-ul"), icon="list-ul")),
            ("quote", blocks.BlockQuoteBlock(icon="openquote")),
            ("table", TableBlock(icon="table")),
        ],
        icon="doc-full",
        label=_("Simple answer"),
        required=False,
    )

def faq_choice_block():
    return blocks.CharBlock(
        required=False,
        search_index=True,
        label=_("Criteria"),
        help_text=_(
            "User select the criteria wich fits to his situation, it will allow him to see related answer(s). Mandatory."
        ),
    )

def faq_step_block():
    return blocks.CharBlock(
        required=False,
        search_index=True,
        label=_("Step name"),
        help_text=_(
            "User click on each steps names to open it and see related answer(s). Mandatory."
        ),
    )    

def faq_intro_block():
    return blocks.CharBlock(
        required=False,
        search_index=True,
        label=_("Introduction"),
        icon="pilcrow",
    )

def faq_answer_block(f1, f2):
    return blocks.StreamBlock(
        [
            ('single_answer', faq_simple_answer()),
            ('multiple_answer', f1),
            ('step_answer', f2),
        ], 
        label=_("Related answer(s)"),
        required=False,
        search_index=True,
    )

def faq_list_block(f, str):
    return blocks.ListBlock(f, label=_("Click on the + below to add another " + str))

class StepBlockSecondary(blocks.StructBlock):
    step_item = faq_step_block()
    step_answer = faq_simple_answer()
        
class ChoiceBlockSecondary(blocks.StructBlock):
    choice_item = faq_choice_block()
    choice_answer = faq_simple_answer()
           
class ChoiceAnswerBlockSecondary(blocks.StructBlock):
    choices_intro = faq_intro_block()
    choices = faq_list_block(ChoiceBlockSecondary, "condition")  

class StepAnswerBlockSecondary(blocks.StructBlock):
    steps_intro = faq_intro_block()
    steps = faq_list_block(StepBlockSecondary, "step")

class ChoiceBlock(blocks.StructBlock):
    choice_item = faq_choice_block()
    choice_answer = faq_answer_block(ChoiceAnswerBlockSecondary(), StepAnswerBlockSecondary())

class ChoiceAnswerBlock(blocks.StructBlock):
    choices_intro = faq_intro_block()
    choices = faq_list_block(ChoiceBlock, "condition")

class StepBlock(blocks.StructBlock):
    step_item = faq_step_block()
    step_answer = faq_answer_block(ChoiceAnswerBlockSecondary(), StepAnswerBlockSecondary())

class StepAnswerBlock(blocks.StructBlock):
    steps_intro = faq_intro_block()
    steps = faq_list_block(StepBlock, "step")


class FaqPage(Page):
    parent_page_types = ["agents.FaqIndexPage"]

    category = models.ForeignKey(
        FaqCategory,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="+",
        verbose_name=_("Category"),
    )
    question = models.CharField(max_length=255, verbose_name=_("Question"))
    answer = StreamField(
        [
            ("single_answer", faq_simple_answer()),
            ("multiple_answer", ChoiceAnswerBlock(icon="help", label=_("Conditonnal answer"))),
            ("step_answer", StepAnswerBlock(icon="tasks", label=_("Step answer"))),
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
            ('related_faq', blocks.PageChooserBlock(target_model='agents.FaqPage', label=_("Related FAQ"))),
        ],
        use_json_field=True,
        null=True, 
        blank=True, 
        verbose_name=_("Similar themes"), 
        help_text=_("You can click on the ⊕ below to add related FAQ to this one. Users will see it in the 'Go further' section"),
    )
    law_texts = StreamField(
        [
            ('law_text', FaqLaw()),
        ],
        use_json_field=True,
        null=True,
        blank=True,
        verbose_name=_("Law texts"),
        help_text=_("You can click on the ⊕ below to add law texts related to this FAQ."),
    )
    tags = ClusterTaggableManager(
        through=FaqPageTag,
        blank=True,
        verbose_name=_("Faq Tags"),
    )

    content_panels = custom_content_panels(["title"]) + [
        FieldPanel("category"),
        FieldPanel("question", icon="help"),
        FieldPanel("answer", icon="doc-full"),
        FieldPanel("related", icon="link"),
        FieldPanel("law_texts", icon="doc-full-inverse"),
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
        if not self.title:  # Si le titre n'est pas déjà défini
            self.title = "Question pour FAQ"
        if not self.slug:  # Si le slug n'est pas déjà défini
            self.slug = "faqslug"
        super().save(*args, **kwargs)