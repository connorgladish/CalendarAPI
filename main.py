import tkinter as tk
import requests
import datetime
import json
import pytz
from PIL import Image, ImageTk

def fetch_data_for_date(api_url, start_date, end_date, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    formatted_start_date = start_date.strftime('%Y-%m-%dT00:00:00.0000000')
    formatted_end_date = end_date.strftime('%Y-%m-%dT23:59:59.9999999')
    response = requests.get(api_url, params={'startDateTime': formatted_start_date, 'endDateTime': formatted_end_date}, headers=headers)
    if response.status_code == 200:
        data = response.json()  # Use response.json() to directly parse JSON response
        events = data.get('value', [])  # Extract events list from 'value' key
        return events
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def convert_to_cst(datetime_str):
    utc_datetime = datetime.datetime.fromisoformat(datetime_str)
    utc_timezone = pytz.timezone('UTC')
    cst_timezone = pytz.timezone('America/Chicago')
    utc_datetime = utc_timezone.localize(utc_datetime)
    cst_datetime = utc_datetime.astimezone(cst_timezone)
    return cst_datetime

def display_event_info(root, event, row, max_font_size=16):
    event_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1, bg="white")  # Set background color to white
    event_frame.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")  # Place frame in respective row

    subject_label = tk.Label(event_frame, text=f"{event['subject']}", bg="lightblue", fg="black", font=("Arial", max_font_size, "bold"))  # Light blue label with black text, bold
    subject_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

    start_label = tk.Label(event_frame, text=f"Start Time: {event['start_datetime']}", bg="lightgreen", fg="black", font=("Arial", max_font_size - 2))  # Light green label with black text
    start_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")

    end_label = tk.Label(event_frame, text=f"End Time: {event['end_datetime']}", bg="lightcoral", fg="black", font=("Arial", max_font_size - 2))  # Light coral label with black text
    end_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")

    location_label = tk.Label(event_frame, text=f"Location: {event['location']}", bg="white", fg="black", font=("Arial", max_font_size - 2))  # White label with black text
    location_label.grid(row=3, column=0, padx=5, pady=2, sticky="w")

    # Calculate length of body text
    body_text_length = sum(len(line) for line in event.get('body', '').split('\n'))
    
    # Calculate font size based on text length
    dynamic_font_size = max_font_size - min(2, body_text_length // 50)  # Adjust dynamically based on text length
    
    # Display body text with dynamic font size
    body_label = tk.Label(event_frame, text=event.get('body', ''), bg="white", fg="black", font=("Arial", dynamic_font_size))
    body_label.grid(row=4, column=0, padx=5, pady=2, sticky="w")

def place_image(root, image_path):
    # Load the image
    img = Image.open(image_path)
    img = img.convert("RGBA")  # Convert to RGBA to preserve transparency

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Resize the image with aspect ratio preserved
    target_height = int(screen_height * 0.55)  # Adjust the vertical size as needed
    aspect_ratio = img.width / img.height
    target_width = int(target_height * aspect_ratio)
    img = img.resize((target_width, target_height), Image.LANCZOS)

    # Convert the image to Tkinter PhotoImage
    photo_img = ImageTk.PhotoImage(img)

    # Create a label to display the image
    image_label = tk.Label(root, image=photo_img, bg="gray")  # Set background color of label to match window
    image_label.image = photo_img  # Keep a reference to the image to prevent garbage collection

    # Place the image label slightly to the left and middle vertically
    image_label.place(relx=0.78, rely=0.45, anchor=tk.CENTER)
    


def main():
    api_url = "https://graph.microsoft.com/v1.0/users/27dfe650-e3d2-42cd-a340-7670243df82e/calendar/calendarview"
    today_date = datetime.date.today()
    start_date = today_date
    end_date = today_date
    api_key = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IlFwYjBvQWNSWGhrRE13dmFrb1RnU2MtRTdEOUFjdkp3NTBYQXc2VjZ2VGMiLCJhbGciOiJSUzI1NiIsIng1dCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSIsImtpZCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9mNGVlMjhmZC05MjQ5LTQyYTAtOTM1Ni02ZjI5Njg4YTAyNjkvIiwiaWF0IjoxNzEzOTM1MDIzLCJuYmYiOjE3MTM5MzUwMjMsImV4cCI6MTcxMzkzODkyMywiYWlvIjoiRTJOZ1lFaWFYSjkrc2xxL3ZPWHRqN2ozNjd6dUFRQT0iLCJhcHBfZGlzcGxheW5hbWUiOiJDYW1wdXMgT3B0aW1pemVyIiwiYXBwaWQiOiJhNzE3M2YxOS05YTQ4LTQzY2EtOTg1Yy1kZmJlZDY0ZGNhYzEiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9mNGVlMjhmZC05MjQ5LTQyYTAtOTM1Ni02ZjI5Njg4YTAyNjkvIiwiaWR0eXAiOiJhcHAiLCJvaWQiOiI3ODU0YjgxNC0wNDMyLTQyZWEtOWY0Zi1lOTg0Mjg2NDY2MzciLCJyaCI6IjAuQVZFQV9TanU5RW1Tb0VLVFZtOHBhSW9DYVFNQUFBQUFBQUFBd0FBQUFBQUFBQUJSQUFBLiIsInJvbGVzIjpbIlVzZXIuUmVhZEJhc2ljLkFsbCIsIkdyb3VwLlJlYWQuQWxsIiwiVXNlci5SZWFkLkFsbCIsIkNhbGVuZGFycy5SZWFkQmFzaWMuQWxsIl0sInN1YiI6Ijc4NTRiODE0LTA0MzItNDJlYS05ZjRmLWU5ODQyODY0NjYzNyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJOQSIsInRpZCI6ImY0ZWUyOGZkLTkyNDktNDJhMC05MzU2LTZmMjk2ODhhMDI2OSIsInV0aSI6IkNwSXZ1SXB1RkVPVmJ5dWVIc3dhQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjA5OTdhMWQwLTBkMWQtNGFjYi1iNDA4LWQ1Y2E3MzEyMWU5MCJdLCJ4bXNfdGNkdCI6MTU4NjI5MTYyNX0.iW2YYfdRoh2tZEblMerrGT4EhF2yGBbvMIraC1GzhFJG-jxFLuoYp1LgMibDEz7uNNXQg2Wmw7khEMYSivh-xKyNuycL81V-YjRgJAYN0vmfxV-NlI6NV0pRf5QAjNEwr056K5NHOZEu1_xAKk4XkhtH6vXLInlaBGsmkbACcWossV7QGn-oHmBa_zdE81pL7Qhl1WM44witHQelrTKcuyxp1Zx5zdTt_kZoySagjV8BZiZPsghZUddb_JYPx7Lpe5bE_nlWMzkAiyfIWFrQTw_0Je5ZrmZETa9QtpgGbzRRmv0oK2b327BY4A2UqO2ylJ4clYjcVLOKCW5_EWAphw"


    events = fetch_data_for_date(api_url, start_date, end_date, api_key)
    if events:
        # Create GUI window
        root = tk.Tk()
        root.title("Event Information")
        root.configure(bg="gray")  # Set background color to gray

        # Set window to fullscreen
        root.attributes('-fullscreen', True)

        for i, event in enumerate(events):
            formatted_event = {}
            formatted_event['subject'] = event.get('subject', 'No subject')
            start_datetime = event.get('start', {}).get('dateTime')
            end_datetime = event.get('end', {}).get('dateTime')
            # Convert UTC to CST
            start_datetime_cst = convert_to_cst(start_datetime)
            end_datetime_cst = convert_to_cst(end_datetime)
            # Parse the datetime strings and format them
            formatted_event['start_datetime'] = start_datetime_cst.strftime("%Y-%m-%d %I:%M %p")
            formatted_event['end_datetime'] = end_datetime_cst.strftime("%Y-%m-%d %I:%M %p")
            formatted_event['location'] = event.get('location', {}).get('displayName', 'No location')
            
            display_event_info(root, formatted_event, i)

        # Image path
        image_path = "dpatransparent.png"  # Replace with your image path

        # Place the image on the right middle center of the screen
        place_image(root, image_path)

        root.mainloop()
    else:
        print("Failed to fetch and format data.")

if __name__ == "__main__":
    main()
