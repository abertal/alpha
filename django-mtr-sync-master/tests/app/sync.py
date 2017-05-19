from mtr.sync.lib.manager import manager


@manager.register('dataset', label='some description')
def some_dataset(model, settings):
    return model.objects.filter(security_level__gte=30)
