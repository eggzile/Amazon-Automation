# 🛒 Amazon India Shopping Automation Bot (Selenium & Python)

This Python script uses **Selenium WebDriver** to automate the process of searching for products on Amazon India, identifying the highest-rated item (with a minimum of 50 reviews), adding it to the cart, and proceeding to the checkout page. It is configured to run using the **Firefox browser**.

⚠️ **Disclaimer:** This script is for educational purposes and personal use to explore web automation with Selenium. Automated purchasing may violate Amazon's terms of service. Use responsibly and at your own risk. **Never use this script to complete actual purchases without user confirmation at the final payment stage.**

***

## 🛠️ Requirements

### 1. Python Libraries

Install the required Python packages using `pip`:

```bash
pip install selenium

Setup and Configuration

Open the Python script (amazon_shopping_bot.py) and configure the following variables in the if __name__ == "__main__": block:

1. Credentials

Replace the placeholder values with your actual Amazon India login details.
Python

    # Your Amazon India credentials
    EMAIL = "your_email_or_mobile"   # <--- REPLACE THIS
    PASSWORD = "your_password"       # <--- REPLACE THIS

2. Search Categories

Define the list of search terms for the products you want to add to your cart.
Python

    # Define categories to search
    categories = [
        "wireless mouse",
        "phone charger cable",
        "water bottle" # Add or change items here
    ]

3. (Optional) Firefox Profile

If you want the bot to use an existing Firefox profile (to maintain login sessions/cookies), you can specify the profile path during initialization:
Python

# Initialize automation
# bot = AmazonIndiaAutomation()  # Default
bot = AmazonIndiaAutomation(profile_path="/path/to/your/firefox/profile") # Use existing profile

▶️ How to Run

    Save the provided Python code as a file (e.g., amazon_shopping_bot.py).

    Open your terminal or command prompt.

    Navigate to the directory where you saved the file.

    Execute the script:

Bash

python amazon_shopping_bot.py

Expected Flow

    A Firefox window will open and attempt to log you in.

    If OTP/2FA or CAPTCHA appears, the script will pause. You must complete the verification manually in the browser, and then press Enter in the console to continue.

    The script will search for each category, select the highest-rated product (with >50 reviews), and add it to the cart.

    It will then navigate to the final checkout page.

    The script pauses at checkout, requiring manual completion of the purchase.

    The browser will remain open until you close it or press Enter in the console.
