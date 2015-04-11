# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'hatak==0.2.7.9',
    'coverage',
    'hatak_logging',
    'hatak_jinja2',
    'hatak_haml',
    'hatak_sql>=0.1.13',
    'hatak_alembic>=0.1.2',
    'hatak_beaker',
    'hatak_debugtoolbar',
    'hatak_statics',
    'hatak_formskit>=0.2.3.4',
    'hatak_flashmsg',
    'waitress',
    'uwsgi',
    'pytest',
    'pytest-cov',
    'coverage==3.7.1',
    'hatak_auth>=0.2.2.2',
    'ipdb',
    'psycopg2',
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
