from datetime import datetime

from django.contrib import admin
from django.contrib import messages

from xlsx.importacao import ImportacaoXlsx
from xlsx.models import Venda, Importacao


class VendaAdmin(admin.ModelAdmin):
    list_display = ('nota', 'valor', 'vencimento', 'importacao',)
    list_display_links = list_display
    search_fields = ('nota',)
    list_filter = ('importacao', 'vencimento',)
    list_per_page = 30
    actions_on_top = True
    actions_on_bottom = True
    readonly_fields = ('nota', 'valor', 'vencimento', 'importacao',)
    fieldsets = (
        (None,
         {'fields': ('nota', 'valor', 'vencimento', 'importacao',)}),
    )


class ImportacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'dt_envio', 'dt_process',)
    list_display_links = list_display

    actions_on_top = True
    actions_on_bottom = True

    def save_model(self, request, obj, form, change):
        super(ImportacaoAdmin, self).save_model(request, obj, form, change)
        try:
            ImportacaoXlsx.importar_vendas(obj)

            obj.dt_process = datetime.now()
            obj.save()

            messages.info(request, 'Arquivo importado com sucesso.')
        except Exception as e:
            messages.error(request, e)


admin.site.register(Venda, VendaAdmin)
admin.site.register(Importacao, ImportacaoAdmin)
