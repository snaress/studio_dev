import optparse


__widgets__ = dict(BasicTree='basicTreeUi',
                   Range='rangeUi')

usage = "widgets -n [WidgetClassName]"

parser = optparse.OptionParser(usage=usage)
parser.add_option('-n', '--name', type='string', help="Widget class name")
parser.add_option('-l', '--list', action='store_true', help="List all widgets class name")


if __name__ == '__main__':
    options, args = parser.parse_args()
    options = eval(str(options))

    #--- List All Widgets ---#
    if options['list']:
        for widget in sorted(__widgets__.keys()):
            print widget

    #--- Show Widget ---#
    else:

        #--- Check Widget Class Name ---#
        if not options['name'] in __widgets__.keys():
            print "Widget class name not found: %s" % options['name']
            for widget in sorted(__widgets__.keys()):
                print widget

        #--- Launch Widget ---#
        else:
            import sys
            from PyQt4 import QtGui

            wp = __import__(__widgets__[options['name']])

            app = QtGui.QApplication(sys.argv)
            w = eval('wp.%s()' % options['name'])
            print w.__doc__
            w.show()
            sys.exit(app.exec_())
