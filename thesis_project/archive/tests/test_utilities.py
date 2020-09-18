import datetime
import unittest

from archive import utilities


class TestConvertDateYYYYMMDD(unittest.TestCase):

    def test_isdate(self):
        may182020 = datetime.date(2020, 5, 18)
        out_date = utilities.convert_date_int_yyyymmdd(may182020)
        self.assertEqual(may182020, out_date)

    def test_isint(self):
        may192020 = 20200519
        out_date = utilities.convert_date_int_yyyymmdd(may192020)
        self.assertIsInstance(out_date, datetime.date)
        self.assertEqual(datetime.date(2020, 5, 19), out_date)


class TestDecodeGenotype(unittest.TestCase):

    def test_isstring(self):
        genotype_wt = 'wild type'
        genotype_ko = "knock out"
        decoded_genotype_wt = utilities.decode_genotype(genotype_wt)
        decoded_genotype_ko = utilities.decode_genotype(genotype_ko)
        self.assertEqual('wild type', decoded_genotype_wt)
        self.assertEqual('knock out', decoded_genotype_ko)

    def test_isbool(self):
        genotype_f = False
        genotype_t = True
        decoded_genotype_f = utilities.decode_genotype(genotype_f)
        decoded_genotype_t = utilities.decode_genotype(genotype_t)
        self.assertEqual('wild type', decoded_genotype_f)
        self.assertEqual('knock out', decoded_genotype_t)


class TestEncodeGenotype(unittest.TestCase):

    def test_isbool(self):
        genotype_t = True
        genotype_f = False
        genotype_t = utilities.encode_genotype(genotype_t)
        genotype_f = utilities.encode_genotype(genotype_f)
        self.assertTrue(genotype_t)
        self.assertFalse(genotype_f)

    def test_iswildtype(self):
        genotype = 'wild type'
        encoded_genotype = utilities.encode_genotype(genotype)
        self.assertFalse(encoded_genotype)

    def test_isknockout(self):
        genotype = 'knock out'
        encoded_genotype = utilities.encode_genotype(genotype)
        self.assertTrue(encoded_genotype)


class TestPrepStringForDB(unittest.TestCase):

    def test_spaces_skilledreaching(self):
        strings_to_test = ["skilled reaching", "Skilled Reaching",  "Skilled reaching", "skilled Reaching"]
        for string in strings_to_test:
            self.assertEqual("skilled-reaching", utilities.prep_string_for_db(string))

    def test_underscore_skilledreaching(self):
        strings_to_test = ["skilled_reaching", "Skilled_Reaching", "Skilled_reaching", "skilled_Reaching"]
        for string in strings_to_test:
            self.assertEqual("skilled-reaching", utilities.prep_string_for_db(string))

    def test_dash_skilledreaching(self):
        strings_to_test = ["skilled-reaching", "Skilled-Reaching", "Skilled-reaching", "skilled-Reaching"]
        for string in strings_to_test:
            self.assertEqual("skilled-reaching", utilities.prep_string_for_db(string))

    def test_slash_skilledreaching(self):
        strings_to_test = ["skilled/reaching", "Skilled/Reaching", "Skilled/reaching", "skilled/Reaching"]
        for string in strings_to_test:
            self.assertEqual("skilled-reaching", utilities.prep_string_for_db(string))













if __name__ == '__main__':
    unittest.main()
