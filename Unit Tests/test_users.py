import unittest
import Main.user as user

class TestUserMethods(unittest.TestCase):

    def test_user_creation(self):
        u = user.User("john", "doe", "johnd", "password")
        self.assertEqual(u.firstName, "John")
        self.assertEqual(u.lastName, "Doe")
        self.assertEqual(u.username, "johnd")
        self.assertTrue(u.check_password("password"))
        self.assertFalse(u.check_password("wrongpassword"))

    def test_password_hashing(self):
        u = user.User("john", "doe", "johnd", "password")
        self.assertNotEqual(u.password, "password")  # Password should be hashed
        self.assertTrue(u.check_password("password"))

    def test_admin_flag(self):
        u = user.User("admin", "user", "uname", "password", isAdmin=True)
        self.assertTrue(u.isAdmin)
        u2 = user.User("regular", "user", "uname", "password")
        self.assertFalse(u2.isAdmin)

if __name__ == '__main__':
    unittest.main()