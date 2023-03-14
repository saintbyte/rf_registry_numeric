from django.db import models


class Registry(models.Model):
    code = models.PositiveIntegerField(verbose_name="Код", db_index=True)
    start = models.PositiveIntegerField(verbose_name="От")
    end = models.PositiveIntegerField(verbose_name="До")
    size = models.PositiveIntegerField(verbose_name="Емкость")
    operator = models.CharField(default="", verbose_name="Оператор", max_length=512)
    region = models.CharField(default="", verbose_name="Регион", max_length=512)
    tax_number = models.PositiveBigIntegerField(null=True, verbose_name="ИНН")

    def __str__(self):
        return f"{self.code} {self.start} - {self.end}"

    class Meta:
        verbose_name = "Реестр российской системы и плана нумерации"
        verbose_name_plural = "Реестр российской системы и плана нумерации"
