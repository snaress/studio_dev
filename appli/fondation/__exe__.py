import optparse


usage = "fondation -p [Project] -v [LogLevel]"
parser = optparse.OptionParser(usage=usage)
parser.add_option('-p', '--project', type='string', help="Load given project (projectName--projectCode)")
parser.add_option('-v', '--verbose', type='choice', default='info',
                  choices=['critical', 'error', 'warning', 'info', 'debug', 'detail'],
                  help=' '.join(["['critical','error','warning','info','debug','detail']",
                                 "Log level (default: 'info')"]))
parser.add_option('-l', '--listProjects', action='store_true', help="List all projects")


if __name__ == '__main__':
    options, args = parser.parse_args()
    options = eval(str(options))

    if options['listProjects']:
        from fondation.core import fondation
        fdn = fondation.Fondation(logLvl='critical')
        for project in fdn._project.projects:
            print project
    else:
        from fondation.gui import fondationUi
        fondationUi.launch(project=options['project'], logLvl=options['verbose'])
