import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import json
import argparse
import logging


def parse_webpage(url):
    """
    Parses the H1 tags of a webpage.

    :param url: The URL of the webpage to parse.
    :return: A dictionary with H1 texts.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        h1_tags = soup.find_all('h1')
        h1_texts = [tag.get_text(strip=True) for tag in h1_tags]

        return {"h1": h1_texts}

    except requests.RequestException as e:
        return f"Request error occurred: {e}"


def parse_api(api_endpoint):
    """
    Parses data from an API endpoint.

    :param api_endpoint: The API endpoint URL.
    :return: A list of item data with 'name' and 'value' keys.
    """
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()
        data = response.json()

        items_data = [{'name': item['name'], 'value': item['value']} for item in data.get('items', [])]
        return items_data

    except requests.RequestException as e:
        return f"Request error occurred: {e}"
    except json.JSONDecodeError as e:
        return f"JSON decode error: {e}"


def parse_file(file_path, file_type):
    """
    Parses data from file.

    :param file_path: The path to file.
    :param file_type: The type of file.
    :return: A list of item data with 'name' and 'value' keys.
    """
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path)
            data = df.to_dict(orient='records')
        elif file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise ValueError("Invalid file type specified. Choose 'csv' or 'json'.")

        return data

    except (pd.errors.ParserError, FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"An error occurred: {e}")
        return None


def parse_database(db_name, query):
    """
    Executes a SQL query against a database and returns the results as a list of dictionaries.

    :param db_name: The database file path.
    :param query: The SQL query to be executed.
    :return: A list of dictionaries, where each dictionary represents a row of query results.
             Returns None if there's an error.
    """
    try:
        with sqlite3.connect(db_name) as conn:
            data = pd.read_sql_query(query, conn).to_dict(orient='records')
        return data
    except (sqlite3.Error, pd.io.sql.DatabaseError) as e:
        print(f"An error occurred while executing the query: {e}")
        return None


def save_to_csv(data, filename):
    """
    Saves data to a CSV file.

    :param data: Data to save (list of dicts or DataFrame).
    :param filename: The name of the file to save the data in.
    """
    try:
        if isinstance(data, pd.DataFrame):
            data.to_csv(filename, index=False)
        elif isinstance(data, list) and all(isinstance(i, dict) for i in data):
            pd.DataFrame(data).to_csv(filename, index=False)
        else:
            raise ValueError("Data format is not supported for CSV conversion.")

        print(f"Data has been saved to {filename}")
    except (ValueError, pd.errors.ParserError) as e:
        print(f"An error occurred: {e}")


def save_to_json(data, filename):
    """
    Saves data to a JSON file.

    :param data: Data to save (list of dicts, a single dict, or DataFrame).
    :param filename: The name of the file to save the data in.
    """
    try:
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient='records')

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Data has been saved to {filename}")
    except (TypeError, ValueError) as e:
        print(f"An error occurred: {e}")


def save_to_db(data, db_name, table_name, if_exists='replace'):
    """
    Saves data to a DB file.

    :param data: Data to save (list of dicts, a single dict, or DataFrame).
    :param db_name: The name of the DB  to save the data in.
    :param table_name: The name of the table to save the data in.
    """
    try:
        df = pd.DataFrame(data)
        with sqlite3.connect(db_name) as conn:
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        print(f"Data has been saved to '{db_name}' in table '{table_name}' with if_exists option set to '{if_exists}'.")
    except (ValueError, sqlite3.Error, pd.errors.ParserError) as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main function to run the data parsing tool.
    """
    parser = argparse.ArgumentParser(description='Data parsing tool.')
    parser.add_argument('source', help='The source of the data. "web" for a webpage, "api" for an API endpoint.')
    parser.add_argument('destination', help='The destination format. "csv", "json", or "db".')
    parser.add_argument('url', help='The URL of the webpage or API endpoint.')
    parser.add_argument('--table', help='The table name for database storage. Required if destination is "db".')
    parser.add_argument('--db', help='The database name for database storage. Required if destination is "db".')
    args = parser.parse_args()

    if args.source == 'web':
        data = parse_webpage(args.url)
    elif args.source == 'api':
        data = parse_api(args.url)
    else:
        raise ValueError("Invalid source specified. Choose 'web' or 'api'.")

    if args.destination == 'csv':
        save_to_csv(data, 'output.csv')
    elif args.destination == 'json':
        save_to_json(data, 'output.json')
    elif args.destination == 'db':
        if not args.table or not args.db:
            raise ValueError("When saving to a database, 'table' and 'db' arguments must be specified.")
        save_to_db(data, args.db, args.table)
    else:
        raise ValueError("Invalid destination format. Choose 'csv', 'json', or 'db'.")


if __name__ == "__main__":
    main()
