from rest_framework.fields import ListField


class CommaSeparatedListField(ListField):
    def to_internal_value(self, data):
        normalized_data = []

        if isinstance(data, str):
            data = [data]

        if isinstance(data, list):
            for item in data:
                normalized_data.extend(item.strip() for item in str(item).split(","))

        return super().to_internal_value(normalized_data)
