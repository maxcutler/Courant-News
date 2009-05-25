from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from south.db import db

import copy

class DynamicType(models.Model):
    """
    A dynamically-defined customization of a model derived from
    DynamicModelBase. Consists of a collection of DynamicTypeFields which
    define the fields that are added to the model.
    """
    
    base = models.ForeignKey(ContentType)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    
    def __unicode__(self):
        return self.name

class DynamicTypeField(models.Model):
    """
    A single, dynamically-defined field for customizing a model.
    """
    
    TYPE_CHOICES = (
        (u'varchar', u'Short Text (less than 255 characters)'),
        (u'text', u'Long Text'),
        (u'int', u'Integer'),
        (u'bool', u'Flag (Boolean)'),
    )
    
    # be sure to specify default values
    TYPE_FIELDS = {
        'varchar': models.CharField(max_length=255, blank=True, null=True, default=None),
        'text': models.TextField(null=True, default=None),
        'int': models.IntegerField(null=True, default=None),
        'bool': models.BooleanField(default=False),
    }
    
    dynamic_type = models.ForeignKey(DynamicType)
    name = models.CharField(max_length=100,
                            help_text="Should be all-lowercase with no spaces (use underscores instead of spaces)")
    value_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    column = models.CharField(max_length=20, editable=False)
    
    def __unicode__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False):
        if not self.pk or self.value_type != DynamicTypeField.objects.get(pk=self.pk).value_type:
            # check column usage by finding what columns of this type are
            # already in use for this DynamicType. Since a field could have
            # been created and then subsequently deleted, there may be gaps,
            # and thus we must start at 01 and search until we find an unused
            # column name
            existing_names = DynamicTypeField.objects.filter(dynamic_type=self.dynamic_type,
                                                             value_type=self.value_type,
                                                             ).order_by("column").values_list("column", flat=True)
            i = 1
            while ("%s%02d" % (self.value_type, i)) in existing_names:
                i += 1
            cname = "%s%02d" % (self.value_type, i)
            
            if not hasattr(Attribute, cname):
                field = self.get_field_for_type(self.name, cname, self.value_type)
                # need to make a new column
                try:
                    db.add_column(Attribute._meta.db_table, cname, field)
                except:
                    # column may exist and Attribute model just doesn't have
                    # it stored as a model field because the column isn't actively
                    # used by any of the existing DynamicTypeFields
                    pass
                
                # add a model field to the Attribute model
                # this is replicated at server-start using introspection
                Attribute.add_to_class(cname, field)
            
            # Zero out the column data in case any junk remains
            # from a previous field using this column
            new_values = {cname: Attribute._meta.get_field(cname).default}
            ids = self.dynamic_type.base.model_class().objects.filter(dynamic_type=self.dynamic_type).values_list('pk', flat=True)
            Attribute.objects.filter(content_type=self.dynamic_type.base,
                                     object_id__in=ids).update(**new_values)

            self.column = cname

        super(DynamicTypeField, self).save(force_insert, force_update)
    
    @staticmethod
    def get_field_for_type(name, column, type):
        field = copy.deepcopy(DynamicTypeField.TYPE_FIELDS[type])
        field.name = name
        field.attname = name
        field.column = column
        return field
    
class Attribute(models.Model):
    """
    Represents the dynamically-defined fields' data for a given model instance.
    Columns are added to this model (and its database table) dynamically as
    required when new DynamicType/DynamicTypeFields are created.
    """
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together = ('content_type', 'object_id')
    
    def _unicode__(self):
        return u'Attr - CT: %d, ID: %d' % (self.content_type_id, self.object_id)
        
    def __init__(self, *args, **kwargs):
        # Add fields to the Attribute model based on the columns used by dynamic models.
        # Fields added through the admin at runtime will get dynamically added (see
        # DynamicTypeField's save() function), so this only needs to run once at server/
        # python initialization
        if not hasattr(Attribute, '_introspected_columns'):
            columns = DynamicTypeField.objects.distinct('column').values_list('column', 'value_type')
            for column, value_type in columns:
                field = DynamicTypeField.get_field_for_type(column, column, value_type)
                Attribute.add_to_class(column, field)
            setattr(Attribute, '_introspected_columns', True)
        super(Attribute, self).__init__(*args, **kwargs)


class DynamicModelBase(models.Model):
    """
    Base class for any model wishing to allow for dynamic customization
    through the admin interface.
    """
    
    dynamic_type = models.ForeignKey(DynamicType, null=True)
    
    class Meta:
        abstract = True
        
    def save(self, force_insert=False, force_update=False):
        # check for the existance of dynamic field attributes on the model
        # instance, which means that either one of the fields was accessed or
        # a value was set (without ever getting the value)
        if self.dynamic_type:
            dfields = DynamicTypeField.objects.filter(dynamic_type=self.dynamic_type)
            attrs = Attribute.objects.get(content_type=ContentType.objects.get_for_model(self),
                                              object_id=self.pk)
            for dfield in dfields:
                if hasattr(self, dfield.name):
                    setattr(attrs, dfield.column, getattr(self, dfield.name))   
            attrs.save()
        
        super(DynamicModelBase, self).save(force_insert, force_update)
        
    def __getattr__(self, name):
        # a model attribute was not found, so it could be an attempt to access
        # a dynamic type field. on the first time such a field is accessed,
        # we will store the values for all of the instance's dynamic fields
        # as attributes on the model instance (so that future accesses will
        # simply return the value without processing); the assumption is that
        # if one dynamic field is accessed, it is likely that another dynamic
        # field will be accessed in the lifetime of the model instance.
        if self.dynamic_type and not name.startswith('_'):            
            dfields = DynamicTypeField.objects.filter(dynamic_type=self.dynamic_type)
            if name in [field.name for field in dfields]:
                attrs = Attribute.objects.get(content_type=ContentType.objects.get_for_model(self),
                                              object_id=self.pk)
                for field in dfields:
                    setattr(self, field.name, getattr(attrs, field.column))
                    
                # now that all the dynamic fields have been stored on the instance,
                # we just call getattr again to get the value
                return getattr(self, name)
        
        # we're ignoring "private" variables that Django checks for (start with
        # underscore), as well as anything else if no dynamic type is set for
        # this model instance
        raise AttributeError
