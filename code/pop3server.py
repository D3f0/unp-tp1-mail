# Ejemplo de servidor de mail basado en framework Twisted
# Tomado de los ejemplos del libro Twisted Netowrk Programming
# de Jessica McKellar (@jessicamckellar)

import os
import sys

from zope.interface import implements

from twisted.cred import checkers, portal
from twisted.cred.checkers import (
    InMemoryUsernamePasswordDatabaseDontUse,
    error,
)

from twisted.internet import protocol, reactor
from twisted.mail import maildir, pop3
from twisted.python import log
from twisted.internet import defer
from glob import glob

class UserInbox(maildir.MaildirMailbox):
    def __init__(self, userDir):
        inboxDir = os.path.join(userDir, 'Inbox')
        maildir.MaildirMailbox.__init__(self, inboxDir)

class POP3ServerProtocol(pop3.POP3):
    def lineReceived(self, line):
        print("CLIENT:", line)
        pop3.POP3.lineReceived(self, line)

    def sendLine(self, line):
        print("SERVER:", line)
        pop3.POP3.sendLine(self, line)

class POP3Factory(protocol.Factory):
    def __init__(self, portal):
        self.portal = portal

    def buildProtocol(self, address):
        proto = POP3ServerProtocol()
        proto.portal = self.portal
        return proto

class MailUserRealm(object):
    implements(portal.IRealm)

    def __init__(self, baseDir):
        if not os.path.exists(baseDir):
            os.makedirs(baseDir)
        self.baseDir = baseDir

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pop3.IMailbox not in interfaces:
            raise NotImplementedError(
                "This realm only supports the pop3.IMailbox interface.")

        userDir = os.path.join(self.baseDir, avatarId)
        avatar = UserInbox(userDir)
        return pop3.IMailbox, avatar, lambda: None

def check_directory_exists(user):
    return os.path.exists(os.path.join('/tmp/maildir/' + user))

class FilesystemBasedChecker(InMemoryUsernamePasswordDatabaseDontUse):

    def __init__(self, path, *largs, **kwargs):
        super(FilesystemBasedChecker, self).__init__(*largs, **kwargs)
        self.path = path

    def requestAvatarId(self, credentials):
        users = map(os.path.basename, glob('/tmp/mail/*'))
        if credentials.username in users:
            return defer.maybeDeferred(
                lambda *args: True).addCallback(
                self._cbPasswordMatch, credentials.username)
        else:
            return defer.fail(error.UnauthorizedLogin("User not in %s" % repr(users)))

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    the_portal = portal.Portal(MailUserRealm('/tmp/mail'))
    reactor.listenTCP(1100, POP3Factory(the_portal))
    # Quitar password
    the_checker = FilesystemBasedChecker('/tmp/mail')
    the_portal.registerChecker(the_checker)
    reactor.run()

