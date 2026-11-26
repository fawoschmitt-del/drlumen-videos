"""Put a finished video on the `media` branch of this repo and print its public download URL.
The media branch is rewritten as a single commit each time and keeps only the newest KEEP videos,
so the repo doesn't grow forever (Buffer downloads the file when the post goes out, so keep a few days).
    python publish.py out/tickle/tickle.mp4 [name.mp4]
"""
import os, sys, subprocess, shutil, tempfile, re, glob

KEEP = 7
HERE = os.path.dirname(os.path.abspath(__file__))

def git(*a, cwd=HERE, check=True):
    return subprocess.run(['git', *a], cwd=cwd, check=check, capture_output=True, text=True).stdout.strip()

def repo_slug():
    url = git('remote', 'get-url', 'origin')
    m = re.search(r'github\.com[/:]([^/]+)/([^/.]+)', url)
    return m.group(1), m.group(2)

def main(src, name=None):
    name = name or os.path.basename(src)
    owner, repo = repo_slug()
    tmp = tempfile.mkdtemp()
    # fetch the current media branch (if any) to keep the latest videos
    have = git('ls-remote', '--heads', 'origin', 'media')
    vids = os.path.join(tmp, 'videos'); os.makedirs(vids)
    if have:
        git('fetch', '--depth', '1', 'origin', 'media:refs/remotes/origin/media', check=False)
        files = git('ls-tree', '--name-only', 'origin/media', 'videos/', check=False).split()
        for f in files:
            with open(os.path.join(tmp, f), 'wb') as fh:
                fh.write(subprocess.run(['git', 'show', f'origin/media:{f}'], cwd=HERE, capture_output=True).stdout)
    shutil.copy(src, os.path.join(vids, name))
    allv = sorted(glob.glob(os.path.join(vids, '*.mp4')), key=os.path.getmtime)
    for f in allv[:-KEEP]: os.remove(f)
    git('init', '-q', '-b', 'media', cwd=tmp)
    git('add', 'videos', cwd=tmp)
    git('-c', 'user.name=Dr Lumen Bot', '-c', 'user.email=bot@users.noreply.github.com', 'commit', '-q', '-m', f'media: {name}', cwd=tmp)
    url = git('remote', 'get-url', 'origin')
    git('push', '-f', url, 'media:media', cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f'https://raw.githubusercontent.com/{owner}/{repo}/media/videos/{name}')

if __name__ == '__main__':
    main(*sys.argv[1:])
