import re

from rest_framework import serializers

from excel.models import Cell


def result(value, sheet_id):
    if value.startswith("="):
        value = value[1:]
        operators = "+-*/() "
        result_start = value
        print(value)

        for el in value:
            if el.isalpha():
                parts = re.split(f"[{re.escape(operators)}]", value)
                var_value = []
                print(value)
                print(parts)
                for part in parts:
                    if part != "" and part[0].isalpha():
                        var_value.append(part)
                print(var_value)
                for el in var_value:
                    try:
                        cell = Cell.objects.get(cell_id=el, sheet_id_id=sheet_id)
                        print(cell.result)
                        if cell.result.isdigit():
                            result_start = result_start.replace(f"{el}", cell.result)
                        else:
                            raise serializers.ValidationError(
                                f"Cell with id {el} does not have a result"
                            )
                        print(result_start)
                    except Cell.DoesNotExist:
                        raise serializers.ValidationError(
                            f"Cell with id {el} does not exist in this sheet"
                        )
                print(result_start)
                result = eval(result_start)
                print(result)
                return str(result)

        try:
            result = eval(value)
            return str(result)
        except Exception as e:
            raise serializers.ValidationError(
                f"Error when calculating the expression: {str(e)}"
            )

    else:
        return value
