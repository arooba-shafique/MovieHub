
# 🎬 MovieHub

MovieHub is a **modern Django-based web application** that lets users **discover, browse, and explore movies** with ease. It integrates with the **TMDB (The Movie Database) API** to fetch dynamic movie data and provides an engaging and interactive movie browsing experience.

---

## 🚀 Features

* 🎞️ **Dynamic Movie Posters** — Fetches movie data and posters from TMDB. ([GitHub][1])
* 🔍 **Search Movies** — Easily search for movies by name. ([GitHub][1])
* 📊 **Movie Details** — View detailed information about each movie. ([GitHub][1])
* 👤 **User Signup/Login** — Authentication system for users. ([GitHub][1])
* 📱 **Responsive Design** — Works on desktop and mobile devices. ([GitHub][1])
* ✨ **Beautiful Hero Section** — Stylish layout with gradient animations and modern UI. ([GitHub][1])

---

## 🛠️ Technologies Used

**Backend:** Python, Django
**Frontend:** HTML, Tailwind CSS, JavaScript
**API:** TMDB API for movie data
**Database:** SQLite

---

## 📦 Project Structure

Typical structure includes:

```
movie_project/      
movies/             
manage.py           
README.md          
.gitignore          
```

---

## 🚀 Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/arooba-shafique/MovieHub.git
   ```

2. **Navigate to the project directory**

   ```bash
   cd MovieHub
   ```

3. **Create and activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   
   venv\Scripts\activate    
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**

   * Create a `.env` file
   * Add your **TMDB API key**

   Example:

   ```env
   TMDB_API_KEY=your_api_key_here
   ```

6. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Open in browser**
   Visit `http://127.0.0.1:8000`

