# Clefs
from wagtail.blocks import (
    URLBlock,
    CharBlock,
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
            ("paragraph", RichTextBlock(icon="pilcrow", label=_("Paragraph"))),
            ("media", MediaBlock(icon="media", label=_("Media"))),
            ("image", ImageChooserBlock(icon="image", label=_("Image"))),
            ("document", DocumentChooserBlock(icon="doc-full", label=_("Document"))),
            ("link", LinkBlock(icon="link", label=_("Link"))),
            ("embed", EmbedBlock(icon="media", label=_("Embed"))),
            ("list", ListBlock(CharBlock(icon="list-ul", label=_("List Item")), icon="list-ul", label=_("List"))),
            ("quote", BlockQuoteBlock(icon="openquote", label=_("Quote"))),
            ("table", TableBlock(table_options=TABLE_OPTIONS, icon="table", label=_("Table"))),
        ], icon="doc-full", label=_("Simple answer"), required=False, *args, **kwargs)

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

def intro_block():
    return CharBlock(
        required=False,
        search_index=True,
        label=_("Introduction"),
        icon="pilcrow",
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

def list_block(f, str):
    return ListBlock(f, label=_("Click on the + below to add another " + str))

class StepBlockSecondary(StructBlock):
    step_item = step_block()
    step_answer = SimpleAnswerBlock()
    class Meta:
        label = _("Step")
        
class ChoiceBlockSecondary(StructBlock):
    choice_item = choice_block()
    choice_answer = SimpleAnswerBlock()
    class Meta:
        label = _("Condition")
        
class ChoiceAnswerBlockSecondary(StructBlock):
    choices_intro = intro_block()
    choices = list_block(ChoiceBlockSecondary, "condition")  
    class Meta:
        icon = "help"
        label = _("Conditonnal answer")
        
class StepAnswerBlockSecondary(StructBlock):
    steps_intro = intro_block()
    steps = list_block(StepBlockSecondary, "step")
    class Meta:
        icon = "tasks"
        label = _("Step answer")
        
class ChoiceBlock(StructBlock):
    choice_item = choice_block()
    choice_answer = multiple_answer_block(ChoiceAnswerBlockSecondary(), StepAnswerBlockSecondary())
    class Meta:
        label = _("Condition")
    
class ChoiceAnswerBlock(StructBlock):
    choices_intro = intro_block()
    choices = list_block(ChoiceBlock, "condition")
    class Meta:
        icon = "help"
        label = _("Conditonnal answer")
        
# Bloc de réponse par étape
class StepBlock(StructBlock):
    step_item = step_block()
    step_answer = multiple_answer_block(ChoiceAnswerBlockSecondary(), StepAnswerBlockSecondary())
    class Meta:
        label = _("Step")
        
# Bloc de réponse à choix multiples
class StepAnswerBlock(StructBlock):
    steps_intro = intro_block()
    steps = list_block(StepBlock, "step")
    class Meta:
        icon = "tasks"
        label = _("Step answer")
