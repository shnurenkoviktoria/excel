from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from excel.models import Sheet, Cell
from excel.serializers import SheetSerializer, CellSerializer, CellSerializerResult


class CellViewSetTests(APITestCase):
    def test_retrieve_cell(self):
        # Create a sheet and cell for testing
        sheet = Sheet.objects.create(sheet_id="test_sheet")
        cell = Cell.objects.create(sheet_id=sheet, cell_id="A1", value="42")

        url = reverse("cell-detail", args=["test_sheet", "A1"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CellSerializer(cell).data)

    def test_update_cell(self):
        # Create a sheet for testing
        sheet = Sheet.objects.create(sheet_id="test_sheet")

        data = {
            "cell_id": "A1",  # Provide a valid cell_id
            "value": "42"  # Replace with valid data
        }

        url = reverse("cell-detail", args=["test_sheet", "A1"])
        response = self.client.post(url, data, format="json")

        print(response.content.decode())  # Print the response content for debugging

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cell(self):
        # Create a sheet and cell for testing
        sheet = Sheet.objects.create(sheet_id="test_sheet")
        cell = Cell.objects.create(sheet_id=sheet, cell_id="A1")

        url = reverse("cell-detail", args=["test_sheet", "A1"])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cell.objects.filter(sheet_id=sheet, cell_id="A1").exists())

    def test_invalid_cell_id(self):
        # Create a sheet for testing
        sheet = Sheet.objects.create(sheet_id="test_sheet")

        data = {
            "cell_id": "123",  # Invalid cell_id
            "value": "42"
        }

        url = reverse("cell-detail", args=["test_sheet", "123"])
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SheetListTests(APITestCase):
    def test_get_sheet(self):
        # Create a sheet and cell for testing
        sheet = Sheet.objects.create(sheet_id="test_sheet")
        Cell.objects.create(sheet_id=sheet, cell_id="A1", value="42")

        url = reverse("sheet-list", args=["test_sheet"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {"A1": {"value": "42", "result": None}}
        self.assertEqual(response.data, expected_data)

    def test_delete_sheet(self):
        # Create a sheet for testing
        sheet = Sheet.objects.create(sheet_id="test_sheet")

        url = reverse("sheet-list", args=["test_sheet"])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Sheet.objects.filter(sheet_id="test_sheet").exists())

    def test_nonexistent_sheet(self):
        url = reverse("sheet-list", args=["nonexistent_sheet"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SheetSerializerTest(TestCase):
    def test_sheet_serializer(self):
        sheet_data = {"sheet_id": "test_sheet"}
        serializer = SheetSerializer(data=sheet_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_sheet_serializer(self):
        # Test with invalid data (missing 'sheet_id')
        sheet_data = {}
        serializer = SheetSerializer(data=sheet_data)
        self.assertFalse(serializer.is_valid())


class CellSerializerTest(TestCase):
    def test_cell_serializer(self):
        sheet = Sheet.objects.create(sheet_id="test_sheet")
        cell_data = {"cell_id": "A1", "value": "42", "sheet_id": sheet.id}
        serializer = CellSerializer(data=cell_data)
        self.assertTrue(serializer.is_valid())


class CellSerializerResultTest(TestCase):
    def test_cell_serializer_result(self):
        sheet = Sheet.objects.create(sheet_id="test_sheet")
        cell_data = {"cell_id": "A1", "value": "42", "sheet_id": sheet.id}
        serializer = CellSerializerResult(data=cell_data)
        self.assertTrue(serializer.is_valid())


class SheetModelTest(TestCase):
    def test_sheet_creation(self):
        sheet = Sheet.objects.create(sheet_id="test_sheet")
        self.assertEqual(sheet.sheet_id, "test_sheet")


class CellModelTest(TestCase):
    def test_cell_creation(self):
        sheet = Sheet.objects.create(sheet_id="test_sheet")
        cell = Cell.objects.create(cell_id="A1", value="42", sheet_id=sheet)
        self.assertEqual(cell.cell_id, "A1")
        self.assertEqual(cell.value, "42")
        self.assertEqual(cell.sheet_id, sheet)
