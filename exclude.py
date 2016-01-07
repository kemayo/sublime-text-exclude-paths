import os.path

import sublime
import sublime_plugin


class SidebarSelectionCommand(sublime_plugin.WindowCommand):
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


class ExcludePathIndexCommand(SidebarSelectionCommand):
    def handle(self, files, folders):
        prefs = sublime.load_settings("Preferences.sublime-settings")
        excluded = prefs.get("index_exclude_patterns", [])
        excluded.extend(files)
        excluded.extend([os.path.join(d, '*') for d in folders])
        print(excluded)
        prefs.set("index_exclude_patterns", list(set(excluded)))
        sublime.save_settings("Preferences.sublime-settings")


class ExcludePathProjectCommand(SidebarSelectionCommand):
    def handle(self, files, folders):
        data = sublime.active_window().project_data()
        project_file_name = sublime.active_window().project_file_name()
        for folder in data['folders']:
            if "folder_exclude_patterns" not in folder:
                folder["folder_exclude_patterns"] = []
            if "file_exclude_patterns" not in folder:
                folder["file_exclude_patterns"] = []
            project_path = folder['path']
            if project_path == '.':
                project_path = os.path.dirname(project_file_name)
            for f in files:
                if f.find(project_path) == 0 and f not in folder["file_exclude_patterns"]:
                    folder["file_exclude_patterns"].append(f)
            for d in folders:
                if d.find(project_path) == 0 and d not in folder["folder_exclude_patterns"]:
                    folder["folder_exclude_patterns"].append(d)
        sublime.active_window().set_project_data(data)


class ExcludePathClearProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        data = sublime.active_window().project_data()
        for folder in data['folders']:
            del(folder["folder_exclude_patterns"])
            del(folder["file_exclude_patterns"])
        sublime.active_window().set_project_data(data)
