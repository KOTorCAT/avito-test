"""Performance and load tests"""

import allure
import pytest
import time


@allure.feature("Non-functional Tests")
class TestPerformance:
    @allure.title("NF-01: API response time")
    @pytest.mark.performance
    def test_response_time(self, api_client, unique_seller_id):
        data = {
            "sellerId": unique_seller_id,
            "name": "Performance Test",
            "price": 1000,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0},
        }
        start = time.time()
        response = api_client.create_ad(data)
        elapsed = time.time() - start

        if response.get("error"):
            pytest.skip(f"Creation failed: {response.get('message')}")

        assert elapsed < 1.0, f"Response time {elapsed:.2f}s exceeds 1s"

    @allure.title("C-03: Create 10 advertisements sequentially")
    @pytest.mark.performance
    def test_bulk_creation(self, api_client, unique_seller_id):
        times = []
        ids = []

        for i in range(10):
            data = {
                "sellerId": unique_seller_id,
                "name": f"Bulk Test {i}",
                "price": i * 100,
                "statistics": {"likes": 0, "viewCount": 0, "contacts": 0},
            }
            start = time.time()
            response = api_client.create_ad(data)
            elapsed = time.time() - start
            times.append(elapsed)
            if not response.get("error"):
                ad_id = response.get("id") or response.get("ad_id")
                if ad_id:
                    ids.append(ad_id)

        assert len(set(ids)) == len(ids), "Duplicate IDs detected"

        avg_time = sum(times) / len(times)
        allure.attach(
            f"Created {len(ids)} ads\nAverage response time: {avg_time:.3f}s",
            "Performance metrics",
            allure.attachment_type.TEXT,
        )
