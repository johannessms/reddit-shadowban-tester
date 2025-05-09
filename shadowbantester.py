import streamlit as st
import praw
import prawcore
import time
import pandas as pd

# Get credentials from Streamlit secrets
client_id = st.secrets["REDDIT_CLIENT_ID"]
client_secret = st.secrets["REDDIT_CLIENT_SECRET"]
user_agent = st.secrets["REDDIT_USER_AGENT"]

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def is_shadowbanned(username):
    try:
        user = reddit.redditor(username)
        _ = user.id
        return False  # Not shadowbanned
    except prawcore.exceptions.NotFound:
        return True  # Shadowbanned or does not exist    
    except Exception as e:
        st.error(f"Error for {username}: {e}")
        return None

st.title("Reddit Shadowban Bulk Tester")

st.write("Enter multiple Reddit usernames (one per line):")
usernames_input = st.text_area("Usernames", height=200)

if st.button("Check"):
    usernames = [u.strip() for u in usernames_input.splitlines() if u.strip()]
    if not usernames:
        st.warning("Please enter at least one username.")
    else:
        if len(usernames) > 60:
            st.warning("Warning: Checking more than 60 usernames might hit Reddit's rate limits. Consider checking in smaller batches.")
        
        results = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, username in enumerate(usernames):
            status_text.text(f"Checking {username}... ({i+1}/{len(usernames)})")
            result = is_shadowbanned(username)
            if result is True:
                results[username] = "Shadowbanned or does not exist"
            elif result is False:
                results[username] = "Not shadowbanned"
            else:
                results[username] = "Error during check"
            
            # Update progress
            progress_bar.progress((i + 1) / len(usernames))
            time.sleep(1)  # Rate limiting
        
        status_text.text("Done!")
        st.write("**Results:**")
        st.table(pd.DataFrame(results.items(), columns=["Username", "Status"]))
        
        # Add download button for results
        csv = pd.DataFrame(results.items(), columns=["Username", "Status"]).to_csv(index=False)
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="shadowban_results.csv",
            mime="text/csv"
        )