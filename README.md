# Turkey Holidays Dataset Generator

![Turkey Flag](https://upload.wikimedia.org/wikipedia/commons/b/b4/Flag_of_Turkey.svg)

[TOC]

---------------------------------------------------------------------

## Description

This Python script is a powerful tool for generating a comprehensive dataset that combines both religious and secular
holidays in Turkey, covering the years 2022 to 2031. By leveraging the pandas, workalendar, and holidays libraries, this
script provides a consolidated view of official days, making it an invaluable resource for any project requiring
holiday-related data in Turkey.

---------------------------------------------------------------------

## Features

- **Efficient Data Handling**: Utilizes pandas for efficient data manipulation and handling.

- **Accurate Date Calculation**: Leverages the workalendar library for precise date calculations, considering specific
  country rules.

- **Comprehensive Dataset**: Includes both secular and religious holidays for a thorough overview.

- **Flexible Integration**: Easily integrates with other projects requiring holiday-related datasets.

---------------------------------------------------------------------

## Usage

### Prerequisites

Ensure you have Python installed. Install the required libraries using:

```bash
pip install -r requirements.txt
```

---------------------------------------------------------------------

## How To Run?

### Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

### Execute the script:

```bash
python main.py
```

- This generates a CSV file named "Turkey_official_and_religious_days.csv" in the project folder.
---------------------------------------------------------------------

## Project Structure

- main.py: Main script initiating data generation.

- src/utils.py: Utility functions for religious and secular holiday datasets.

---------------------------------------------------------------------

## Dataset Overview

- ds: Date (timestamp format)

- Secular Holidays: Columns indicating secular holidays (1 for holiday, 0 for non-holiday).

- Ramadan Feast: Indicator for Ramadan Feast (1 for feast day and two days after the first day).

- Sacrifice Feast: Indicator for Sacrifice Feast (1 for feast day and three days after the first day).

- Fasting: Indicator for 30 days before each year's Kurban Bayramı.

---------------------------------------------------------------------

## Additional Information

- The Hijri calendar's lunar nature causes Ramadan to shift earlier each year in the Gregorian calendar. Roughly every
  32 years, Ramadan aligns with the same dates.

Feel free to adapt and enhance this script to meet your specific project requirements. If you find any issues or have
suggestions, please open an issue.

Happy coding!