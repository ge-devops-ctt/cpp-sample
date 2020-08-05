import os 
from git import Repo

# Manage semver du to conflict with a Conan dependency
import importlib.util
spec = importlib.util.spec_from_file_location("semver", "/opt/pyenv/versions/3.7.5/lib/python3.7/site-packages/semver.py")
semver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(semver)

# dir_path = os.path.abspath(".")
dir_path = os.getenv("CI_PROJECT_DIR", "/app")
repo = Repo(dir_path)


def latest_tag():
    try:
        tag = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)[-1]
    except:
        tag = "1.0.0"

    return str(tag)


def get_version():
    branch = os.getenv("CI_COMMIT_REF_NAME") if "CI_COMMIT_REF_NAME" in os.environ else repo.head.reference.name
    tag = latest_tag()
   
    next_tag = semver.VersionInfo.parse(tag).bump_minor()
    
    new_tag = os.getenv("CI_COMMIT_TAG")
    if new_tag:
        version = new_tag
    elif branch == "master":
        version = next_tag.bump_prerelease()
    else:
        version = f"{next_tag}-{branch}"

    return version

def main():
    print(get_version())

main()
