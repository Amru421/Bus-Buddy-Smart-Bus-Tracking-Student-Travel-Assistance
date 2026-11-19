# 🚌 BusBuddy – Smart Public Transport Tracking System

**Your Journey, Made Simpler!**

## 📌 About the Project

BusBuddy is a smart public transport tracking web application designed to make daily bus travel easier, faster, and more convenient.

The platform helps passengers search for available buses, explore routes, check departure times, view estimated arrival times, and monitor simulated bus locations through an interactive map.

It also provides an admin dashboard to manage bus information and routes.

## 🎯 Problem Statement

Passengers often face difficulties finding suitable buses, knowing their routes, checking departure timings, and estimating arrival times.

BusBuddy aims to provide a centralized digital platform that simplifies public transport information and improves the passenger travel experience.

## 💡 Objectives

- Simplify bus and route searching.
- Provide bus departure information.
- Display estimated arrival times.
- Show bus locations on an interactive map.
- Help students and passengers plan journeys.
- Provide administrators with bus management facilities.

## ✨ Key Features

### 👤 Passenger Features
- User registration and login.
- Passenger dashboard.
- Search buses by source and destination.
- View available bus routes.
- Check bus departure timings.
- Track simulated bus locations.
- View estimated arrival times.

### 🛠️ Admin Features
- Secure admin login.
- Admin dashboard.
- Add new buses.
- View available buses.
- Delete bus records.
- Manage bus information.

### 🗺️ Tracking Features
- Interactive map integration.
- Simulated bus movement.
- Automatic location updates.
- Estimated arrival information.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| HTML5 | Webpage structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend functionality |
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database management |
| Leaflet.js | Interactive maps |
| OpenStreetMap | Map data |

## 📂 Project Structure

```text
BusBuddy/
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── tracking.html
│   ├── routes.html
│   ├── admin.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── app.js
│           └── tracking.js
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.9 or above.
- Visual Studio Code.
- Web browser.
- Internet connection for map services.

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/BusBuddy.git
```

### Step 2: Open the Project

```bash
cd BusBuddy
```

### Step 3: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 4: Run the Application

```bash
python backend/app.py
```

### Step 5: Open in Browser

```text
http://127.0.0.1:5000
```

The application will initialize the SQLite database and insert sample bus records automatically.

## 🔐 Demo Administrator Account

For testing the admin dashboard:

- **Email:** admin@busbuddy.com
- **Password:** Admin123!

Change the default password and secret key before deployment.

## 🚌 Sample Bus Information

The application includes sample routes such as:

- Majestic → Electronic City
- Silk Board → Whitefield
- Hebbal → Banashankari
- Kengeri → Majestic

## 🔮 Future Enhancements

- Real-time GPS-based bus tracking.
- Integration with actual public transport APIs.
- Push notifications for bus delays.
- Google Maps integration.
- Fare estimation.
- Favourite routes and bus stops.
- Kannada and other regional language support.
- Mobile application integration.

## ⚠️ Current Project Limitations

This version is an educational prototype. Bus locations and estimated arrival times are simulated for demonstration purposes. It does not currently connect to physical GPS devices or live public transport services.

## 🌍 Expected Impact

BusBuddy aims to improve public transport accessibility, reduce uncertainty during travel, and help students and passengers plan their daily journeys more efficiently.

## 👩‍💻 Project Category

- Domain: Smart Transportation
- Project Type: Web Application
- Application: Public Transport Management
- Development Status: Prototype

## 📄 License

This project is developed for educational and academic purposes.

---

**BusBuddy – Making Public Transportation Smarter, Simpler, and More Accessible. 🚌**
