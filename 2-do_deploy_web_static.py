#!/usr/bin/python3
# Fabfile to distribute an archive to your web servers,

from fabric.api import env, put, run, local
from os.path import exists, isdir
import os.path
import re


# Set the username and host for SSH connection to the server
env.user = 'ubuntu'
env.hosts = ['35.172.220.65', '34.204.53.150']
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):

    """deploy web static"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(path_name))
        run('tar -xzf /tmp/{} -C {}/'.format(file_name, path_name))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(path_name, path_name))
        run("rm -rf {}/web_static".format(path_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path_name))

        if not isdir("/var/www/html/hbnb_static"):
            run("sudo mkdir -p /var/www/html/hbnb_static")

        run("sudo cp -r /data/web_static/current/* /var/www/html/hbnb_static/")
        return True
    except Exception:
        return False
