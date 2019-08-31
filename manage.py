import os
import sys
import json
from time import sleep
from getpass import getpass
from gettext import gettext as _
from argparse import ArgumentParser
from functools import partial
from subprocess import check_call

PROXY_PORTS = [
    {'PROXY_PORT_80': '10080', 'PROXY_PORT_443': '10443'},
    {'PROXY_PORT_80': '20080', 'PROXY_PORT_443': '20443'},
]
REPOSITORY_URL = 'https://github.com/vsevolod-skripnik/vash.git'


def get_production_credentials():
    credentials = {
        'host': os.environ.get('PRODUCTION_HOST', input('  Production host: ')),
        'username': os.environ.get('PRODUCTION_USERNAME', input('  Production username: ')),
    }
    if not os.environ.get('SSHPASS'):
        os.environ['SSHPASS'] = getpass('  Password: ')
    return credentials


def send_image(image_path):
    print(_('Sending image...'))

    credentials = get_production_credentials()
    file_name = image_path.split(os.path.sep)[-1]
    production_folder = '/tmp'
    command = [
        'sshpass', '-e',
        'scp', f'{image_path}', f'{credentials["username"]}@{credentials["host"]}:{production_folder}'
    ]
    check_call(command)
    return f'{production_folder}/{file_name}'


def load_image(image_path):
    print('Loading image...')
    command = ['docker', 'load']
    with open(image_path) as file:
        check_call(command, stdin=file)
    print()


def create_port_forwarding(port_80, port_443):
    command = ['sudo', 'iptables', '-A', 'PREROUTING', '-t', 'nat', '-i', 'eth0', '-p', 'tcp', '--dport', '80', '-j', 'REDIRECT', '--to-port', port_80]
    check_call(command)

    command = ['sudo', 'iptables', '-A', 'PREROUTING', '-t', 'nat', '-i', 'eth0', '-p', 'tcp', '--dport', '443', '-j', 'REDIRECT', '--to-port', port_443]
    check_call(command)


def delete_port_forwarding(port_80, port_443):
    command = ['sudo', 'iptables', '-D', 'PREROUTING', '-t', 'nat', '-i', 'eth0', '-p', 'tcp', '--dport', '80', '-j', 'REDIRECT', '--to-port', port_80]
    check_call(command)

    command = ['sudo', 'iptables', '-D', 'PREROUTING', '-t', 'nat', '-i', 'eth0', '-p', 'tcp', '--dport', '443', '-j', 'REDIRECT', '--to-port', port_443]
    check_call(command)


def switch_ports(current_80, current_443):
    if current_80 == PROXY_PORTS[0]['PROXY_PORT_80']:
        previous_80 = PROXY_PORTS[1]['PROXY_PORT_80']
        previous_443 = PROXY_PORTS[1]['PROXY_PORT_443']
    else:
        previous_80 = PROXY_PORTS[0]['PROXY_PORT_80']
        previous_443 = PROXY_PORTS[0]['PROXY_PORT_443']

    create_port_forwarding(current_80, current_443)
    delete_port_forwarding(previous_80, previous_443)


class Project:
    SERVICE_NAMES = ('bundler', 'engine', 'proxy')

    def __init__(self, name):
        print(_(f'Initializing project “{name}”...'))
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
        # ~/projects/{name}/versions/latest -> ~/projects/vash
        self.latest_version_path = f'{self.versions_folder_path}/latest'

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

        self.prepare_folders()

        self.version = 'latest'
        self.version_folder_path = f'{self.versions_folder_path}/{self.version}'
        if not os.path.islink(self.latest_version_path):
            print(_(f'  “{self.latest_version_path}”'))
            print(_(f'   -> “{self.repository_folder_path}”'))
            os.symlink(self.repository_folder_path, self.latest_version_path, target_is_directory=True)
        self.installed_versions = os.listdir(self.versions_folder_path)

        self.registry_path = f'{self.project_folder_path}/registry.json'
        if not os.path.isfile(self.registry_path):
            with open(self.registry_path, 'w') as file:
                file.write('[]')

        self.environment: dict

        self.proxy_port_80 = '80'
        self.proxy_port_443 = '443'

    def read_registry(self):
        with open(self.registry_path, 'r') as file:
            registry_entries = json.load(file)
        return registry_entries

    def update_registry(self, version, environment):
        entry = {'version': version, 'environment': environment}

        registry_entries_max_count = 10
        registry_entries = self.read_registry()
        registry_entries.insert(0, entry)
        if len(registry_entries) > registry_entries_max_count:
            del registry_entries[registry_entries_max_count - 1:]

        with open(self.registry_path, 'w') as file:
            json.dump(registry_entries, file)

    def prepare_folders(self):
        print(_('Preparing folders...'))

        folder_paths = [
            self.project_folder_path,
            self.versions_folder_path,
            self.resources_folder_path,
        ]
        for folder_path in folder_paths:
            if not os.path.isdir(folder_path):
                print(_(f'  “{folder_path}”'))
                os.makedirs(folder_path)

        for resource_name, resource_folder_path in self.resource_folder_paths.items():
            if not os.path.isdir(resource_folder_path):
                print(_(f'  “{resource_folder_path}”'))
                os.makedirs(resource_folder_path)
        else:
            print()

    def prepare_version(self, version):
        print(_(f'Preparing version “{version}”'))

        if version not in self.installed_versions:
            print('  Installing...')
            working_folder_before_install = os.getcwd()

            version_folder_path = f'{self.versions_folder_path}/{version}'

            os.chdir(self.versions_folder_path)
            command = ['git', 'clone', f'{REPOSITORY_URL}', f'{version}']
            check_call(command)

            os.chdir(version_folder_path)
            command = ['git', 'checkout', f'{version_folder_path}']
            check_call(command)

            command = ['git', 'reset', '--hard']
            check_call(command)

            os.chdir(working_folder_before_install)

            self.installed_versions.append(version)

        self.version = version
        self.version_folder_path = f'{self.versions_folder_path}/{version}'

        print()

    def prepare_environment(self):
        print('Preparing environment...')

        environment_variables = {
            'USER_ID': f'{os.getuid()}',
            'RESOURCES_FOLDER': f'{self.resources_folder_path}',
        }

        registry_entries = self.read_registry()
        try:
            current_proxy_port_80 = registry_entries[0]['environment']['PROXY_PORT_80']
        except (KeyError, IndexError):
            environment_variables.update(PROXY_PORTS[0])
        else:
            if current_proxy_port_80 == PROXY_PORTS[0]['PROXY_PORT_80']:
                environment_variables.update(PROXY_PORTS[1])
                self.proxy_port_80 = PROXY_PORTS[1]['PROXY_PORT_80']
                self.proxy_port_443 = PROXY_PORTS[1]['PROXY_PORT_443']
            else:
                environment_variables.update(PROXY_PORTS[0])
                self.proxy_port_80 = PROXY_PORTS[0]['PROXY_PORT_80']
                self.proxy_port_443 = PROXY_PORTS[0]['PROXY_PORT_443']

        for service_name in self.SERVICE_NAMES:
            variable_name = f'DOCKER_{service_name.upper()}_IMAGE'
            variable_value = f'{self.name}_{service_name}:{self.version}'
            environment_variables[variable_name] = variable_value

        for resource_name, resource_folder_path in self.resource_folder_paths.items():
            variable_name = f'{resource_name.upper()}_FOLDER'
            environment_variables[variable_name] = f'{resource_folder_path}'

        self.environment = environment_variables
        for variable_name, variable_value in self.environment.items():
            print(_(f'  “{variable_name}” = “{variable_value}”'))
            os.environ[variable_name] = variable_value
        print()

    def run(self, version, with_engine=True, with_proxy=True, with_bundler=True, as_daemon=False, no_build=False):
        self.prepare_version(version)
        self.prepare_environment()

        print(_(f'Running “{self.name}” version “{version}”...'))
        command = ['docker-compose']

        if with_engine:
            command.extend(['-f', f'{self.version_folder_path}/compose/engine.yml'])
        if with_proxy:
            command.extend(['-f', f'{self.version_folder_path}/compose/proxy.yml'])
        if with_bundler:
            command.extend(['-f', f'{self.version_folder_path}/compose/bundler.yml'])

        command.extend(
            [
                '--project-directory', f'{self.version_folder_path}',
                '--project-name', f'{self.name}',
                'up',
            ]
        )

        if not no_build:
            command.append('--build')
        if as_daemon:
            command.append('--detach')

        check_call(command)

        if as_daemon:
            registry_environment = {
                'PROXY_PORT_80': self.environment['PROXY_PORT_80'],
                'PROXY_PORT_443': self.environment['PROXY_PORT_443'],
            }
            self.update_registry(version=version, environment=registry_environment)

        print()

    def create_index_page(self):
        print(_('Creating index page...'))

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
            print(_('  Done.'))
        else:
            print(_('  Exists.'))
        print()

    def test_index_page(self):
        print(_(f'Testing index page...'))

        import requests
        requests.packages.urllib3.disable_warnings()

        url = f'https://127.0.0.1:{self.proxy_port_443}/'
        max_tries = 3
        for try_ in range(max_tries):
            try:
                response = requests.get(url, verify=False)
            except requests.exceptions.ConnectionError:
                print('  Fail. Sleep 5 seconds...')
                sleep(5)
            else:
                if response.status_code == 200:
                    message = 'Fine.'
                    is_fine = True
                    break
                else:
                    message = f'Oh no: {response.status_code}'
                    is_fine = False
                    break
        else:
            message = 'Max tries exceeded.'
            is_fine = False

        print(f'  {message}')
        print()
        return is_fine

    def save_image(self, service_name):
        print(_('Saving image...'))

        image_name = f'{self.name}_{service_name}:{self.version}'
        image_file = f'{self.version}.tar'
        image_path = f'/tmp/{image_file}'

        command = ['docker', 'save', '-o', f'{image_path}', f'{image_name}']
        check_call(command)
        print('  Done.')
        print()
        return image_path


def initialize_project(name):
    return Project(name)


def run_project(name, version, as_daemon):
    project = initialize_project(name)
    project.run(version, as_daemon=as_daemon)
    return project


def deploy_project(name, version):
    project = run_project(name, version, as_daemon=True)

    project.create_index_page()
    if project.test_index_page():
        image_path = project.save_image('proxy')
        send_image(image_path)
    else:
        raise SystemExit(_('Go check stuff.'))


def update_project(name, version):
    project = initialize_project(name)
    production_image_path = f'/tmp/{version}.tar'
    load_image(production_image_path)
    project.run(version, with_bundler=False, with_engine=False, no_build=True, as_daemon=True)

    if project.test_index_page():
        switch_ports(
            project.environment['PROXY_PORT_80'],
            project.environment['PROXY_PORT_443'],
        )
        if project.test_index_page():
            pass
        else:
            pass

    else:
        raise SystemExit(_('Go check stuff.'))


def get_command(argv):
    category_parser = ArgumentParser()
    category_parser.add_argument('category')
    namespace, arguments = category_parser.parse_known_args(argv[1:])

    argument_parser = ArgumentParser()
    argument_parser.add_argument('name', help=_('Project name.'))

    if namespace.category == 'initialize':
        command_function = initialize_project

    elif namespace.category in ('run', 'deploy', 'update'):
        argument_parser.add_argument(
            '-v', '--version', default='latest', help=_('Project version.')
        )

        if namespace.category == 'run':
            argument_parser.add_argument(
                '-d', '--daemon', dest='as_daemon',
                action='store_true', help=_('Enter daemon mode after start.')
            )
            command_function = run_project
        elif namespace.category == 'update':
            command_function = update_project
        else:
            command_function = deploy_project

    else:
        raise SystemExit(_(f'Unknown command category {namespace.category}.'))

    command_arguments = argument_parser.parse_args(arguments)
    return partial(command_function, **vars(command_arguments))


if __name__ == '__main__':
    command = get_command(sys.argv)
    command()


# vsevoland vsevoland = (root) NOPASSWD: /bin/bash /root/scripts/delete_port_forwarding_B.sh
