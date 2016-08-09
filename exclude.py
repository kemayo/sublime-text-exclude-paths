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
        settings = sublime.load_settings("Preferences.sublime-settings")
        core_files = set(settings.get('file_exclude_patterns', []))
        core_folders = set(settings.get('folder_exclude_patterns', []))
        project_file_name = self.window.project_file_name()
        changed = False

        for folder in data['folders']:
            old_files = set(folder.get("file_exclude_patterns", [])) - core_files
            old_folders = set(folder.get("folder_exclude_patterns", [])) - core_folders

            new_files = old_files.copy()
            new_folders = old_folders.copy()

            folder_path = folder['path']
            if not os.path.exists(folder_path):
                folder_path = os.path.normpath(os.path.join(os.path.dirname(project_file_name), folder_path))

            for f in files:
                if f.find(folder_path) == 0:
                    new_files.add(f)
            for d in folders:
                if os.path.samefile(folder_path, d):
                    # don't allow the root of the project to be ignored
                    continue
                if d.find(folder_path) == 0:
                    new_folders.add(d)

            # print('files', new_files, old_files)
            # print('folders', new_folders, old_folders)
            if old_files != files or old_folders != folders:
                folder["file_exclude_patterns"] = list(new_files | core_files)
                folder["folder_exclude_patterns"] = list(new_folders | core_folders)
                changed = True

        if changed:
            # print("changed", data)
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
