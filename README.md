# Grade Tracker

---
## How it Works:
#### 1. It uses a Canvas API to access your canvas account.
#### 2. It then searches for your classes that you are currently enrolled in (In my case I have it set to Spring 2026)
#### 3. After that, it finds your "current_grade" for each class and saves it to the Shortcuts folder inside your ICloud Drive
#### 4. It also calculates your GPA and saves it to the same folder
#### 5. Inside your shortcut app on IOS, you can create a shortcut that sends the grades to your phone as a text message each week

## How to Run it
#### 1. Clone the repository:
   ```bash
   git clone https://github/jonahmabry/grade_tracker.git
   cd grade_tracker
   ```

#### 2. Set up the Python environment:
```bash
uv sync
source .venv/bin/activate
```

#### 3. Configure environment variables:
Create a `.env` file with your Canvas API key

Your `.env` file should look like:
```bash
CANVAS_TOKEN={your_canvas_api_token}
```

#### 4. Run `main.py`
