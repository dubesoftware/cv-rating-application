# CV Rating Application
A minimal proof-of-concept application that enables a user to upload their CV and receive back a score out of 10 as well as several recommendations for improvement.

## Instructions
This application is written in the Flask python web framework. To run it, do the following:
- Install Python >= 3.13.2 using your preferred Python version manager, such as [asdf](https://asdf-vm.com/) or [mise](https://mise.jdx.dev/)
- Run the command `python -v` to confirm that your Python installation was successful
- Create a virtual environment with the command `python3 -m venv {env-name}`, where env-name is the desired name of your virtual environment
- Install the [Pip](https://pypi.org/project/pip/) Python package installer
- From a terminal, enter a preferred working directory and clone the project repo
- From the project's root directory' run the command `pip install -r requirements.txt`
- Once the dependencies are successfully installed, set up the ConvertAPI and OpenAI keys by adding them into your server's os.environ (environment variables). WARNING: Under *no* circumstances should credentials be shared in messages, emails, or checked in with source code as inline variables
- Run the project with the command `python run.py`
- View the web interface at http://127.0.0.1:5000