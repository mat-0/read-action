import os
import sys
import json
from github import Github
from actions_toolkit import core
from utils import title_parser, get_book, return_write_file, CleanBook

def read():
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("Cannot find GitHub token")

        g = Github(github_token)
        repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
        issue_number = int(os.getenv('ISSUE_NUMBER'))
        issue = repo.get_issue(number=issue_number)

        if not issue:
            raise ValueError("Cannot find GitHub issue")

        title = issue.title
        number = issue.number
        body = issue.body
        core.export_variable("IssueNumber", number)

        book_isbn, date = title_parser(title)
        if not book_isbn:
            raise ValueError(f"Cannot find book ISBN from given input: {title}")

        file_name = core.get_input("readFileName")
        if not file_name:
            file_name = '_data/read.yml'

        providers = core.get_input("providers")
        if providers:
            providers = providers.split(',')
        else:
            providers = isbn._providers # type: ignore

        book_metadata = get_book({
            'date': date,
            'body': body,
            'book_isbn': book_isbn,
            'providers': providers
        }, file_name)

        return_write_file(file_name, book_metadata)

    except Exception as e:
        core.set_failed(str(e))

if __name__ == "__main__":
    read()