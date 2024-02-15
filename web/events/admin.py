from django.contrib import admin
from ls.joyous.models import (MultidayEventPage, RecurringEventPage,
                              MultidayRecurringEventPage, removeContentPanels)

# Hide unwanted event types
MultidayEventPage.is_creatable = True
RecurringEventPage.is_creatable = False
MultidayRecurringEventPage.is_creatable = False

# Hide unwanted content
removeContentPanels(["category", "tz", "group_page"])