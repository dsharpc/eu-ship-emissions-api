from typing import Optional, Dict
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import pandas as pd
from sql import crud, models, schemas
from sql.database import SessionLocal, engine
from gcp_storage import list_files_in_storage, download_file_as_bytes
from cleaner import clean_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Endpoints for THETIS-MRV data for Carbon Chain", description="Built by Daniel Sharp")

class AlreadyExistsException(Exception):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _create_ship(ship: schemas.Ship, db: Session) -> models.Ship:
    """Helper function that inserts a Ship record into the database if it doesns't exist already

    Parameters
    ----------
    ship : schemas.Ship
    db : Session

    Returns
    -------
    models.Ship
        Ship object of newly inserted record

    Raises
    ------
    AlreadyExistsException
        Raised if Ship record already exists in database
    """
    db_ship = crud.get_ship(db, imo_number=ship.imo_number, reporting_period=ship.reporting_period)
    if db_ship:
        raise AlreadyExistsException()
    return crud.create_ship(db=db, ship=ship)

def _create_monitoring_result(monitoring_result: schemas.MonitoringResult, db: Session):
    """Helper function that inserts a MonitoringResult record into the database if it doesns't exist already

    Parameters
    ----------
    monitoring_result : schemas.MonitoringResult
    db : Session

    Returns
    -------
    models.MonitoringResult
        Ship object of newly inserted record

    Raises
    ------
    AlreadyExistsException
        Raised if MonitoringResult record already exists in database
    """
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
def load_data_into_db(db: Session = Depends(get_db)) -> Dict[str, int]:
    """Download data files from the GCP Storage Bucket and insert the data into the database.

    Parameters
    ----------
    db : Session, optional
        database session, by default Depends(get_db)

    Returns
    -------
    Dict[str, int]
        Count of the records that failed to be inserted
    """
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
    """Returns data for a specific Ship

    Parameters
    ----------
    imo_number : int
        Ship's IMO Number
    reporting_period : int
        Ship's reporting period of interest
    db : Session, optional

    Returns
    -------
    models.Ship
        Relevant data for the Ship
    """
    ship = crud.get_ship(db, imo_number=imo_number, reporting_period=reporting_period)
    return ship

@app.get("/monitoring_result/", response_model=schemas.MonitoringResult)
def monitoring_result(imo_number: int, reporting_period: str, db: Session = Depends(get_db)):
    """Returns data for a specific MonitoringResult

    Parameters
    ----------
    imo_number : int
        Ship's IMO Number
    reporting_period : int
        Ship's reporting period of interest
    db : Session, optional

    Returns
    -------
    models.MonitoringResult
        Relevant data for the MonitoringResult
    """
    monitoring_result = crud.get_monitoring_result(db, imo_number=imo_number, reporting_period=reporting_period)
    return monitoring_result

@app.get("/thetis_mrv_view/", response_model=list[schemas.ThetisMRVView])
def thetis_mrv_view(imo_number: Optional[int] = None, ship_name: Optional[str] = None, reporting_period: int = None, db: Session = Depends(get_db)):
    """View that mimics frontpage of the THETIS-MRV website. It allows for search functionality on ship name, where a substring can be given
    and all records that contain the substring in the ship name column are returned. Data ordered by IMO Number and reporting period.

    Parameters
    ----------
    imo_number : Optional[int], optional
        Ship's IMO Number, by default None
    ship_name : Optional[str], optional
        Ship's name (can be a substring for search functionality), by default None
    reporting_period : int, optional
        Ship's reporting period, by default None
    db : Session, optional

    Returns
    -------
    ThetisMRVView
        Returns the data as shown in the frontpage of the THETIS-MRV Website
    """
    ships = crud.thetis_mrv_view(db, imo_number=imo_number, ship_name=ship_name, reporting_period=reporting_period)
    return ships.limit(50).all()

@app.get("/ships_with_top_total_emissions/", response_model=list[schemas.ThetisMRVView])
def ships_with_top_total_emissions(top_n: int = 10, db: Session = Depends(get_db)):
    """Endpoint that returns ships ordered by total emissions

    Parameters
    ----------
    top_n : int = 10
        Number of results to return
    db : Session, optional

    Returns
    -------
    ThetisMRVView
        Returns the data as shown in the frontpage of the THETIS-MRV Website
    """
    ships = crud.ships_with_top_total_emissions(db)
    return ships.limit(top_n).all()

@app.get("/ships_with_worst_emission_per_distance/", response_model=list[schemas.ThetisMRVView])
def ships_with_worst_emission_per_distance(top_n: int = 10, db: Session = Depends(get_db)):
    """Endpoint that returns ships ordered by average emissions per distance

    Parameters
    ----------
    top_n : int = 10
        Number of results to return
    db : Session, optional

    Returns
    -------
    ThetisMRVView
        Returns the data as shown in the frontpage of the THETIS-MRV Website
    """
    ships = crud.ships_with_worst_emission_per_distance(db)
    return ships.limit(top_n).all()
