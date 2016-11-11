import sublime
import sublime_plugin
import re

class LogcatFormatDetectionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    syntax = self.detect_view_syntax()
    if syntax:
      self.view.set_syntax_file("Packages/Logcat/%s.tmLanguage" % syntax)

  def detect_view_syntax(self):
    for row in range(0, 9):
      region = self.view.full_line(self.view.text_point(row, 0))
      line = self.view.substr(region)
      syntax = self.detect_line_syntax(line)
      if syntax:
        return syntax

  def detect_line_syntax(self, line):
    if re.match(r'(?x)^(?:\s*(\d+:)\s*)?([DEFIVW])/(.*)\(\s*(\d+)\):\s+(.*)', line):
      return 'logcat-brief.tmLanguage'
    elif re.match(r'(?x)^(?:\s*(\d+:)\s*)?([\d-]+)\s+([\d:.]+)\s+([DEFIVW])/(.*?):\s+(.*)', line):
      return 'logcat-cts-host.tmLanguage'
    elif re.match(r'(?x)^(?:\s*(\d+:)\s*)?([\d-]+)\s+([\d:.]+)\s+(\d+)\s+(\d+)\s+([DEFIVW])\s+(.*?):\s+(.*)', line):
      return 'logcat-threadtime'
    elif re.match(r'(?x)^(?:\s*(\d+:)\s*)?([\d-]+)\s+([\d:.]+)\s+([DEFIVW])/(.*)\(\s*(\d+)\):\s+(.*)', line):
      return 'logcat-time'
