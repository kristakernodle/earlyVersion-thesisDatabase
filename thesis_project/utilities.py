import yaml


def read_project_config(yaml_full_path):
    with open(yaml_full_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['database_config_dir']
