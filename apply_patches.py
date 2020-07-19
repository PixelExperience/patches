# Usage curl -s https://raw.githubusercontent.com/PixelExperience/patches/ten/apply_patches.py | python3

import subprocess, sys

private_repositories = [{
    "name": "external_motorola_faceunlock",
    "path": "external/motorola/faceunlock"
}]

private_patches = [{
    "file": "face_unlock_fwb.patch",
    "path": "frameworks/base"
}, {
    "file": "face_unlock_settings.patch",
    "path": "packages/apps/Settings"
}]

branch = "ten"
repo_base_url = "https://bitbucket.org/PixelExperience"
patch_base_url = "https://bitbucket.org/pixelexperience/patches/raw/master"

for repo in private_repositories:
    url = repo_base_url + '/' + repo['name']
    print('Fetching "' + url + '"')
    cmd = ['git clone ' + url + ' ' + repo['path'] + ' -b ' + branch]
    result = subprocess.call([' '.join(cmd)], shell=True)
    if result != 0:
        print('ERROR: Failed to clone private repository')
        sys.exit(result)

for path in private_patches:
    print('Applying patch "' + path['file'] + '" into dir "' + path['path'] +
          '"')
    cmd = [
        'curl -s {0}/{1}/{2} | git am --3way'.format(patch_base_url, branch,
                                                     path['file'])
    ]
    result = subprocess.call([' '.join(cmd)], cwd=path['path'], shell=True)
    if result != 0:
        print('ERROR: Failed to apply patch')
        sys.exit(result)

print('All done')
