from models.participant_details import ParticipantDetails
from models.trials import Trial
from models.experiments import list_all_experiments, Experiment
from database.cursors import Cursor
from models.mouse import Mouse


######################
# TODO: TDD for main
######################


def list_participants(experiment_name='all'):
    if experiment_name == 'all':
        all_participants = dict()
        with Cursor() as cursor:
            all_experiments = list_all_experiments(cursor)
        for experiment_name in all_experiments:
            all_participants[experiment_name] = sorted(set((Mouse.from_db_by_id(mouse_id).eartag
                                                            for mouse_id in list_participants(experiment_name))),
                                                       key=int)
        return all_participants
    experiment_participant_details = ParticipantDetails.list_participants(experiment_name)
    return sorted(set(experiment_participant_details), key=int)


def main():
    """ Main program """
    # Code goes over here.
    return 0


if __name__ == "__main__":
    main()
