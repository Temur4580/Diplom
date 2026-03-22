class TestData:
    # Search queries
    SEARCH_QUERY = "малыш и карлсон который живёт на крыше"
    SEARCH_QUERY_SHORT = "Карлсон"

    # Category slugs
    CATEGORY_SLUG = "psihologiya-uspekha-lichnaya-ehffektivnost-motivaciya-110337"

    # Product IDs
    PRODUCT_ID = 3122670
    INVALID_PRODUCT_ID = "invalid_id"

    # API endpoints
    ENDPOINTS = {
        "search": "/web/api/v2/search/product",
        "facet_search": "/web/api/v2/search/facet-search",
        "categories": "/web/api/v1/categories/tree",
        "cart": "/web/api/v1/cart/product",
    }

    # Customer info
    CUSTOMER_CITY_ID = 11469
    AB_TEST_GROUP = 1


test_data = TestData()
