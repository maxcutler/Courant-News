import os
import sys
import shutil
import subprocess

COURANT_SVN_URL = 'svn://code.courantnews.com/courant/trunk'

def extend_parser(parser):
    parser.add_option(
        '-c', '--courant',
        metavar='DIR_OR_URL',
        dest='courant_source',
        default=COURANT_SVN_URL,
        help='Location of a svn/git/hg/bzr directory or URL to use for the installation of Courant',
    )
    
    parser.add_option(
        '-r', '--requirements',
        action='store_true',
        dest='requirements',
        default=True,
        help='Download required external library dependencies'
    )
    
    parser.add_option(
        '', '--skip-requirements',
        action='store_false',
        dest='requirements',
        help='Skip downloading required external library dependencies',
    )

    parser.add_option(
        '-n', '--name',
        metavar='PROJECT_NAME',
        dest='project_name',
        default=None,
        help='Name of your project folder',
    )
    
    parser.conflict_handler = "resolve"

    parser.add_option(
        '-p', '--project',
        metavar='DIR_OR_URL_OR_NAME',
        dest='project_source',
        default=None,
        help='Name of the project template bundled with Courant to use as a starting point, or the location of a svn/git/hg/bzr directory or URL to use for the installation of your site project. Will override project_template if provided',
    )
    
def adjust_options(options, args):
    if not args:
        return # caller will raise error
    
    if options.project_name and not options.project_source:
        print "You must choose either a template or source URL for your project"
        sys.exit(101)
    
    if not options.project_name and options.project_source:
        print "You must choose a name for your project directory"
        sys.exit(101)
    

def after_install(options, home_dir):
    if sys.platform == 'win32':
        bin = 'Scripts'
    else:
        bin = 'bin'
        
    # resolve some paths
    env_dir = os.path.abspath(home_dir)
    src_dir = join(env_dir, 'src')
    easy_install = os.path.abspath(join(env_dir, bin,'easy_install'))    
        
    # install pip
    logger.notify("Installing pip...")
    call_subprocess([easy_install, '--quiet', '--always-copy', 'pip'],
                    filter_stdout=filter_lines, show_stdout=False)
    pip = easy_install = os.path.abspath(join(home_dir, bin,'pip'))
    
    # checkout courant
    if os.path.exists(options.courant_source):
        source = os.path.abspath(options.courant_source)
    else:
        source = options.courant_source
    logger.notify("Installing courant... (from %s)" % source)
    call_subprocess([pip, '-q', 'install', '-E', env_dir, '-e', source],
                    filter_stdout=filter_lines, show_stdout=False)
    
    # install requirements
    if options.requirements:
        logger.notify("Installing external dependencies... (warning: could take awhile)")
        if os.path.exists(source):
            # local copy, so we need to use that path
            requirements_dir = join(source, 'setup')
        else:
            # remote copy, which pip will have installed
            requirements_dir = join(src_dir, 'courant', 'setup')
        call_subprocess([pip, '-q', 'install', '-E', env_dir, '-r', join(requirements_dir, 'external_libs.txt')],
                        filter_stdout=filter_lines, show_stdout=False)
    else:
        logger.notify("Skipping external dependencies...")
    
    # if supplied, checkout site's project
    logger.notify("Creating site project...")
    if options.project_source:
        template_dir = os.path.abspath(join(src_dir, 'courant', 'courant', 'projects', options.project_source))
        
        # determine whether this is a local repo, a template, or a remote repo
        isTemplate = False
        if os.path.exists(options.project_source):
            psource = os.path.abspath(options.project_source)
        elif os.path.exists(template_dir):
            psource = template_dir
            isTemplate = True
        else:
            psource = options.project_source
            
        logger.indent += 4
        
        if not isTemplate:
            logger.notify("Installing site project... (from %s)" % psource)
            call_subprocess([pip, '-q', 'install', '-E', env_dir, '-e', "%s#egg=%s" % (psource, options.project_name),
                             '--src=%s' % env_dir,
                             '--no-install'],
                            filter_stdout=filter_lines, show_stdout=False)
        else:
            if os.path.exists(template_dir):
                logger.notify("Copying template '%s'..." % options.project_source)
                target_dir = join(env_dir, options.project_name)
                
                if os.path.exists(target_dir):
                    logger.notify('Project folder already exists. Skipping...')
                else:
                    # if the desired template is not under source control, we can just copy it over
                    if not '.svn' in os.listdir(template_dir):
                        shutil.copytree(template_dir, target_dir)
                    else:
                        # otherwise we need to export it from the repo
                        process = subprocess.Popen(["svn", "info", template_dir], stdout=subprocess.PIPE)
                        output = process.communicate()[0].split('\n')
                        template_url = None
        
                        for line in output:
                            if line.startswith('URL:'):
                                template_url = line.split(': ')[1].strip('\r').strip()
                        if template_url:
                            p = subprocess.Popen(["svn", "export", template_url, target_dir], stdout=subprocess.PIPE)
                            p.wait()
                        else:
                            logger.notify("Error: could not determine URL of project template")
            else:
                logger.notify("Error: specified template '%s' does not exist in %s" % (options.project_source, template_dir))
        logger.indent -= 4

    logger.notify("Finished!")
    
def filter_lines(line):
    if not line.strip():
        return Logger.DEBUG
    for prefix in ['Searching for', 'Reading ', 'Best match: ', 'Processing ',
                   'Moving ', 'Adding ', 'running ', 'writing ', 'Creating ',
                   'creating ', 'Copying ', 'warning: manifest_maker',
                   'zip_safe flag not set', 'Installed', 'Finished']:
        if line.startswith(prefix):
            return Logger.DEBUG
    for suffix in ['module references __file__', 'module references __path__',
                   'inspect.getsourcefile']:
        if line.endswith(suffix):
            return Logger.DEBUG
    return Logger.NOTIFY