from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import URL, generate_short_code
from app.schemas import URLCreate, URLResponse
from app.cache import (
    get_cached_url, set_cached_url,
    increment_click_cache, get_cached_clicks
)
from app.kafka_producer import publish_click_event
from app.websocket_manager import manager

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_url = URL(
        original_url=str(url_data.original_url),
        short_code=short_code
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    set_cached_url(short_code, str(new_url.original_url))

    return new_url


@router.get("/urls", response_model=list[URLResponse])
def get_all_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).all()
    return urls


@router.get("/{short_code}")
async def redirect_url(short_code: str, db: Session = Depends(get_db)):
    cached_url = get_cached_url(short_code)

    if cached_url:
        increment_click_cache(short_code)
        cached_clicks = get_cached_clicks(short_code)

        publish_click_event(short_code, cached_url)

        await manager.broadcast({
            "event": "click",
            "short_code": short_code,
            "original_url": cached_url,
            "clicks": cached_clicks,
            "source": "cache"
        })

        return {
            "original_url": cached_url,
            "clicks": cached_clicks,
            "source": "cache"
        }

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    url.clicks += 1
    db.commit()

    set_cached_url(short_code, url.original_url)
    publish_click_event(short_code, url.original_url)

    await manager.broadcast({
        "event": "click",
        "short_code": short_code,
        "original_url": url.original_url,
        "clicks": url.clicks,
        "source": "database"
    })

    return {
        "original_url": url.original_url,
        "clicks": url.clicks,
        "source": "database"
    }


@router.websocket("/ws/analytics")
async def analytics_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/stats/{short_code}", response_model=URLResponse)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    cached_clicks = get_cached_clicks(short_code)
    if cached_clicks > 0:
        url.clicks = cached_clicks

    return url