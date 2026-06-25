import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPOSE = (
    f"docker compose -f {ROOT}/docker-compose.yml "
    f"-f {ROOT}/docker-compose.dev.yml -p sidc"
)
DUMP_FILE = os.path.join(ROOT, "sidc.dump")
MEDIA_DIR = os.path.join(ROOT, "media")

remote_host = sys.argv[1] if len(sys.argv) > 1 else "samireland.com"
local_site_hostname = sys.argv[2] if len(sys.argv) > 2 else "localhost"
postgres_container = "sidc_postgres"
django_container = "sidc_django"
db_user = "sidc"
db_name = "sidc"


def run(cmd, *, check=True, **kwargs):
    subprocess.run(cmd, shell=isinstance(cmd, str), check=check, **kwargs)


def terminate_db_connections():
    run(
        f'docker exec {postgres_container} psql -U {db_user} postgres -c '
        f'"SELECT pg_terminate_backend(pid) FROM pg_stat_activity '
        f"WHERE datname = '{db_name}' AND pid <> pg_backend_pid();\""
    )


# Dump production database
with open(DUMP_FILE, "wb") as dump:
    run(
        f'ssh {remote_host} "docker exec {postgres_container} '
        f'pg_dump -U {db_user} -Fc {db_name}"',
        stdout=dump,
    )

# Restore into local postgres
run(f"{COMPOSE} stop django")
terminate_db_connections()
run(
    f'docker exec {postgres_container} psql -U {db_user} postgres -c '
    f'"DROP DATABASE IF EXISTS {db_name};"'
)
run(
    f'docker exec {postgres_container} psql -U {db_user} postgres -c '
    f'"CREATE DATABASE {db_name};"'
)
with open(DUMP_FILE, "rb") as dump:
    run(
        [
            "docker", "exec", "-i", postgres_container,
            "pg_restore", "-U", db_user, "-d", db_name,
            "--no-owner", "--no-acl",
        ],
        stdin=dump,
        check=False,
    )

# Point Wagtail site at local hostname
run(
    f'docker exec {postgres_container} psql -U {db_user} {db_name} -c '
    f"\"UPDATE wagtailcore_site SET hostname = '{local_site_hostname}', "
    f"site_name = '{local_site_hostname}';\""
)

run(f"{COMPOSE} start django")

# Sync media from production
run(f'ssh {remote_host} "docker cp {django_container}:/home/app/media ./"')
if os.path.isdir(MEDIA_DIR):
    run(f"rm -rf {MEDIA_DIR}")
run(f"scp -r {remote_host}:media {ROOT}/")
run(f'ssh {remote_host} "rm -rf media"')

# Host media/ is not mounted in containers — copy into the docker volume
run(f"docker exec {django_container} sh -c 'rm -rf /home/app/media/*'")
run(f"docker cp {MEDIA_DIR}/. {django_container}:/home/app/media/")

os.remove(DUMP_FILE)
