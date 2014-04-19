phdb README

1. append to c:\Python27\Lib\site-packages\pyramid-1.1-py2.7.egg\pyramid\scaffolds\__init__.py

class MakoRoutesAlchemyProjectTemplate(PyramidTemplate):
    _template_dir = 'mytemplate'
    summary = 'pyramid SQLAlchemy project using url dispatch (no traversal) and mako as templating engine'
    template_renderer = staticmethod(paste_script_template_renderer)

2. change c:\Python27\Lib\site-packages\pyramid-1.1-py2.7.egg\pyramid\scaffolds\tests.py

templates = ['pyramid_starter', 'pyramid_alchemy', 'pyramid_routesalchemy', 'pyramid_mytemplate',]

3. c:\Python27\Lib\site-packages\pyramid-1.1-py2.7.egg\EGG-INFO\entry_points.txt

pyramid_mytemplate=pyramid.scaffolds:MakoRoutesAlchemyProjectTemplate




