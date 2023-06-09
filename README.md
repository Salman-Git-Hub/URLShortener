# URLShortener
A simple URL shortener application.

![Example](../assets/img/example.png?raw=true)

## How to use?

 - First clone the repo.
```
git clone https://github.com/Salman-Git-Hub/URLShortener.git
```

 - Move to `URLShortener` folder.
```
cd URLShortener
```

 - Create a `.env` file, see [sample](.env_sample) for help.

 - Install the packages.
```
python -m pip install -r requirements.txt
```

 - Run, add `--reload` for auto reload
```
python -m uvicorn shortener_app.main:app
```
<br>

Open your browser and enter the base url (the one you wrote in the `.env` file) and add
`/docs` at the end of the url.
<br><br>
Or, simple click on the url shown by the application

![Output](../assets/img/img.png?raw=true)
