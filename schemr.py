import sublime, sublime_plugin
import os, zipfile
from random import random

class Schemr():
	def load_schemes(self):
		color_schemes = []

		for root, dirs, files in os.walk(sublime.packages_path()):
			for filename in (filename for filename in files if filename.endswith('.tmTheme')):
				name = filename.replace('.tmTheme', '')
				filepath = os.path.join(root, filename).replace(sublime.packages_path(), 'Packages').replace('\\', '/')
				color_schemes.append(['Scheme: ' + name, filepath])

		for root, dirs, files in os.walk(sublime.installed_packages_path()):
			for package in (package for package in files if package.endswith('.sublime-package')):
				zf = zipfile.ZipFile(os.path.join(sublime.installed_packages_path(), package))
				for filename in (filename for filename in zf.namelist() if filename.endswith('.tmTheme')):
					name = os.path.basename(filename).replace('.tmTheme', '')
					filepath = os.path.join(root, package, filename).replace(sublime.installed_packages_path(), 'Packages').replace('.sublime-package', '').replace('\\', '/')
					color_schemes.append(['Scheme: ' + name, filepath])

		default_schemes = os.path.join(os.getcwd(), 'Packages', 'Color Scheme - Default.sublime-package')
		if os.path.exists(default_schemes):
			zf = zipfile.ZipFile(default_schemes)
			for filename in (filename for filename in zf.namelist() if filename.endswith('.tmTheme')):
				name = os.path.basename(filename).replace('.tmTheme', '')
				filepath = os.path.join('Packages', 'Color Scheme - Default', filename).replace('\\', '/')
				color_schemes.append(['Scheme: ' + name, filepath])

		color_schemes.sort()
		return color_schemes

	def set_scheme(self, s):
		self.settings().set('color_scheme', s)
		sublime.save_settings('Preferences.sublime-settings')

	def get_scheme(self):
		return self.settings().get('color_scheme')

	def cycle_scheme(self, d):
		color_schemes = self.load_schemes()
		the_scheme = self.get_scheme()
		the_index = [scheme[1] for scheme in color_schemes].index(the_scheme)
		num_of_schemes = len(color_schemes)

		if d == "next":
			index = the_index + 1 if the_index < num_of_schemes - 1 else 0

		if d == "prev":
			index = the_index - 1 if the_index > 0 else num_of_schemes - 1

		if d == "rand":
			index = int(random() * len(color_schemes))

		self.set_scheme(color_schemes[index][1])
		sublime.status_message(color_schemes[index][0])

	def settings(self):
		return sublime.load_settings('Preferences.sublime-settings')

Schemr = Schemr()

class SchemrListSchemesCommand(sublime_plugin.WindowCommand):
	def run(self):
		color_schemes = Schemr.load_schemes()
		the_scheme = Schemr.get_scheme()
		the_index = [scheme[1] for scheme in color_schemes].index(the_scheme)

		def on_done(index):
			if index != -1:
				Schemr.set_scheme(color_schemes[index][1])
				sublime.status_message(color_schemes[index][0])

			if index == -1:
				Schemr.set_scheme(color_schemes[the_index][1])

		def on_select(index):
			Schemr.set_scheme(color_schemes[index][1])

		try:
			self.window.show_quick_panel(color_schemes, on_done, 0, the_index, on_select)
		except:
			self.window.show_quick_panel(color_schemes, on_done)

class SchemrNextSchemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Schemr.cycle_scheme("next")

class SchemrPreviousSchemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Schemr.cycle_scheme("prev")

class SchemrRandomSchemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		Schemr.cycle_scheme("rand")
