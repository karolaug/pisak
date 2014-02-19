import unittest
import tempfile
import shutil
from pisak_view import model

class LibraryTest(unittest.TestCase):
    def setUp(self):
        self.library_path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.library_path)

        
class LibraryUsageTest(LibraryTest):
    TEST_IMAGE = ("hon/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgFBgcGBQgHBgcJCAgJDBMMDA"
        "sLDBgREg4THBgdHRsYGxofIywlHyEqIRobJjQnKi4vMTIxHiU2OjYwOiwwMTD"
        "/wAALCAAgACABAREA/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAA"
        "AAAAAAAAAAAAAAAA/9oACAEBAAA/AL+AAAAA/9k=")

    def test_create(self):
        new_library = model.create_library(self.library_path)
        self.assertIsInstance(len(new_library.categories), int)
        new_library.scan()
        new_library.close()


class LibraryConfictTest(LibraryTest):
    def test_double_create(self):
        new_library = model.create_library(self.library_path)
        try:
            self.assertRaises(model.LibraryException, model.create_library, self.library_path)
        finally:
            new_library.close()


if __name__ == '__main__':
    unittest.main()
