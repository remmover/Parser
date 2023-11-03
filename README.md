# README

## Data Parsing Tool

This Python script is a versatile data parsing tool designed to fetch and parse data from various sources like web pages, APIs, CSV, and JSON files, then save the parsed data to different formats including CSV, JSON, or an SQLite database. The tool uses `requests` for HTTP requests, `BeautifulSoup` for HTML parsing, `pandas` for handling dataframes, and `sqlite3` for interacting with SQLite databases.

### Features

- Parse H1 tags from web pages
- Fetch data from API endpoints and parse JSON responses
- Read data from CSV and JSON files
- Execute SQL queries against SQLite databases and fetch results
- Save parsed data to CSV, JSON, or SQLite database

### Dependencies

Before running the script, ensure you have the following Python modules installed:

- requests
- BeautifulSoup (`bs4`)
- pandas
- sqlite3
- json
- argparse
- logging (for extended functionality if required)

You can install these dependencies using `pip`:

```shell
poetry install
```

### Usage

The script is run from the command line, accepting arguments to specify the data source and destination.

```shell
python data_parsing_tool.py [source] [destination] [url] [--table TABLE] [--db DB]
```

#### Arguments:

- `source`: The source of the data. Options: "web" for a webpage, "api" for an API endpoint.
- `destination`: The destination format. Options: "csv", "json", or "db".
- `url`: The URL of the webpage or API endpoint to parse.
- `--table`: (Optional for db destination) The table name for database storage.
- `--db`: (Optional for db destination) The database name for database storage.

#### Examples:

1. To parse H1 tags from a webpage and save to a CSV file:

    ```shell
    python data_parsing_tool.py web csv https://example.com
    ```

2. To fetch data from an API endpoint and save to a JSON file:

    ```shell
    python data_parsing_tool.py api json https://api.example.com/data
    ```

3. To parse data from an API and save to an SQLite database:

    ```shell
    python data_parsing_tool.py api db https://api.example.com/data --table tablename --db database.db
    ```

### Output

The script will output the parsed data to the specified format and path:

- For CSV: `output.csv`
- For JSON: `output.json`
- For SQLite DB: `database.db` with the specified table name.

### Error Handling

The script includes try-except blocks for error handling during the HTTP requests, file parsing, and database operations. It will print error messages if something goes wrong during the process.

### Logging

For extended functionality, you can integrate the `logging` module to capture detailed logs. This can be helpful for debugging and keeping track of the tool's operation history.

---

For any further assistance or to report issues, please open an issue on the GitHub repository page associated with this tool.
