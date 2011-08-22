#!/usr/bin/env python
import os
import re
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

description="""Add permissions per field instead of per model::

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

Note that you need to set ``model`` even when the admin class is not an inline admin."""

version = '0.0.1'

for scheme in INSTALL_SCHEMES.values():
    scheme["data"] = scheme["purelib"]

setup(name='django-finegrained-permissions',
    version=version,
    description='Add permissions per field instead of per model',
    author='L. van de Kerkhof',
    author_email='fgp@permanentmarkers.nl',
    maintainer='L. van de Kerkhof',
    maintainer_email='fgp@permanentmarkers.nl',
    keywords='django model permission finegrained field',
    long_description=description,
    url='https://github.com/specialunderwear/django-finegrained-permissions',
    packages=['fgp'],
    platforms = "any",
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
