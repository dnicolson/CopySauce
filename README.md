#CopySauce

CopySauce was developed for working on Sitecore .NET projects to circumvent the build process by copying static files to the webroot. It should also work for .NET projects where the webroot is separate to the source files.

##Configuring

Projects, file types and exclude patterns can be manually managed by editing this file:

`~\AppData\Local\CopySauce\CopySauce.json`

##Requirements

- Windows
- Python 2.7
- [Watchdog](http://pypi.python.org/pypi/watchdog) module

##Optional

[PyInstaller](http://www.pyinstaller.org/) (py2exe would probably work as well) can be used to make an executable:

    python pyinstaller.py -F CopySauce.py -i CopySauce.ico
