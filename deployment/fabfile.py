from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, put
import random

REPO_URL = "https://github.com/samirelanduk/samireland.com.git"


def deploy():
    site_folder = "/home/%s/sites/%s" % (env.user, env.host)
    source_folder = site_folder + "/source"
    base_path = source_folder + "/samireland/templates/base.html"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _add_google_analytics(env.host, base_path)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ["static", "source", "virtualenv"]:
        run("mkdir -p %s/%s" % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        run("cd %s && git fetch" % source_folder)
    else:
        run("git clone %s %s" % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run("cd %s && git reset --hard %s" % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + "/samireland/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(
     settings_path,
     'ALLOWED_HOSTS =.+$',
     'ALLOWED_HOSTS = ["%s", "%s"]' % (site_name, "www." + site_name)
    )
    sed(
     settings_path,
     '"media", "images"',
     '"../../samireland-media"'
    )
    append(
     settings_path,
     'STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../static"))'
    )
    secret_settigs_file = source_folder + "/samireland/secret_settings.py"
    put("../samireland/secret_settings.py", secret_settigs_file)
    put("../samireland/config.py", source_folder + "/samireland/config.py")
    sed(
     secret_settigs_file,
     ': local_db',
     ': live_db'
    )

def _add_google_analytics(host, base_path):
    if host == "samireland.com":
        sed(
         base_path,
         "<!--google-analytics-->",
         "{% block analytics %}{% endblock %}"
        )

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + "/../virtualenv"
    if not exists(virtualenv_folder + "/bin/pip"):
        run("virtualenv --python=python3 %s" % virtualenv_folder)
    run("%s/bin/pip3 install -r %s/requirements.txt" % (
     virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    run("cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput" %
     source_folder
    )


def _update_database(source_folder):
    run("cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput" %
     source_folder
    )
