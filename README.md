# Cinema
# About project
## Models
   
   - User 
     - first_name
     - last_name
     - age
     - email
     - password
     - is_admin
     - is_active
   - Halls
     - title
     - rows
     - columns
   - Movies 
     - title 
     - description
     - year
     - description
     - duration
     - genres 
     - actors 
     - producer
     - age_rating 
     - in_rental
   - Sessions
     - movie (ForeignKey to Movie)
     - hall (ForeignKey to Hall)
     - date
     - start_at
     - end_at
     - tickets_price
     - is_active
   - Tickets
     - session (ForeignKey to Sessions)
     - owner (ForeignKey to CustomUser)
     - column 
     - row
     - sold
     - price
     - passed
     - is_active
## Urls
   - Home page
     - /home/ - Home page
   - Auth
     - auth/registration/ - Register users
     - auth/login/ - Login page
     - auth/refresh/ - Refreshing access token
     - auth/logout-access/ - Logout from account
     - auth/logout-refresh/ - Logout from account
 
   - Users
     - users/all/ - All users list
     - users/ - All active users list
     - users/{user_id}/ - User detail by id
     - users/create/ - Register user
     - users/update/{user_id}/ - Update user by id
     - users/delete/{user_id}/ - Delete user by id
   - Halls
     - halls/ - Halls list
     - halls/{hall_id}/ - Hall detail by id
     - halls/create/ - Create hall
     - halls/update/{hall_id}/ - Update hall 
     - halls/delete/{hall_id}/ - Delete hall
   - Sessions
     - sessions/ - Sessions list
     - sessions/{session_id}/ - Session dy id
     - sessions/movie/{movie_id}/ - Sessions with movie by movie_id
     - sessions/search/ - Page for search session by params
     - sessions/create/ - Create session
     - sessions/update/{session_id} - Update session
     - sessions/delete/{session_id} - Delete session
   - Movies
     - movies/ - All movies in rental list
     - movies/{movie_id} - Movie detail
     - movies/create/ - Create movie
     - movies/update/{movie_id}/ - Update movie
     - movies/delete/{movie_id}/ - Delete movie
   - Tickets
     - tickets/sold/ - All sold tickets
     - tickets/active/ - All active tickets
     - tickets/{ticket_id}/ - Ticket detail 
     - tickets/{session_id}/ - Tickets for session by session_id
   - API 
      - / - Swagger documentation for API 
## Setup 

1. Clone the repository:
    ```sh
    $ git clone https://github.com/Vladon2356/FinalProject-Flask.git
    $ cd FinalProject-Flask
    ```
2. Up docker container
    ```sh
   $ docker-compose build
   $ docker-compose up
   ```

Now Your can to search site
