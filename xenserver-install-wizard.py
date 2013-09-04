#!/usr/bin/env python

import sys, subprocess, argparse
import xapi, replace, grub, networking, iptables, storage, templates, logging, hostname, openstack
from tui import Tui

def reboot():
	print >>sys.stderr, "Triggering an immediate reboot"
	cmd = [ "/sbin/reboot" ]
	x = subprocess.call(cmd)
	if x <> 0:
		print >>sys.stderr, "FAILED: to trigger a reboot (%s)" % (" ".join(cmd))

def stop_xend():
	print >>sys.stderr, "Permanently stopping xend"
	if subprocess.call(["/sbin/chkconfig", "--level", "345", "xend", "off"]) <> 0:
		print >>sys.stderr, "FAILED: to disable xend"
	if subprocess.call(["/sbin/service", "xend", "stop"]) <> 0:
		print >>sys.stderr, "FAILED: to stop xend"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Lock a single server')
	parser.add_argument('--yes-to-all', action='store_true')
	parser.add_argument('--reboot', dest="auto_reboot", action='store_true')
	args = parser.parse_args()

	tui = Tui(args.yes_to_all)
	r = logging.analyse(tui)
	if r:
		replace.file(r[0], r[1])
		logging.restart()
	stop_xend ()
	xapi.start ()
	need_to_reboot = False
	r = grub.analyse(tui)
	if r:
		need_to_reboot = True
		replace.file(r[0], r[1])
	r = networking.analyse(tui)
	if r:
		need_to_reboot = True
		for change in r:
			replace.file(change[0], change[1])
		networking.restart()
	r = iptables.analyse(tui)
	if r:
		replace.file(r[0], r[1])
		iptables.restart()
	storage.analyse(tui)
	openstack.analyse(tui)
	hostname.analyse(tui)
	templates.create()
	print "Welcome to XenServer!"
	if need_to_reboot:
		if args.auto_reboot:
			reboot()
		elif tui.yesno("A reboot is needed before XenServer is fully ready. Would you like to reboot now?", False):
			reboot()
	
