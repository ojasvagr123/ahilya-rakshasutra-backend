from fastapi import APIRouter, Request, Depends, Header, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from ..db import get_session
from ..models import HoneypotEvent
import os

router = APIRouter(prefix="/honeypot", tags=["honeypot"])
INGEST_TOKEN = os.getenv("INGEST_TOKEN", "dev")

def check_token(x_ingest_token: str | None):
    if INGEST_TOKEN and x_ingest_token != INGEST_TOKEN:
        raise HTTPException(status_code=401, detail="bad token")

class CowrieEvent(BaseModel):
    timestamp: str | None = None
    src_ip: str | None = None
    message: str | None = None
    sensor: str | None = None

class WebEvent(BaseModel):
    ip: str
    user_agent: str | None = None
    path: str
    area: str | None = "Unknown"

@router.post("/cowrie/ingest")
def cowrie_ingest(ev: CowrieEvent, session: Session = Depends(get_session), x_ingest_token: str | None = Header(default=None)):
    check_token(x_ingest_token)
    e = HoneypotEvent(ip=ev.src_ip or "unknown", user_agent=ev.sensor or "cowrie", path="/cowrie", area="SSH")
    session.add(e); session.commit()
    return {"ok": True}

@router.post("/web/ingest")
def web_ingest(ev: WebEvent, session: Session = Depends(get_session), x_ingest_token: str | None = Header(default=None)):
    check_token(x_ingest_token)
    e = HoneypotEvent(ip=ev.ip, user_agent=ev.user_agent, path=ev.path, area=ev.area or "Unknown")
    session.add(e); session.commit()
    return {"ok": True}
