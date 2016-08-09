# Sublime Text 3 plugin: Exclude Paths

Add a sidebar menu item to exclude paths from the project and / or from indexing.

Adds a "clear all excludes" command to the palette so you can undo this without having to hand-edit a project file (which you might not even have).

## Install

### Package Control

The easiest way to install this is with [Package Control](http://wbond.net/sublime\_packages/package\_control).

 * If you just went and installed Package Control, you probably need to restart Sublime Text before doing this next bit.
 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package" (it'll take a few seconds)
 * Type "Exclude Paths" when the list appears to find it.

Package Control will automatically keep Exclude Paths up to date with the latest version.

## Questions

### How is this stored?

It depends on how you opened the project. If you used the `Open Project...` menu item to open a `.sublime-project` file, changes will be saved to the project file. If you've just opened a folder (via `subl`, the `Open...` menu item, or dragging it onto Sublime), Sublime Text will remember it internally, but won't persist that across openings.

### Why don't my changes to `Preferences.sublime-settings` apply now?

Higher-priority settings in Sublime Text (like those in project data) override lower priority settings (like those in your generic preferences file). As such, anything we set in the project file will completely replace your default settings.

When per-project exclusions are changed, we do copy the core ones in. However, this only happens on-change, so drift can occur when you edit your core settings.
