import optparse


__dialogs__ = dict(Confirm='basicsUi',
                   Settings='settingsUi')

usage = "dialogs -n [DialogClassName]"

parser = optparse.OptionParser(usage=usage)
parser.add_option('-n', '--name', type='string', help="Dialog class name")
parser.add_option('-l', '--list', action='store_true', help="List all dialogs class name")


if __name__ == '__main__':
    options, args = parser.parse_args()
    options = eval(str(options))

    #--- List All Dialogs ---#
    if options['list']:
        for dialog in sorted(__dialogs__.keys()):
            print dialog

    #--- Show Dialog ---#
    else:

        #--- Check Dialog Class Name ---#
        if not options['name'] in __dialogs__.keys():
            print "Dialog class name not found: %s" % options['name']
            for dialog in sorted(__dialogs__.keys()):
                print dialog

        #--- Launch Dialog ---#
        else:
            import sys
            from PyQt4 import QtGui

            wp = __import__(__dialogs__[options['name']])

            app = QtGui.QApplication(sys.argv)
            w = eval('wp.%s()' % options['name'])
            print w.__doc__
            w.show()
            sys.exit(app.exec_())
