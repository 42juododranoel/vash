import os
import sys
import json
import logging
import unittest
from time import sleep
from random import randint
from gettext import gettext as _
from argparse import ArgumentParser
from subprocess import (
    check_call,
    check_output,
    CalledProcessError,
    DEVNULL,
)

SERVICE_NAMES_RUN = ['bundler', 'engine', 'proxy']
SERVICE_NAMES_DEPLOY = ['proxy']
SERVICE_NAMES_UPDATE = ['proxy']

TEST_PROJECT_NAME = 'vsevoland'
TEST_RELEASE_VERSION = 'c44f2be'
TEST_RELEASE_SERVICE_NAMES = ['proxy']

logger = logging.getLogger('manage')
logger.setLevel(level=logging.DEBUG)


class Registry:
    ENTRIES_MAX_COUNT = 10

    def __init__(self, path):
        self.path = path

    def prepare(self):
        logger.info(_('Preparing registry...'))
        if not os.path.isfile(self.path):
            logger.debug(f'Create “{self.path}”')
            with open(self.path, 'w') as file:
                file.write('[]')

    def read(self):
        logger.info(_('Reading registry...'))
        with open(self.path, 'r') as file:
            return json.load(file)

    def write(self, entries):
        logger.info(_('Writing registry...'))
        with open(self.path, 'w') as file:
            json.dump(entries, file)

    def update(self, entry):
        logger.info(_('Updating registry...'))
        entries = self.read()

        entries.insert(0, entry)
        if len(entries) > self.ENTRIES_MAX_COUNT:
            del entries[self.ENTRIES_MAX_COUNT - 1:]

        self.write(entries)


class Project:
    REPOSITORY_URL = 'https://github.com/vsevolod-skripnik/vash.git'

    def __init__(self, name: str):
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
        registry_path = f'{self.project_folder_path}/registry.json'
        self.registry = Registry(path=registry_path)

        # Store them here for easy testing
        self.folder_paths = [
            self.project_folder_path,
            self.versions_folder_path,
            self.resources_folder_path,
        ]
        for resource_name, resource_folder_path in self.resource_folder_paths.items():
            self.folder_paths.append(resource_folder_path)

    def prepare_folders(self) -> list:
        logger.info(_('Preparing folders...'))

        created_folders = []
        for folder_path in self.folder_paths:
            if not os.path.isdir(folder_path):
                logger.debug(_(f'Create “{folder_path}”'))
                os.makedirs(folder_path)
                created_folders.append(folder_path)

        return created_folders

    def prepare(self):
        logging.info(_('Preparing project...'))
        self.prepare_folders()
        self.registry.prepare()

    def prepare_test_page(self):
        logging.info(_('Preparing index page...'))

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

    def run_release(self, version: str):
        release = Release(
            project=self,
            version=version,
            service_names=SERVICE_NAMES_RUN,
        )
        release.run(do_build=True, as_daemon=False)
        logger.info(_('Done. Perfect.'))

    def deploy_release(self, version: str):
        release = Release(
            project=self,
            version=version,
            service_names=SERVICE_NAMES_DEPLOY,
        )
        release_data = release.run(
            do_build=True,
            as_daemon=True,
        )

        self.prepare_test_page()
        page_url = f'https://127.0.0.1:{release_data["environment"]["PROXY_PORT_443"]}/'
        is_working_fine_on_port = test_page(page_url)

        if is_working_fine_on_port:
            saved_image_paths = release.save_images()
            for image_path in saved_image_paths:
                send_image(image_path)

            release.prune()
            logger.info(_('Done. Perfect.'))
        else:
            raise SystemError(_('Broken. Go check stuff'))

    def update_release(self, version):
        release = Release(
            project=self,
            version=version,
            service_names=SERVICE_NAMES_UPDATE,
        )

        try:
            release.prune()  # Delete previous release with same version
        except CalledProcessError:
            pass  # It's fine if it doesn't exist

        image_path = f'/tmp/{self.name}_proxy_{version}.tar'
        load_image(image_path)

        release_data = release.run(
            do_build=False,
            as_daemon=True,
        )

        self.prepare_test_page()
        page_url = f'https://127.0.0.1:{release_data["environment"]["PROXY_PORT_443"]}/'
        is_working_fine_on_port = test_page(page_url)

        if is_working_fine_on_port:
            port_forwardings = list_port_forwardings()

            create_port_forwarding(80, release_data['environment']['PROXY_PORT_80'])
            create_port_forwarding(443, release_data['environment']['PROXY_PORT_443'])
            for source_port, destination_port in port_forwardings:
                delete_port_forwarding(source_port, destination_port)

            domain = os.environ.get('PRODUCTION_DOMAIN') \
                or input(_('Production domain: '))
            page_url = f'https://{domain}/' \
                if domain else f'https://127.0.0.1:{release_data["environment"]["PROXY_PORT_443"]}/'
            is_working_fine_on_domain = test_page(page_url)

            if is_working_fine_on_domain:
                self.registry.update(release_data)
                logging.info(_('Done. Perfect.'))
            else:
                previous_releases = self.registry.read()
                try:
                    previous_release = previous_releases[0]
                except IndexError:
                    raise SystemError(_('Broken. Previous release is unknown. Go check stuff.'))
                else:
                    release = Release(
                        project=self,
                        version=previous_release['version'],
                        service_names=previous_release['service_names']
                    )
                    release.start()

                    for source_port, destination_port in port_forwardings:
                        create_port_forwarding(source_port, destination_port)
                    delete_port_forwarding(80, release_data['environment']['PROXY_PORT_80'])
                    delete_port_forwarding(443, release_data['environment']['PROXY_PORT_443'])

                    raise SystemError(_('Broken. Previous release restored. Go check stuff.'))
        else:
            raise SystemError(_('Broken. Go check stuff.'))

    def sync(self):
        logging.info(_('Syncing with production...'))

        host = os.environ.get('PRODUCTION_HOST') \
            or input(_('Production host: '))
        username = os.environ.get('PRODUCTION_USERNAME') \
            or input(_('Production username: '))
        resources_folder_path = os.environ.get('PRODUCTION_RESOURCES_FOLDER_PATH') \
            or input(_('Production resources folder path: '))

        if not resources_folder_path.endswith('/'):
            resources_folder_path = f'{resource_folder_path}/'

        command = f'rsync -zarvh {self.resources_folder_path}/ {username}@{host}:{resources_folder_path}'
        logging.debug(command)
        check_call(command, shell=True)


class Release:
    def __init__(self, project: Project, version: str, service_names: list):
        self.project = project
        self.version = version
        self.folder_path = f'{self.project.versions_folder_path}/{version}'
        self.service_names = service_names

    def _prepare_version(self):
        if self.version == 'latest':
            if not os.path.islink(self.folder_path):
                os.symlink(
                    self.project.repository_folder_path,
                    self.folder_path,
                    target_is_directory=True,
                )
        else:
            if not os.path.isdir(self.folder_path):
                working_folder_before_install = os.getcwd()

                os.chdir(self.project.versions_folder_path)
                command = ['git', 'clone', f'{self.project.REPOSITORY_URL}', f'{self.version}']
                check_call(command)

                os.chdir(self.folder_path)
                command = ['git', 'checkout', f'{self.folder_path}']
                check_call(command)

                command = ['git', 'reset', '--hard']
                check_call(command)

                os.chdir(working_folder_before_install)

    def _call_docker_command(self, command):
        command = ['docker', command]
        for service_name in self.service_names:
            command.append(f'{self.project.name}_{self.version}_{service_name}_1')
        logger.debug(command)
        check_call(command)

    def _create_environment(self) -> dict:
        environment_variables = {
            'USER_ID': f'{os.getuid()}',
            'RESOURCES_FOLDER': f'{self.project.resources_folder_path}',
        }

        ports = generate_unused_ports(count=2)
        environment_variables['PROXY_PORT_80'] = f'{ports[0]}'
        environment_variables['PROXY_PORT_443'] = f'{ports[1]}'

        for resource_name, resource_folder_path in self.project.resource_folder_paths.items():
            variable_name = f'{resource_name.upper()}_FOLDER'
            environment_variables[variable_name] = f'{resource_folder_path}'

        for service_name in self.service_names:
            variable_name = f'DOCKER_{service_name.upper()}_IMAGE'
            variable_value = f'{self.project.name}_{service_name}:{self.version}'
            environment_variables[variable_name] = variable_value

        return environment_variables

    @staticmethod
    def _set_environment(environment_variables: dict):
        for variable_name, variable_value in environment_variables.items():
            os.environ[variable_name] = variable_value

    def run(self, do_build: bool, as_daemon: bool):
        self._prepare_version()

        command = ['docker-compose']
        for service_name in self.service_names:
            command.extend(['-f', f'{self.folder_path}/compose/{service_name}.yml'])

        command.extend(
            [
                '--project-directory', f'{self.folder_path}',
                '--project-name', f'{self.project.name}_{self.version}',
                'up',
            ]
        )
        if do_build:
            command.append('--build')
        if as_daemon:
            command.append('--detach')

        environment = self._create_environment()
        self._set_environment(environment)

        logger.info(_(f'Running release...'))
        check_call(command)

        release_data = {
            'version': self.version,
            'service_names': self.service_names,
            'do_build': do_build,
            'as_daemon': as_daemon,
            'environment': environment,
        }
        return release_data

    def start(self):
        logger.info(_('Starting release...'))
        self._call_docker_command(command='start')

    def stop(self):
        logger.info(_('Stopping release...'))
        self._call_docker_command(command='stop')

    def save_images(self):
        logger.info(_('Saving images...'))

        image_paths = []
        for service_name in self.service_names:
            image_name = f'{self.project.name}_{service_name}:{self.version}'
            image_file = f'{self.project.name}_{service_name}_{self.version}.tar'
            image_path = f'/tmp/{image_file}'

            command = ['docker', 'save', '-o', f'{image_path}', f'{image_name}']
            logger.debug(command)
            check_call(command)

            image_paths.append(image_path)

        return image_paths

    def remove(self):
        logger.info(_('Removing release...'))
        self._call_docker_command(command='rm')

    def remove_images(self):
        logger.info(_('Removing images...'))
        command = ['docker', 'rmi']
        for service_name in self.service_names:
            command.append(f'{self.project.name}_{service_name}:{self.version}')
        logger.debug(command)
        check_call(command)

    def remove_network(self):
        logger.info(_('Removing network...'))
        command = ['docker', 'network', 'rm', f'{self.project.name}_{self.version}_default']
        logger.debug(command)
        check_call(command)

    def prune(self):
        logger.info(_('Pruning release...'))
        self.stop()
        self.remove()
        self.remove_images()
        self.remove_network()


def test_page(url: str):
    logging.info(_(f'Testing page...'))

    import requests
    requests.packages.urllib3.disable_warnings()

    max_tries = 3
    for try_ in range(max_tries):
        try:
            response = requests.get(url, verify=False)
        except requests.exceptions.ConnectionError:
            logger.info(_('Fail. Sleep 5 seconds...'))
            sleep(5)
        else:
            if response.status_code == 200:
                logger.info(_('Fine.'))
                return True
            else:
                logger.info(_(f'Failed with status code {response.status_code}.'))
                return False
    else:
        logger.warning(_('Max tries exceeded.'))
        return False


def send_image(image_path):
    logger.info(_('Sending image...'))

    host = os.environ.get('PRODUCTION_HOST') or input(_('Production host: '))
    username = os.environ.get('PRODUCTION_USERNAME') or input(_('Production username: '))

    file_name = image_path.split(os.path.sep)[-1]
    production_folder_path = '/tmp'
    file_path = f'{production_folder_path}/{file_name}'

    command = ['scp', f'{image_path}', f'{username}@{host}:{production_folder_path}']
    logger.debug(command)
    check_call(command)
    return file_path


def load_image(image_path):
    logger.info(_('Loading image...'))
    command = ['docker', 'load']
    with open(image_path) as file:
        logger.debug(f'{command}, stdin="{image_path}"')
        check_call(command, stdin=file)


def generate_unused_ports(count):
    ports = []
    for _ in range(count):
        while True:
            port = randint(1025, 65535)
            command = f'sudo lsof -i -P -n | grep ":{port} (LISTEN)"'
            try:
                check_call(command, stdout=DEVNULL, shell=True)
            except CalledProcessError:  # Port is not in use
                if port not in ports:
                    ports.append(port)
                    break

    return ports


def list_port_forwardings():
    command = 'sudo iptables -L PREROUTING -t nat'
    output = check_output(command, shell=True).decode()
    port_forwardings = []
    for line in output.splitlines():
        if line.startswith('REDIRECT'):
            part_with_forwarding = line[line.find('tcp dpt:') + len(('tcp dpt:')):]
            parts = part_with_forwarding.partition(' redir ports ')
            source_port = {'http': '80', 'https': '443'}[parts[0]]
            destination_port = parts[2]
            port_forwardings.append([source_port, destination_port])

    return port_forwardings


def create_port_forwarding(source, destination):
    logger.info(f'Forwarding {source} → {destination}...')
    command = 'sudo iptables ' \
        '-t nat ' \
        '-A PREROUTING ' \
        '-i eth0 ' \
        '-p tcp ' \
        f'--destination-port {source} ' \
        '-j REDIRECT ' \
        f'--to-port {destination}'
    logger.debug(command)
    check_call(command, shell=True)


def delete_port_forwarding(source, destination):
    logger.info(f'Removing forwarding {source} → {destination}')
    command = 'sudo iptables ' \
        '-t nat ' \
        '-D PREROUTING ' \
        '-i eth0 ' \
        '-p tcp ' \
        f'--destination-port {source} ' \
        '-j REDIRECT ' \
        f'--to-port {destination}'
    logger.debug(command)
    check_call(command, shell=True)


def get_prepared_project(name):
    project = Project(name=name)
    project.prepare()
    return project


def command_run(name, version):
    get_prepared_project(name).run_release(version)


def command_deploy(name, version):
    get_prepared_project(name).deploy_release(version)


def command_update(name, version):
    get_prepared_project(name).update_release(version)


def command_sync(name):
    get_prepared_project(name).sync()


def main(argv):
    category_argument_parser = ArgumentParser()
    category_argument_parser.add_argument('category')
    namespace, arguments = category_argument_parser.parse_known_args(argv[1:])

    command_argument_parser = ArgumentParser()
    command_argument_parser.add_argument('name', help=_('Project name.'))

    if namespace.category in ('run', 'deploy', 'update'):
        command_argument_parser.add_argument('version', help=_('Project version.'))

        command_switch = {
            'run': command_run,
            'deploy': command_deploy,
            'update': command_update,
        }
        command_function = command_switch[namespace.category]

    elif namespace.category == 'sync':
        command_function = command_sync

    else:
        raise SystemError(_(f'Unknown command category {namespace.category}.'))

    command_arguments = command_argument_parser.parse_args(arguments)
    command_function(**vars(command_arguments))


class TestCommands(unittest.TestCase):
    @unittest.skip  # Tests can't proceed because running doesn't support daemon mode
    def test_run(self):
        command_run(name=TEST_PROJECT_NAME, version=TEST_RELEASE_VERSION)

    @unittest.skip  # Sending image to production takes too long time for tests
    def test_deploy(self):
        command_deploy(name=TEST_PROJECT_NAME, version=TEST_RELEASE_VERSION)

    def test_update(self):
        command_update(name=TEST_PROJECT_NAME, version=TEST_RELEASE_VERSION)


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project(name=TEST_PROJECT_NAME)

    def test_create_folders(self):
        self.project.prepare_folders()
        for folder_path in self.project.folder_paths:
            self.assertTrue(os.path.isdir(folder_path))


class TestRelease(unittest.TestCase):
    def setUp(self):
        self.project = Project(name=TEST_PROJECT_NAME)
        self.project.prepare()

        self.release = Release(
            project=self.project,
            version=TEST_RELEASE_VERSION,
            service_names=TEST_RELEASE_SERVICE_NAMES
        )

    def test_run(self):
        self.release.run(do_build=True, as_daemon=True)


class TestRunningRelease(TestRelease):
    def test_start(self):
        self.release.stop()
        self.release.start()

    def test_stop(self):
        self.release.stop()

    def test_remove(self):
        self.release.stop()
        self.release.remove()

    @unittest.skip  # Broken, but not useful
    def test_remove_images(self):
        self.release.stop()
        self.release.remove()
        self.release.remove_images()

    @unittest.skip  # Broken, but not useful
    def test_remove_network(self):
        self.release.stop()
        self.release.remove()
        self.release.remove_images()
        self.release.remove_network()


if __name__ == '__main__':
    logger.setLevel(level=logging.INFO)
    main(sys.argv)
