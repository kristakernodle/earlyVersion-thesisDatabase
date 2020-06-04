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
test_trial_table_seed = (9990, 'test experiment one',
                         (20200502, '/exp/one/trial/dir/1'),
                         (20200503, '/exp/one/trial/dir/2'),
                         (20200504, '/exp/one/trial/dir/3'))
