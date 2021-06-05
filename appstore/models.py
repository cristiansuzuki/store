from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.IntegerField(default=0)  # --> preço em CENTAVOS <--

    def __str__(self):
        return self.nome

    def get_display_price(self):
        return "{0:.2f}".format(self.preco / 100)


# class Venda(models.Model):
#     produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
#     quantidade_produto = models.IntegerField()
#     valor_total = models.FloatField()
#     data_venda = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.produto.name
