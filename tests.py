import unittest
import user_upload as up

class test_class(unittest.TestCase):
    
    def test_valid_emails(self):
        with open("valid.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if not up.check_email(line, "test", "case"):
                    print line
                self.assertTrue(up.check_email(line, "test", "case"))

    def test_invalid_emails(self):
        with open("invalid.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if up.check_email(line, "test", "case"):
                    print line
                self.assertFalse(up.check_email(line, "test", "case"))
                
if __name__ == '__main__':
    unittest.main()
