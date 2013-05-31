import shutil, json, time, os, sys, re
from win32com.shell import shell
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

defaults = {
    "projects": [],
    "folders_to_watch": ["css", "images", "img", "javascript", "js", "layouts", "views", "xsl"],
    "file_exclude_patterns": ["^\.", ".*\\.cs$"],
    "folder_exclude_patterns": ["^\."]
}

class ChangeHandler(FileSystemEventHandler):
    def __init__(self,file_exclude_patterns,folder_exclude_patterns):
        self.file_exclude_patterns = file_exclude_patterns
        self.folder_exclude_patterns = folder_exclude_patterns

    def _get_directories(self, path):
        directories = []
        while 1:
            path, directory = os.path.split(path)

            if directory != "":
                directories.append(directory)
            else:
                if path != "":
                    directories.append(path)
                break
        return directories

    def exclude_check(self, src, is_directory):
        for pattern in self.folder_exclude_patterns:
            for directory in self._get_directories(src):
                if re.match(pattern,directory):
                    # print "Excluding directory", os.path.basename(src)
                    return True
        if not is_directory:
            for pattern in self.file_exclude_patterns:
                if re.match(pattern,os.path.basename(src)):
                    # print "Excluding file", os.path.basename(src)
                    return True

    def on_created(self, event):
        if self.exclude_check(event.src_path,event.is_directory):
            return
        try:
            if (event.is_directory):
                shutil.copytree(event.src_path,event.src_path.replace(project,webroot))
            else:
                shutil.copy(event.src_path,event.src_path.replace(project,webroot))
            print "Added", event.src_path.replace(project,"")
        except Exception, err:
            print err

    def on_deleted(self, event):
        if self.exclude_check(event.src_path,event.is_directory):
            return
        try:
            os.unlink(event.src_path.replace(project,webroot))
            print "Removed", event.src_path.replace(project,"")
        except Exception, err:
            print err

    def on_modified(self, event):
        if self.exclude_check(event.src_path,event.is_directory):
            return
        try:
            if not event.is_directory:
                shutil.copy(event.src_path,event.src_path.replace(project,webroot))
                print "Updated", event.src_path.replace(project,"")
        except Exception, err:
            print err

class ShellError(Exception):
    def __init__(self, message):
        print "An error occurred!\n"
        raw_input("%s\n" % message)
        sys.exit()

class Settings():
    def __init__(self):
        self.settingsfile = os.path.join(os.path.expanduser("~"),"AppData\\Local\\CopySauce\\CopySauce.json")
        directory = os.path.dirname(self.settingsfile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        jsonfile = open(self.settingsfile,"ab+")
        try:
            self.settings = json.loads(jsonfile.read())
        except ValueError, e:
            self.settings = defaults

    def get(self,key):
        if key not in self.settings:
            return []
        return self.settings[key]

    def set(self,key,value):
        try:
            if value not in self.settings[key]:
                self.settings[key].append(value)
        except KeyError:
            self.settings[key] = [value]
        jsonfile = open(self.settingsfile,"w+")
        jsonfile.write(json.dumps(self.settings, sort_keys=True, indent=4, separators=(',', ': ')))

def get_project(projects):
    if len(projects):
        for i in range(len(projects)):
            print str((i + 1)) + ".", projects[i]['source']
        print
        choice = raw_input("Choose a previous project or press enter to choose a new one.\n\n")
        print
    try:
        int(choice)
        if int(choice) in range(1,len(projects) + 1):
            return [projects[(int(choice) - 1)]['source'],projects[(int(choice) - 1)]['webroot']]
    except (ValueError, UnboundLocalError):
        print "Choose the source directory...\n\n"
        try:
            pidl, display_name, image_list = shell.SHBrowseForFolder()
            project = shell.SHGetPathFromIDList(pidl)
            return [project,None]
        except Exception, e:
            raise ShellError(e)

def get_webroot(project):
    os.chdir(project)

    dependency = ""
    cwd = project
    for i in range(1,10):
        cwd = os.path.dirname(cwd)
        if "Dependency" in os.listdir(cwd):
            dependency = os.path.join(cwd,"Dependency")
            break
        if "dependency" in os.listdir(cwd):
            dependency = os.path.join(cwd,"dependency")
            break

    if dependency:
        if os.path.exists(os.path.join(dependency,"Sitecore")):
            dependency = os.path.join(dependency,"Sitecore\\Website")
        else:
            dependency = os.path.join(dependency,"Website")
        print dependency
        choice = raw_input("\nUse the above webroot? [y]\n\n")
        if choice.lower() == "y":
            print
            return dependency

    print "Choose the webroot...\n\n"
    try:
        pidl, display_name, image_list = shell.SHBrowseForFolder()
        webroot = shell.SHGetPathFromIDList(pidl)
    except Exception, e:
        raise ShellError(e)
    return webroot

if __name__ == "__main__":
    print "\nCopySauce running...\n"

    settings = Settings()
    event_handler = ChangeHandler(settings.get("file_exclude_patterns"),settings.get("folder_exclude_patterns"))
    [project, webroot] = get_project(settings.get("projects"))
    if not webroot:
        webroot = get_webroot(project)
    settings.set("projects",{"source": project, "webroot": webroot})

    print "Project: %s" % project
    print "Webroot: %s\n" % webroot

    for path in settings.get('folders_to_watch'):
        if not os.path.exists("%s\\%s" % (project,path)):
            #print "Skipping ", path
            continue
        print "Watching", path + "..."
        p = "%s\\%s" % (project,path)
        observer = Observer()
        observer.schedule(event_handler, path=p, recursive=True)
        observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
