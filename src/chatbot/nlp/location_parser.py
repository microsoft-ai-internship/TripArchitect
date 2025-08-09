def extract_locations(text: str) -> list[str]:
    """Metinden lokasyon listesi çıkarır"""
    return [loc.strip() for loc in text.split(',') if loc.strip()]