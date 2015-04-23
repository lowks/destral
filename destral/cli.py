import os
import sys
import subprocess
import unittest
import logging

from destral.utils import detect_module
from destral.openerp import OpenERPService


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('destral.cli')


def main():
    service = OpenERPService()
    if len(sys.argv) < 2:
        paths = subprocess.check_output([
            "git", "diff", "--name-only", "HEAD~1..HEAD"
        ])
        paths = [x for x in paths.split('\n') if x]
        modules_to_test = []
        for path in paths:
            module = detect_module(path)
            if module and module not in modules_to_test:
                modules_to_test.append(module)

    else:
        modules_to_test = sys.argv[1:]

    results = []
    for module in modules_to_test:
        req = os.path.join(
            service.config['addons_path'], module, 'requirements.txt'
        )
        pip = os.path.join(sys.prefix, 'bin', 'pip')
        if os.path.exists(req) and os.path.exists(pip):
            logger.info('Requirements file %s found. Installing...', req)
            subprocess.check_call([pip, "install", "-r", req])
        logger.info('Testing module %s', module)
        os.environ['OOTEST_MODULE'] = module
        tests_module = 'addons.{}.tests'.format(module)
        logger.debug('Test module: %s', tests_module)
        try:
            suite = unittest.TestLoader().loadTestsFromName(tests_module)
        except AttributeError, e:
            logger.debug('Test suits not found...%s', e)
            suite = unittest.TestSuite()
        if not suite.countTestCases():
            suite = unittest.TestLoader().loadTestsFromName('destral.testing')
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            results.append(False)
        else:
            results.append(True)

    if not all(results):
        sys.exit(1)



if __name__ == '__main__':
    main()
