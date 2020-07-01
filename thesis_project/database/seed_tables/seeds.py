import utilities as util

birthdate1 = util.convert_date_int_yyyymmdd(20200101)
birthdate2 = util.convert_date_int_yyyymmdd(20200102)
start1 = util.convert_date_int_yyyymmdd(20200501)
end1 = util.convert_date_int_yyyymmdd(20200601)
start2 = util.convert_date_int_yyyymmdd(20200515)
end2 = util.convert_date_int_yyyymmdd(20200615)
test_mouse_table_seed = [(9990, birthdate2, 'wild type', 'male', True, 'test experiment one', start1, end1),
                         (9991, birthdate1, 'wild type', 'male', False, 'test experiment two', start2, end2),
                         (9992, birthdate1, 'wild type', 'male', True, 'test experiment one', start1, end1),
                         (9993, birthdate1, 'wild type', 'male', False, 'test experiment two', start2, end2),
                         (9994, birthdate1, 'wild type', 'female', True, 'test experiment one', start1, end1),
                         (9995, birthdate1, 'wild type', 'female', False, 'test experiment two', start2, end2),
                         (9996, birthdate1, 'knock out', 'female', True, 'test experiment one', start1, end1),
                         (9997, birthdate1, 'knock out', 'female', False, 'test experiment two', start2, end2),
                         (9998, birthdate1, 'knock out', 'female', True, 'test experiment one', start1, end1),
                         (9999, birthdate2, 'knock out', 'female', False, 'test experiment two', start2, end2)]

exp_one = ('test experiment one', '/test/directory/experiment/one')
exp_two = ('test experiment two', '/test/directory/experiment/two')

test_session_table_seed = {(9990, 'test-experiment-one'):
                               [(20200502, '/exp/one/trial/dir/9990/Training/20200502'),
                                (20200503, '/exp/one/trial/dir/9990/Training/20200503'),
                                (20200504, '/exp/one/trial/dir/9990/Training/20200504')],
                           (9991, 'test-experiment-two'):
                               [(20200516, '/exp/two/trial/dir/9991/Training/20200516'),
                                (20200517, '/exp/two/trial/dir/9991/Training/20200517'),
                                (20200518, '/exp/two/trial/dir/9991/Training/20200518')],
                           (9992, 'test-experiment-one'):
                               [(20200502, '/exp/one/trial/dir/9992/Training/20200502'),
                                (20200503, '/exp/one/trial/dir/9992/Training/20200503'),
                                (20200504, '/exp/one/trial/dir/9992/Training/20200504')],
                           (9993, 'test-experiment-two'):
                               [(20200516, '/exp/two/trial/dir/9993/Training/20200516'),
                                (20200517, '/exp/two/trial/dir/9993/Training/20200517'),
                                (20200518, '/exp/two/trial/dir/9993/Training/20200517')],
                           (9994, 'test-experiment-one'):
                               [(20200502, '/exp/one/trial/dir/9994/Training/20200502'),
                                (20200503, '/exp/one/trial/dir/9994/Training/20200503'),
                                (20200504, '/exp/one/trial/dir/9994/Training/20200504')],
                           (9995, 'test-experiment-two'):
                               [(20200516, '/exp/two/trial/dir/9995/Training/20200516'),
                                (20200517, '/exp/two/trial/dir/9995/Training/20200517'),
                                (20200518, '/exp/two/trial/dir/9995/Training/20200518')],
                           (9996, 'test-experiment-one'):
                               [(20200502, '/exp/one/trial/dir/9996/Training/20200502'),
                                (20200503, '/exp/one/trial/dir/9996/Training/20200503'),
                                (20200504, '/exp/one/trial/dir/9996/Training/20200504')],
                           (9997, 'test-experiment-two'):
                               [(20200516, '/exp/two/trial/dir/9997/Training/20200516'),
                                (20200517, '/exp/two/trial/dir/9997/Training/20200517'),
                                (20200518, '/exp/two/trial/dir/9997/Training/20200518')],
                           (9998, 'test-experiment-one'):
                               [(20200502, '/exp/one/trial/dir/9998/Training/20200502'),
                                (20200503, '/exp/one/trial/dir/9998/Training/20200503'),
                                (20200504, '/exp/one/trial/dir/9998/Training/20200504')],
                           (9999, 'test-experiment-two'):
                               [(20200516, '/exp/two/trial/dir/9999/Training/20200516'),
                                (20200517, '/exp/two/trial/dir/9999/Training/20200517'),
                                (20200518, '/exp/two/trial/dir/9999/Training/20200518')],
                           }

test_blind_review_reviewers_seed = [
    ('reviewer', 'one', '/blind/review/reviewer_one/toScore', '/blind/review/reviewer_one/Scored'),
    ('reviewer', 'two', '/blind/review/reviewer_two/toScore', '/blind/review/reviewer_two/Scored')]
