# Testing Sample App (WIP)

This is a sample application designed for testing a user management system with microservices. The application is built to allow user creation, viewing, and deletion, implemented using **FastAPI** for the backend and **Streamlit** for the frontend.

## Project Structure 

The application is divided into microservices and frontend:

PENDING DIAGRAM


### Backend

The backend consists of the **user-management** microservice, which handles user CRUD operations using **FastAPI** and a **PostgreSQL** database. The service includes functionality for user authentication and permission checks.

### Frontend

The frontend is a **Streamlit** application that communicates with the backend through API calls. It allows users to interact with the system by viewing a list of users, adding new users, and deleting them.

### Microservices

- **user-management**: Manages user authentication and CRUD operations for users.
- **postgresql**: PostgreSQL database to store user information.
- **ui**: Frontend application built using Streamlit.

### Features

- **User CRUD operations**: Create, read, update, and delete users.
- **Permissions handling**: Each user has associated permissions which can be validated before performing certain actions.
- **Streamlit UI**: A simple user interface to manage users.

## Running the Application

To run the application locally, you can use `docker-compose` to spin up all the necessary services. Make sure you have **Docker** and **Docker Compose** installed.

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
