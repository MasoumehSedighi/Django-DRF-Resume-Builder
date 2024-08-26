# Resume-Builder
<div align="center">
<img loading="lazy" style="width:700px" src=".[/docs/hamravesh-banner.png](https://static.vecteezy.com/system/resources/previews/004/619/996/non_2x/online-job-application-color-icon-job-search-website-online-resume-builder-cv-maker-recruitment-website-isolated-illustration-vector.jpg)">
</div>


A resume builder web application using Django REST Framework


# usage
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
docker-compose run --rm app sh -c "python manage.py createsuperuser" 
```
7. Run the tests using the following command:
 ```bash
 docker-compose run --rm app sh -c "python manage.py test"
```
# API document usage
 open your browser with these URLs:
 - http://localhost:8000/docs/
 - http://localhost:8000/redoc/

# Bugs
Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.
