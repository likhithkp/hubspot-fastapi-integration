
# Redis, HubSpot, and FastAPI Integration

This project demonstrates how to integrate **Redis**, **HubSpot**, and **FastAPI** to build a scalable backend solution. Redis is used for managing OAuth credentials and session data, while HubSpot’s API is used to manage CRM data. FastAPI is the web framework that provides fast, asynchronous APIs.

## Features

- **OAuth Credential Management**: Redis is used to securely manage OAuth credentials and sessions.
- **HubSpot Integration**: Fetch and manage CRM and marketing data using HubSpot’s API.
- **FastAPI**: A fast web framework for creating asynchronous APIs.
- **Caching**: Redis is also used for caching data to improve the performance of the system.

## Technologies

- **FastAPI**: A modern web framework for building high-performance APIs with Python.
- **Redis**: In-memory data store for caching, OAuth credential management, and session management.
- **HubSpot API**: CRM and marketing automation integration via HubSpot's REST API.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7+
- Redis (for local development, or a Redis cloud service)
- HubSpot API key (you will need to generate one from HubSpot’s developer portal)

### Steps to Set Up

1. **Clone the Repository**

   ```bash
   git clone https://github.com/likhithkp/hubspot-fastapi-integration
   cd hubspot-fastapi-integration
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Redis**

   Ensure Redis is running locally or configure it to use a cloud Redis service. If you're running Redis locally, you can start it with:

   ```bash
   redis-server
   ```

5. **Configure HubSpot API**

   Set up your HubSpot API key in the `.env` file or directly in your environment variables:

   ```bash
   HUBSPOT_API_KEY=your-hubspot-api-key
   ```

6. **Run the FastAPI Application**

   ```bash
   uvicorn app.main:app --reload
   ```

   This will start the FastAPI server locally on `http://127.0.0.1:8000`.

## Usage

### Endpoints

- **GET /integrations/hubspot/authorize**: Create oauth state and generate authorized URL.
- **GET /integrations/hubspot/oauth2callback**: Callback function which validates the credentials.
- **GET /integrations/hubspot/credentials**: Fetch credentials from redis and send to frontend.
- **GET /integrations/hubspot/get_hubspot_items**: Fetches required data (any data) from HubSpot.
  
For detailed API documentation, visit `http://127.0.0.1:8000/docs` after running the server.

### Managing OAuth Credentials

- Redis is used to store and manage OAuth tokens securely for each user session.
- When a user logs in, the OAuth credentials are stored in Redis for quick access.

## Contributing

Contributions are welcomed! If you'd like to contribute to the project, follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
