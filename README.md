# Digital Student Feedback System (Backend)

Welcome to the backend repository for the **Digital Student Feedback System**. This robust Django-based API powers an academic prototype designed to collect, process, and analyze student feedback for courses and instructors. It features a unique **Hybrid Sentiment Analysis** engine to extract actionable insights from both quantitative ratings and qualitative text feedback.

## 🚀 Key Features

### Current Features
*   **Custom Authentication:** Secure, email-based authentication utilizing JWT (JSON Web Tokens).
*   **Survey & Feedback Management:** Granular tracking of feedback mapped to `Courses` and `Instructors`. Supports both associated and strictly anonymous feedback submissions.
*   **Hybrid Sentiment Analysis:** A sophisticated service layer leveraging NLP (`vaderSentiment`). It calculates a normalized sentiment score dynamically weighted by:
    *   Text Analysis (50% weight) - Using VADER NLP
    *   Numeric Ratings (40% weight)
    *   Recommendation Flags (10% weight)
*   **Analytics Engine:** Real-time metrics aggregation including sentiment distribution (Positive/Neutral/Negative), average ratings, timeline trends, and anonymity rates.
*   **Granular Permissions:** Authenticated users can fetch and manage their own non-anonymous feedback and update their profiles, while administrators have sweeping analytical access.
*   **Dockerized Architecture:** Completely containerized with PostgreSQL for easy deployment, scalability, and local development.

### 🔮 Planned / Upcoming Features
*   **Report Analysis Dashboard:** Comprehensive reporting insights directly within the admin dashboard.
*   **Generative Feedback Summaries:** AI-driven summaries of massive qualitative feedback sets for courses/instructors.
*   **Sentiment Word Clouds:** Visual representations of frequently used terms in positive vs. negative feedback.
*   **Data Export (Download to CSV):** One-click data exports for institutional records and offline analysis.
*   **Time-Gating:** Restricting survey submissions to specific time windows (e.g., end-of-semester weeks).

---

## 🛠️ Technology Stack
*   **Framework:** Django & Django REST Framework (DRF)
*   **Database:** PostgreSQL (`postgres:15`)
*   **Containerization:** Docker & Docker Compose
*   **Authentication:** `djangorestframework-simplejwt`
*   **NLP/Sentiment:** `vaderSentiment`
*   **Cross-Origin:** `django-cors-headers`

---

## ⚙️ Setup & Installation

This project is fully dockerized. To get started locally:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd backend
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   *This command will build the Django web container and launch the PostgreSQL database container.*

3. **Database Migrations:**
   *(If not run automatically by an entrypoint)*
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a Superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

The API will be available locally at `http://localhost:8001/` (or the port specified in your `docker-compose.yml`).

---

## 📡 Core API Endpoints

### 👤 Users (`/api/users/`)

#### 1. Register User
*   **Endpoint:** `POST /api/users/register/`
*   **Request:**
    ```json
    {
      "email": "student@example.com",
      "password": "securepassword123",
      "first_name": "Jane",
      "last_name": "Doe"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "email": "student@example.com",
      "first_name": "Jane",
      "last_name": "Doe"
    }
    ```

#### 2. User Login
*   **Endpoint:** `POST /api/users/login/`
*   **Request:**
    ```json
    {
      "email": "student@example.com",
      "password": "securepassword123"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "refresh": "eyJhbGci...<refresh_token>",
      "access": "eyJhbGci...<access_token>"
    }
    ```

#### 3. Get User Profile
*   **Endpoint:** `GET /api/users/profile/`
*   **Headers:** `Authorization: Bearer <access_token>`
*   **Response (200 OK):**
    ```json
    {
      "id": 1,
      "email": "student@example.com",
      "first_name": "Jane",
      "last_name": "Doe"
    }
    ```

#### 4. Update User Profile
*   **Endpoint:** `PATCH /api/users/profile/`
*   **Headers:** `Authorization: Bearer <access_token>`
*   **Request:**
    ```json
    {
      "first_name": "Janet"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "id": 1,
      "email": "student@example.com",
      "first_name": "Janet",
      "last_name": "Doe"
    }
    ```

### 📝 Surveys & Feedback (`/api/surveys/`)

#### 1. List Courses
*   **Endpoint:** `GET /api/surveys/courses/`
*   **Headers:** `Authorization: Bearer <access_token>`
*   **Response (200 OK):**
    ```json
    [
      {
        "id": 1,
        "title": "Introduction to Computer Science",
        "code": "CS101",
        "description": "Basics of algorithms and programming."
      }
    ]
    ```

#### 2. List Instructors
*   **Endpoint:** `GET /api/surveys/instructors/`
*   **Headers:** `Authorization: Bearer <access_token>`
*   **Response (200 OK):**
    ```json
    [
      {
        "id": 1,
        "first_name": "Alan",
        "last_name": "Turing",
        "department": "Computer Science"
      }
    ]
    ```

#### 3. Submit Feedback
*   **Endpoint:** `POST /api/surveys/feedbacks/`
*   **Headers:** `Authorization: Bearer <access_token>`
*   **Request:**
    ```json
    {
      "course": 1,
      "instructor": 1,
      "rating": 4,
      "text": "Great course, but the assignments were very difficult.",
      "would_recommend": true,
      "is_anonymous": false
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "id": 15,
      "course": 1,
      "instructor": 1,
      "rating": 4,
      "text": "Great course, but the assignments were very difficult.",
      "would_recommend": true,
      "is_anonymous": false,
      "sentiment_score": 0.68,
      "sentiment_label": "Positive",
      "created_at": "2024-05-18T10:00:00Z"
    }
    ```

#### 4. View My Feedback
*   **Endpoint:** `GET /api/surveys/feedbacks/`
*   **Headers:** `Authorization: Bearer <access_token>`
*   **Description:** Returns a list of feedbacks submitted by the authenticated user.
*   **Response (200 OK):**
    ```json
    [
      {
        "id": 15,
        "course": 1,
        "instructor": 1,
        "rating": 4,
        "text": "Great course...",
        "sentiment_label": "Positive"
      }
    ]
    ```

### 📊 Analytics (`/api/analytics/`)

#### 1. Course Analytics
*   **Endpoint:** `GET /api/analytics/course/<id>/`
*   **Headers:** `Authorization: Bearer <access_token>` (Requires Admin/Staff)
*   **Response (200 OK):**
    ```json
    {
      "course_id": 1,
      "course_code": "CS101",
      "total_feedbacks": 120,
      "average_rating": 4.1,
      "sentiment_distribution": {
        "positive": 80,
        "neutral": 25,
        "negative": 15
      },
      "recommendation_rate": 85.5
    }
    ```

#### 2. Instructor Analytics
*   **Endpoint:** `GET /api/analytics/instructor/<id>/`
*   **Headers:** `Authorization: Bearer <access_token>` (Requires Admin/Staff)
*   **Response (200 OK):**
    ```json
    {
      "instructor_id": 1,
      "name": "Alan Turing",
      "total_feedbacks": 200,
      "average_rating": 4.5,
      "sentiment_distribution": {
        "positive": 150,
        "neutral": 40,
        "negative": 10
      }
    }
    ```

---

## 🧠 How the Hybrid Sentiment Analysis Works

Instead of relying solely on NLP (which can misinterpret sarcasm or academic phrasing), our `SentimentService` calculates a robust hybrid score:
1. **Qualitative (50%):** VADER analyzes the open text feedback for polarity.
2. **Quantitative (40%):** The user's integer rating (e.g., 1-5 scale) is normalized.
3. **Binary Intent (10%):** The `would_recommend` boolean is converted to a positive/negative boost.
*Note: If the recommendation boolean is omitted or the user provided no text, the weighting scales dynamically to cover 100% using available factors.*
