"""Idempotency and corner case tests"""

import allure
import pytest
import concurrent.futures
import random


@allure.feature("Idempotency and Corner Cases")
class TestIdempotency:
    @allure.title("C-01: Repeated POST with same data - different IDs")
    @pytest.mark.idempotency
    def test_create_same_ad_twice(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Same Ad",
            "price": 1000,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        first = api_client.create_ad(data)
        second = api_client.create_ad(data)

        first_id = first.get("id") or first.get("ad_id")
        second_id = second.get("id") or second.get("ad_id")

        assert first_id is not None, "First ad has no ID"
        assert second_id is not None, "Second ad has no ID"
        assert first_id != second_id, "Should create different ads with different IDs"

    @allure.title("C-02: GET idempotency")
    @pytest.mark.idempotency
    def test_get_idempotent(self, api_client, unique_seller_id):
        # Create ad
        data = {
            "sellerId": unique_seller_id,
            "name": "Idempotent Test",
            "price": 1000,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        create_response = api_client.create_ad(data)
        ad_id = create_response.get("id") or create_response.get("ad_id")
        assert ad_id, "Failed to create test ad"

        first = api_client.get_ad_by_id(ad_id)
        second = api_client.get_ad_by_id(ad_id)

        # Remove timestamp fields if they exist
        for field in ["createdAt", "updatedAt"]:
            first.pop(field, None)
            second.pop(field, None)

        assert first == second, "Multiple GET requests should return identical data"

    @allure.title("C-04: Concurrent advertisement creation")
    @pytest.mark.idempotency
    def test_concurrent_creation(self, api_client, unique_seller_id):
        def create():
            data = {
                "sellerId": unique_seller_id,
                "name": f"Concurrent {random.randint(1, 10000)}",
                "price": 1000,
                "likes": 0,
                "viewCount": 0,
                "contacts": 0,
            }
            return api_client.create_ad(data)

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create) for _ in range(3)]
            results = [f.result() for f in futures]

        ids = [r.get("id") or r.get("ad_id") for r in results]
        valid_ids = [i for i in ids if i is not None]
        assert len(set(valid_ids)) == len(valid_ids), "Duplicate IDs detected"

    @allure.title("C-10: Extra fields in JSON are ignored")
    @pytest.mark.corner
    def test_extra_fields_ignored(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Test",
            "price": 1000,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
            "extraField": "should be ignored",
            "anotherExtra": 12345,
        }
        response = api_client.create_ad(data)
        assert "id" in response or "ad_id" in response, "Creation should succeed"
