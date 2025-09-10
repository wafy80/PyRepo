# PyRepo

**PyRepo** is a modern, open source web file browser built with Python and Flask. It lets you explore, navigate, and download files from one or more local directories through a clean, responsive web interface inspired by GitHub’s repository style.

## Features

- 🌐 **Modern Web Interface**: Clean, intuitive, and responsive UI, optimized for both desktop and mobile devices.
- 📁 **Multi-root Support**: Configure and browse multiple root directories independently.
- 🔒 **Security by Default**: Hidden directories (starting with `.`) are not listed, but remain accessible if you know the path.
- 📥 **Direct Download**: Download any file with a single click.
- 🧭 **Dynamic Breadcrumbs**: Easily navigate nested folders with a clear breadcrumb trail.
- ⚡ **Easy Configuration**: All settings (roots, port, title) are managed via `.ini` file or environment variables.
- 🏷️ **Detailed View**: See file/folder name, size, and last modified date at a glance.
- 🐧 **Linux Friendly**: Designed and tested on Linux systems.

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/wafy80/pyrepo.git
   cd pyrepo
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Configure your roots**
   Edit `pyrepo.ini` to set your root directories and desired port.

4. **Run the server**
   ```bash
   python app.py
   ```
   Now browse your files at `http://localhost:<port>`.

## Contributing

Contributions, bug reports, and suggestions are welcome!  
If you want to add features, improve the UI, or report issues, please open an issue or pull request.

---

**PyRepo** is designed for anyone who needs a lightweight, elegant, and easily extensible way to browse and share files via the web.  
Join the development and help us make