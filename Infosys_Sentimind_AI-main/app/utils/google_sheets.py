import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from gspread_formatting import *

def write_to_google_sheets(data):
    try:
        # Define the scope (what the app is allowed to access)
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # Load the credentials from the JSON key file
        creds = ServiceAccountCredentials.from_json_keyfile_name("data/sentimind-ai-post-call-f23a2ac187f6.json", scope)

        # Authorize the client
        client = gspread.authorize(creds)

        # Open the Google Sheet by name
        sheet_name = "RTSA"
        sheet = client.open(sheet_name).sheet1

        # Check if the sheet is empty
        sheet_data = sheet.get_all_values()
        print("Sheet Data:", sheet_data)  # Debugging

        if not sheet_data:
            # Add headers if the sheet is empty
            headers = [
                "Timestamp", "User Name", "Email ID", "Sentiment", "Emotional State",
                "Purchase Intent", "Behavioral Intent", "Advanced Intent", "Recommendations",
                "Call Summary", "Performance Analytics", "Deal Status", "Follow-Up Suggestions",
                "Negotiation Tactics", "Objection Handling"
            ]
            print("Adding headers to the sheet...")  # Debugging
            sheet.append_row(headers)  # Add headers as the first row

            # Apply formatting to the headers
            header_format = CellFormat(
                textFormat=TextFormat(
                    bold=True,  # Make text bold
                    fontSize=12,  # Set font size
                    foregroundColor=Color(1, 0, 0)  # Set font color (red in this case)
                ),
                backgroundColor=Color(0.9, 0.9, 0.9),  # Set background color (light gray)
                horizontalAlignment="CENTER"  # Center-align text
            )

            # Apply formatting to the first row (headers)
            format_cell_range(sheet, "A1:O1", header_format)

        # Prepare the data to be written
        row = [
            datetime.now().isoformat(),  # Timestamp
            data.get("user_name", "Unknown"),  # User Name
            data.get("email", "unknown@example.com"),  # Email ID
            data.get("sentiment", ""),  # Sentiment
            data.get("emotion", ""),  # Emotional State
            data.get("purchase_intent", ""),  # Purchase Intent
            data.get("behavioral_intent", ""),  # Behavioral Intent
            data.get("advanced_intent", ""),  # Advanced Intent
            data.get("recommendations", ""),  # Recommendations
            data.get("summary", ""),  # Call Summary
            data.get("performance_analytics", ""),  # Performance Analytics
            data.get("deal_status", ""),  # Deal Status
            data.get("follow_up_suggestions", ""),  # Follow-Up Suggestions
            data.get("negotiation_tactics", ""),  # Negotiation Tactics
            data.get("objection_handling", "")  # Objection Handling
        ]

        # Append the data to the sheet
        print("Appending row:", row)  # Debugging
        sheet.append_row(row)

        # Apply font size 12 to the newly added row
        last_row = len(sheet.get_all_values())  # Get the last row number
        cell_range = f"A{last_row}:O{last_row}"  # Define the range for the last row
        font_format = CellFormat(
            textFormat=TextFormat(
                fontSize=12  # Set font size to 12
            )
        )
        format_cell_range(sheet, cell_range, font_format)  # Apply formatting to the last row

        return True
    except Exception as e:
        print(f"Error writing to Google Sheets: {e}")
        return False