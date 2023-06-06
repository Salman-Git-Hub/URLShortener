from fastapi import HTTPException


def bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def not_found(request):
    msg = f'URL {request.url} does not exists!'
    raise HTTPException(status_code=404, detail=msg)
