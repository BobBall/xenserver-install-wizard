import subprocess

WHIPTAIL = "/usr/bin/whiptail"

class Tui():
	def __init__(self, auto_default=False):
		self.auto_default = auto_default

	def yesno(self, question, default=None):
		if self.auto_default and default:
			return default
		width = len(question)
		if width > 80:
			width = 80
		cmd = [ WHIPTAIL, "--yesno", question, "10", str(width) ]
		code = subprocess.call(cmd)
		if code == 0:
			return True
		return False

	def choose(self, question, options):
		if self.auto_default and default:
			return default
		cmd = [ WHIPTAIL, "--menu", question, "10", "50", str(len(options)) ]
		for option in options:
			cmd.append(option[0])
			cmd.append(option[1])
		x = subprocess.Popen(cmd, stderr = subprocess.PIPE)
		y = x.communicate()
		return str(y[1])

	def text(self, question, default):
		if self.auto_default and default:
			return default
		cmd = [ WHIPTAIL, "--inputbox", question, "8", "50", default ]
		x = subprocess.Popen(cmd, stderr = subprocess.PIPE)
		y = x.communicate()
		return str(y[1])

	
