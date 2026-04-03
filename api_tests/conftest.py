"""Pytest configuration and fixtures"""

import pytest
import random
import time
from typing import Dict, Any, Tuple

from api_tests.utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    """API client fixture"""
    return ApiClient()


@pytest.fixture
def unique_seller_id() -> int:
    """Generate unique seller ID in range 111111-999999"""
    return random.randint(111111, 999999)


@pytest.fixture
def valid_ad_data(unique_seller_id: int) -> Dict[str, Any]:
    """Generate valid advertisement data - API requires 'likes' field at top level!"""
    return {
        "sellerId": unique_seller_id,
        "name": f"Test Ad {random.randint(1, 10000)}",
        "price": random.randint(100, 100000),
        "likes": 0,  
        "viewCount": 0,  
        "contacts": 0,  
    }


@pytest.fixture
def created_ad(
    api_client: ApiClient, valid_ad_data: Dict[str, Any]
) -> Tuple[str, Dict[str, Any]]:
    """Create advertisement and return its ID and data"""
    response = api_client.create_ad(valid_ad_data)
    if response.get("error"):
        pytest.skip(f"Cannot create ad: {response.get('message')}")
    ad_id = response.get("id") or response.get("ad_id")
    assert ad_id, f"Created ad should have an ID. Response: {response}"
    return ad_id, valid_ad_data


@pytest.fixture
def created_ads_for_seller(api_client: ApiClient, unique_seller_id: int) -> list:
    """Create multiple ads for the same seller"""
    ads = []
    for i in range(3):
        data = {
            "sellerId": unique_seller_id,
            "name": f"Seller Ad {i}",
            "price": 1000 + i * 100,
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        }
        response = api_client.create_ad(data)
        if not response.get("error"):
            ad_id = response.get("id") or response.get("ad_id")
            if ad_id:
                ads.append({"id": ad_id, "data": data})
        time.sleep(0.1)
    return ads
