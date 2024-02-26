from django.db import models


class Sheet(models.Model):
    sheet_id = models.CharField(max_length=100)


class Cell(models.Model):
    cell_id = models.CharField(max_length=100)
    sheet_id = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    cell_value = models.CharField(max_length=100, name="value", null=True)
    cell_result = models.CharField(max_length=100, name="result", null=True)
