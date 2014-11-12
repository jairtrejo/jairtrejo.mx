from fabric.api import local, hosts
import os
import fabric.contrib.project as project

PROD = 'jtrejo@jairtrejo.mx'
DEST_PATH = '/home/jtrejo/webapps/jtrejomx'
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DEPLOY_PATH = os.path.join(ROOT_PATH, 'deploy')


def clean():
    local('rm -rf ./deploy')


def generate():
    local('hyde -g -s .')


def regen():
    clean()
    generate()
    local('python archive-reorder.py')


def serve():
    local('hyde -w -s . -k')


def reserve():
    regen()
    serve()


@hosts(PROD)
def publish():
    regen()
    project.rsync_project(
        remote_dir=DEST_PATH,
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
    local('scp ../curriculum/jair-trejo.pdf jtrejo@jairtrejo.mx:/home/jtrejo/webapps/jtrejomx/resume.pdf')
