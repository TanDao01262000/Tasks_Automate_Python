from email_fetch import *
from reformat_content import *
from summarize_api import *


def main():
    emails = fetch()
    for i in range(len(emails)):
        emails[i]['content']  = clean_string(emails[i]['content'])
    return emails


if __name__ == '__main__':
    main()