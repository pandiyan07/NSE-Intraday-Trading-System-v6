# Project Title

**NSE Intraday Trading System v6**

## Table of Contents

-   [About The Project](#about-the-project)
-   [Built With](#built-with)
-   [Key Features](#key-features)
-   [Getting Started](#getting-started)
-   [Technologies Used
    (Prerequisites)](#technologies-used-prerequisites)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Project Structure](#project-structure)
-   [How It Works](#how-it-works)
-   [Main Python Functions](#main-python-functions)
-   [Configuration](#configuration)
-   [License Description](#license-description)
-   [Disclaimer](#disclaimer)

## About The Project

This project is a modular intraday NSE trading analysis system that
continuously scans a configurable watchlist, downloads 2-minute and
5-minute market data, computes RSI, price breakout percentages, volume
statistics and ranking scores, compares multiple breakout tables,
identifies common opportunities, checks market holidays, and generates
formatted trading reports. The application is organized into independent
scheduler, calculation, aggregation and reporting modules.

### Built With

-   Python 3
-   yfinance
-   pandas
-   multiprocessing
-   datetime
-   time

### Key Features

-   Multi-timeframe market data download
-   2-minute and 5-minute analysis
-   RSI averaging
-   One, Two and Three candle breakout detection
-   Breakout ranking system
-   Common-stock comparison
-   Holiday checker
-   Volume analysis
-   Modular architecture
-   Multiprocessing support

## Getting Started

### Technologies Used (Prerequisites)

-   Python 3.10+
-   pip
-   Internet connection

Required packages: - pandas - yfinance

### Installation

``` bash
git clone https://github.com/yourusername/nse-trading-system-v6.git
cd nse-trading-system-v6
pip install -r requirements.txt
python Trading_system_v6.py
```

## Usage

Execute `Trading_system_v6.py`. The scheduler downloads market data,
calculation modules process indicators and breakout metrics, and the
reporting module generates ranked trading tables.

## Project Structure

``` text
Trading_system_v6.py      # Main application and orchestration
APPENDER.py               # Technical calculations and breakout logic
SCHEDULER.py              # Scheduled market data downloads
PRINTER.py                # Ranking, report generation and output formatting
```

## How It Works

1.  Initialize configuration and shared objects.
2.  Start scheduler processes.
3.  Download 2-minute and 5-minute Yahoo Finance data.
4.  Calculate average RSI values.
5.  Calculate one-, two- and three-candle breakout percentages.
6.  Perform volume and momentum analysis.
7.  Rank breakout candidates.
8.  Compare breakout and percentage-change tables.
9.  Identify common stocks.
10. Check trading holidays.
11. Format output tables.
12. Display final trading report.

## Main Python Functions

  -----------------------------------------------------------------------
  Function                            Description
  ----------------------------------- -----------------------------------
  `SCHEDULE_TASK()`                   Schedules and downloads
                                      multi-timeframe market data.

  `DATA_FETCHER()`                    Retrieves Yahoo Finance OHLC data.

  `RSI_14_AVERAGE_CALCULATOR()`       Computes average RSI over rolling
                                      windows.

  `ONE_CANDLE_PRICE_BREAKOUT()`       Calculates single-candle breakout
                                      percentage.

  `TWO_CANDLE_PRICE_BREAKOUT()`       Calculates two-candle breakout
                                      percentage.

  `THREE_CANDLE_PRICE_BREAKOUT()`     Detects three-candle breakout
                                      patterns.

  `CHECK_HOLIDAY()`                   Displays current and upcoming
                                      market holidays.

  `COMMON_STOCKS()`                   Finds stocks common to multiple
                                      ranking tables.

  `CONSISTENCY_RANKING()`             Maintains cumulative breakout
                                      ranking scores.
  -----------------------------------------------------------------------

## Configuration

-   Editable watchlist
-   Download intervals
-   Market start time
-   Ranking parameters
-   Breakout thresholds

## License Description

Recommended License: MIT License.

Permission is granted to use, modify and distribute the software while
retaining the copyright notice.

## Disclaimer

This software is intended for educational, research and
strategy-development purposes only. It does not provide investment
advice or guarantee trading performance.
