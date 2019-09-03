import os
import sys
import json
from time import sleep
from gettext import gettext as _
from argparse import ArgumentParser
from functools import partial
from subprocess import check_call, CalledProcessError

PORT_FORWARDING = [
    ['80', '443'],
    ['10080', '10443'],
    ['20080', '20443'],
]


def create_port_forwarding(source, destination):
    command = 'sudo iptables ' \
        '-t nat ' \
        '-A PREROUTING ' \
        '-i eth0 ' \
        '-p tcp ' \
        f'--destination-port {source} ' \
        '-j REDIRECT ' \
        f'--to-port {destination}'
    check_call(command, shell=True)


def delete_port_forwarding(source, destination):
    command = 'sudo iptables ' \
        '-t nat ' \
        '-D PREROUTING ' \
        '-i eth0 ' \
        '-p tcp ' \
        f'--destination-port {source} ' \
        '-j REDIRECT ' \
        f'--to-port {destination}'
    check_call(command, shell=True)


def purge_release(name, version):
    commands = [
        ['docker', 'stop', f'{name}_{version}_proxy_1'],
        ['docker', 'rm', f'{name}_{version}_proxy_1'],
        ['docker', 'rmi', f'{name}_proxy:{version}'],
        ['docker', 'network', 'rm', f'{name}_{version}_default']
    ]
    for command in commands:
        try:
            check_call(command)
        except CalledProcessError:
            pass


def get_opposite_port(port):
    # 10080 -> 20080
    if port == PORT_FORWARDING[1][0]:
        return PORT_FORWARDING[2][0]
    # 10443 -> 20443
    elif port == PORT_FORWARDING[1][1]:
        return PORT_FORWARDING[2][1]
    # 20080 -> 10080
    elif port == PORT_FORWARDING[2][0]:
        return PORT_FORWARDING[1][0]
    # 20443 -> 10443
    else:
        return PORT_FORWARDING[1][1]


class Project:
    REPOSITORY_URL = 'https://github.com/vsevolod-skripnik/vash.git'
    SERVICE_NAMES = ['bundler', 'engine', 'proxy']
    REGISTRY_ENTRIES_MAX_COUNT = 10

    def __init__(self, name: str):
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

        # ~/projects/{name}/registry.json
        self.registry_path = f'{self.project_folder_path}/registry.json'

    def prepare_registry(self):
        print(_('Preparing registry...'))
        if not os.path.isfile(self.registry_path):
            print(f'Create “{self.registry_path}”')
            with open(self.registry_path, 'w') as file:
                file.write('[]')

    def prepare_folders(self):
        print(_('Preparing folders...'))

        folder_paths = [
            self.project_folder_path,
            self.versions_folder_path,
            self.resources_folder_path,
        ]
        for folder_path in folder_paths:
            if not os.path.isdir(folder_path):
                print(_(f'Create “{folder_path}”'))
                os.makedirs(folder_path)

        for resource_name, resource_folder_path in self.resource_folder_paths.items():
            if not os.path.isdir(resource_folder_path):
                print(_(f'Create “{resource_folder_path}”'))
                os.makedirs(resource_folder_path)

    def read_registry(self):
        with open(self.registry_path, 'r') as file:
            return json.load(file)

    def write_registry(self, entries):
        with open(self.registry_path, 'w') as file:
            json.dump(entries, file)

    def update_registry(self, version, options):
        entries = self.read_registry()

        entry = {'version': version, 'options': options}
        entries.insert(0, entry)
        if len(entries) > self.REGISTRY_ENTRIES_MAX_COUNT:
            del entries[self.REGISTRY_ENTRIES_MAX_COUNT - 1:]

        self.write_registry(entries)

    def _get_run_options_for_latest(self):
        options = {
            'service_names': self.SERVICE_NAMES,
            'as_daemon': False,
            'no_build': False,
            'runtime_environment': {
                'PROXY_PORT_80': PORT_FORWARDING[0][0],
                'PROXY_PORT_443': PORT_FORWARDING[0][1],
            }
        }
        return options

    def _get_run_options_for_previous(self):
        registry_entries = self.read_registry()
        if not registry_entries:
            raise SystemError(_('No previous version, because registry is empty.'))
        else:
            options = registry_entries[1]['options']
            version = registry_entries[1]['version']
        return version, options

    def _get_run_options_for_version(self):
        options = {
            'service_names': ['proxy'],
            'as_daemon': True,
            'no_build': True,
        }

        registry_entries = self.read_registry()
        # If registry is empty, run on port 10080
        if not registry_entries:
            options['runtime_environment'] = {
                'PROXY_PORT_80': PORT_FORWARDING[1][0],
                'PROXY_PORT_443': PORT_FORWARDING[1][1],
            }
        else:
            # If previous release was running on 10080, run current on 20080
            if registry_entries[0]['options']['runtime_environment']['PROXY_PORT_80'] == PORT_FORWARDING[1][0]:
                options['runtime_environment'] = {
                    'PROXY_PORT_80': PORT_FORWARDING[2][0],
                    'PROXY_PORT_443': PORT_FORWARDING[2][1],
                }
            # Otherwise run on 10080
            else:
                options['runtime_environment'] = {
                    'PROXY_PORT_80': PORT_FORWARDING[1][0],
                    'PROXY_PORT_443': PORT_FORWARDING[1][1],
                }

        return options

    def _install_latest(self, release):
        if not os.path.islink(release.folder_path):
            os.symlink(self.repository_folder_path, release.folder_path, target_is_directory=True)

    def _install_version(self, release):
        if not os.path.isdir(release.folder_path):
            working_folder_before_install = os.getcwd()

            os.chdir(self.versions_folder_path)
            command = ['git', 'clone', f'{self.REPOSITORY_URL}', f'{release.version}']
            check_call(command)

            os.chdir(release.folder_path)
            command = ['git', 'checkout', f'{release.folder_path}']
            check_call(command)

            command = ['git', 'reset', '--hard']
            check_call(command)

            os.chdir(working_folder_before_install)

    def run_release(self, version: str):
        print(_(f'Preparing release “{version}”...'))

        if version == 'latest':
            release = Release(project=self, version=version)
            self._install_latest(release)
            options = self._get_run_options_for_latest()
            release.run(**options)

        else:
            # Version is like “ec45d12”
            release = Release(project=self, version=version)
            self._install_version(release)
            options = self._get_run_options_for_version()
            release.run(**options)
            self.update_registry(version, options)

        return release, options

    def restore_previous_release(self, service_names):
        print(_('Starting release...'))
        version, options = self._get_run_options_for_previous()
        release = Release(project=self, version=version)
        release.start(service_names)
        self.update_registry(version, options)
        return release, options

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
                '     <title>Test title</title>'
                '  </head>'
                '  <body>'
                '    <p>Test paragraph</p>'
                '  </body>'
                '</html>'
            )
            with open(page_path, 'w') as file:
                file.write(page_content)

    def test_page(self, url: str):
        print(_(f'Testing index page...'))

        import requests
        requests.packages.urllib3.disable_warnings()

        max_tries = 3
        for try_ in range(max_tries):
            try:
                response = requests.get(url, verify=False)
            except requests.exceptions.ConnectionError:
                print(_('Fail. Sleep 5 seconds...'))
                sleep(5)
            else:
                if response.status_code == 200:
                    print(_('Fine.'))
                    return True
                else:
                    print(_(f'Failed with status code {response.status_code}.'))
                    return False
        else:
            print(_('Max tries exceeded.'))
            return False

    @staticmethod
    def get_production_credentials():
        credentials = {
            'host': os.environ.get('PRODUCTION_HOST') or input(_('Production host: ')),
            'username': os.environ.get('PRODUCTION_USERNAME') or input(_('Production username: ')),
        }
        return credentials

    def save_image(self, version, service_name):
        print(_('Saving image...'))

        image_name = f'{self.name}_{service_name}:{version}'
        image_file = f'{self.name}_{service_name}_{version}.tar'
        image_path = f'/tmp/{image_file}'

        command = ['docker', 'save', '-o', f'{image_path}', f'{image_name}']
        check_call(command)
        return image_path

    def send_image(self, image_path):
        print(_('Sending image...'))

        credentials = self.get_production_credentials()
        file_name = image_path.split(os.path.sep)[-1]
        production_folder_path = '/tmp'
        command = ['scp', f'{image_path}', f'{credentials["username"]}@{credentials["host"]}:{production_folder_path}']
        check_call(command)
        return f'{production_folder_path}/{file_name}'

    @staticmethod
    def load_image(image_path):
        print(_('Loading image...'))
        command = ['docker', 'load']
        with open(image_path) as file:
            check_call(command, stdin=file)

    def update_production(self, version):
        print(_('Updating production...'))
        credentials = self.get_production_credentials()
        production_manage_file_path = os.environ.get('PRODUCTION_MANAGE_FILE_PATH') \
            or input('Path to `manage.py` on production: ')

        command = [
            'ssh', f'{credentials["username"]}@{credentials["host"]}',
            'python3', production_manage_file_path, 'update', self.name, version
        ]
        check_call(command)


class Release:
    def __init__(self, project: Project, version: str):
        self.project = project
        self.version = version
        self.folder_path = f'{self.project.versions_folder_path}/{version}'
        self.environment = self.get_environment()

    def get_environment(self):
        print(_(f'Getting general environment...'))

        environment_variables = {
            'USER_ID': f'{os.getuid()}',
            'RESOURCES_FOLDER': f'{self.project.resources_folder_path}',
        }

        for resource_name, resource_folder_path in self.project.resource_folder_paths.items():
            variable_name = f'{resource_name.upper()}_FOLDER'
            environment_variables[variable_name] = f'{resource_folder_path}'

        return environment_variables

    def run(self, service_names: list, runtime_environment: dict, as_daemon: bool, no_build: bool):
        print(_(f'Getting runtime environment...'))
        for service_name in self.project.SERVICE_NAMES:
            variable_name = f'DOCKER_{service_name.upper()}_IMAGE'
            variable_value = f'{self.project.name}_{service_name}:{self.version}'
            runtime_environment[variable_name] = variable_value
        self.environment.update(runtime_environment)

        for variable_name, variable_value in self.environment.items():
            os.environ[variable_name] = variable_value

        print(_(f'Running release “{self.version}”...'))
        command = ['docker-compose']
        for service_name in (service_names or self.project.SERVICE_NAMES):
            command.extend(['-f', f'{self.folder_path}/compose/{service_name}.yml'])

        command.extend(
            [
                '--project-directory', f'{self.folder_path}',
                '--project-name', f'{self.project.name}_{self.version}',
                'up',
            ]
        )

        if not no_build:
            command.append('--build')
        if as_daemon:
            command.append('--detach')

        check_call(command)

    def _start_stop_remove(self, action, service_names):
        command = ['docker', action]
        for service_name in service_names:
            command.append(f'{self.project.name}_{self.version}_{service_name}_1')
        check_call(command)

    def start(self, service_names):
        print(_(f'Starting release...'))
        self._start_stop_remove(action='start', service_names=service_names)

    def stop(self, service_names):
        print(_(f'Stopping release...'))
        self._start_stop_remove(action='stop', service_names=service_names)

    def remove(self, service_names, with_image=True, with_network=True):
        print(_(f'Removing release...'))
        self._start_stop_remove(action='remove', service_names=service_names)

        if with_image:
            command = ['docker', 'rmi'],
            for service_name in service_names:
                command.append(f'{self.project.name}_{service_name}:{self.version}')
            check_call(command)

        if with_network:
            command = ['docker', 'network', 'rm', f'{self.project.name}_{self.version}_default']
            check_call(command)


def command_initialize_project(name):
    project = Project(name)
    project.prepare_folders()
    project.prepare_registry()
    return project


def command_run_release(name, version):
    project = command_initialize_project(name)
    release, options = project.run_release(version)
    return project, release, options


def command_deploy_release(name, version):
    project, release, options = command_run_release(name, version)

    project.create_index_page()
    url = f'https://127.0.0.1:{options["runtime_environment"]["PROXY_PORT_443"]}/'
    if project.test_page(url):
        image_path = project.save_image(version, service_name='proxy')
        project.send_image(image_path)
        purge_release(name, version)
    else:
        raise SystemError(_('Go check stuff.'))


def command_update_project(name, version):
    purge_release(name, version)  # Delete previous release with same version if exists

    image_path = f'/tmp/{name}_proxy_{version}.tar'
    Project.load_image(image_path)

    project, release, options = command_run_release(name, version)

    project.create_index_page()
    url = f'https://127.0.0.1:{options["runtime_environment"]["PROXY_PORT_443"]}/'
    if project.test_page(url):
        print('Forwarding ports...')

        create_port_forwarding('80', options["runtime_environment"]["PROXY_PORT_80"])
        create_port_forwarding('443', options["runtime_environment"]["PROXY_PORT_443"])

        registry_entries = project.read_registry()

        # If not first launch
        is_first_launch = len(registry_entries) > 1
        if is_first_launch:
            delete_port_forwarding('80', get_opposite_port(options["runtime_environment"]["PROXY_PORT_80"]))
            delete_port_forwarding('443', get_opposite_port(options["runtime_environment"]["PROXY_PORT_443"]))

        url = f'https://127.0.0.1/'
        # if project.test_page(url):
        if True:
            # If previous release is unknown
            print('Cleaning previous releases...')
            if not is_first_launch:
                previous_release_entry = registry_entries[1]
                previous_release = Release(project, previous_release_entry['version'])
                previous_release.stop(service_names=['proxy'])
                
                try:
                    pre_previous_release_entry = registry_entries[2]
                except IndexError:
                    pass  # Do nothing if pre-previous release is unknown
                else:
                    pre_previous_release = Release(project, pre_previous_release_entry['version'])
                    pre_previous_release.remove(service_names=['proxy'], with_image=True, with_network=True)

            print(_('Removing image...'))
            os.remove(image_path)

            print(_('Done.'))
            print(_(':-)'))
        else:
            if is_first_launch:
                print(_('Restoring previous release...'))

                release, options = project.restore_previous_release(service_names=['proxy'])

                create_port_forwarding('80', options["runtime_environment"]["PROXY_PORT_80"])
                create_port_forwarding('443', options["runtime_environment"]["PROXY_PORT_443"])

                delete_port_forwarding('80', get_opposite_port(options["runtime_environment"]["PROXY_PORT_80"]))
                delete_port_forwarding('443', get_opposite_port(options["runtime_environment"]["PROXY_PORT_443"]))

                raise SystemError(_('Previous release restored. Go check stuff.'))
            else:
                raise SystemError(_('No previous release to restore. Go check stuff.'))
    else:
        registry_entries = project.read_registry()
        del registry_entries[0]
        project.write_registry(registry_entries)
        raise SystemError(_('Go check stuff.'))


def get_command(argv):
    category_parser = ArgumentParser()
    category_parser.add_argument('category')
    namespace, arguments = category_parser.parse_known_args(argv[1:])

    argument_parser = ArgumentParser()
    argument_parser.add_argument('name', help=_('Project name.'))

    if namespace.category == 'initialize':
        command_function = command_initialize_project

    elif namespace.category in ('run', 'deploy', 'update'):
        argument_parser.add_argument('version', help=_('Project version.'))
        command_switch = {
            'run': command_run_release,
            'deploy': command_deploy_release,
            'update': command_update_project,
        }
        command_function = command_switch[namespace.category]

    else:
        raise SystemExit(_(f'Unknown command category {namespace.category}.'))

    command_arguments = argument_parser.parse_args(arguments)
    return partial(command_function, **vars(command_arguments))


if __name__ == '__main__':
    command = get_command(sys.argv)
    command()
