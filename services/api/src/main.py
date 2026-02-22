import os, uuid
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Project, Appraisal
from .appraisal_engine.schemas import Assumptions, Outputs
from .appraisal_engine.engine import run_appraisal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dev Appraisal API")

origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/calculate", response_model=Outputs)
def calculate(a: Assumptions):
    return run_appraisal(a)

@app.post("/projects")
def create_project(payload: dict, db: Session = Depends(get_db)):
    p = Project(id=str(uuid.uuid4()), name=payload["name"], location=payload.get("location"))
    db.add(p)
    db.commit()
    return {"id": p.id}

@app.post("/projects/{project_id}/appraisals")
def create_appraisal(project_id: str, payload: dict, db: Session = Depends(get_db)):
    assumptions = Assumptions.model_validate(payload["assumptions"])
    outputs = run_appraisal(assumptions).model_dump()

    a = Appraisal(
        id=str(uuid.uuid4()),
        project_id=project_id,
        version_name=payload.get("version_name", "Base Case"),
        assumptions=assumptions.model_dump(),
        outputs=outputs,
        gdv=outputs["gdv"],
        tdc=outputs["tdc"],
        profit=outputs["profit"],
        profit_margin=outputs["profit_margin"],
        residual_land_value=outputs["residual_land_value"],
    )
    db.add(a)
    db.commit()
    return {"id": a.id, "outputs": outputs}

@app.get("/projects/{project_id}/appraisals")
def list_appraisals(project_id: str, db: Session = Depends(get_db)):
    rows = db.query(Appraisal).filter(Appraisal.project_id == project_id).order_by(Appraisal.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "version_name": r.version_name,
            "created_at": str(r.created_at),
            "kpis": {
                "gdv": r.gdv,
                "tdc": r.tdc,
                "profit": r.profit,
                "profit_margin": r.profit_margin,
                "residual_land_value": r.residual_land_value,
            },
        }
        for r in rows
    ]
