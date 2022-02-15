from rest_framework import status
from rest_framework.test import APITestCase

doctor_data = {
    "email": "",
    "username": "test_doctor",
    "address": "",
    "phone": "+989021110787",
    "first_name": "doc",
    "last_name": "docdoc",
    "password": "doc1234",
    "confirm_password": "doc1234",
    "is_patient": 0,
    "is_doctor": 1,
}
patient_data = {
    "email": "",
    "username": "test_patient",
    "address": "",
    "phone": "+989011235813",
    "first_name": "pat",
    "last_name": "patpat",
    "password": "pat1234",
    "confirm_password": "pat1234",
    "is_patient": 1,
    "is_doctor": 0,
}
doctor_login = {"username": "test_doctor", "password": "doc1234"}
patient_login = {"username": "test_patient", "password": "pat1234"}


class Tests(APITestCase):
    def test_create_doctor(self):
        response = self.client.post(
            "http://chiron.aeonem.xyz/user/", doctor_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_patient(self):
        response = self.client.post(
            "http://chiron.aeonem.xyz/user/", patient_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_doctor(self):
        self.client.post("http://chiron.aeonem.xyz/user/", doctor_data, format="json")
        response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", doctor_login, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_patient(self):
        self.client.post("http://chiron.aeonem.xyz/user/", patient_data, format="json")
        response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_doctors(self):
        self.client.post("http://chiron.aeonem.xyz/user/", patient_data, format="json")
        self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        response = self.client.get("http://chiron.aeonem.xyz/user/drs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_appointment(self):
        self.client.post("http://chiron.aeonem.xyz/user/", doctor_data, format="json")
        self.client.post("http://chiron.aeonem.xyz/user/", patient_data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        data = {"doctor": "test_doctor", "date": "2021-02-15\t22:21"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        response = self.client.post(
            "http://chiron.aeonem.xyz/appointment/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_approve_appointment(self):
        self.client.post("http://chiron.aeonem.xyz/user/", doctor_data, format="json")
        self.client.post("hhttp://chiron.aeonem.xyz/user/", patient_data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        data = {"doctor": "test_doctor", "date": "2021-02-15\t22:21"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.post("http://chiron.aeonem.xyz/appointment/", data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", doctor_login, format="json"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.get("http://chiron.aeonem.xyz/appointment/")
        response = self.client.post("http://chiron.aeonem.xyz/appointment/1/approve/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_reject_appointment(self):
        self.client.post("http://chiron.aeonem.xyz/user/", doctor_data, format="json")
        self.client.post("http://chiron.aeonem.xyz/user/", patient_data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        data = {"doctor": "test_doctor", "date": "2021-02-15\t22:21"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.post("http://chiron.aeonem.xyz/appointment/", data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", doctor_login, format="json"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.get("http://chiron.aeonem.xyz/appointment/")
        response = self.client.post("http://chiron.aeonem.xyz/appointment/1/reject/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_approved_appointment(self):
        self.client.post("http://chiron.aeonem.xyz/user/", doctor_data, format="json")
        self.client.post("http://chiron.aeonem.xyz/user/", patient_data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        data = {"doctor": "test_doctor", "date": "2021-02-15\t22:21"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.post("http://chiron.aeonem.xyz/appointment/", data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", doctor_login, format="json"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.get("http://chiron.aeonem.xyz/appointment/")
        self.client.post("http://chiron.aeonem.xyz/appointment/1/approve/")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        response = self.client.get("http://chiron.aeonem.xyz/appointment/1/visit/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_rejected_appointment(self):
        self.client.post("http://chiron.aeonem.xyz/user/", doctor_data, format="json")
        self.client.post("http://chiron.aeonem.xyz/user/", patient_data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        data = {"doctor": "test_doctor", "date": "2021-02-15\t22:21"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.post("http://chiron.aeonem.xyz/appointment/", data, format="json")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", doctor_login, format="json"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        self.client.get("http://chiron.aeonem.xyz/appointment/")
        self.client.post("http://chiron.aeonem.xyz/appointment/1/reject/")
        login_response = self.client.post(
            "http://chiron.aeonem.xyz/user/login/", patient_login, format="json"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + login_response.json()["token"]
        )
        response = self.client.get("http://chiron.aeonem.xyz/appointment/1/visit/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
