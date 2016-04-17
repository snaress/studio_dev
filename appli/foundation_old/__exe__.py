import optparse


usage = "foundation -p [Project] -v [LogLevel]"
parser = optparse.OptionParser(usage=usage)
parser.add_option('-p', '--project', type='string', help="Load given project (projectName--projectCode)")
parser.add_option('-v', '--logLvl', type='choice', default='info',
                  choices=['critical', 'error', 'warning', 'info', 'debug', 'detail'],
                  help=' '.join(["['critical','error','warning','info','debug','detail']",
                                 "Log level (default: 'info')"]))
parser.add_option('-L', '--projectList', action='store_true', help="List all projects")


if __name__ == '__main__':
    options, args = parser.parse_args()
    options = eval(str(options))

    if options['projectList']:
        from appli.foundation.core import foundation
        fdn = foundation.Foundation(logLvl='critical')
        for project in fdn.project.projects:
            print project
    else:
        from foundation_old.gui import foundationUi
        foundationUi.launch(project=options['project'], logLvl=options['logLvl'])
