"""

fibonacci(7): 13
fibonacci(30): 832040
fibonacci(365): 8531073606282249384383143963212896619394786170594625964346924608389878465365
fibonacci(720): 1323171012053243520828784042795469593341319770463238313551473338336502410952765153371119398122747569819754164672344667591018783803781288766524146031040
fibonacci(1440): 3914866508431471361148793987953607300088428753972908501657382404690211361501063264625978882315580290519447457728293373764066788584024069398800428459770142350811894770729873194010281749733661407513804651252026669135283792063431807004225506814702922160621247026028619389629299722842113162285992338142080
fibonacci(1800): 6733912172802933472606353001846945074658287378884326089477601632746080275952604203199580265153593862390858117766432295498560989719530281829452850286454536277301941625978000791367655413469297462257623927534855511388238610890658838439857922737938956952361558179389004339772497124977152035343580348215676156404424782380266118900316342135562815217465023272599528784782167145877600

"""

from unittest import TestCase, main
from mr_fibonacci import fibonacci, generate_tweet_text


class TestFibonacciGenerator(TestCase):

    def test_fibonacci_for_n_0(self):
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_for_n_7(self):
        self.assertEqual(fibonacci(7), 13)

    def test_fibonacci_for_n_365(self):
        self.assertEqual(fibonacci(365), 8531073606282249384383143963212896619394786170594625964346924608389878465365)

    def test_fibonacci_for_n_1800(self):
        self.assertEqual(fibonacci(1800), 6733912172802933472606353001846945074658287378884326089477601632746080275952604203199580265153593862390858117766432295498560989719530281829452850286454536277301941625978000791367655413469297462257623927534855511388238610890658838439857922737938956952361558179389004339772497124977152035343580348215676156404424782380266118900316342135562815217465023272599528784782167145877600)

    def test_fibonacci_for_not_equal(self):
        self.assertNotEqual(fibonacci(7), 7)


class TestFibonacciWithFileReadWrite(TestCase):

    def setUp(self):
        with open('tests/n_remained.txt') as test_file:
            self.n = int(test_file.read().strip())

    def tearDown(self):
        self.n += 1

        with open('tests/n_remained.txt', 'w') as test_file:
            test_file.write(str(self.n))

    def test_fibonacci_from_file_for_n_0(self):
        self.assertEqual(fibonacci(self.n), 0)

    def test_fibonacci_from_file_for_n_1(self):
        self.assertEqual(fibonacci(self.n), 1)

    def test_fibonacci_from_file_for_n_2(self):
        self.assertEqual(fibonacci(self.n), 1)

    def test_fibonacci_from_file_for_n_3(self):
        self.assertEqual(fibonacci(self.n), 2)

    def test_fibonacci_from_file_for_n_4(self):
        self.assertEqual(fibonacci(self.n), 3)
        self.n = -1


class TestFibonacciTweetGenerator(TestCase):

    def test_fibonacci_tweet_generator_for_0(self):
        fib_0 = fibonacci(0)
        tweet_text = '{} for n = {}'.format(fib_0, 0)
        self.assertEqual(generate_tweet_text(0, fib_0), tweet_text)

    def test_fibonacci_tweet_generator_for_7(self):
        fib_7 = fibonacci(7)
        tweet_text = '{} for n = {}'.format(fib_7, 7)
        self.assertEqual(generate_tweet_text(7, fib_7), tweet_text)

    def test_fibonacci_tweet_generator_for_30(self):
        fib_30 = fibonacci(30)
        tweet_text = '{} for n = {}'.format(fib_30, 30)
        self.assertEqual(generate_tweet_text(30, fib_30), tweet_text)

    def test_fibonacci_tweet_generator_for_character_limit_rtype(self):
        fib_1440 = fibonacci(1440)
        self.assertIsInstance(generate_tweet_text(1440, fib_1440), tuple)

    def test_fibonacci_tweet_generator_for_character_limit_split(self):
        fib_1440 = fibonacci(1440)
        tweet_text = generate_tweet_text(1440, fib_1440)
        self.assertEqual(tweet_text[0], str(fib_1440)[:260])
        self.assertEqual(tweet_text[1], str(fib_1440)[260:] + ' for n = 1440')
        self.assertEqual(len(tweet_text[0]), 260)


if __name__ == '__main__':
    main()
