import pytest
import sys
import os
import yaml

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from utils import title_parser, get_book, return_write_file, CleanBook

class TestUtils:

    def test_title_parser(self):
        input = "9781527209855 2020-03-01"
        title_parser_result = title_parser(input)
        assert title_parser_result == ('9781527209855', '2020-03-01')

    def test_get_book(self):
        book_info = {
            'date': '2020-03-01',
            'body': 'Sample body',
            'book_isbn': '9781527209855',
            'providers': ['goob', 'openl', 'ismn']
        }
        file_name = '_data/read.yml'
        book_metadata = get_book(book_info, file_name)
        assert book_metadata is not None
        assert len(book_metadata) > 0
        assert isinstance(book_metadata[0], CleanBook)
        assert book_metadata[0].title is not None
        assert book_metadata[0].authors is not None

    def test_return_write_file(self):
        file_name = 'test_file.yml'
        book_metadata = [
            CleanBook(
                title='Sample Book',
                authors=['Sample Author'],
                publisher='Sample Publisher',
                year='2020',
                isbn='9781527209855'
            )
        ]
        return_write_file(file_name, book_metadata)
        with open(file_name, 'r') as file:
            content = yaml.safe_load(file)
            assert content is not None
            assert len(content) > 0
            assert content[0]['title'] == 'Sample Book'
            assert content[0]['authors'] == ['Sample Author']
            assert content[0]['isbn'] == '9781527209855'
            assert content[0]['year'] == '2020'

if __name__ == "__main__":
    pytest.main()