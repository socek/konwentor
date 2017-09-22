from os import path

from baelfire.template import TemplateTask


class GeneratedOnceTemplateTask(TemplateTask):

    def __init__(self, *args, **kwargs):
        kwargs['check_template'] = False
        super().__init__(*args, **kwargs)


class InitPy(GeneratedOnceTemplateTask):
    path = '/templates/initpy'

    def get_template_path(self):
        return path.join('project/init.py.tpl')

    def get_output_file(self):
        return self.paths['project:initpy']


class PShell(GeneratedOnceTemplateTask):
    path = '/templates/pshell'

    def get_template_path(self):
        return path.join('project/pshell.py.tpl')

    def get_output_file(self):
        return self.paths['project:pshell']


class ManagePy(GeneratedOnceTemplateTask):
    path = '/templates/manage'

    def get_template_path(self):
        return path.join('project/manage.py.tpl')

    def get_output_file(self):
        return self.paths['project:managepy']


class Routes(GeneratedOnceTemplateTask):
    path = '/templates/routes'

    def get_template_path(self):
        return path.join('project/routes.py.tpl')

    def get_output_file(self):
        return self.paths['project:routes']


class Settings(GeneratedOnceTemplateTask):
    path = '/templates/settings'

    def get_template_path(self):
        return path.join('project/settings.py.tpl')

    def get_output_file(self):
        return self.paths['project:default']


class FrontendIni(TemplateTask):
    name = 'Creating frontend.ini file'
    path = '/frontend.ini'

    def generate_links(self):
        super().generate_links()
        self.add_link('bael.hatak.tasks:CreateDataDir')
        self.add_link('bael.hatak.tasks:BaelfireInitFile')

    def get_output_file(self):
        return self.paths['data:frontend.ini']

    def get_template_path(self):
        return 'frontend.ini.tpl'


class TestFixtures(GeneratedOnceTemplateTask):
    path = '/templates/testfixtures'

    def get_template_path(self):
        return path.join('project/fixtures.py.tpl')

    def get_output_file(self):
        return self.paths['application:fixtures']


class Conftest(GeneratedOnceTemplateTask):
    path = '/templates/conftest'

    def get_template_path(self):
        return path.join('project/conftest.py.tpl')

    def get_output_file(self):
        return self.paths['project:conftest']


class Pytestini(GeneratedOnceTemplateTask):
    path = '/templates/pytestini'

    def get_template_path(self):
        return path.join('project/pytest.ini.tpl')

    def get_output_file(self):
        return self.paths['project:pytestini']


class TestSettings(GeneratedOnceTemplateTask):
    path = '/templates/testsettings'

    def get_template_path(self):
        return path.join('project/testsettings.py.tpl')

    def get_output_file(self):
        return self.paths['project:testsettings']


class RedmeFile(GeneratedOnceTemplateTask):
    path = '/templates/readmefile'

    def get_template_path(self):
        return path.join('project/readme.txt.tpl')

    def get_output_file(self):
        return self.paths['readmefile']
