from nose.plugins.base import Plugin

import os
from collections import defaultdict

# needs polib from http://pypi.python.org/pypi/polib
import polib


import gettext
track_gettext = True


# maybe we should subsclass GNUTranslations and
# monkeypatch it in the gettext module for
# stuff using the module interface?
class GettextCoverageData():
    msg_ids = defaultdict(int)

    def _gettext(self, msgid):
        return msgid
        #return gettext_real.gettext_(msgid)

    def gettext(self, msgid):
        # so we can temporarily disable this
        if track_gettext:
            self.msg_ids[msgid] = self.msg_ids[msgid] + 1
        return self._gettext(msgid)

    def dgettext(self, domain, msgid):
        return self.gettext(msgid)

    def ldgettext(self, domain, msgid):
        return self.gettext(msgid)

    def __init__(self, potfile="po/keys.pot"):
        if os.access(potfile, os.R_OK):
            self.pot = polib.pofile(potfile)
        else:
            raise IOError("%s could not be read" % potfile)

    # "pprint" support for default dict, fake it
    def details(self):
        buf = ""
        for key in self.msg_ids:
            buf = buf + "\"%s\" : %s,\n" % (key, self.msg_ids[key])
        return buf

    def report(self):
        num_msgs = len(self.pot)
        coverage = {}
        for entry in self.pot:
            msgid = entry.msgid
            coverage[msgid] = False
            if msgid in self.msg_ids:
                coverage[msgid] = True
        #print coverage
        total_true = 0
        for msgid in coverage:
            if coverage[msgid]:
                total_true = total_true + 1

        coverage = 0
        if total_true:
            coverage = float(total_true) / float(num_msgs)

        return "gettext coverage: %2.2f%% total msgs: %s msgs covered: %s\n" % (coverage * 100, num_msgs, total_true)


class GettextCoverage(Plugin):
    """Output test results as ugly, unstyled html.
    """
    name = 'gettext-cover'
    status = {}
    score = 100
    enabled = True

    def options(self, parser, env):
        Plugin.options(self, parser, env)

        parser.add_option("--gettext-cover-pot-file", action="store",
                          default="po/keys.pot",
                          dest="cover_pot_file",
                          help="pot file containing gettext msgs")
        parser.add_option("--gettext-cover-details", action="store_true",
                           default=False,
                           dest="cover_details",
                           help="show coverage stats for all strings")

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.pot_file = options.cover_pot_file

        self.cover_details = options.cover_details

    def begin(self):
        self.gtc = GettextCoverageData(potfile=self.pot_file)

        gettext.gettext = self.gtc.gettext
        gettext.dgettext = self.gtc.dgettext
        gettext.ldgettext = self.gtc.ldgettext
        gettext.lgettext = self.gtc.gettext

    def report(self, stream):
        if self.cover_details:
            stream.writeln(self.gtc.details())
        stream.writeln(self.gtc.report())
