def create_resources(resource_class, paths):
    for path in paths:
        resource = resource_class(path)
        resource.create()


def delete_resources(resource_class, paths):
    for path in paths:
        resource = resource_class(path)
        resource.delete()


def rename_resource(resource_class, path, new_path):
    resource = resource_class(path)
    resource.move(new_path)
