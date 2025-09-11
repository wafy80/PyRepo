from flask import Flask, send_from_directory, render_template, abort
import os
import datetime
import configparser

config = configparser.ConfigParser()
config.read('pyrepo.ini')

BASE_DIRS = [d.strip() for d in config.get('pyrepo', 'base_dirs', fallback=os.environ.get("PYREPO_BASE_DIR", os.path.abspath("files"))).split(',')]
PORT = config.getint('pyrepo', 'port', fallback=int(os.environ.get("PYREPO_PORT", 5000)))
HOST = config.get('pyrepo', 'host', fallback=os.environ.get("PYREPO_HOST", "::"))
TITLE = config.get('pyrepo', 'title', fallback= os.environ.get("PYREPO_TITLE", "PyRepo"))

roots = []
for idx, base in enumerate(BASE_DIRS):
    name = os.path.basename(base.rstrip('/')) or base
    roots.append({'name': name, 'idx': idx, 'path': base})

app = Flask(__name__)

def safe_join(base, *paths):
    final_path = os.path.abspath(os.path.join(base, *paths))
    if not final_path.startswith(base):
        abort(404)
    return final_path

def human_size(size):
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def human_mtime(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%d/%m/%Y %H:%M")

@app.route('/')
def home():
    return render_template("roots.html", roots=roots, title=TITLE)

@app.route('/<int:root_idx>/', defaults={'subpath': ''})
@app.route('/<int:root_idx>/<path:subpath>')
def browse(root_idx, subpath):
    if root_idx < 0 or root_idx >= len(BASE_DIRS):
        abort(404)
    BASE_DIR = BASE_DIRS[root_idx]
    abs_dir = safe_join(BASE_DIR, subpath)
    if not os.path.isdir(abs_dir):
        abort(404)
    dirs = []
    files = []
    try:
        for name in sorted(os.listdir(abs_dir)):
            full_path = os.path.join(abs_dir, name)
            if name.startswith('.'):
                continue
            try:
                stat = os.stat(full_path)
            except OSError:
                continue
            mtime = human_mtime(stat.st_mtime)
            if os.path.isdir(full_path):
                dirs.append((name, True, '-', mtime))
            else:
                size = human_size(stat.st_size)
                files.append((name, False, size, mtime))
    except OSError:
        pass
    entries = dirs + files
    rel_path = subpath.strip('/')
    return render_template("browser.html", entries=entries, 
                                           rel_path=rel_path,
                                           title=TITLE,
                                           root_idx=root_idx,
                                           roots=roots)

@app.route('/download/<int:root_idx>/<path:subpath>')
def download_file(root_idx, subpath):
    if root_idx < 0 or root_idx >= len(BASE_DIRS):
        abort(404)
    BASE_DIR = BASE_DIRS[root_idx]
    abs_file = safe_join(BASE_DIR, subpath)
    dir_name = os.path.dirname(abs_file)
    file_name = os.path.basename(abs_file)
    if not os.path.isfile(abs_file):
        abort(404)
    return send_from_directory(dir_name, file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)