# Google Sheets API Integration

This project demonstrates how to interact with Google Sheets using the `gspread` library, along with other necessary tools for automation. It allows you to append data to a Google Sheet and manage sheet interactions programmatically.

## Prerequisites

Before running the code, you need to set up your Google Cloud Console and generate API credentials for Google Sheets access. Follow the instructions provided in the official `gspread` documentation:

- [Google Sheets API Setup Guide](https://docs.gspread.org/en/latest/index.html)

Once the API is set up, you will need a service account JSON file to authenticate your application with Google Sheets.

## Required Libraries

To run the project, you must install the following Python libraries:

```bash
pip install gspread google-auth webdriver-manager selenium
