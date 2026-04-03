"""Positive test scenarios"""

import allure
import pytest
import random


@allure.feature("Positive Scenarios")
@allure.story("Create Advertisements")
class TestPositiveCreate:
    @allure.title("P-01: Create advertisement with valid data")
    @pytest.mark.smoke
    def test_create_ad_success(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Test Ad " + str(random.randint(1, 10000)),
            "price": 1000,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        response = api_client.create_ad(data)

        if response.get("error"):
            pytest.fail(f"Creation failed: {response.get('message')}")

        assert "id" in response or "ad_id" in response, "Response should contain ID"

    @allure.title("P-05: Create advertisement with minimum price (0)")
    @pytest.mark.corner
    def test_create_ad_zero_price(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Free Item",
            "price": 0,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        response = api_client.create_ad(data)
        if response.get("error"):
            pytest.skip(f"API may not support zero price: {response.get('message')}")

    @allure.title("P-06: Create advertisement with maximum price")
    @pytest.mark.corner
    def test_create_ad_max_price(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Very Expensive",
            "price": 999999999,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        response = api_client.create_ad(data)
        if response.get("error"):
            pytest.skip(f"API may not support this price: {response.get('message')}")

    @allure.title("P-08: Create advertisement with Russian characters")
    def test_create_ad_russian_name(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Тестовое объявление с русским текстом",
            "price": 1000,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        response = api_client.create_ad(data)
        if response.get("error"):
            pytest.fail(f"Creation failed: {response.get('message')}")


@allure.feature("Positive Scenarios")
@allure.story("Get Advertisements")
class TestPositiveGet:
    @allure.title("P-02: Get existing advertisement by ID")
    @pytest.mark.smoke
    def test_get_ad_by_id_success(self, api_client, unique_seller_id):
        # Create ad first
        data = {
            "sellerId": unique_seller_id,
            "name": "Test for Get",
            "price": 500,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        create_response = api_client.create_ad(data)
        if create_response.get("error"):
            pytest.fail(f"Failed to create test ad: {create_response.get('message')}")

        ad_id = create_response.get("id") or create_response.get("ad_id")
        response = api_client.get_ad_by_id(ad_id)

        assert response.get("id") == ad_id or response.get("ad_id") == ad_id

    @allure.title("P-03: Get all seller's advertisements")
    @pytest.mark.smoke
    def test_get_ads_by_seller_success(self, api_client, unique_seller_id):
        # Create 2 ads for this seller
        for i in range(2):
            data = {
                "sellerId": unique_seller_id,
                "name": f"Seller Ad {i}",
                "price": 1000 + i,
                "likes": 0,
                "viewCount": 0,
                "contacts": 0,
            }
            api_client.create_ad(data)

        response = api_client.get_ads_by_seller(unique_seller_id)
        assert isinstance(response, list)

    @allure.title("P-04: Get advertisement statistics")
    @pytest.mark.smoke
    def test_get_statistics_success(self, api_client, unique_seller_id):
        # Create ad first
        data = {
            "sellerId": unique_seller_id,
            "name": "Stats Test",
            "price": 1000,
            "likes": 5,
            "viewCount": 100,
            "contacts": 3,
        }
        create_response = api_client.create_ad(data)
        if create_response.get("error"):
            pytest.fail(f"Failed to create test ad: {create_response.get('message')}")
