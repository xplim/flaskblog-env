# Flask Blog

## Getting Started

1. Create a virtual environment.

    ```sh
    $ python -m venv venv
    ```

2. Add new files to the `venv/bin/` directory to manage environment variables.

    - **`.env-activate`**

        ```
        export SECRET_KEY="..."
        export SQLALCHEMY_DATABASE_URI="sqlite:///site.db"
        export EMAIL_USER="[username]@gmail.com"
        export EMAIL_PASS="..."
        ```

       - **`SECRET_KEY`**: Used to generate a token to reset password.
         Use Python's built-in `secrets` module to generate one as follows in the Terminal:

         ```sh
         $ python
         ```

         ```python
         >>> import secrets
         >>> secrets.token_hex(16)
         '9ae26a636cc6dd4496fbbdf1baf39905'
         ```

       - **`EMAIL_USER`** and **`EMAIL_PASS`**: Used to send out emails with the password reset link.

         - The current [`[MAIL_]` configurations](flaskblog/application/config.py) are set for the Gmail server.
           Different settings are required if you'd like to use a different mail service provider to send out the emails.

    - **`.env-deactivate`**

        ```
        unset SECRET_KEY
        unset SQLALCHEMY_DATABASE_URI
        unset EMAIL_USER
        unset EMAIL_PASS
        ```

3. In the `venv/bin/activate` file, add the following code blocks (wrapped between the `START` and `END` comments), to deactivate and activate our custom environment variables.

    ```sh
    deactivate () {
        # >>> START >>>
        # deactivate custom environment variables
        if [ -f $VIRTUAL_ENV/bin/.env-deactivate ] ; then
            source $VIRTUAL_ENV/bin/.env-deactivate
        fi
        # <<<< END <<<<

        # reset old environment variables
        ...
    ```

    ```sh
    VIRTUAL_ENV=".../flaskblog-env/venv"
    export VIRTUAL_ENV

    _OLD_VIRTUAL_PATH="$PATH"
    PATH="$VIRTUAL_ENV/bin:$PATH"
    export PATH

    # >>> START >>>
    # activate custom environment variables
    if [ -f $VIRTUAL_ENV/bin/.env-activate ] ; then
        source $VIRTUAL_ENV/bin/.env-activate
    fi
    # <<<< END <<<<

    # unset PYTHONHOME if set
    ...
    ```

4. Activate the virtual environment.

    ```sh
    $ source venv/bin/activate
    ```

5. Install packages required.

    ```sh
    $ pip install -r requirements.txt
    ```

6. Start the server for the Flask web application.

    ```sh
    $ cd flaskblog

    $ python run.py
    ...
    * Running on http://127.0.0.1:[PORT_NUMBER]/
    ...
    ```

7. Open `http://localhost:[PORT_NUMBER]` in the web browser.

## Acknowledgments

This project is created by following along the [*Flask Tutorials*][1] series by *Corey Schafer*.

<!-- Reference Links -->
[1]: https://youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
