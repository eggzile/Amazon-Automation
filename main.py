from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import re # Import regex for cleaner text extraction

class AmazonIndiaAutomation:
    def __init__(self, profile_path=None):
        """Initialize Firefox with existing profile to use logged-in session"""
        options = webdriver.FirefoxOptions()
        
        # Use existing Firefox profile if provided
        if profile_path:
            options.add_argument('-profile')
            options.add_argument(profile_path)
        
        self.driver = webdriver.Firefox(options=options)
        # Increased wait time for more stability on slow connections/pages
        self.wait = WebDriverWait(self.driver, 20) 
        self.driver.maximize_window()
        
        # Navigate to Amazon India
        self.driver.get("https://www.amazon.in")
        time.sleep(3)
        print("✓ Firefox opened with Amazon.in")
    
    def login(self, email, password):
        """Login to Amazon India account"""
        try:
            print("\n--- Logging in to Amazon.in ---")
            
            # Go to Amazon India homepage
            self.driver.get("https://www.amazon.in")
            time.sleep(2)
            
            # Click on Sign in button
            try:
                sign_in_btn = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "nav-link-accountList"))
                )
                sign_in_btn.click()
                time.sleep(2)
            except:
                print("Already on login page or sign-in button not found")
            
            # Enter email/mobile number
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            email_field.clear()
            email_field.send_keys(email)
            
            # Click Continue
            continue_btn = self.driver.find_element(By.ID, "continue")
            continue_btn.click()
            time.sleep(2)
            
            # Enter password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_field.clear()
            password_field.send_keys(password)
            
            # Click Sign in
            sign_in_submit = self.driver.find_element(By.ID, "signInSubmit")
            sign_in_submit.click()
            time.sleep(4)
            
            # Check if OTP/CAPTCHA is required
            current_url = self.driver.current_url
            if "ap/mfa" in current_url or "ap/cvf" in current_url:
                print("\n⚠️  OTP/2FA Required!")
                print("Please enter the OTP on the browser and complete verification")
                input("Press Enter after you've completed verification...")
            elif "ap/signin" in current_url:
                print("\n⚠️  Login may have failed or CAPTCHA required")
                print("Please complete the login manually in the browser")
                input("Press Enter after you've logged in...")
            else:
                print("✓ Login successful!")
            
            # Verify login
            time.sleep(2)
            self.driver.get("https://www.amazon.in")
            time.sleep(2)
            
            try:
                account_elem = self.driver.find_element(By.ID, "nav-link-accountList")
                if "Hello" in account_elem.text or "नमस्ते" in account_elem.text:
                    print("✓ Login verified - Account detected")
                    return True
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"✗ Login error: {e}")
            print("Please login manually in the browser")
            input("Press Enter after you've logged in...")
            return False
    
    def search_category(self, search_term):
        """Search for items in a category"""
        try:
            # Navigate to home if not there
            if "amazon.in" not in self.driver.current_url:
                self.driver.get("https://www.amazon.in")
                time.sleep(2)
            
            # Ensure search box is present and clickable
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
            )
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            print(f"✓ Searched for: {search_term}")
            return True
        except Exception as e:
            print(f"✗ Search failed: {e}")
            return False
    
    def find_highest_rated_product(self):
        """Find and click the highest rated product from search results"""
        try:
            # Wait for search results container to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-list")))
            time.sleep(3)
            
            # Scroll down to load more products
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            # Get all product items. 'div[data-component-type="s-search-result"]' is more robust than a-section
            products = self.driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
            
            highest_rating = 0.0
            best_product = None
            best_product_name = ""
            best_review_count = 0
            
            print(f"  Analyzing {len(products)} products...")
            
            for idx, product in enumerate(products):
                try:
                    # 1. Get Product Name
                    try:
                        product_name_elem = product.find_element(By.CSS_SELECTOR, "h2 a span")
                        current_product_name = product_name_elem.text
                    except NoSuchElementException:
                        current_product_name = f"Product #{idx+1}"
                    
                    # 2. Get Rating and Review Count
                    rating_container = product.find_element(By.CSS_SELECTOR, "div.a-row.a-size-small")
                    
                    # Extract Rating
                    rating_elem = rating_container.find_element(By.CSS_SELECTOR, "span[aria-label*='out of']")
                    rating_text = rating_elem.get_attribute("aria-label")
                    rating_match = re.search(r"(\d+\.?\d*) out of", rating_text)
                    rating = float(rating_match.group(1)) if rating_match else 0.0
                    
                    # Extract Review Count
                    review_count_elem = rating_container.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text")
                    review_text = review_count_elem.text.replace(",", "").strip()
                    review_count = int(review_text) if review_text.isdigit() else 0
                    
                    # 3. Determine if it's the best product
                    # Only consider products with at least 50 reviews and a rating > 0
                    if rating > 0 and review_count >= 50:
                        # Prioritize higher rating, then higher review count for tie-breaking
                        if rating > highest_rating or (rating == highest_rating and review_count > best_review_count):
                            highest_rating = rating
                            best_product = product
                            best_review_count = review_count
                            best_product_name = current_product_name
                            
                            print(f"  → Candidate #{idx+1}: {best_product_name[:50]}... | {rating}★ ({review_count} reviews)")
                
                except (NoSuchElementException, StaleElementReferenceException, ValueError, AttributeError) as e:
                    # Catch exceptions for products that don't have all the expected rating/review elements
                    # print(f"Skipping product {idx+1} due to missing element or parsing error: {type(e).__name__}")
                    continue
            
            if best_product:
                print(f"\n✓ SELECTED: {best_product_name[:60]}...")
                print(f"  Rating: {highest_rating}/5.0 | Reviews: {best_review_count}")
                
                # Scroll to product
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", best_product)
                time.sleep(1)
                
                # Click the product link (h2 a)
                link = best_product.find_element(By.CSS_SELECTOR, "h2 a")
                self.driver.execute_script("arguments[0].click();", link)
                time.sleep(3)
                return True
            else:
                print("✗ No products found with 50+ reviews meeting criteria.")
                return False
                
        except Exception as e:
            print(f"✗ Error finding product: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Rest of the methods (add_to_cart, go_to_cart, proceed_to_checkout, automate_shopping, and Usage block) remain the same.
    # ... (Keep all other methods and the usage block exactly as they were in your original code)
    
    def add_to_cart(self):
        """Add the current product to cart"""
        try:
            # Check if "Add to Cart" button exists
            try:
                add_to_cart_btn = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
                )
                add_to_cart_btn.click()
                time.sleep(3)
                print("✓ Product added to cart")
                
                # Close any popups
                try:
                    close_btn = self.driver.find_element(By.CSS_SELECTOR, "#attach-close_sideSheet-link")
                    close_btn.click()
                    time.sleep(1)
                except:
                    pass
                
                return True
            except TimeoutException:
                print("✗ Add to Cart button not found - product may need customization")
                return False
                
        except Exception as e:
            print(f"✗ Could not add to cart: {e}")
            return False
    
    def go_to_cart(self):
        """Navigate to shopping cart"""
        try:
            self.driver.get("https://www.amazon.in/gp/cart/view.html")
            time.sleep(3)
            print("✓ Opened shopping cart")
            return True
        except Exception as e:
            print(f"✗ Failed to open cart: {e}")
            return False
    
    def proceed_to_checkout(self):
        """Proceed to checkout page"""
        try:
            # Go to cart first
            self.go_to_cart()
            
            # Click proceed to checkout
            checkout_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='proceedToRetailCheckout']"))
            )
            checkout_btn.click()
            time.sleep(4)
            print("✓ Proceeded to checkout page")
            print("\n⚠️  PAUSED - Complete your purchase manually")
            return True
        except Exception as e:
            print(f"✗ Failed to proceed to checkout: {e}")
            return False
    
    def automate_shopping(self, categories, email=None, password=None):
        """Main automation function"""
        print("=" * 60)
        print("Amazon India Shopping Automation Started")
        print("=" * 60)
        
        # Login if credentials provided
        if email and password:
            self.login(email, password)
        else:
            print(f"\n⏸️  Please verify you're logged in, then press Enter...")
            input()
        
        successful_adds = 0
        
        # Process each category
        for i, category in enumerate(categories, 1):
            print(f"\n[{i}/{len(categories)}] Processing: {category}")
            print("-" * 60)
            
            if self.search_category(category):
                if self.find_highest_rated_product():
                    if self.add_to_cart():
                        successful_adds += 1
                        print(f"  ✓ Added to cart ({successful_adds}/{len(categories)})")
                    else:
                        print(f"  ✗ Failed to add to cart")
                else:
                    print(f"  ✗ Could not find suitable product")
            else:
                print(f"  ✗ Search failed")
            
            # Small delay between categories
            if i < len(categories):
                time.sleep(2)
        
        # Summary
        print("\n" + "=" * 60)
        print(f"Summary: {successful_adds}/{len(categories)} items added to cart")
        print("=" * 60)
        
        # Proceed to checkout
        if successful_adds > 0:
            print("\n--- Proceeding to checkout ---")
            self.proceed_to_checkout()
        else:
            print("\n⚠️  No items were added to cart")
        
        # Keep browser open
        print("\n✋ Browser will stay open. Close it manually when done.")
        input("Press Enter to close the browser...")
        self.driver.quit()

# Usage
if __name__ == "__main__":
    # Your Amazon India credentials
    # IMPORTANT: Keep these secure! Don't share this file with anyone
    EMAIL = "email"  # Your Amazon email or mobile number
    PASSWORD = "password" # Your Amazon password
    
    # Define categories to search
    categories = [
        "wireless mouse",
        "phone charger cable",
        "water bottle"
    ]
    
    print("""
╔════════════════════════════════════════════════════════════╗
║      Amazon India Automation - Firefox Version             ║
╚════════════════════════════════════════════════════════════╝

Instructions:
1. Firefox will open and automatically log you in
2. Complete OTP/2FA if prompted
3. The script will search and add highest-rated items
4. You'll need to complete the checkout manually

Press Ctrl+C to cancel at any time.
""")
    
    input("Press Enter to start...")
    
    # Initialize automation
    bot = AmazonIndiaAutomation()
    
    # Run automation with auto-login
    bot.automate_shopping(categories, email=EMAIL, password=PASSWORD)