Django finegrained permissions
==============================

Add permissions per field instead of per model::

    from django.db import models
    from django.contrib import admin
    import fgp
    
    @fgp.guard('slave', name='can_edit_slave')
    class Harddisk(models.Model):
        type = models.CharField(max_length=255)
        slave = models.BooleanField(default=False)
    
    @fgp.enforce
    class HarddiskAdmin(admin.ModelAdmin)
        model = Harddisk
    
    admin.site.register(Harddisk, HarddiskAdmin)

or::

    admin.site.register(Harddisk, fgp.enforce(Harddisk, admin.ModelAdmin))