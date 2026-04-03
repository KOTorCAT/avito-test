"""End-to-end test scenarios"""

import allure
import pytest


@allure.feature("E2E Scenarios")
class TestE2E:
    @allure.title("F-01: Complete advertisement lifecycle")
    @pytest.mark.smoke
    def test_complete_lifecycle(self, api_client, unique_seller_id):
        # 1. Create ad
        data = {
            "sellerId": unique_seller_id,
            "name": "E2E Test Item",
            "price": 5000,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        create_response = api_client.create_ad(data)
        assert not create_response.get(
            "error"
        ), f"Failed to create ad: {create_response.get('message')}"

        ad_id = create_response.get("id") or create_response.get("ad_id")
        assert ad_id, "Failed to get ad ID"

        # 2. Get ad by ID
        ad = api_client.get_ad_by_id(ad_id)
        assert ad.get("name") == data["name"]
        assert ad.get("price") == data["price"]

        # 3. Get statistics
        stats = api_client.get_statistics(ad_id)
        allure.attach(str(stats), "Statistics", allure.attachment_type.JSON)

        # 4. Get all seller ads
        seller_ads = api_client.get_ads_by_seller(unique_seller_id)
        assert len(seller_ads) >= 1
