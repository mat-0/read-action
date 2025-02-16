import isbnlib
import yaml

class CleanBook:
    def __init__(self, title, authors, publisher, year, isbn):
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.year = year
        self.isbn = isbn

def title_parser(title):
    # Assuming the title format is "ISBN - Date"
    parts = title.split(' ')
    if len(parts) < 2:
        return None, None
    book_isbn = parts[0]
    date = parts[1]
    return book_isbn, date

def get_book(details, file_name):
    book_isbn = details['book_isbn']
    providers = details['providers']
    book_metadata = []

    for provider in providers:
        try:
            book = isbnlib.meta(book_isbn, service=provider)
            if book:
                clean_book = CleanBook(
                    title=book.get('Title'),
                    authors=book.get('Authors'),
                    publisher=book.get('Publisher'),
                    year=book.get('Year'),
                    isbn=book_isbn
                )
                book_metadata.append(clean_book)
                break
        except isbnlib.ISBNLibException:
            continue

    if not book_metadata:
        raise ValueError(f"Cannot find book metadata for ISBN: {book_isbn}")

    return book_metadata

def return_write_file(file_name, book_metadata):
    data = [book.__dict__ for book in book_metadata]
    with open(file_name, 'w') as file:
        yaml.dump(data, file)