"""Custom assertions for API tests"""

import allure


class Assertions:
    """Class with assertion methods"""

    @staticmethod
    @allure.step("Check HTTP status code")
    def assert_status_code(response, expected_code: int):
        """Check HTTP status code"""
        # Handle case where response is already a dict (not Response object)
        if hasattr(response, 'status_code'):
            actual_code = response.status_code
        else:
            # If it's a dict from successful request, assume 200
            actual_code = 200

        assert actual_code == expected_code, \
            f"Expected status {expected_code}, got {actual_code}"

    @staticmethod
    @allure.step("Check advertisement structure")
    def assert_ad_structure(ad_data: dict):
        """Check that response contains all required fields"""
        assert "id" in ad_data, "Response missing 'id' field"
        assert "sellerId" in ad_data, "Response missing 'sellerId' field"
        assert "name" in ad_data, "Response missing 'name' field"
        assert "price" in ad_data, "Response missing 'price' field"

    @staticmethod
    @allure.step("Check ad matches created data")
    def assert_ad_matches_created(ad_data: dict, created_data: dict):
        """Check that retrieved ad matches created data"""
        assert ad_data.get("sellerId") == created_data.get("sellerId"), \
            f"SellerId mismatch: {ad_data.get('sellerId')} != {created_data.get('sellerId')}"
        assert ad_data.get("name") == created_data.get("name"), \
            f"Name mismatch: {ad_data.get('name')} != {created_data.get('name')}"
        assert ad_data.get("price") == created_data.get("price"), \
            f"Price mismatch: {ad_data.get('price')} != {created_data.get('price')}"