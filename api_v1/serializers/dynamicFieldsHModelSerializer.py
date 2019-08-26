from rest_framework.serializers import HyperlinkedModelSerializer


class DynamicFieldsHModelSerializer(HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsHModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
 
        if exclude is not None:
            # Drop any fields that are specified in the `exclude` argument.
            exclude = set(exclude)
            for field_name in exclude:
                self.fields.pop(field_name)
