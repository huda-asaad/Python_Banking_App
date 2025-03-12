import unittest
import os
import csv
from banking import (create_customer_file, generate_account_id, Add_new_customer, 
                      Info, Withdraw, Deposit, Transfer, FILE_NAME)

class TestBankApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """تهيئة الملف قبل بدء الاختبارات."""
        create_customer_file()

    def setUp(self):
        """تهيئة البيانات قبل كل اختبار."""
        self.customer = Add_new_customer("John", "Doe", "password123", 1000.0, 500.0)
        self.customer.save_to_csv()

    def tearDown(self):
        """حذف الملف بعد كل اختبار."""
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)

    def test_create_customer_file(self):
        """اختبار إنشاء ملف العملاء."""
        self.assertTrue(os.path.exists(FILE_NAME))
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            header = next(reader)
            self.assertEqual(header, ["account_id", "first_name", "last_name", "password", 
                                     "balance_checking", "balance_savings", "overdraft_count", "account_status"])

    def test_generate_account_id(self):
        """اختبار إنشاء معرف حساب جديد."""
        account_id = generate_account_id()
        self.assertTrue(account_id.isdigit())
        self.assertGreater(int(account_id), 10000)

    def test_add_new_customer(self):
        """اختبار إضافة عميل جديد."""
        customer = Add_new_customer("Jane", "Doe", "password456", 2000.0, 1000.0)
        customer.save_to_csv()
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
            self.assertEqual(len(rows), 3)  # العنوان + عميلين

    def test_info_load_customer_info(self):
        """اختبار تحميل معلومات العميل."""
        info = Info(self.customer.account_id, "password123")
        self.assertTrue(info.load_customer_info())
        self.assertEqual(info.first_name, "John")
        self.assertEqual(info.last_name, "Doe")
        self.assertEqual(info.balance_checking, 1000.0)
        self.assertEqual(info.balance_savings, 500.0)

    def test_withdraw_success(self):
        """اختبار سحب ناجح."""
        withdraw = Withdraw(self.customer.account_id, "password123", 200.0, "checking")
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
            new_balance = float(rows[1][4])  # الرصيد الجديد للحساب الجاري
            self.assertEqual(new_balance, 800.0)

    def test_withdraw_overdraft(self):
        """اختبار السحب على المكشوف."""
        withdraw = Withdraw(self.customer.account_id, "password123", 1200.0, "checking")
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
            new_balance = float(rows[1][4])  # الرصيد الجديد بعد السحب والرسوم
            self.assertEqual(new_balance, -235.0)  # 1000 - 1200 - 35 = -235

    def test_deposit_success(self):
        """اختبار إيداع ناجح."""
        deposit = Deposit(self.customer.account_id, "password123", 300.0, "checking")
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
            new_balance = float(rows[1][4])  # الرصيد الجديد للحساب الجاري
            self.assertEqual(new_balance, 1300.0)

    def test_transfer_success(self):
        """اختبار تحويل ناجح."""
        customer2 = Add_new_customer("Jane", "Doe", "password456", 2000.0, 1000.0)
        customer2.save_to_csv()
        transfer = Transfer(self.customer.account_id, "password123", customer2.account_id, 500.0, "checking")
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
            sender_balance = float(rows[1][4])  # رصيد المرسل
            receiver_balance = float(rows[2][4])  # رصيد المستقبل
            self.assertEqual(sender_balance, 500.0)  # 1000 - 500 = 500
            self.assertEqual(receiver_balance, 2500.0)  # 2000 + 500 = 2500

if __name__ == '__main__':
    unittest.main()