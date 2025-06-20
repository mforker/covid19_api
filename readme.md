# COVID-19 Data API

This project provides a FastAPI-based web API for accessing historical and current COVID-19 data for various states and union territories in India. The data is sourced from official government sources and is available in a JSON format.

The API is deployed at [https://covid19-api-3ymt.onrender.com](https://covid19-api-3ymt.onrender.com)
Check the API Documentation here: [https://covid19-api-3ymt.onrender.com/docs](https://covid19-api-3ymt.onrender.com/docs)

## Features

- **Current State Data**: Retrieve the latest COVID-19 data for one or more states/UTs.
- **Historical State Data**: Access cumulative COVID-19 statistics from January 31, 2020, to December 31, 2024, for specified states/UTs.
- **Current India Data**: Get the latest aggregate COVID-19 data for the entire country.
- **State/UT List**: Obtain a list of all states and union territories for which data can be retrieved.

## Endpoints

### 1. Root

- **URL**: `/`
- **Method**: GET
- **Description**: Returns a simple welcome message.
- **Response**: 
  ```json
  {
    "message": "Hello World"
  }
  ```

### 2. Current State Data

- **URL**: `/current_data/states/{states_str}`
- **Method**: GET
- **Parameters**:
  - `states_str`: Comma-separated list of state/UT names.
- **Description**: Fetches the latest COVID-19 data for the specified states/UTs.
- **Response**: JSON object with active cases, cured cases, and deaths for each state.

### 3. Historical State Data

- **URL**: `/historical_data/states/{states_str}`
- **Method**: GET
- **Parameters**:
  - `states_str`: Comma-separated list of state/UT names.
- **Description**: Retrieves historical COVID-19 data for the specified states/UTs.
- **Response**: JSON object with cumulative cases, cured/migrated, and deaths data.

### 4. Current India Data

- **URL**: `/current_data/india`
- **Method**: GET
- **Description**: Provides the latest aggregate COVID-19 data for India.
- **Response**: JSON object with active cases and discharged data.

### 5. State/UT List

- **URL**: `/states_ut_list`
- **Method**: GET
- **Description**: Returns a list of states and union territories available for querying.
- **Response**: JSON object with a list of state/UT names.

## Installation

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the FastAPI application using `uvicorn api:app --reload`.

## Data Sources

- Historical data is obtained from `data/state_wise_cases_31_jan_2020-5_may_2023.csv` and `data/state_wise_cases_6_may_2023-31_Dec_2024.csv`.
- Current data is fetched from the Ministry of Health and Family Welfare's official website.

## Usage

Once the server is running, you can interact with the API using a tool like `curl`, Postman, or simply via a web browser by navigating to the appropriate endpoint URLs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## Author
Mitesh Nandan

Data Analyst, AI/ML Enthusiast
[LinkedIn Profile](https://www.linkedin.com/in/mitesh-nandan/)