# Facebook Auto Poster - Selenium Assignment

## What This Script Does

In this assignment I automated posting a status update on Facebook using Selenium. Basically, the script opens up Firefox, goes to facebook.com, logs in with your credentials, finds the "What's on your mind?" box, types a message, and clicks the Post button. It does the whole thing automatically without you having to touch anything.

The flow is pretty simple:
1. Opens Firefox browser
2. Navigates to Facebook
3. Handles the cookie popup (if it shows up)
4. Logs into my account
5. Clicks on the post area
6. Types out a message
7. Clicks Post
8. Closes the browser

## How to Set It Up

### Prerequisites
- Python 3.x installed on your machine
- Firefox browser installed
- `selenium` library (install with `pip install selenium`)

### Geckodriver Setup
I've included `geckodriver.exe` in the project folder itself. The script looks for it in the same directory (`./geckodriver.exe`), so as long as you don't move it, it should work fine. If you're on a different OS you'll need to download the right version from Mozilla geckodriver releases page (https://github.com/mozilla/geckodriver/releases).

### Putting In Your Credentials
Open `facebook_auto_poster.py` and find these two lines near the top:

```python
fb_email = "YOUR_EMAIL_HERE"
fb_password = "YOUR_PASSWORD_HERE"
```

Replace them with your actual Facebook email and password. I know storing passwords in plain text isn't ideal - I would normally use a `.env` file or something, but for this assignment I kept it simple.

> **Note:** Real credentials removed before submitting.

## How to Run It

Open a terminal in the project folder and just run:

```
python facebook_auto_poster.py
```

The browser will pop up and do everything on its own. You'll see debug messages in the terminal so you can follow along with what's happening.

## Challenges I Faced & How I Solved Them

### 1. Dealing with Dynamic/Changing IDs on Facebook

This was probably the most frustrating part of the whole assignment. When I first started, I tried to use `By.ID` or `By.CLASS_NAME` to find the post text box, but the IDs on Facebook are randomly generated and change every time you load the page. Something like `div_id_a8f3x` one time and `div_id_k9m2z` the next. I was so confused why my script worked once and then completely broke the second time I ran it.

After a lot of Googling , I realized I needed to use XPath with attributes that DON'T change, like `@role` and `@aria-label`. For example, I used `//div[@role="textbox" and @aria-label="What's on your mind?"]` to find the text area. This was way more reliable because those accessibility attributes stay the same even when the random IDs change.

### 2. StaleElementReferenceException

I kept getting this `StaleElementReferenceException` error and I had NO idea what it meant at first. Turns out, when Facebook loads the post dialog, it kind of rebuilds the DOM (the page structure), so the element reference I had from before becomes "stale" - basically, the element I found earlier doesn't exist anymore because the page changed.

I spent an hour trying to figure out why my click wasn't registering, and realized I needed an explicit wait using `WebDriverWait` instead of just `time.sleep()`. The explicit wait actually checks if the element is there and clickable before trying to interact with it. I still use some `time.sleep()` calls in a few places as a safety net (probably not the best practice, but it works and I was tired of debugging lol).

## Tools & Technologies Used
- Python 3
- Selenium WebDriver
- Mozilla Firefox
- Geckodriver

## Disclaimer
This script is for educational purposes only, as part of my assignment. Automating interactions on Facebook might be against their Terms of Service, so please don't use this for anything illegal.