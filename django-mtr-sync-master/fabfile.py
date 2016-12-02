from mtr.fabric.local import env, clear, subl, install, docs, recreate, \
    migrate, locale, celery, shell, run, test, manage

env.vars = {
    'apps': [],
    'project': {
        'apps': ['app'],
        'dir':  'tests',
    },
    'docs': 'docs'
}
