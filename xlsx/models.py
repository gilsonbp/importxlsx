from django.db import models


class Importacao(models.Model):
    descricao = models.CharField(max_length=200, verbose_name='Descrição')
    arquivo = models.FileField(verbose_name='Arquivo', upload_to='arquivos')
    dt_envio = models.DateTimeField(auto_now_add=True, verbose_name='Data de envio')
    dt_process = models.DateTimeField(verbose_name='Data do processamento', editable=False, null=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Importação'
        verbose_name_plural = 'Importações'


class VendaManager(models.Manager):
    def import_venda(self, data):
        """
        Grava os dados importados no banco de dados
        :param data: Dicionário com os campos importados
        :return: A venda gravada
        """
        venda = self.model(
            **data
        )
        venda.save(using=self._db)
        return venda


class Venda(models.Model):
    nota = models.CharField(max_length=10, verbose_name='Nota Fiscal', db_index=True, editable=False)
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor', editable=False)
    vencimento = models.DateField(verbose_name='Vencimento', editable=False)
    importacao = models.ForeignKey(Importacao, verbose_name='Importação', editable=False)

    objects = VendaManager()

    def __str__(self):
        return self.nota

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'