import os.path

import sublime
import sublime_plugin


class SidebarSelection:
    def run(self, paths=None):
        paths = paths or []
        files = []
        folders = []
        for path in paths:
            if os.path.isdir(path):
                folders.append(path)
            else:
                files.append(path)
        self.handle(files, folders)


class ExcludePathIndexCommand(SidebarSelection, sublime_plugin.WindowCommand):
    def handle(self, files, folders):
        prefs = sublime.load_settings("Preferences.sublime-settings")
        excluded = prefs.get("index_exclude_patterns", [])
        excluded.extend(files)
        excluded.extend([os.path.join(d, '*') for d in folders])
        prefs.set("index_exclude_patterns", list(set(excluded)))
        sublime.save_settings("Preferences.sublime-settings")


class ExcludePathProjectCommand(SidebarSelection, sublime_plugin.WindowCommand):
    def handle(self, files, folders):
        data = self.window.project_data()
        project_file_name = self.window.project_file_name()
        for folder in data['folders']:
            if "folder_exclude_patterns" not in folder:
                folder["folder_exclude_patterns"] = []
            if "file_exclude_patterns" not in folder:
                folder["file_exclude_patterns"] = []
            folder_path = folder['path']
            if not os.path.exists(folder_path):
                folder_path = os.path.normpath(os.path.join(os.path.dirname(project_file_name), folder_path))
            for f in files:
                if f.find(folder_path) == 0 and f not in folder["file_exclude_patterns"]:
                    folder["file_exclude_patterns"].append(f)
            for d in folders:
                if os.path.samefile(folder_path, d):
                    # don't allow the root of the project to be ignored
                    continue
                if d.find(folder_path) == 0 and d not in folder["folder_exclude_patterns"]:
                    folder["folder_exclude_patterns"].append(d)
            # unique it
            folder["file_exclude_patterns"] = list(set(folder["file_exclude_patterns"]))
            folder["folder_exclude_patterns"] = list(set(folder["folder_exclude_patterns"]))
        self.window.set_project_data(data)


class ExcludePathClearProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        data = self.window.project_data()
        for folder in data['folders']:
            if "folder_exclude_patterns" in folder:
                del(folder["folder_exclude_patterns"])
            if "file_exclude_patterns" in folder:
                del(folder["file_exclude_patterns"])
        self.window.set_project_data(data)
