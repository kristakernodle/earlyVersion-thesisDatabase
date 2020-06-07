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

test_trial_table_seed = {(9990, 'test-experiment-one'):
                             [(20200502, '/exp/one/trial/dir/9990/1'),
                              (20200503, '/exp/one/trial/dir/9990/2'),
                              (20200504, '/exp/one/trial/dir/9990/3')],
                         (9991, 'test-experiment-two'):
                             [(20200516, '/exp/two/trial/dir/9991/1'),
                              (20200517, '/exp/two/trial/dir/9991/2'),
                              (20200518, '/exp/two/trial/dir/9991/3')],
                         (9992, 'test-experiment-one'):
                             [(20200502, '/exp/one/trial/dir/9992/1'),
                              (20200503, '/exp/one/trial/dir/9992/2'),
                              (20200504, '/exp/one/trial/dir/9992/3')],
                         (9993, 'test-experiment-two'):
                             [(20200516, '/exp/two/trial/dir/9993/1'),
                              (20200517, '/exp/two/trial/dir/9993/2'),
                              (20200518, '/exp/two/trial/dir/9993/3')],
                         (9994, 'test-experiment-one'):
                             [(20200502, '/exp/one/trial/dir/9994/1'),
                              (20200503, '/exp/one/trial/dir/9994/2'),
                              (20200504, '/exp/one/trial/dir/9994/3')],
                         (9995, 'test-experiment-two'):
                             [(20200516, '/exp/two/trial/dir/9995/1'),
                              (20200517, '/exp/two/trial/dir/9995/2'),
                              (20200518, '/exp/two/trial/dir/9995/3')],
                         (9996, 'test-experiment-one'):
                             [(20200502, '/exp/one/trial/dir/9996/1'),
                              (20200503, '/exp/one/trial/dir/9996/2'),
                              (20200504, '/exp/one/trial/dir/9996/3')],
                         (9997, 'test-experiment-two'):
                             [(20200516, '/exp/two/trial/dir/9997/1'),
                              (20200517, '/exp/two/trial/dir/9997/2'),
                              (20200518, '/exp/two/trial/dir/9997/3')],
                         (9998, 'test-experiment-one'):
                             [(20200502, '/exp/one/trial/dir/9998/1'),
                              (20200503, '/exp/one/trial/dir/9998/2'),
                              (20200504, '/exp/one/trial/dir/9998/3')],
                         (9999, 'test-experiment-two'):
                             [(20200516, '/exp/two/trial/dir/9999/1'),
                              (20200517, '/exp/two/trial/dir/9999/2'),
                              (20200518, '/exp/two/trial/dir/9999/3')],
                         }
