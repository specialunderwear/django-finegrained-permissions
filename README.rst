Django finegrained permissions
==============================

Add permissions per field instead of per model::

    from django.db import models
    from django.contrib import admin
    import fgp
    
    @fgp.guard('slave', 'master', name='can_edit_master_slave')
    class Harddisk(models.Model):
        type = models.CharField(max_length=255)
        slave = models.BooleanField(default=False)
        master = models.BooleanField(default=True)
    
    @fgp.enforce
    class HarddiskAdmin(admin.ModelAdmin)
        model = Harddisk
    
    admin.site.register(Harddisk, HarddiskAdmin)

or::

    admin.site.register(Harddisk, fgp.enforce(Harddisk, admin.ModelAdmin))

Note that you need to set ``model`` even when the admin class is not an inline admin.

To add permissions to admin settings execute::

    ./manage.py syncdb --all

