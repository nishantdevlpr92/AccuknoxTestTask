# Accuknox

## Description

Accuknox is a social networking application API developed using Django Rest Framework. It provides various functionalities for user authentication, user search, friend management, and handling friend requests.

## Table of Contents
  - [Prerequisites](#prerequisites)
  - [Functionality](#functionality)
  - [Configuration](#configuration)
  - [Installation](#installation)
- [Usage](#usage)
- [License](#license)


### Prerequisites

List the software and tools that need to be installed before running the Docker Compose file. Provide links to installation instructions if necessary.

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)


## Functionality

    1. **User Authentication:**
        - Users can log in with their email and password.
        - Users can sign up with their email (no OTP verification required).

    2. **User Search:**
        - Search users by email or name (paginate up to 10 records per page).
        - Returns user(s) matching the search query.

    3. **Friend Management:**
        - Send, accept, or reject friend requests.
        - List friends (users who have accepted friend requests).
        - List pending friend requests (received friend requests).

    4. **Constraints:**
        - Only authenticated users can access most APIs.
        - Limit users to sending a maximum of 3 friend requests within a minute.


### Configuration

Contains the postgress environment variables that override the variables set in the .env file.

Here is a sample of `.env` file with key-value pairs:

```plaintext
POSTGRES_PASSWORD=betterwork
POSTGRES_USER=betterwork
POSTGRES_DB=betterwork
PGHOST=db
POSTGRES_PORT=5432
```

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/nishantdevlpr92/AccuknoxTestTask.git
   ```

2. Checkout in to the branch:

   ```bash
   git checkout main
   ```

3. Build Docker images for the services defined in your Docker Compose configuration:

   ```bash
   sudo docker-compose build
   ```
4. Start server:

   ```bash
   sudo docker-compose up -d
   ```

5. Create superuser:

   ```bash
   sudo docker exec -it accuknoxtesttask_web_1 python manage.py createsuperuser
   ```

6. Enter into django shell:

   ```bash
   sudo docker exec -it accuknoxtesttask_web_1 python manage.py shell
   ```

7. Down the containers:

   ```bash
   sudo docker-compose down -v
   ```

8. To run test cases:
   ```
   sudo docker exec -it accuknoxtesttask_web_1 python manage.py test
   ```

9. To find attached postman collection:
   [Accuknox.postman_collection.json](Accuknox.postman_collection.json) 

### Usage

1. Start the development server:

   ```bash
   sudo docker-compose up -d
   ```

2. Access the application at 

   `http://localhost:8000/`

3. Get the api documentation at 

   `http://localhost:8000/swagger`

4. Use this sign-up API (`http://localhost:8000/account/sign-up/`) to register user(this api manage case-insensitive).

5. Use this login API (`http://localhost:8000/devices-data/`) to login user to get access and refresh token to access another apis with user info.

6. The API at (`http://localhost:8000/api/user-list/`) is utilized to retrieve all active users, with a pagination setting of 10 users per page. Additionally, this API supports searching for users based on either their email or name(allowing for partial matches.)"

7. To list the friend connections of the logged-in user, make a request to (`http://localhost:8000/api/my-friend-list/`).

8. To send a friend request from a logged-in user to another valid user, call this(`http://localhost:8000/api/send-friend-request/`) API with the ID of the user you wish to send the request to.

9. A logged-in user can access the list of friend requests they've received by using this API: (`http://localhost:8000/api/friend-request-list/`)

10. If a logged-in user wishes to accept or reject a friend request connection, they can utilize the following API endpoint: (`http://localhost:8000/api/accept-reject-request/1/`)

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
