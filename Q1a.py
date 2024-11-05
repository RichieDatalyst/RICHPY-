import selenium
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import requests

# Initialize the Edge WebDriver
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

urlPath = 'https://www.youtube.com/c/UnfoldDataScience/videos'
driver.get(urlPath)

# Scroll down to load more videos (you may adjust the number of scrolls as needed)
scrolls = 10
for _ in range(scrolls):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)

# Find all video elements on the page
videos = driver.find_elements(By.CLASS_NAME, "style-scope ytd-rich-grid-media")

# Create a list to store video data
video_data_list = []

# Iterate through each video element
for video in videos:
    # Extract information for each video
    title = video.find_element(By.XPATH, './/*[@id="video-title"]').text
    views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
    duration_text = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text
    if "months" in duration_text:
        months_ago = int(duration_text.split()[0])
        upload_date = datetime.now() - timedelta(days=30 * months_ago)
    elif "years" in duration_text:
        years_ago = int(duration_text.split()[0])
        upload_date = datetime.now() - timedelta(days=365 * years_ago)
    else:
        # Handle other cases if needed
        upload_date = None
   
    # Append the extracted data to the list
    video_data_list.append({
        'Video Title': title,
        'Views Count': views,
        'Upload Date': upload_date.strftime('%d %B %Y') if upload_date else 'N/A',
    })

# Print the collected video data
for video_data in video_data_list:
    print(video_data)





# Filter videos uploaded between Sep 10, 2019, and Sep 10, 2023
start_date = datetime(2019, 9, 10)
end_date = datetime(2023, 9, 10)

# Convert 'Upload Date' strings to datetime objects
for video_data in video_data_list:
    if video_data['Upload Date'] != 'N/A':
        video_data['Upload Date'] = datetime.strptime(video_data['Upload Date'], '%d %B %Y')

# Filter videos based on upload date
filtered_videos = [video for video in video_data_list if video_data['Upload Date'] is not None and start_date <= video_data['Upload Date'] <= end_date]

# Check if there are videos that meet the filtering criteria
if filtered_videos:
    # Calculate the average views count per video for videos uploaded in the last 30 days
    today = datetime.now()
    last_30_days_videos = [video for video in filtered_videos if (today - video_data['Upload Date']).days <= 30]

if last_30_days_videos:
    average_views_last_30_days = sum(int(video_data['Views Count'].replace(' views', '').replace(',', '')) for video_data in last_30_days_videos) / len(last_30_days_videos)
else:
    average_views_last_30_days = 0  # No videos in the last 30 days

    # Determine the most common day of the week for video uploads
    weekday_counts = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

# Filter out videos with 'N/A' upload date and convert to weekday
    upload_days = [video_data['Upload Date'].weekday() for video_data in filtered_videos if video_data['Upload Date'] != 'N/A']

if upload_days:
    most_common_day = weekday_counts[max(set(upload_days), key=upload_days.count)]
else:
    most_common_day = 'N/A'  # No valid upload dates found
   
    # Detect any outliers in the views count
    views = [int(video_data['Views Count'].replace(' views', '').replace(',', '')) for video_data in filtered_videos]
    z_scores = [(view - sum(views) / len(views)) / (sum((view - sum(views) / len(views))**2 for view in views) / len(views))**0.5 for view in views]
    outliers = [filtered_videos[i] for i, z_score in enumerate(z_scores) if abs(z_score) > 3]

    # Display results
    print(f'Average Views Count for Videos Uploaded in the Last 30 Days: {average_views_last_30_days:.2f}')
    print(f'Most Common Day of the Week for Video Uploads: {most_common_day}')
    print(f'Detected Outliers in Views Count: {len(outliers)} videos')
    



# Close the WebDriver
driver.quit()
