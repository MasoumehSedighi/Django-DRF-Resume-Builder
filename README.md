# Resume-Builder
<div align="center">
 <h3>A resume builder application using Django REST Framework and Token Authentication</h3>
<img loading="lazy" style="width:400px" src="resume-img.jpg">
</div>

# Features
- Custom User Model
- Profile model
- Signal Profile
- Django RestFramework
- Token Authentication
- API Docs
- Docker
- Flake8
- Tests

# Setup Project
1. You'll need to have [Docker installed](https://docs.docker.com/get-docker/).

2. Clone this repo anywhere you want and move into the directory:
```bash
git clone git@github.com:MasoumehSedighi/Django-DRF-Resume-Builder.git
```

3. Add a .env file to the root of the project as shown in .env.example and add your created config
4. Start with Docker Compose:
```bash
docker compose up --build
docker compose up
```
5. Visit <http://localhost:8000> in your favorite browser.
6. Run the following command to create a superuser with admin priviledges:
 ```bash
docker compose run --rm app sh -c "python manage.py createsuperuser" 
```
7. Run the tests using the following command:
 ```bash
 docker compose run --rm app sh -c "python manage.py test"
```
# API document
 in order to use the api in document format you can simply head to this url
 
 - http://localhost:8000/docs/

   ![image](https://github.com/user-attachments/assets/0ed2df34-6db8-414a-94e7-5e812b7f0091)

  or if you prefer redoc you can use :
  
 - http://localhost:8000/redoc/

![image](https://github.com/user-attachments/assets/75201502-2c38-4593-afc5-8e748b6893ba)


# Bugs
Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.
