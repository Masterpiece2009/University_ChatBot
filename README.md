Here's the content for a README file for your project:

---

# University Chat Application with Secure File Transfer

## Team Members
- Abdelrahman Aly Mostafa
- Hassan Yasser
- Shehab Eldein Mohammed
- Omar Abdelaziz
- Tarek Saad

---

## Project Description
This project implements a **University Chat Application** with the following features:
1. **Chat Interface**: A GUI-based chat application allowing secure communication between a client and server.
2. **Course and Faculty Information**: Users can retrieve information about courses, professors, and departments.
3. **File Transfer**: Secure file transfer feature between client and server.
4. **Email Services**: Automated email sending and retrieval via SMTP and IMAP protocols.
5. **Web Integration**: Integration with a web interface for registration purposes.

---

## Technologies Used
- **Programming Language**: Python
- **Frameworks/Modules**:
  - `tkinter` for GUI development.
  - `smtplib` and `imap_tools` for email handling.
  - `socket` and `ssl` for network communication.
  - `webbrowser` for browser integration.
- **Security**: TLS encryption for secure communication.

---

## File Overview

### `server.py`
- **Purpose**: Implements the server-side logic of the chat application.
- **Features**:
  - Handles incoming connections with SSL encryption.
  - Processes chat commands and user requests.
  - Manages email sending, retrieval, and file transfers.
- **Execution**: 
  ```bash
  python server.py
  ```

### `client.py`
- **Purpose**: Implements the client-side logic with a user-friendly GUI.
- **Features**:
  - Allows users to send commands or chat messages to the server.
  - Supports secure file uploads.
  - Provides a scrolled chat display.
- **Execution**:
  ```bash
  python client.py
  ```

### `login.pdf`
- **Purpose**: Contains the HTML structure and style for the login interface.
- **Integration**: Used to integrate with the chat application for user registration functionality.

---

## How to Run the Project
1. **Setup Environment**:
   - Install Python 3.x.
   - Install required libraries:
     ```bash
     pip install imap-tools
     ```

2. **Prepare Certificates**:
   - Place `certificate.crt` and `private.key` files in the project directory.

3. **Start Server**:
   ```bash
   python server.py
   ```

4. **Run Client**:
   ```bash
   python client.py
   ```

---

## Features and Commands
- Start interaction: `start`
- Available commands:
  - `1`: List available courses.
  - `2`: Display professor names.
  - `3`: Show tuition fees and re-registration costs.
  - `4`: List faculty departments.
  - `5`: Transfer files.
  - `6`: Send email.
  - `7`: Retrieve sent emails.
  - `8`: Open registration page.
  - `9`: Exit.

---

## Future Enhancements
- Add user authentication for the chat system.
- Enhance the GUI for a more intuitive user experience.
- Expand email functionalities with attachments.

---

## License
This project is developed by **Team Members**. All rights reserved.

---

