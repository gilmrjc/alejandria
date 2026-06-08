"""Unit tests for GapService."""

from shared.services.gap_service import GapService


def test_gap_service_init():
    """Test GapService initialization."""
    service = GapService()
    assert service.session is not None


def test_list_gaps_as_dict_empty():
    """Test listing gaps as dict with no gaps."""
    service = GapService()
    gaps = service.list_gaps_as_dict()
    assert isinstance(gaps, list)
