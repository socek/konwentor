# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'hatak==0.2.7.8',
    'waitress',
    'psycopg2',
    'uwsgi',
    'coverage',

    'hatak_logging',
    'hatak_jinja2',
    'hatak_haml',
    'hatak_sql>=0.1.6',
    'hatak_alembic',
    'hatak_beaker',
    'hatak_debugtoolbar',
    'hatak_statics>=0.2.3',
    'hatak_formskit>=0.2.3.1',
    'hatak_flashmsg',
    'hatak_auth>=0.2.2.1',
    'pytest',
    'pytest-cov',
]
dependency_links = [

]

if __name__ == '__main__':
    setup(name='Konwentor',
          version='0.2.2.1',
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
                        'konwentor_manage = konwentor.application.manage:run',
                        ''])
          ),
          )
