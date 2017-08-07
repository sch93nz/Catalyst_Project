import unittest
import user_upload as up

class test_class(unittest.TestCase):
    """This is a test class to see how 
    well the email validation works"""

    def test_valid_emails(self):
        """This checks that the list of valid emails will be passed"""
        with open("valid.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if not up.check_email(line, "test", "case"):
                    print line
                self.assertTrue(up.check_email(line, "test", "case"))

    def test_invalid_emails(self):
        """This checks that the emails that should fail will faill"""
        with open("invalid.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if up.check_email(line, "test", "case"):
                    print line
                self.assertFalse(up.check_email(line, "test", "case"))
                
if __name__ == '__main__':
    unittest.main()
