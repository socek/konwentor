# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'hatak==0.1.3',
    'waitress',
    'pyramid_debugtoolbar',
    'pyramid_beaker',
    'pyramid_jinja2',
    'psycopg2',
    'formskit==0.4.1',
    'uwsgi',
    'soktest',
    'coverage',
    'alembic',
    'pyyaml',
    'Hamlish-Jinja',
]
dependency_links = [

]

if __name__ == '__main__':
    setup(name='Konwentor',
          version='0.2',
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
                        'hatak_tests = konwentor.application.tests.runner:run',
                        'hatak_alembic = konwentor.application.alembic:run'
                        ''])
          ),
          )
