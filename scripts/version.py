import os 
import semver
import subprocess
from git import Repo

dir_path = os.path.abspath("..") 
print(dir_path)
repo = Repo(dir_path)

def latest_tag():
    try:
        tag = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)[-1]
    except:
        tag = "1.0.0"
    
    return str(tag)

def get_version():
    branch = repo.head.reference.name
    tag = latest_tag()
    next_tag = semver.VersionInfo.parse(tag).bump_minor()
    if branch == "master":
        next_tag.bump_prerelease()
    else:
        return f"{next_tag}-{branch}"

def list_commit(tag):
    return list(repo.iter_commits(f'...{tag}'))

def main():
    tag = latest_tag()
    print(tag)
    ver = semver.VersionInfo.parse(tag)
    print(ver.bump_patch())
    print(ver.bump_minor())
    print(ver.bump_major())
    print(ver.bump_minor().bump_prerelease().bump_prerelease())
    print(list_commit(tag))
    print(get_version())

main()






