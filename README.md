# elevator_system
git clone https://github.com/kartikrathee95/elevator_system.git
1. pip install virtualenv
2. virtualenv env_name
3. env_name\Scripts\activate
4. pip install -r requirements.txt
5. run command: python manage.py runserver
6. go to 127.0.0.1:8000
7. click on 2nd button and go to terminal
8. Enter no of floors and users to generate testcase_file for.
9. Click on 3rd button, go to terminal and input : No_of_elevators and Maximum_floors_in_building
10. Click Enter.
11. System starts and UI will start once all testcases are fed to the system.

In next step, we can run the system on multiple production servers and the scripts now are working in sync with the business logic:

The further integration to productioon server will work like this on AWS:
# DEPLOY BACKEND

1. docker build -t elevator:latest --build-arg YOUR_ENV=testinhg .
3. aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 602037364990.dkr.ecr.us-east-1.amazonaws.com
4. docker tag elevator:latest 602037364990.dkr.ecr.us-east-1.amazonaws.com/ECR_RepoName:latest
5.docker push 602037364990.dkr.ecr.us-east-1.amazonaws.com/ECR_RepoName:latest
6. aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 602037364990.dkr.ecr.us-east-1.amazonaws.com
7. docker pull 602037364990.dkr.ecr.us-east-1.amazonaws.com/ECR_RepoName
8. docker run -p 8003:8000 --restart always -e ENV_FOR_DYNACONF=testing 602037364990.dkr.ecr.us-east-1.amazonaws.com/ECR_RepoName:latest

Now elevators can be turned ON at 08:00 hrs in the morning and stopped when the business day ends.
# UPDATE UI

1. python tkinter code flow understanding will allow us to make system even more functional on user end.
2. Take PR and deploy , testing servers ip = localhost:8000
