# Interactive Online Auction System
![DALL·E 2023-12-17 13 15 55 - Create a YouTube thumbnail for a channel named 'Lobolatory Manager'  The design should feature a stylized laboratory setting with flasks and test tube (1)_16x9](https://github.com/Luksonini/cs50_commerce/assets/97095836/fc5d7388-d0de-4a58-8197-81f72d217be4)


![image](https://github.com/Luksonini/cs50_commerce/assets/97095836/19b575dc-b577-4418-80fb-b35a31dc12c4)

## Overview
The Interactive Online Auction System is a dynamic web application for auction enthusiasts. It offers a feature-rich platform for seamless auction participation, including listing browsing, active bidding, and user watchlist management.

## Features
- **Browse Auctions:** View auctions without logging in.
- **User Participation:** Log in to bid, comment, and manage auctions.
- **Watchlist Management:** Add or remove listings from a personal watchlist.
- **Admin Dashboard:** Oversee listings, bids, and user interactions.

## Installation
To install the Interactive Online Auction System, follow these steps:

```bash
# Clone the repository to your local machine
git clone https://github.com/yourusername/interactive-auction-system.git

# Navigate into the project directory
cd interactive-auction-system

# Install required dependencies (assuming you have Python and pip installed)
pip install -r requirements.txt

# Apply the migrations to create database schema
python manage.py migrate

# Start the development server
python manage.py runserver
