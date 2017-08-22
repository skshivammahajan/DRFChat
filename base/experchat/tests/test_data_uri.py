import pytest

from experchat.utils import validate_data_uri


class TestDataURI:
    """
    Test data-uri validation utility.
    """
    valid_data_uri = """data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA
        AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO
        9TXL0Y4OHwAAAABJRU5ErkJggg=="""
    invalid_data_uris = [
        "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12\
            P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
        "data:png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElE\
            QVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAOTXL0Y4OHwAAAABJRU5ErkJggg==",
        "data:image/png;,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElE\
            QVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
        "data:image/png;base64,",
        "data:image/png;base64,invalid",
    ]

    def test_valid_uri(self):
        assert validate_data_uri(self.valid_data_uri)

    def test_invalid_uri(self):
        for data_uri_str in self.invalid_data_uris:
            with pytest.raises(ValueError):
                validate_data_uri(data_uri_str)
