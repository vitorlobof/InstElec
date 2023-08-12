import importlib


def import_by_full_name(class_path):
    module_path, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    
    class_object = getattr(module, class_name)
    return class_object
