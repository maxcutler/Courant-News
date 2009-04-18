from django.db import models
from django.conf import settings
from django.template import Template, Context, loader

from courant.core.search import search

def _get_database_engine():
    if settings.DATABASE_ENGINE == 'mysql':
        return settings.DATABASE_ENGINE
    elif settings.DATABASE_ENGINE.startswith('postgresql'):
        return 'pgsql'
    raise ValueError, "Only MySQL and PostgreSQL engines are supported by Sphinx."

def generate_config():
    t = loader.get_template('sphinx.conf')
    params = {
        'sphinx_port': settings.SPHINX_PORT,
        'db_type': _get_database_engine(),
        'db_host': settings.DATABASE_HOST,
        'db_port': settings.DATABASE_PORT,
        'db_user': settings.DATABASE_USER,
        'db_pass': settings.DATABASE_PASSWORD,
        'db_name': settings.DATABASE_NAME
    }
    
    models = []
    delta_counter = 0
    for model, configs in search._registry.items():
        opts = {}
        opts['name'] = model._meta.verbose_name_plural
        opts['extends'] = 'base'
        
        # get the db column names for the filter fields
        opts['filter_fields'] = []
        if configs['filter_fields']:
            for field in configs['filter_fields']:
                opts['filter_fields'].append(model._meta.get_field(field).column)
        if 'content_type' not in opts['filter_fields']:
            opts['filter_fields'].append('content_type')
            
        # fill in some default fields
        fields = list(configs['fields'])
        if configs['filter_fields']:
            fields.extend(configs['filter_fields'])
        if model._meta.pk.name not in fields:
            fields.insert(0, model._meta.pk.name)
        if configs['date_field'] and configs['date_field'] not in fields:
            fields.append(configs['date_field'])
        
        # add the desired fields to the query
        q = ['SELECT']
        for field in fields:
            column = '%s.%s' % (model._meta.db_table, model._meta.get_field(field).column)
            if field == configs['date_field']:
                if params['db_type'] == 'mysql':
                    q.append('UNIX_TIMESTAMP(%s) as date,' % column)
                elif params['db_type'] == 'pgsql':
                    q.append("date_part('epoch', %s) as date," % column)
            else:
                q.append('%s,' % column)
                
        # if there is no date for a model, we need to give it one
        # so that it shows up in results
        if not configs['date_field']:
            q.append('0 as date, ')
            
        # must store the content type
        q.append('django_content_type.id AS content_type')
        
        # join on the content type table to get the proper content type ids
        q.append("FROM %s INNER JOIN django_content_type ON django_content_type.app_label = '%s' AND django_content_type.model = '%s'" % (
            model._meta.db_table, model._meta.app_label, model._meta.module_name
        ))
        
        # make the query into a string
        opts['query'] = ' '.join(q)
            
        # if we want delta indexes, we have to modify this entry
        # and add a second entry for the delta index itself
        if configs['use_delta']:
            delta_counter += 1
            
            opts_delta = opts.copy()
            opts_delta['name'] += '_delta'
            opts_delta['extends'] = opts['name']
            
            opts['pre_query'] = 'UPDATE sphinx_counter SET max_doc_id = (SELECT COUNT(*) FROM %s) WHERE counter_id = %d' % (model._meta.db_table, delta_counter)
            opts['query'] += ' WHERE %s.id<=( SELECT max_doc_id FROM sphinx_counter WHERE counter_id=%d )' % (model._meta.db_table, delta_counter)
            opts_delta['query'] += ' WHERE %s.id>( SELECT max_doc_id FROM sphinx_counter WHERE counter_id=%d )' % (model._meta.db_table, delta_counter)
            
            models.append(opts)
            models.append(opts_delta)
        else:
            models.append(opts)
    params['models'] = models
    
    c = Context(params)
    return t.render(c)
    
