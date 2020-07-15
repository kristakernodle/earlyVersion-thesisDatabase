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

test_blind_review_reviewers_seed = [
    ('reviewer', 'one', '/blind/review/reviewer_one/toScore', '/blind/review/reviewer_one/Scored'),
    ('reviewer', 'two', '/blind/review/reviewer_two/toScore', '/blind/review/reviewer_two/Scored')]

test_session_table_seed = {(9990, 'test-experiment-one'):
                               [(20200502, '/exp/one/dir/9990/20200502_S1'),
                                (20200503, '/exp/one/dir/9990/20200503_S2'),
                                (20200504, '/exp/one/dir/9990/20200504_S3')],
                           (9991, 'test-experiment-two'):
                               [(20200516, '/exp/two/dir/9991/20200516_S1'),
                                (20200517, '/exp/two/dir/9991/20200517_S2'),
                                (20200518, '/exp/two/dir/9991/20200518_S3')],
                           (9992, 'test-experiment-one'):
                               [(20200502, '/exp/one/dir/9992/20200502_S1'),
                                (20200503, '/exp/one/dir/9992/20200503_S2'),
                                (20200504, '/exp/one/dir/9992/20200504_S3')],
                           (9993, 'test-experiment-two'):
                               [(20200516, '/exp/two/dir/9993/20200516_S1'),
                                (20200517, '/exp/two/dir/9993/20200517_S2'),
                                (20200518, '/exp/two/dir/9993/20200518_S3')],
                           (9994, 'test-experiment-one'):
                               [(20200502, '/exp/one/dir/9994/20200502_S1'),
                                (20200503, '/exp/one/dir/9994/20200503_S2'),
                                (20200504, '/exp/one/dir/9994/20200504_S3')],
                           (9995, 'test-experiment-two'):
                               [(20200516, '/exp/two/dir/9995/20200516_S1'),
                                (20200517, '/exp/two/dir/9995/20200517_S2'),
                                (20200518, '/exp/two/dir/9995/20200518_S3')],
                           (9996, 'test-experiment-one'):
                               [(20200502, '/exp/one/dir/9996/20200502_S1'),
                                (20200503, '/exp/one/dir/9996/20200503_S2'),
                                (20200504, '/exp/one/dir/9996/20200504_S3')],
                           (9997, 'test-experiment-two'):
                               [(20200516, '/exp/two/dir/9997/20200516_S1'),
                                (20200517, '/exp/two/dir/9997/20200517_S2'),
                                (20200518, '/exp/two/dir/9997/20200518_S3')],
                           (9998, 'test-experiment-one'):
                               [(20200502, '/exp/one/dir/9998/20200502_S1'),
                                (20200503, '/exp/one/dir/9998/20200503_S2'),
                                (20200504, '/exp/one/dir/9998/20200504_S3')],
                           (9999, 'test-experiment-two'):
                               [(20200516, '/exp/two/dir/9999/20200516_S1'),
                                (20200517, '/exp/two/dir/9999/20200517_S2'),
                                (20200518, '/exp/two/dir/9999/20200518_S3')],
                           }
