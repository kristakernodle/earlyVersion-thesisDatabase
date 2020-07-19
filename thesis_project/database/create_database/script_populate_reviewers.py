from models.reviewers import Reviewer

from database.database import Database
from data.constants import dbDetails, dbUser_Krista

Database.initialize(**dbDetails, **dbUser_Krista)

Reviewer('Krista', 'K',
         '/Users/Krista/Desktop/blindScoring/Krista_K/toScore_KK',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Krista_K/Scored_KK').save_to_db()

Reviewer('Jen', 'M',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Jen_M/toScore_JM',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Jen_M/Scored_JM').save_to_db()

Reviewer('Dan', 'L',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Dan_L/toScore_DL',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Dan_L/Scored_DL').save_to_db()

Reviewer('Alli', 'B',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_B/toScore_AB',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_B/Scored_AB').save_to_db()

Reviewer('Alli', 'C',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_C/toScore_AC',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Alli_C/Scored_AC').save_to_db()

Reviewer('Kenny', 'F',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Kenny_F/toScore_KF',
         '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/blindedScoring/Kenny_F/Scored_KF').save_to_db()
