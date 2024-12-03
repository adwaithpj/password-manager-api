import pytest
import httpx

# Sample endpoint for testing
BASE_URL = "http://127.0.0.1:8000"  # Update with your actual server URL
PASSWORD_ENDPOINT = "/v1/pass/create"  # Update if your endpoint path is different
BEARER_ENDPOINT = "/v1/auth/token"
# Test data
test_data = [
    {
        "website_name": "Google",
        "username_email": "user@gmail.com",
        "password": "password123",
    },
    {
        "website_name": "Facebook",
        "username_email": "user@fb.com",
        "password": "fbpass456",
    },
    {
        "website_name": "Twitter",
        "username_email": "user@twitter.com",
        "password": "twtr789",
    },
    {
        "website_name": "Instagram",
        "username_email": "user@insta.com",
        "password": "instapass321",
    },
    {
        "website_name": "LinkedIn",
        "username_email": "user@linkedin.com",
        "password": "linkedinpass",
    },
    {
        "website_name": "YouTube",
        "username_email": "user@youtube.com",
        "password": "ytpass123",
    },
    {
        "website_name": "Reddit",
        "username_email": "user@reddit.com",
        "password": "redditpass987",
    },
    {
        "website_name": "Amazon",
        "username_email": "user@amazon.com",
        "password": "amazonpass456",
    },
    {
        "website_name": "Netflix",
        "username_email": "user@netflix.com",
        "password": "netflix123",
    },
    {
        "website_name": "Spotify",
        "username_email": "user@spotify.com",
        "password": "spotifypass789",
    },
    {
        "website_name": "GitHub",
        "username_email": "user@github.com",
        "password": "githubpass123",
    },
    {
        "website_name": "Dropbox",
        "username_email": "user@dropbox.com",
        "password": "dropbox123",
    },
    {
        "website_name": "Yahoo",
        "username_email": "user@yahoo.com",
        "password": "yahoopass111",
    },
    {
        "website_name": "Outlook",
        "username_email": "user@outlook.com",
        "password": "outlook321",
    },
    {
        "website_name": "Discord",
        "username_email": "user@discord.com",
        "password": "discord123",
    },
    {
        "website_name": "Zoom",
        "username_email": "user@zoom.com",
        "password": "zoompw987",
    },
    {
        "website_name": "Trello",
        "username_email": "user@trello.com",
        "password": "trellopass456",
    },
    {
        "website_name": "Slack",
        "username_email": "user@slack.com",
        "password": "slack123",
    },
    {
        "website_name": "eBay",
        "username_email": "user@ebay.com",
        "password": "ebaypass999",
    },
    {
        "website_name": "Flipkart",
        "username_email": "user@flipkart.com",
        "password": "flipkart789",
    },
    {
        "website_name": "Snapchat",
        "username_email": "user@snapchat.com",
        "password": "snapchat123",
    },
    {
        "website_name": "Pinterest",
        "username_email": "user@pinterest.com",
        "password": "pinpass555",
    },
    {
        "website_name": "Quora",
        "username_email": "user@quora.com",
        "password": "quorapass456",
    },
    {
        "website_name": "Bing",
        "username_email": "user@bing.com",
        "password": "bingpass123",
    },
    {
        "website_name": "PayPal",
        "username_email": "user@paypal.com",
        "password": "paypal321",
    },
    {
        "website_name": "Venmo",
        "username_email": "user@venmo.com",
        "password": "venmopass111",
    },
    {
        "website_name": "Canva",
        "username_email": "user@canva.com",
        "password": "canvapass456",
    },
    {
        "website_name": "Airbnb",
        "username_email": "user@airbnb.com",
        "password": "airbnb123",
    },
    {
        "website_name": "Coursera",
        "username_email": "user@coursera.com",
        "password": "courserapass789",
    },
    {
        "website_name": "Udemy",
        "username_email": "user@udemy.com",
        "password": "udemypass123",
    },
]


@pytest.fixture(scope="session")
def get_bearer_token():
    """Retrieve Bearer token before running the tests."""
    login_data = {"username": "adwaith@test.com", "password": "admin@test"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Use `data` instead of `json` for form submissions
    login_response = httpx.post(
        f"{BASE_URL}{BEARER_ENDPOINT}", data=login_data, headers=headers
    )

    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json().get("access_token")
    assert token, "Bearer token not returned from login response"
    return token


@pytest.mark.parametrize("payload", test_data)
def test_password_create_endpoint(payload, get_bearer_token):
    headers = {
        "Authorization": f"Bearer {get_bearer_token}",
        "Content-Type": "application/json",
    }
    response = httpx.post(
        f"{BASE_URL}{PASSWORD_ENDPOINT}", json=payload, headers=headers
    )

    # Assertions
    assert (
        response.status_code == 201
    ), f"Failed for {payload['website_name']} with {response.text}"
    assert response.status_code == 201, f"Unexpected response: {response.text}"
