from typing import Optional
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import pandas as pd
from sql import crud, models, schemas
from sql.database import SessionLocal, engine
from gcp_storage import list_files_in_storage, download_file_as_bytes
from cleaner import clean_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class AlreadyExistsException(Exception):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _create_ship(ship: schemas.Ship, db: Session):
    db_ship = crud.get_ship(db, imo_number=ship.imo_number, reporting_period=ship.reporting_period)
    if db_ship:
        raise AlreadyExistsException()
    return crud.create_ship(db=db, ship=ship)

def _create_monitoring_result(monitoring_result: schemas.MonitoringResult, db: Session):
    db_monitoring_result = crud.get_monitoring_result(db, imo_number=monitoring_result.imo_number, reporting_period=monitoring_result.reporting_period)
    if db_monitoring_result:
        raise AlreadyExistsException()
    return crud.create_monitoring_result(db=db, monitoring_result=monitoring_result)

@app.post("/create_ship/", response_model=schemas.Ship)
def create_ship(ship: schemas.Ship, db: Session = Depends(get_db)):
    return _create_ship(ship, db)

@app.post("/create_monitoring_result/", response_model=schemas.MonitoringResult)
def create_monitoring_result(monitoring_result: schemas.MonitoringResult, db: Session = Depends(get_db)):
    return _create_monitoring_result(monitoring_result, db)

@app.get("/load_data/")
def load_data_into_db(db: Session = Depends(get_db)):
    failed_inserts = {"ships": [], "monitoring_results": []}
    files = list_files_in_storage()
    dfs = []
    for file in files:
        data = download_file_as_bytes(file)
        dfs.append(clean_file(data))
    data = pd.concat(dfs).to_dict(orient="records")
    for d in data:
        ship = schemas.Ship(**d)
        try:
            _ = _create_ship(ship, db)
        except AlreadyExistsException:
            failed_inserts["ships"].append(ship)
        monitoring_result = schemas.MonitoringResult(**d)
        try:
            _ = _create_monitoring_result(monitoring_result, db)
        except AlreadyExistsException:
            failed_inserts["monitoring_results"].append(monitoring_result)
            
    return failed_inserts

@app.get("/ship/", response_model=schemas.Ship)
def ship(imo_number: int, reporting_period: int, db: Session = Depends(get_db)):
    ship = crud.get_ship(db, imo_number=imo_number, reporting_period=reporting_period)
    return ship

@app.get("/monitoring_result/", response_model=schemas.MonitoringResult)
def monitoring_result(imo_number: int, reporting_period: str, db: Session = Depends(get_db)):
    monitoring_result = crud.get_monitoring_result(db, imo_number=imo_number, reporting_period=reporting_period)
    return monitoring_result

@app.get("/thetis_mrv_view/", response_model=list[schemas.ThetisMRVView])
def thetis_mrv_view(imo_number: Optional[int] = None, ship_name: Optional[str] = None, reporting_period: int = None, db: Session = Depends(get_db)):
    ships = crud.thetis_mrv_view(db, imo_number=imo_number, ship_name=ship_name, reporting_period=reporting_period)
    return ships.limit(50).all()

