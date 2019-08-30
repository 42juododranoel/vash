import os
import sys
import gettext
from argparse import ArgumentParser
from functools import partial
from subprocess import check_call

_ = gettext.gettext


class Project:
    SERVICE_NAMES = ('bundler', 'engine', 'proxy')
    
    def __init__(self, name):
        self.name = name

        # ~/projects/vash/manage.py
        self.manage_file_path = os.path.abspath(__file__)
        # ~/projects/vash
        self.repository_folder_path = os.path.sep.join(
            self.manage_file_path.split(os.path.sep)[:-1]
        )
        # ~/projects
        self.projects_folder_path = os.path.sep.join(
            self.repository_folder_path.split(os.path.sep)[:-1]
        )
        # ~/projects/{name}
        self.project_folder_path = f'{self.projects_folder_path}/{name}'

        # ~/projects/{name}/versions
        self.versions_folder_path = f'{self.project_folder_path}/versions'
        # ~/projects/{name}/versions/rolling -> ~/projects/vash
        self.rolling_version_path = f'{self.versions_folder_path}/rolling'

        # ~/projects/{name}/resources
        self.resources_folder_path = f'{self.project_folder_path}/resources'
        # ~/projects/{name}/resources/{resource}
        self.resource_folder_paths = {
            'assets': f'{self.resources_folder_path}/assets',
            'certificates': f'{self.resources_folder_path}/certificates',
            'files': f'{self.resources_folder_path}/files',
            'pages': f'{self.resources_folder_path}/pages',
            'scripts': f'{self.resources_folder_path}/scripts',
            'styles': f'{self.resources_folder_path}/styles',
            'templates': f'{self.resources_folder_path}/templates',

        }
        # ~/projects/{name}/resources/pages/_html
        self.html_pages_folder_path = f'{self.resource_folder_paths["pages"]}/_html'

        self.version: str
        self.version_folder_path: str
        
        self.environment: dict

    def set_version(self, version):
        self.version = version
        self.version_folder_path = f'{self.versions_folder_path}/{version}'

    def set_environment(self):
        print('Creating environment...')

        environment_variables = {
            'USER_ID': f'{os.getuid()}',
            'PROJECT_FOLDER': f'{self.version_folder_path}',
            'RESOURCES_FOLDER': f'{self.resources_folder_path}',
        }

        for service_name in self.SERVICE_NAMES:
            variable_name = f'DOCKER_{service_name.upper()}_IMAGE'
            variable_value = f'{self.name}_{service_name}:{self.version}'
            environment_variables[variable_name] = variable_value

        for resource_name, resource_folder_path in self.resource_folder_paths.items():
            variable_name = f'{resource_name.upper()}_FOLDER'
            environment_variables[variable_name] = f'{resource_folder_path}'
        
        self.environment = environment_variables 
        for variable_name, variable_value in self.environment.items():
            print(f'  “{variable_name}” = “{variable_value}”')
            os.environ[variable_name] = variable_value
        print()

    def initialize(self):
        print(f'Initializing project “{self.name}”...')
        self.create_folders()
        self.create_rolling()
        print()
    
    def run(self, version, as_daemon=False):
        print(f'Running project “{self.name}”...')
        self.set_version(version)
        self.set_environment()
        self.run_project(as_daemon)
        print()
    
    def create_folders(self):
        print('Creating folders...')

        folder_paths = [
            self.project_folder_path,
            self.versions_folder_path,
            self.resources_folder_path,
        ]
        for folder_path in folder_paths:
            print(f'  “{folder_path}”')
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)

        for resource_name, resource_folder_path in self.resource_folder_paths.items():
            print(f'  “{resource_folder_path}”')
            if not os.path.isdir(resource_folder_path):
                os.makedirs(resource_folder_path)
        else:
            print()

    def create_rolling(self):
        print('Creating rolling version folder...')
        if not os.path.islink(self.rolling_version_path):
            print(f'  “{self.rolling_version_path}”')
            print(f'   -> “{self.repository_folder_path}”')
            os.symlink(self.repository_folder_path, self.rolling_version_path, target_is_directory=True)
        else:
            print('  Exists.')
        print()
    
    def run_project(self, as_daemon=False):
        print(f'Running project...')
    
        command = [
            'docker-compose',
                '-f', f'{self.version_folder_path}/compose/engine.yml',
                '-f', f'{self.version_folder_path}/compose/proxy.yml',
                '-f', f'{self.version_folder_path}/compose/bundler.yml',
                '--project-directory', f'{self.version_folder_path}',
                '--project-name', f'{self.name}',
                'up',
                '--build',
        ]
        if as_daemon:
            command.append('--detach')
        check_call(command)
        print()

    def create_index_page(self):
        print('Creating index page...')
        
        if not os.path.isdir(self.html_pages_folder_path):
            os.makedirs(self.html_pages_folder_path)
        page_path = f'{self.html_pages_folder_path}/index.html'
        if not os.path.isfile(page_path):
            page_content = (
                '<!DOCTYPE html>'
                '<html>'
                '  <head>'
                '    <meta charset="utf-8">'
                '     <title>Test</title>'
                '  </head>'
                '  <body>'
                '    <p>Test</p>'
                '  </body>'
                '</html>'
            )
            with open(page_path, 'w') as file:
                file.write(page_content)
            print('  Done.')
        else:
            print('  Exists.')
        print()


def initialize_project(name):
    project = Project(name)
    project.initialize()


def run_project(name, version, as_daemon=False):
    project = Project(name)
    project.run(version, as_daemon)


def get_command(argv):
    category_parser = ArgumentParser()
    category_parser.add_argument('category')
    namespace, arguments = category_parser.parse_known_args(argv[1:])

    if namespace.category == 'initialize':
        argument_parser = ArgumentParser()
        argument_parser.add_argument('name', help=_('Project name.'))
        command_function = initialize_project

    elif namespace.category == 'run':
        argument_parser = ArgumentParser()
        argument_parser.add_argument('name', help=_('Project name.'))
        argument_parser.add_argument('version', help=_('Project version.'))
        argument_parser.add_argument(
            '-d', '--daemon', dest='as_daemon', 
            action='store_true', help=_('Enter daemon mode after start.')
        )
        command_function = run_project

    else:
        raise SystemExit(_(f'Unknown command category {namespace.category}.'))

    command_arguments = argument_parser.parse_args(arguments)
    return partial(command_function, **vars(command_arguments))


if __name__ == '__main__':
    command = get_command(sys.argv)
    command()
