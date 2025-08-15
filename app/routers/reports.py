from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from ..models import Report, ReportType
from ..schemas import ReportIn, ReportOut
from ..deps import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("", response_model=ReportOut)
def create_report(body: ReportIn, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if body.type not in ("sms", "url", "voip"):
        raise HTTPException(status_code=400, detail="type must be sms|url|voip")
    rep = Report(
        type=ReportType(body.type),
        payload_json=body.payload or {},
        lat=body.lat, lon=body.lon,
        area=body.area or "Unknown",
        created_by=user.id
    )
    session.add(rep)
    session.commit()
    session.refresh(rep)
    return ReportOut(
        id=rep.id, type=rep.type.value, payload=rep.payload_json,
        lat=rep.lat, lon=rep.lon, area=rep.area,
        created_at=rep.created_at.isoformat()
    )
