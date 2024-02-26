from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from excel.models import Sheet, Cell
from excel.result import result
from excel.serializers import CellSerializer, CellSerializerResult


class CellViewSet(viewsets.ViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ["cell_id"]


    def retrieve(self, request, sheet_id, cell_id):
        try:
            sheet = Sheet.objects.get(sheet_id__iexact=sheet_id)
        except Sheet.DoesNotExist:
            sheet = Sheet(sheet_id=sheet_id)
            sheet.save()

        serializer = CellSerializer(data={"cell_id": cell_id})
        serializer.is_valid(raise_exception=True)

        try:
            cell = Cell.objects.get(sheet_id=sheet, cell_id__iexact=cell_id)
        except Cell.DoesNotExist:
            cell = Cell(cell_id=cell_id, sheet_id=sheet)
            cell.save()

        serializer = CellSerializer(cell)
        return Response(serializer.data)

    def update(self, request, sheet_id, cell_id):
        try:
            sheet = Sheet.objects.get(sheet_id__iexact=sheet_id)
        except Sheet.DoesNotExist:
            sheet = Sheet(sheet_id=sheet_id)
            sheet.save()

        try:
            cell = Cell.objects.get(sheet_id=sheet, cell_id__iexact=cell_id)
        except Cell.DoesNotExist:
            cell = Cell(cell_id=cell_id, sheet_id=sheet)
            cell.save()

        serializer = CellSerializer(cell, data=request.data)
        serializer_result = CellSerializerResult(cell, data=request.data)

        if serializer_result.is_valid() and serializer.is_valid():
            cell.value = serializer.validated_data["value"]
            value = cell.value
            sheet_id = cell.sheet_id_id
            cell.result = result(value, sheet_id)
            serializer_result.save()
            serializer.save()
            return Response(serializer_result.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, sheet_id, cell_id):
        try:
            sheet = Sheet.objects.get(sheet_id__iexact=sheet_id)
        except Sheet.DoesNotExist:
            sheet = Sheet(sheet_id=sheet_id)
            sheet.save()

        try:
            cell = Cell.objects.get(sheet_id=sheet, cell_id__iexact=cell_id)
        except Cell.DoesNotExist:
            cell = Cell(cell_id=cell_id, sheet_id=sheet)
            cell.save()

        cell.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SheetList(viewsets.ViewSet):
    def get(self, request, sheet_id):
        sheet = get_object_or_404(Sheet, sheet_id__iexact=sheet_id)
        cell_data = {}
        cells = Cell.objects.filter(sheet_id=sheet)
        for cell in cells:
            cell_data[cell.cell_id] = {
                "value": cell.value,
                "result": cell.result
            }
        return Response(cell_data, status=status.HTTP_200_OK)

    def delete(self, request, sheet_id):
        sheet = get_object_or_404(Sheet, sheet_id__iexact=sheet_id)
        sheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)