import unittest
import tempfile
import shutil
import base64
import io
import os.path
from pisak_view import model

class LibraryTest(unittest.TestCase):
    def setUp(self):
        self.library_path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.library_path)

        
class LibraryPhotoTest(LibraryTest):
    TEST_IMAGE = ("/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgFBgcGBQgHBgcJCAgJDBMMDA"
        "sLDBgREg4THBgdHRsYGxofIywlHyEqIRobJjQnKi4vMTIxHiU2OjYwOiwwMTD"
        "/wAALCAAgACABAREA/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAA"
        "AAAAAAAAAAAAAAAA/9oACAEBAAA/AL+AAAAA/9k=")

    def setUp(self):
        super(LibraryPhotoTest, self).setUp()
        test_filename = os.path.join(self.library_path, "test.jpg")
        test_file = open(test_filename, "wb")
        encoded_file = io.StringIO(self.TEST_IMAGE)
        base64.decode(encoded_file, test_file)
        test_file.close()
        encoded_file.close()


class LibraryUsageTest(LibraryPhotoTest):
    def test_create(self):
        new_library = model.create_library(self.library_path)
        try:
            self.assertIsInstance(len(new_library.categories), int)
            new_photos = new_library.scan()
            self.assertEqual(len(new_photos), 1)
            new_photos = new_library.scan()
            self.assertEqual(len(new_photos), 0)
        finally:
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
