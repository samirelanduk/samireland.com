#!/usr/bin/env python3
"""Pull production database and media into the local Docker environment."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTGRES_CONTAINER = "sidc_postgres"
DJANGO_CONTAINER = "sidc_django"
DB_USER = "sidc"
DB_NAME = "sidc"
MEDIA_DIR = os.path.join(ROOT, "media")
REMOTE_MEDIA_DIR = "/home/app/media"


def run(cmd, *, check=True, **kwargs):
    if isinstance(cmd, str):
        kwargs.setdefault("shell", True)
    return subprocess.run(cmd, check=check, **kwargs)


def die(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def require_container(name):
    result = run(
        ["docker", "inspect", "-f", "{{.State.Running}}", name],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        die(f"Container {name} not found — is your local stack running?")
    if result.stdout.strip() != "true":
        die(f"Container {name} is not running.")


def ssh_run(remote_host, remote_cmd, *, stdout=None):
    result = subprocess.run(
        ["ssh", remote_host, remote_cmd],
        stdout=stdout,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        die(result.stderr.decode().strip() or f"ssh command failed: {remote_cmd}")
    return result


def pull_database(remote_host, dump_path):
    print(f"Dumping database from {remote_host}...")
    with open(dump_path, "wb") as dump_file:
        ssh_run(
            remote_host,
            f"docker exec {POSTGRES_CONTAINER} pg_dump -U {DB_USER} -Fc {DB_NAME}",
            stdout=dump_file,
        )

    if os.path.getsize(dump_path) < 100:
        die("Database dump is empty — pg_dump likely failed.")
    with open(dump_path, "rb") as dump_file:
        if dump_file.read(5) != b"PGDMP":
            die("Database dump is not a valid pg_dump archive.")

    print("Restoring database locally...")
    run(f"docker stop {DJANGO_CONTAINER} sidc_upgrade", check=False)

    terminate_connections = (
        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
        f"WHERE datname = '{DB_NAME}' AND pid <> pg_backend_pid();"
    )
    run(
        f'docker exec {POSTGRES_CONTAINER} psql -U {DB_USER} postgres -c '
        f'"{terminate_connections}"',
        check=False,
    )
    run(
        f'docker exec {POSTGRES_CONTAINER} psql -U {DB_USER} postgres -c '
        f'"DROP DATABASE IF EXISTS {DB_NAME};"'
    )
    run(
        f'docker exec {POSTGRES_CONTAINER} psql -U {DB_USER} postgres -c '
        f'"CREATE DATABASE {DB_NAME};"'
    )

    with open(dump_path, "rb") as dump_file:
        result = subprocess.run(
            [
                "docker", "exec", "-i", POSTGRES_CONTAINER,
                "pg_restore", "-U", DB_USER, "-d", DB_NAME,
                "--no-owner", "--no-acl",
            ],
            stdin=dump_file,
            stderr=subprocess.PIPE,
            check=False,
        )
    if result.returncode not in (0, 1):
        die(result.stderr.decode().strip() or "pg_restore failed.")


def set_local_hostname(hostname):
    print(f"Setting Wagtail site hostname to {hostname}...")
    run(
        f'docker exec {POSTGRES_CONTAINER} psql -U {DB_USER} {DB_NAME} -c '
        f"\"UPDATE wagtailcore_site SET hostname = '{hostname}', "
        f"site_name = '{hostname}';\""
    )


def pull_media(remote_host, archive_path):
    print(f"Syncing media from {remote_host}...")
    with open(archive_path, "wb") as archive_file:
        ssh_run(
            remote_host,
            f"docker exec {DJANGO_CONTAINER} tar -c -C {REMOTE_MEDIA_DIR} .",
            stdout=archive_file,
        )

    if os.path.getsize(archive_path) < 1:
        die("Media archive is empty.")

    staging_dir = tempfile.mkdtemp(prefix="sidc-media-")
    try:
        result = subprocess.run(
            ["tar", "-xf", archive_path, "-C", staging_dir],
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            die(result.stderr.decode().strip() or "Failed to extract media archive.")

        if os.path.isdir(MEDIA_DIR):
            shutil.rmtree(MEDIA_DIR)
        shutil.move(staging_dir, MEDIA_DIR)
        staging_dir = None
    finally:
        if staging_dir and os.path.isdir(staging_dir):
            shutil.rmtree(staging_dir)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "remote_host",
        nargs="?",
        default="samireland.com",
        help="SSH host to pull from (default: samireland.com)",
    )
    parser.add_argument(
        "--hostname",
        default="localhost",
        help="Wagtail site hostname for local dev (default: localhost)",
    )
    parser.add_argument(
        "--skip-db",
        action="store_true",
        help="Skip database pull",
    )
    parser.add_argument(
        "--skip-media",
        action="store_true",
        help="Skip media sync",
    )
    args = parser.parse_args()

    require_container(POSTGRES_CONTAINER)

    dump_path = None
    media_archive = None
    if not args.skip_db:
        dump_path = tempfile.mktemp(suffix=".dump")
    if not args.skip_media:
        media_archive = tempfile.mktemp(suffix=".tar")

    try:
        if not args.skip_db:
            pull_database(args.remote_host, dump_path)
            set_local_hostname(args.hostname)
            run(f"docker start {DJANGO_CONTAINER}", check=False)

        if not args.skip_media:
            pull_media(args.remote_host, media_archive)
    finally:
        for path in (dump_path, media_archive):
            if path and os.path.exists(path):
                os.remove(path)

    print("Done.")


if __name__ == "__main__":
    main()
