"""Negative test scenarios"""

import allure
import pytest


@allure.feature("Negative Scenarios")
class TestNegative:

    @allure.title("N-01: Create advertisement without name field")
    @pytest.mark.regression
    def test_create_ad_missing_name(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "price": 1000,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
        }
        response = api_client.raw_request("POST", "/api/1/item", json=data)
        # API может требовать name
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}"

    @allure.title("N-02: Create advertisement with empty name")
    @pytest.mark.regression
    def test_create_ad_empty_name(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "",
            "price": 1000,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
        }
        response = api_client.raw_request("POST", "/api/1/item", json=data)
        assert response.status_code in [400, 422]

    @allure.title("N-03: Create advertisement with negative price")
    @pytest.mark.regression
    def test_create_ad_negative_price(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Test",
            "price": -100,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
        }
        response = api_client.raw_request("POST", "/api/1/item", json=data)
        assert response.status_code in [400, 422]

    @allure.title("N-04: Create advertisement with price as string")
    @pytest.mark.regression
    def test_create_ad_string_price(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Test",
            "price": "not_a_number",
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
        }
        response = api_client.raw_request("POST", "/api/1/item", json=data)
        assert response.status_code in [400, 422]

    @allure.title("N-06: Get advertisement by non-existent ID")
    @pytest.mark.regression
    def test_get_ad_invalid_id(self, api_client):
        response = api_client.raw_request("GET", "/api/1/item/nonexistent_id_12345")
        # API может возвращать 400 или 404
        assert response.status_code in [400, 404], f"Expected 400/404, got {response.status_code}"

    @allure.title("N-08: Get advertisements with invalid sellerId")
    @pytest.mark.regression
    def test_get_ads_invalid_seller(self, api_client):
        response = api_client.raw_request("GET", "/api/1/invalid_seller/item")
        assert response.status_code in [400, 404]

    @allure.title("N-09: Create advertisement with price = null")
    @pytest.mark.regression
    def test_create_ad_null_price(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Test",
            "price": None,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
        }
        response = api_client.raw_request("POST", "/api/1/item", json=data)
        assert response.status_code in [400, 422]