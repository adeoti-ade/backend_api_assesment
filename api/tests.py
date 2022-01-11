from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APIClient
from .utils import create_account_with_phone_numbers

from django.urls import reverse

class InboundTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("api:inbound")
        self.client = APIClient()
        user = create_account_with_phone_numbers()
        self.client.force_authenticate(user=user)
        self.data = {
                "_to": "08133703766",
                "_from": "4924195509198",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        cache.clear()
    
    def test_success_request(self):
        response = self.client.post(self.url, data=self.data)
        response_message = response.data["message"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_message, "inbound sms ok")

    def test_no_to_parameter(self):
        self.data.pop("_to")
        response = self.client.post(self.url, data=self.data)
        error_response = response.data["errors"]["_to"][0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_response, "_to is missing")

    def test_invalid_to_parameter(self):
        self.data["_to"] = ""
        response = self.client.post(self.url, data=self.data)
        error_response = response.data["errors"]["_to"][0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_response, "_to is invalid")

    def test_to_not_found_for_user(self):
        self.data["_to"] = "362728262"
        response = self.client.post(self.url, data=self.data)
        error_response = response.data["errors"]["_to"][0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_response, "_to parameter not found")

    def test_to_from_pair_save_to_cache(self):
        self.client.post(self.url, data=self.data)
        cache_value = cache.get(self.data["_to"])
        self.assertEqual(cache_value, self.data["_from"])


class OutBoundTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("api:outbound")
        self.client = APIClient()
        user = create_account_with_phone_numbers()
        self.client.force_authenticate(user=user)
        cache.clear()
    
    def test_success_request(self):
        data = {
                "_to": "1234556778",
                "_from": "08133703766",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        response = self.client.post(self.url, data=data)
        response_message = response.data["message"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_message, "outbound sms ok")

    def test_no_from_parameter(self):
        data = {
                "_to": "4924195509198",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        response = self.client.post(self.url, data=data)
        error_response = response.data["errors"]["_from"][0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_response, "_from is missing")

    def test_invalid_from_parameter(self):
        data = {
                "_to": "4924195509198",
                "_from": "",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        response = self.client.post(self.url, data=data)
        error_response = response.data["errors"]["_from"][0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_response, "_from is invalid")

    def test_from_not_found_for_user(self):
        data = {
                "_to": "4924195509198",
                "_from": "234455566",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        response = self.client.post(self.url, data=data)
        error_response = response.data["errors"]["_from"][0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_response, "_from parameter not found")


class InBounDOutBoundTest(TestCase):
    cache.clear()
    def setUp(self) -> None:
        self.outbound_url = reverse("api:outbound")
        self.inbound_url = reverse("api:inbound")
        self.client = APIClient()
        user = create_account_with_phone_numbers()
        self.client.force_authenticate(user=user)
    
    def test_stop_request(self):
        inbound_data = {
                "_to": "08133703766",
                "_from": "4924195509198",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        outbound_data = {
                "_to": "4924195509198",
                "_from": "08133703766",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        inbound_response = self.client.post(self.inbound_url, data=inbound_data)
        outbound_response = self.client.post(self.outbound_url, data=outbound_data)
        self.assertEqual(inbound_response.status_code, 200)
        self.assertEqual(outbound_response.status_code, 400)
        error_response = outbound_response.data["errors"]["_from"][0]
        message = "sms from {_from} to {_to} blocked by STOP request".format(_from=outbound_data["_from"], _to=outbound_data["_to"])
        self.assertEqual(error_response, message)

    def test_limit_reached_request(self):
        create_account_with_phone_numbers("08133703711")
        outbound_data = {
                "_to": "49241955091900",
                "_from": "08133703711",
                "_text": "2627282i12j2nb2g272g2b262g262"
            }
        for _ in range(50):
            outbound_response = self.client.post(self.outbound_url, data=outbound_data)
            self.assertEqual(outbound_response.status_code, 200)
        new_outbound_response = self.client.post(self.outbound_url, data=outbound_data)
        error_response = new_outbound_response.data["errors"]["_from"][0]
        message = "limit reached for from {_from}".format(_from=outbound_data["_from"])
        self.assertEqual(error_response, message)