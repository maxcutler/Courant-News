import os
import sys

COURANT_SVN_URL = 'svn://code.courantnews.com/courant/trunk'

def extend_parser(parser):
    parser.add_option(
        '-s', '--source',
        metavar='DIR_OR_URL',
        dest='courant_source',
        default=COURANT_SVN_URL,
        help='Location of a svn/git/hg/bzr directory or URL to use for the installation of Courant')
    
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
                    filter_stdout=filter_lines, show_stdout=False,)
    
    # install requirements
    logger.notify("Installing external dependencies...")
    if os.path.exists(source):
        # local copy, so we need to use that path
        requirements_dir = join(source, 'setup')
    else:
        # remote copy, which pip will have installed
        requirements_dir = join(src_dir, 'courant', 'setup')
    call_subprocess([pip, '-q', 'install', '-E', env_dir, '-r', join(requirements_dir, 'external_libs.txt')],
                    filter_stdout=filter_lines, show_stdout=False)
    
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