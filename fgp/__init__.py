from django.db.models.base import ModelBase
from django.contrib.admin.options import BaseModelAdmin

class InvalidPermissionName(Exception):
    """
    Exception that occurs when a cls allready has an attribute by the name of
    the permission.
    """

_permissions = set()

class guard(object):
    """A decorator to add some permissions to something"""
    
    def __init__(self, *args, **kwargs):
        self.field_names = args
        self.permission_name = kwargs.get('name', None)
    
    def __call__(self, cls):

        permission_name = self.permission_name or \
            "fgp_%s" % cls._meta.verbose_name.replace(' ', '_')
        permission_description = "Can edit %s" % \
            " ".join(map(str.lower, self.field_names))
        
        cls._meta.permissions.append(
            (permission_name,
            permission_description)
        )
        if hasattr(cls, permission_name):
            raise InvalidPermissionName(
                "Can not use %s as permission name, because\
                 %s allready has that as an atribute"
            )
            
        _permissions.add(permission_name)
        
        guarded_field_name_set = set(self.field_names)
        
        setattr(cls, permission_name, guarded_field_name_set)
        
        return cls        

class enforce(object):
    """
    Enforce the permissions set by guard for some ModelAdmin.
    """
    def __new__(typ, model_or_admin=None, cls=None, attrs=None):
        obj = object.__new__(typ)
        
        if isinstance(model_or_admin, ModelBase):
            obj.model = model_or_admin
        elif issubclass(model_or_admin, BaseModelAdmin):
            if hasattr(model_or_admin, 'model'):
                obj.model = model_or_admin.model
                admin_class = model_or_admin
            else:
                raise(AttributeError("%s is neither a model nor a ModelAdmin" % model_or_admin.__name__))
        else:
            raise TypeError("enforce can not accept parameters of type %s" % model_or_admin.__name__)
            
        if cls:                    
            admin_class = type(obj.model.__name__ + cls.__name__, (cls,), attrs or {'model':obj.model})
        
        if admin_class:
            return obj.__call__(admin_class)
            
        return obj
        
    def __call__(self, cls):
        cls_permissions = []
        for permission in _permissions:
            if hasattr(cls.model, permission):
                cls_permissions.append(permission)
        
        def get_readonly_fields(self, request, obj=None):
            guarded_field_name_list = []
            for permisson_name in cls_permissions:
                if not request.user.has_perm(permisson_name):
                    guarded_field_name_list.extend(getattr(cls.model, permisson_name, []))
            
            return set(self.readonly_fields).union(set(guarded_field_name_list))

        cls.get_readonly_fields = get_readonly_fields
        
        return cls