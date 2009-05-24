from models import Attribute, DynamicTypeField

# Add fields to the Attribute model based on the columns used by dynamic models.
# Fields added through the admin at runtime will get dynamically added (see
# DynamicTypeField's save() function), so this only needs to run once at server/
# python initialization
columns = DynamicTypeField.objects.distinct('column').values_list('column', 'value_type')
for column, value_type in columns:
    field = DynamicTypeField.get_field_for_type(column, column, value_type)
    Attribute.add_to_class(column, field)