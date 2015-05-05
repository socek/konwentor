# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'hatak==0.2.7.10',
    'hatak_logging',
    'hatak_jinja2==0.2',
    'hatak_haml',
    'hatak_sql>=0.1.15',
    'hatak_alembic>=0.1.3',
    'hatak_beaker',
    'hatak_debugtoolbar',
    'hatak_statics',
    'hatak_formskit==0.2.3.6',
    'hatak_flashmsg',
    'waitress',
    'uwsgi',
    'pytest',
    'pytest-cov',
    'hatak_auth>=0.2.5',
    'ipdb',
    'psycopg2',
]
dependency_links = [
    'https://github.com/socek/hatak_auth/tarball/master#egg=hatak_auth-0.2.5',
    'https://github.com/socek/hatak_jinja2/tarball/master#egg=hatak_jinja2-0.2',
    'https://github.com/socek/hatak_formskit/tarball/master#egg=hatak_formskit-0.2.3.6',
    'https://github.com/socek/hatak/tarball/master#egg=hatak-0.2.7.10',
]

if __name__ == '__main__':
    setup(name='Konwentor',
          version='0.2.3',
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
