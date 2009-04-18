from django.core.management.base import LabelCommand
from django.conf import settings

from optparse import make_option
import os

from courant.core.search.utils import generate_config

class Command(LabelCommand):
    option_list = LabelCommand.option_list + (
        make_option('--index','-i', help='If you\'re using this command to index, then you can specify which index to index. Default is --all.'),
    )
    
    config = {
        'searchd': settings.SPHINX_BIN + '/searchd',
        'indexer': settings.SPHINX_BIN + '/indexer',
        'sphinx_conf': ' --config ' + settings.PROJECT_PATH + '/courant/search/sphinx.conf',
        'sphinx_port': ' --port %d' % settings.SPHINX_PORT
    }
        
    def handle_label(self, label, **options):
        if label == 'start':
            os.system(self.config['searchd'] + self.config['sphinx_conf'] + self.config['sphinx_port'])
        elif label == 'stop':
            os.system(self.config['searchd'] + self.config['sphinx_conf'] + ' --stop')
        elif label == 'index':
            if not options['index']:
                options['index'] = '--all'
            os.system(self.config['indexer'] + self.config['sphinx_conf'] + ' ' + options['index'])
            os.system(self.config['indexer'] + self.config['sphinx_conf'] + ' articles --buildstops ' + settings.PROJECT_PATH + '/courant/search/words.txt 10000')
        elif label == 'generate_config':
            file = open(self.config['sphinx_conf'].split()[1], 'w')
            file.write(generate_config())
            file.close()