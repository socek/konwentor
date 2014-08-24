# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'sqlalchemy-migrate',
    'hatak==0.1.2',
    'waitress',
    'pyramid_debugtoolbar',
    'pyramid_beaker',
    'pyramid_jinja2',
    'psycopg2',
    'formskit==0.4.1',
    'uwsgi',
    'soktest',
    'toster',
    'coverage',
]
dependency_links = [

]

if __name__ == '__main__':
    setup(name='Konwentor',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'': 'src'},
          install_requires=install_requires,
          dependency_links=dependency_links,
          include_package_data=True,
          entry_points=(
              '\n'.join([
                        '[paste.app_factory]',
                        'main = konwentor.application.init:main',
                        '[console_scripts]',
                        'tests = konwentor.application.tests.runner:run',
                        ''])
          ),
          )
