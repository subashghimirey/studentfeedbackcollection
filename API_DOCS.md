# User & Authentication API Documentation

All endpoints are prefixed with: `http://localhost:8001/api/`

## 1. Authentication

### Login (Get Access Token)
**Endpoint:** `POST /login/`
**Description:** Authenticates a user and returns JWT access and refresh tokens.
**Required Body:**
```json
{
  "email": "user@example.com",
  "password": "your_secure_password"
}
```
**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI...",
  "refresh": "eyJhbGciOiJIUzI..."
}
```

### Refresh Token
**Endpoint:** `POST /login/refresh/`
**Description:** Get a new access token using a valid refresh token.
**Required Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI..."
}
```
**Response (200 OK):** returns a new `"access"` token.

---

## 2. User Management

### Register / Create User
**Endpoint:** `POST /users/`
**Description:** Creates a new user account. Open to anyone.
**Required Body:**
```json
{
  "email": "student@university.edu",
  "password": "secure_password"
}
```
**Optional Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```

### Get Current User Profile
**Endpoint:** `GET /users/me/`
**Description:** Returns the profile details of the currently logged-in user.
**Headers Required:** `Authorization: Bearer <access_token>`
**Body:** None
**Response (200 OK):**
```json
{
  "id": 1,
  "email": "student@university.edu",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "date_joined": "2026-05-05T10:00:00Z"
}
```

### Deactivate Account
**Endpoint:** `POST /users/deactivate/`
**Description:** Soft-deletes the logged-in user's account.
**Headers Required:** `Authorization: Bearer <access_token>`
**Body:** None
**Response (200 OK):** `{"message": "Account deactivated successfully."}`

### List Users (Admin Only)
**Endpoint:** `GET /users/`
**Description:** Returns a list of all users. Supports search via `?search=john`.
**Headers Required:** `Authorization: Bearer <access_token>` (Must be Admin/Staff)
**Body:** None

---

## 3. Password Reset Flow

### Request Password Reset Link
**Endpoint:** `POST /password-reset/`
**Description:** Generates a reset link for the user (simulated in the response for now).
**Required Body:**
```json
{
  "email": "student@university.edu"
}
```
**Response (200 OK):**
```json
{
  "message": "Password reset link generated.",
  "link": "/reset-password/Nw/bdu3a3-9a3..."
}
```

### Confirm Password Reset
**Endpoint:** `POST /password-reset-confirm/<uidb64>/<token>/`
**Description:** Submits the new password using the UID and Token from the generated link.
**URL Parameters:** `uidb64` and `token` (extracted from the link).
**Required Body:**
```json
{
  "password": "new_secure_password"
}
```
**Response (200 OK):** `{"message": "Password has been reset successfully"}`

---

## 4. Master Data (Courses & Instructors)

### List Courses
**Endpoint:** `GET /courses/`
**Description:** Returns a list of all available courses.
**Headers Required:** `Authorization: Bearer <access_token>`
**Response:**
```json
[
  {
    "id": 1,
    "code": "CS101",
    "name": "Intro to Computer Science"
  }
]
```

### List Instructors
**Endpoint:** `GET /instructors/`
**Description:** Returns a list of all available instructors.
**Headers Required:** `Authorization: Bearer <access_token>`
**Response:**
```json
[
  {
    "id": 1,
    "name": "Dr. Alan Turing"
  }
]
```

---

## 5. Feedback Submissions

### Submit Feedback
**Endpoint:** `POST /feedbacks/`
**Description:** Submit anonymous or user-linked feedback for a course or instructor.
**Headers Required:** None (Open to all if `is_anonymous` is true, otherwise pass token)
**Required Body:**
```json
{
  "feedback_type": "COURSE",  // Use "INSTRUCTOR" if grading a specific teacher
  "course": 1,                // ID of the course
  "instructor": null,         // Required (ID) IF feedback_type is "INSTRUCTOR"
  "semester": "SPRING",       // "SPRING", "SUMMER", "FALL", "WINTER"
  "is_anonymous": true,
  "teaching_quality": 5,      // Rating (1-5)
  "course_content": 4,        // Rating (1-5)
  "engagement": 5,            // Rating (1-5)
  "overall_satisfaction": 4,  // Rating (1-5)
  "positive_feedback": "The materials were clear and well-structured.",
  "improvement_feedback": "Exams were a bit too long for the time allotted."
}
```
**Optional Body:**
```json
{
  "would_recommend": true
}
```
**Response (201 Created):**
```json
{
  "id": 1,
  "course_code": "CS101",
  ... (saved data including auto-generated 'created_at')
}
```

### List All Feedback (Admin/Staff Only)
**Endpoint:** `GET /feedbacks/`
**Description:** Get all student feedback submissions.
**Headers Required:** `Authorization: Bearer <access_token>`
**Response:** Array of feedback objects.
