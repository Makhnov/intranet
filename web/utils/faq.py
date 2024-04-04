# Clefs
from wagtail.blocks import (
    URLBlock,
    CharBlock,
    BooleanBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    ListBlock,
    BlockQuoteBlock,
)

# Blocks (Images, Documents, Embeds)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

# Blocks, Medias, PJ, etc.
from utils.streamfield import (
    CustomMediaBlock as MediaBlock,
    CustomLinkBlock as LinkBlock,
    CustomEmbedBlock as EmbedBlock,
    CustomPDFBlock as PDFBlock,
    CustomDOCXBlock as DOCXBlock,
    CustomButtonBlock as ButtonBlock,
)

# Tables
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from utils.variables import TABLE_OPTIONS

# Traductions
from django.utils.translation import gettext_lazy as _

# Textes de loi (embed bloc)
class FaqLaw(StructBlock):
    text_name = CharBlock(required=True, max_length=255, label=_("Law text reference"))
    text_link = URLBlock(required=True, label=_("Law text link"))
    
    class Meta:
        verbose_name = _("Law text")
        verbose_name_plural = _("Law texts")
        icon = "doc-full"
        
############################
## STRUCTURE DES REPONSES ##
############################ 
""" STRUCTURE DES REPONSES
BLOCS REPONSE NIVEAU 1 autorisés (autant que souhaité) :

✔️ SIMPLE
    
▶️ ETAPE PAR ETAPE
        BLOCS REPONSE NIVEAU 2 dans une réponse par étape (un bloc par étape) :        
            ✔️SIMPLE
            ▶️ETAPE PAR ETAPE
                BLOCS REPONSE NIVEAU 3 dans une réponse par étape (un bloc par étape) :
                    ✔️SIMPLE
            ▶️CHOIX MULTIPLES
                BLOCS REPONSE NIVEAU 3 dans une réponse à choix multiple (un bloc en réponse à chaque choix) :
                    ✔️SIMPLE
                    
▶️ CHOIX MULTIPLES
        BLOCS REPONSE NIVEAU 2 dans une réponse à choix multiple (un bloc en réponse à chaque choix)         
            ✔️SIMPLE
            ▶️ETAPE PAR ETAPE
                BLOCS REPONSE NIVEAU 3 dans une réponse par étape (un bloc par étape) :
                    ✔️SIMPLE
            ▶️CHOIX MULTIPLES
                BLOCS REPONSE NIVEAU 3 dans une réponse à choix multiple (un bloc en réponse à chaque choix) :
                    ✔️SIMPLE
"""

# Bloc de réponse simple utilisable à tous les niveaux (1, 2 et 3)
class SimpleAnswerBlock(StreamBlock):
    def __init__(self, *args, **kwargs):
        super().__init__([
            ("heading", CharBlock(classname="title", icon="title", label=_("Heading"))),
            ("paragraph", RichTextBlock(
                icon="pilcrow", 
                label=_("Paragraph"),
                editor="full",
                )),
            ("media", MediaBlock(icon="media", label=_("Media"))),
            ("image", ImageChooserBlock(icon="image", label=_("Image"))),
            ("document", DocumentChooserBlock(icon="doc-full", label=_("Document"))),
            ("link", LinkBlock(icon="link", label=_("Link"))),
            ("button", ButtonBlock(icon="button", label=_("Button"))),
            ("embed", EmbedBlock(icon="media", label=_("Embed"))),
            ("list", ListBlock(CharBlock(icon="list-ul", label=_("List Item")), icon="list-ul", label=_("List"))),
            ("quote", BlockQuoteBlock(icon="openquote", label=_("Quote"))),
            ("table", TableBlock(table_options=TABLE_OPTIONS, icon="table", label=_("Table"))),
        ], icon="doc-full", label=_("Simple answer"), required=False *args, **kwargs)
        
    class Meta:
        form_classname = 'simple-block' 
        
def choice_block():
    return CharBlock(
        required=False,
        search_index=True,
        label=_("Criteria"),
        help_text=_(
            "User select the criteria wich fits to his situation, it will allow him to see related answer(s). Mandatory."
        ),
    )

def step_block():
    return CharBlock(
        required=False,
        search_index=True,
        label=_("Step name"),
        help_text=_(
            "User click on each steps names to open it and see related answer(s). Mandatory."
        ),
    )    

def reduce_chooice_block():
    return BooleanBlock(
        required=False,
        label=_("Size reduction"),
        help_text=_("Check this box if you want to create a smaller version of choice answer (Perfect for the choices inside another choice answer)"),
    )

def ordonnated_step_block():
    return BooleanBlock(
        required=False,
        label=_("Ordonnated steps"),
        help_text=_("Check this box if you want to create an ordonnated version of step answer (Step 1, Step 2, Step 3, etc.)"),
    )

def multiple_answer_block(f1, f2):
    return StreamBlock(
        [
            ('single_answer', SimpleAnswerBlock()),
            ('multiple_answer', f1),
            ('step_answer', f2),
        ], 
        label=_("Related answer(s)"),
        required=False,
        search_index=True,
    )

def list_block(f, element, liste):
    return ListBlock(f, label=("Ajouter " + element), help_text=("Cliquez sur le + ci-dessous pour ajouter " + element + liste))


class ChoiceBlockSecondary(StructBlock):
    choice_item = choice_block()
    choice_answer = SimpleAnswerBlock()
    class Meta:
        label = _("Condition")
        
class StepBlockSecondary(StructBlock):
    step_item = step_block()
    step_answer = SimpleAnswerBlock()
    class Meta:
        label = _("Step")
        
class ChoiceAnswerBlockSecondary(StructBlock):
    reduction = reduce_chooice_block()
    choices = list_block(ChoiceBlockSecondary, "une option", " dans vos conditions")  
    class Meta:
        icon = "choice"
        label = _("Conditonnal answer")
        
class StepAnswerBlockSecondary(StructBlock):
    ordonnated = ordonnated_step_block()
    steps = list_block(StepBlockSecondary, "un élément", " dans votre liste")
    class Meta:
        icon = "tasks"
        label = _("Step answer")
        
class ChoiceBlock(StructBlock):
    choice_item = choice_block()
    choice_answer = multiple_answer_block(ChoiceAnswerBlockSecondary(), StepAnswerBlockSecondary())
    class Meta:
        label = _("Condition")
    
class ChoiceAnswerBlock(StructBlock):
    reduction = reduce_chooice_block()
    choices = list_block(ChoiceBlock, "une option", " dans vos conditions")
    class Meta:
        icon = "choice"
        label = _("Conditonnal answer")
        
class StepBlock(StructBlock):
    step_item = step_block()
    step_answer = multiple_answer_block(ChoiceAnswerBlockSecondary(), StepAnswerBlockSecondary())
    class Meta:
        label = _("Step")
        
class StepAnswerBlock(StructBlock):
    ordonnated = ordonnated_step_block()
    steps = list_block(StepBlock, "un élément", " dans votre liste")
    class Meta:
        icon = "tasks"
        label = _("Step answer")
