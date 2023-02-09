from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . views import dashboard
from . models import Data
from . models import Dashboard

# Register your models here.

class DataImportExportAdmin(ImportExportModelAdmin):
    list_display = ('cfname', 'north_coord', 'east_coord', 'kmeans_label', 'total_beds')

admin.site.register(Data, DataImportExportAdmin)

class DataImportExportAdmin(ImportExportModelAdmin):
    list_display = ('cfname', 'total_covid_patients', 'discharged', 'conf_died')

admin.site.register(Dashboard, DataImportExportAdmin)
