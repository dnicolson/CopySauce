#CopySauce

CopySauce was developed for working on Sitecore .NET projects to circumvent the build process by copying static files to the web root. It should also work for .NET projects where the web root is separate to the source files.

##Configuring

When first launched there will be a prompt to locate the project and web root directories. After this a `.CopySauce.json` will be created in the root of the project directory with these options:

    {
        "web_root": "",
        "file_exclude_patterns": [
            "^\\.",
            ".*\\.cs$"
        ],
        "folder_exclude_patterns": [
            "^\\."
        ],
        "folders_to_watch": [
            "css",
            "images",
            "img",
            "javascript",
            "js",
            "layouts",
            "views",
            "xsl"
        ],
        "cmd_after_copy": ""
    }

##Requirements

- Windows
- Python 2.7
- [Watchdog](http://pypi.python.org/pypi/watchdog) module

##Optional

[PyInstaller](http://www.pyinstaller.org/) (py2exe would probably work as well) can be used to make an executable:

    python pyinstaller.py -F CopySauce.py -i CopySauce.ico
