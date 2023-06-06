from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL
from sqlalchemy.orm import Session
import validators

from . import schemas, models, crud, errors
from .config import get_settings
from .database import get_db, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_url_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    details_endpoint = app.url_path_for(
        "URL info", admin_key=db_url.admin_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=details_endpoint))
    return db_url


@app.get("/")
def home():
    return "Hello World!"


@app.post("/url", response_model=schemas.URLInfo, name="Shorten url")
def shorten_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        errors.bad_request("Invalid url!")
    db_url = crud.create_url(db, url)
    return get_url_info(db_url)


@app.get("/{url_key}", name="Access url")
def access_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    # walrus operator (:=); assign variables in middle of expressions
    # For more see:
    #   - https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions
    #   - https://realpython.com/python-walrus-operator/
    if db_url := crud.get_url_by_key(db, url_key):
        crud.update_view_count(db, db_url)
        return RedirectResponse(db_url.target_url)
    else:
        errors.not_found(request)


@app.get("/admin/urls", name="List urls", response_model=list[schemas.URLInfo])
def all_urls(db: Session = Depends(get_db)):
    db_urls = [get_url_info(d) for d in crud.get_all_url(db)]
    if db_urls:
        return db_urls
    else:
        return "No urls created!"


@app.get("/admin/{admin_key}", name='URL info', response_model=schemas.URLInfo)
def url_info(admin_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_url_by_admin_key(db, admin_key):
        return get_url_info(db_url)
    else:
        print("Hmm")
        errors.not_found(request)


@app.delete("/delete/{admin_key}", name="Delete url")
def delete_url(admin_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_admin_key(db, admin_key)
    if db_url.is_active:
        crud.update_url(db, db_url)
        return {
            "message": f"Deleted URL for: {db_url.target_url}"
        }
    else:
        errors.not_found(request)


@app.put("/update/{admin_key}", name="Activate url")
def activate_url(admin_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_not_active_url(db, admin_key)
    if not db_url.is_active:
        crud.update_url(db, db_url)
        return {
            "message": f"Activated URL for: {db_url.target_url}"
        }
    else:
        errors.not_found(request)
