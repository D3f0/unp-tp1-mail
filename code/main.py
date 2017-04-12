import sys
from twisted.python import log
from twisted.internet import reactor
from smtpserver import  LocalSMTPFactory
from pop3server import portal, POP3Factory, MailUserRealm, FilesystemBasedChecker

log.startLogging(sys.stdout)

# POP3
the_portal = portal.Portal(MailUserRealm('/tmp/mail'))
the_checker = FilesystemBasedChecker('/tmp/mail')
the_portal.registerChecker(the_checker)
reactor.listenTCP(1100, POP3Factory(the_portal))

# SMTP
reactor.listenTCP(2500, LocalSMTPFactory("/tmp/mail"))
reactor.run()