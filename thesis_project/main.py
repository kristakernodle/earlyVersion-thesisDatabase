import blind_review
import project_config
import utilities as util
import thesis_database

project_config_folder_path = project_config.__path__._path


def get_database_config(project_name):
    project_config = f"{project_config_folder_path[0]}/{project_name}_project_config.yaml"
    return util.read_project_config(project_config)


def update_project_database(project_name):
    database_config_path = get_database_config(project_name)
    db_details, _, main_user, _ = thesis_database.utilities.read_config(database_config_path)
    # thesis_database.populate_from_files.populate_db_from_back_up_csv(db_details, main_user)
    thesis_database.update_from_data_dirs(db_details, main_user)


def main():
    project_name = input("Project name: ")
    update = input(f"Do you want to update the database for {project_name}? [y/N]: ")

    if update.lower() in ['y', 'yes', 't', 'true', '1']:
        update_project_database(project_name)
    else:
        print("Project not updated")


if __name__ == '__main__':
    main()
