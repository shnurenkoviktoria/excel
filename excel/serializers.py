from rest_framework import serializers

from excel.models import Sheet, Cell


class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = ["sheet_id"]


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ["value", "cell_id"]

    def validate_cell_id(self, value):
        if value[0].isalpha() == False:
            raise serializers.ValidationError(
                "The name of the cell must start only with letters"
            )
        return value


class CellSerializerResult(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ["value", "result"]

