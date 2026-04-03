"""API Client for Avito Advertisement Service"""

import requests
import allure
from typing import Dict, Any, List, Union


class ApiClient:
    """Client for Avito API"""

    BASE_URL = "https://qa-internship.avito.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Avito-Tests/1.0",
            }
        )

    @allure.step("POST /api/1/item - Create advertisement")
    def create_ad(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new advertisement"""
        response = self.session.post(f"{self.BASE_URL}/api/1/item", json=data)
        if response.status_code != 200:
            # Don't raise, return error info for debugging
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text,
            }
        result = response.json()
        # API may return different ID field names
        if isinstance(result, dict):
            if "id" not in result and "ad_id" in result:
                result["id"] = result["ad_id"]
        return result

    @allure.step("GET /api/1/item/{id} - Get advertisement")
    def get_ad_by_id(self, ad_id: str) -> Union[Dict[str, Any], List]:
        """Get advertisement by ID"""
        response = self.session.get(f"{self.BASE_URL}/api/1/item/{ad_id}")
        if response.status_code == 404:
            return {"error": "not_found", "status_code": 404}
        if response.status_code != 200:
            return {
                "error": f"HTTP {response.status_code}",
                "status_code": response.status_code,
            }
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return data

    @allure.step("GET /api/1/{sellerId}/item - Get seller's advertisements")
    def get_ads_by_seller(self, seller_id: int) -> List[Dict[str, Any]]:
        """Get all advertisements by seller ID"""
        response = self.session.get(f"{self.BASE_URL}/api/1/{seller_id}/item")
        if response.status_code == 404:
            return []
        if response.status_code != 200:
            return []
        data = response.json()
        return data if isinstance(data, list) else []

    @allure.step("GET /api/1/statistic/{id} - Get statistics")
    def get_statistics(self, ad_id: str) -> Dict[str, Any]:
        """Get statistics by advertisement ID"""
        response = self.session.get(f"{self.BASE_URL}/api/1/statistic/{ad_id}")
        if response.status_code == 404:
            return {"error": "not_found"}
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return data

    @allure.step("Raw request without assertions")
    def raw_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Execute raw request for negative testing"""
        url = f"{self.BASE_URL}{endpoint}"
        return self.session.request(method, url, **kwargs)
