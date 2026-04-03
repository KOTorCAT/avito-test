"""Test data generator"""

import random
from faker import Faker

fake = Faker("ru_RU")


class DataGenerator:
    """Generate test data for advertisements"""

    @staticmethod
    def generate_seller_id() -> int:
        """Generate seller ID in range 111111-999999"""
        return random.randint(111111, 999999)

    @staticmethod
    def generate_ad_data(seller_id: int = None) -> dict:
        """Generate valid advertisement data - ALL fields required!"""
        return {
            "sellerId": seller_id or DataGenerator.generate_seller_id(),
            "name": fake.catch_phrase()[:100],
            "price": random.randint(0, 10000000),
            "statistics": {
                "likes": random.randint(0, 1000),
                "viewCount": random.randint(0, 10000),
                "contacts": random.randint(0, 100),
            },
        }

    @staticmethod
    def generate_minimal_ad_data(seller_id: int = None) -> dict:
        """Generate minimal valid data with all required fields"""
        return {
            "sellerId": seller_id or DataGenerator.generate_seller_id(),
            "name": fake.catch_phrase()[:50],
            "price": 1000,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0},
        }

    @staticmethod
    def generate_ad_data_with_custom_stats(
        seller_id: int = None, likes: int = 0, views: int = 0, contacts: int = 0
    ) -> dict:
        """Generate ad data with custom statistics values"""
        return {
            "sellerId": seller_id or DataGenerator.generate_seller_id(),
            "name": fake.catch_phrase()[:50],
            "price": random.randint(100, 10000),
            "statistics": {"likes": likes, "viewCount": views, "contacts": contacts},
        }

    @staticmethod
    def generate_long_name(length: int = 1000) -> str:
        """Generate a long name with specified length"""
        return "A" * length

    @staticmethod
    def generate_xss_payload() -> str:
        """Generate XSS injection payload"""
        return "<script>alert('xss')</script>"

    @staticmethod
    def generate_sql_injection() -> str:
        """Generate SQL injection payload"""
        return "'; DROP TABLE items; --"
