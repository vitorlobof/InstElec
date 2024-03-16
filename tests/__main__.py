import unittest


def run_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        start_dir='tests', pattern='*.py')

    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    return result


if __name__ == '__main__':
    test_result = run_tests()
