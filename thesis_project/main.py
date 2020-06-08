from models.experiments import Experiments as Experiments
from models.mouse import Mouse as Mouse
from models.participant_details import ParticipantDetails as ParticipantDetails
from models.trials import Trials as Trials


######################
# TODO: TDD for main
######################

# TODO: make the experiment_name default = 'all'
#   and return dictionary {experiment_name: list(unique eartags)}
def list_participants(experiment_name):
    experiment_participant_details = ParticipantDetails.list_participants(experiment_name)
    experiment_trials = Trials.list_participants(experiment_name)
    return sorted(set(experiment_participant_details).union(experiment_trials), key=int)


def main():
    """ Main program """
    # Code goes over here.
    return 0


if __name__ == "__main__":
    main()
