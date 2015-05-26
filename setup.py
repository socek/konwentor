# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'hatak==0.2.7.11',
    'hatak_logging',
    'hatak_jinja2==0.2',
    'hatak_haml',
    'hatak_sql>=0.1.16',
    'hatak_alembic>=0.1.3',
    'hatak_beaker',
    'hatak_debugtoolbar',
    'hatak_statics',
    'hatak_formskit==0.2.3.7',
    'hatak_flashmsg',
    'waitress',
    'uwsgi',
    'pytest',
    'pytest-cov',
    'hatak_auth>=0.2.6',
    'ipdb',
    'psycopg2',
]
prefix = 'https://github.com/socek/'
dependency_links = [
    # unhash this if you want lates version
    # prefix + 'hatak/tarball/master#egg=hatak-0.2.7.11',
    # prefix + 'hatak_auth/tarball/master#egg=hatak_auth-0.2.6',
    # prefix + 'hatak_jinja2/tarball/master#egg=hatak_jinja2-0.2',
    # prefix + 'hatak_formskit/tarball/master#egg=hatak_formskit-0.2.3.7',
    # prefix + 'hatak_sql/tarball/master#egg=hatak_sql-0.1.16',
]

if __name__ == '__main__':
    setup(name='Konwentor',
          version='0.2.4',
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
