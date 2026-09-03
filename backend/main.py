from flask import Flask,jsonify,request
from database import db,Hackathon,ModeEnum,StatusEnum,MAX_INTERESTCOUNT_VALUE
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import or_, and_
from flask_alembic import Alembic
from werkzeug.exceptions import NotFound
from datetime import datetime,timedelta
import os,json,re

#NOTE: If interestCount value is a number whether it is integer or string type it will join the db
#NOTE: If hasPrize value is a string or bool type since it is validated as a str.lower() it will join the db
#NOTE: If hasPrize is False then even if we add a value in the prizeDetails field it will throw an error
#NOTE: prizeDetails can only be *ADDED* in db only if hasPrize is True in any other case it will be None
#NOTE: prizeDetails can only be *UPDATED* if hasPrize was set to True and in the PATCH request hasPrize is either True or None
#NOTE: If hasPrize is False while being *UPDATED* then prizeDetails will always be None no matter the values we assign to it
#NOTE: If status and mode, do not contain any of their appropriate values they will throw an error and wont join db.
#NOTE: status and mode are handled as str values at first and then they get converted to StatusEnum or ModeEnum types

today = datetime.now().replace(microsecond=0)
tommorow = today + timedelta(days=1)
allowed = ["name", "url", "description", "startDate", "endDate", "updatedAt", "submittedAt", "location", "mode",
           "organizer", "hasPrize", "prizeDetails", "tags", "status", "interestCount"]

db_dir = os.path.abspath("./db")
os.makedirs(db_dir,exist_ok=True)

app = Flask(__name__,instance_path=db_dir)
app.json.sort_keys = False #prevents alphabetical order when json is returned
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hackathon.db"
app.config['ALEMBIC_RENDER_AS_BATCH'] = True
db.init_app(app)

alembic = Alembic()
alembic.init_app(app) 

with app.app_context():
    db.create_all()

# --- CORS for frontend (Vite dev server) ---
@app.after_request
def _cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS, DELETE"
    return response

@app.route("/api/<path:_path>", methods=["OPTIONS"])
@app.route("/api/hackathons", methods=["OPTIONS"])
@app.route("/api/hackathons/<path:_sub>", methods=["OPTIONS"])
def _cors_preflight(_path=None, _sub=None):
    return ("", 204)

def _get_input(key: str):
    """Read from JSON body if present, else from form data. Normalizes empty strings to None."""
    val = None
    if request.is_json:
        data = request.get_json(silent=True) or {}
        val = data.get(key)
        # JSON may contain list for tags -> join to string
        if isinstance(val, list):
            val = ",".join(str(v) for v in val)
        if isinstance(val, bool):
            # keep bool for hasPrize; stringify later via str().lower() checks
            return val
    if val is None:
        val = request.form.get(key)
    if val == "":
        return None
    return val

def _parse_date(value):
    """Accept YYYY-MM-DD HH:MM:SS, YYYY-MM-DD, ISO8601."""
    if not value:
        return None
    # try backend's canonical format
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    try:
        # fallback ISO parse
        return datetime.fromisoformat(value.replace("Z", ""))
    except Exception:
        raise ValueError("Wrong date format")

def parse_parameters(method:str):
    now = datetime.now()
    
    if method == "POST":
        params = {
            "name": _get_input("name"),
            "url": _get_input("url"),
            "description": _get_input("description"),
            "organizer": _get_input("organizer"),
            "status": _get_input("status"),
            "mode": _get_input("mode"),
            "tags": _get_input("tags"),
            "startDate": _get_input("startDate"),
            "endDate": _get_input("endDate"),
            "location": _get_input("location"),
            "hasPrize": _get_input("hasPrize"),
            "prizeDetails": _get_input("prizeDetails"),
            "submittedAt": now,
            "updatedAt": now,
            "interestCount": 0, #we dont even parse interestCount from the request since it is always 0 when a new hackathon is added
        }
    elif method == "PATCH":
        params = {
            "name": _get_input("name"),
            "url": _get_input("url"),
            "description": _get_input("description"),
            "organizer": _get_input("organizer"),
            "status": _get_input("status"),
            "mode": _get_input("mode"),
            "tags": _get_input("tags"),
            "startDate": _get_input("startDate"),
            "endDate": _get_input("endDate"),
            "location": _get_input("location"),
            "hasPrize": _get_input("hasPrize"),
            "prizeDetails": _get_input("prizeDetails"),
            "updatedAt": now,
            "interestCount": _get_input("interestCount"),
        }
        #we dont need to implement same logic in POST request since
        #we only need name and url to be provided and error-case is 
        #handled directly from validate_parameters() func underneath
        all_values_are_none = True
        for key,value in params.items():
            if (value is not None) and (key != "updatedAt"):
                all_values_are_none = False
                break
        
        if all_values_are_none:
            return False,"No data provided to update"
        
    return True,params

def validate_parameters2(params:dict,method:str,hackathon_to_update:Hackathon = None):
    
    if method == "POST":
        validated_parameters = {
                            "name": None,
                            "description":None,
                            "url": None,
                            "startDate": None,
                            "endDate": None,
                            "location": None,
                            "mode": None,
                            "organizer": None,
                            "hasPrize": None,
                            "prizeDetails": None,
                            "tags": None,
                            "status": None,
                            "submittedAt": None,
                            "updatedAt": None,
                            "interestCount": None,
                        }
        
        #validating required fields for POST request
        if (params["name"] is None) or (params["url"] is None):
            return False,"name and url are required"
        
        for key,value in params.items():
            
            if (key in allowed) and value is not None:
                    
                if key == "status":
                    try:
                        value = StatusEnum(value)
                    except ValueError:
                        return False,"Wrong status"
                
                if key == "mode":
                    # frontend sends "in-person", backend stores "in_person"
                    if isinstance(value, str) and value == "in-person":
                        value = "in_person"
                    try:
                        value = ModeEnum(value)  #converts string "online" to ModeEnum.online
                    except ValueError:
                        return False,"Wrong mode"
                
                if key == "hasPrize":
                    if str(value).lower() == "true":
                        value = True
                    elif str(value).lower() == "false":
                        value = False
                    else:
                        return False,"Wrong hasPrize"
                
                if key == "interestCount":
                    if not(isinstance(value,int)):
                        try:
                            value = int(value)
                        except ValueError:
                            return False, "Wrong interestCount"
                    if value < 0 or value > MAX_INTERESTCOUNT_VALUE:
                        return False, "Wrong interestCount" #maybe we cahange it to big interestCount in the future

                if key == "prizeDetails":
                    if (validated_parameters["hasPrize"] is None) or (validated_parameters["hasPrize"] is False):
                        return False, f"prizeDetails cannot contain any value when hasPrize is {str(validated_parameters['hasPrize'])}"
                
                if key in ["startDate", "endDate"]:
                    try:
                        value = _parse_date(value) if value else None
                    except ValueError:
                        return False,"Wrong date format"
                
                validated_parameters[key] = value
        
        if (validated_parameters["startDate"] is not None) and validated_parameters["endDate"] is not None:
            if validated_parameters["startDate"] > validated_parameters["endDate"]:
                return False,"startDate cannot be greater than endDate"
                
        return True, validated_parameters
    
    elif method == "PATCH":
        validated_parameters = {
                                "name": hackathon_to_update.name,
                                "description":hackathon_to_update.description,
                                "url": hackathon_to_update.url,
                                "startDate": hackathon_to_update.startDate,
                                "endDate": hackathon_to_update.endDate,
                                "location": hackathon_to_update.location,
                                "mode": hackathon_to_update.mode,
                                "organizer": hackathon_to_update.organizer,
                                "hasPrize": hackathon_to_update.hasPrize,
                                "prizeDetails": hackathon_to_update.prizeDetails,
                                "tags": hackathon_to_update.tags,
                                "status": hackathon_to_update.status,
                                "submittedAt": hackathon_to_update.submittedAt,
                                "updatedAt": hackathon_to_update.updatedAt,
                                "interestCount": hackathon_to_update.interestCount,
                                }
        
        for key,value in params.items():
            
            if (key in allowed) and value is not None:
                    
                if key == "status":
                    try:
                        value = StatusEnum(value)
                    except ValueError:
                        return False,"Wrong status"
                
                if key == "mode":
                    if isinstance(value, str) and value == "in-person":
                        value = "in_person"
                    try:
                        value = ModeEnum(value)  #converts string "online" to ModeEnum.online
                    except ValueError:
                        return False,"Wrong mode"
                
                if key == "hasPrize":
                    if str(value).lower() == "true":
                        value = True
                        params[key] = True
                    elif str(value).lower() == "false":
                        value = False
                        params[key] = False
                        #params["prizeDetails"] = None #prizeDetails is None anyways IF hackathon doesnt have a prize                       
                    else:
                        return False,"Wrong hasPrize"
                
                if key == "interestCount":
                    if not(isinstance(value,int)):
                        try:
                            value = int(value)
                        except ValueError:
                            return False, "Wrong interestCount"
                    if value < 0 or value > MAX_INTERESTCOUNT_VALUE:
                        return False, "Wrong interestCount" #maybe we cahange it to big interestCount in the future
                
                if key == "prizeDetails":
                    if params["hasPrize"] is None: #sto request
                        if (hackathon_to_update.hasPrize is False) or (hackathon_to_update.hasPrize is None):
                            #we dont accept prizeDetails so we do:
                            return False,f"prizeDetails cannot contain any value when hasPrize is {str(hackathon_to_update.hasPrize)}"
                    else:
                        if (params["hasPrize"] is False) and (params["prizeDetails"] is not None):
                            return False,f"prizeDetails cannot contain any value when hasPrize is False"
                        
                if key in ["startDate", "endDate"]:
                    try:
                        value = _parse_date(value) if value else None
                    except ValueError:
                        return False,"Wrong date format"
                        
                validated_parameters[key] = value
        
        if (validated_parameters["startDate"] is not None) and validated_parameters["endDate"] is not None:
            if validated_parameters["startDate"] > validated_parameters["endDate"]:
                return False,"startDate cannot be greater than endDate"

        if (params["hasPrize"] is False) and (hackathon_to_update.prizeDetails is not None):#or hackathon_to_update.prizeDetails is not None
            validated_parameters["prizeDetails"] = None
        if (params["hasPrize"] is False) and (hackathon_to_update.prizeDetails is None):
            validated_parameters["prizeDetails"] = None
    
    return True,validated_parameters

def tokenize(query_string):
    return re.findall(r'\w+', query_string)
    
@app.route("/api/hackathons",methods=["GET"])
def all_hackathons():
    now = datetime.now().replace(microsecond=0) #Formats time like this: YYYY-MM-DD HH:MM:SS example: 2026-05-01 15:12:00

    params = {
        "status" : request.args.get('status').lower() if request.args.get('status') else None,
        "upcoming" : request.args.get('upcoming').lower() if request.args.get('upcoming') else None,
        "past" : request.args.get('past').lower() if request.args.get('past') else None,
        "tags" : request.args.get('tags'),
        "q" : request.args.get('q'),
        "sort" : request.args.get('sort').lower() if request.args.get("sort") else None
    }

    query = db.session.query(Hackathon) # Arxiko query pou kanei build up stin sinexeia
                                        # me vasi ta params pou exoun epistrafei

    #status parameter
    if params["status"]:
        if (params["status"] in (StatusEnum.draft.value, StatusEnum.pending.value, StatusEnum.published.value, StatusEnum.needs_changes.value)):
            query = query.filter(Hackathon.status == params["status"])
        else:
            return jsonify(error="Wrong status"), 400

    #upcoming parameter
    if params["upcoming"] == "true":
        query = query.filter(Hackathon.startDate > now)
    elif params["upcoming"] == "false":
        query = query.filter(Hackathon.startDate < now)
    elif params["upcoming"]:
        return jsonify(error="Wrong upcoming"), 400

    #past parameter
    if params["past"] == "true":
        query = query.filter(Hackathon.startDate < now)
    elif params["past"] == "false":
        query = query.filter(Hackathon.startDate > now)
    elif params["past"]:
        return jsonify(error="Wrong past"), 400

    #tags parameter NEEDS REFACTORING
    if params["tags"]:
        tokens = tokenize(params["tags"])
        
        conditions = []
        for token in tokens:
            field_match = Hackathon.tags.ilike(f"%{token}%")
            conditions.append(or_(field_match))

        query = query.filter(or_(*conditions))
        
    #q parameter
    if params["q"]:
        tokens = tokenize(params["q"])
        print(tokens)
        if tokens:
            searchable_fields = [
                Hackathon.name, Hackathon.url, Hackathon.description,
                Hackathon.location, Hackathon.organizer,
                Hackathon.prizeDetails, Hackathon.tags,
            ]

            conditions = []
            for token in tokens:
                field_matches = [field.ilike(f"%{token}%") for field in searchable_fields]
                conditions.append(or_(*field_matches))

            query = query.filter(and_(*conditions))
        elif tokens == []:
            return jsonify(error="Wrong q"), 400
        
    #sort parameter
    allowed_sort_values = ["name","startdate","enddate","submittedat","updatedat","interestcount"]
    if params["sort"]:
        if params["sort"] not in allowed_sort_values:
            return jsonify(error="Wrong sort"),400
        elif params["sort"] == "name":
            query = query.order_by(Hackathon.name)
        elif params["sort"] == "startdate":
            query = query.order_by(Hackathon.startDate)
        elif params["sort"] == "enddate":
            query = query.order_by(Hackathon.endDate)
        elif params["sort"] == "submittedat":
            query = query.order_by(Hackathon.submittedAt)
        elif params["sort"] == "updatedat":
            query = query.order_by(Hackathon.updatedAt.desc())
        elif params["sort"] == "interestcount":
            query = query.order_by(Hackathon.interestCount.desc()) #highest to lowest
            
    results = query.all()
    data = [result.to_dict() for result in results]
    return jsonify(data),200

@app.route("/api/hackathons/", methods=['GET'], defaults={'hackathon_id': None})
@app.route("/api/hackathons/<hackathon_id>",methods=['GET'])
def find_hackathon(hackathon_id):
    
    if (hackathon_id is None) or (hackathon_id.strip() == ""):
        return jsonify(error="id is required"),400
    
    try:
        hackathon = int(hackathon_id)
    except ValueError:
        return jsonify(error="id must be a number"),400
    
    try:
        hackathon = db.get_or_404(Hackathon, hackathon_id)
        return jsonify(hackathon.to_dict()),200
    except NotFound:
        return jsonify(error="Wrong id"),404

@app.route("/api/hackathons/", methods=['PATCH'], defaults={'hackathon_id': None})
@app.route("/api/hackathons/<hackathon_id>",methods=['PATCH'])
def update_hackathon(hackathon_id):
    
    if (hackathon_id is None) or (hackathon_id.strip() == ""):
        return jsonify(error="id is required"),400
    
    try:
        int(hackathon_id)
    except ValueError:
        return jsonify(error="id must be a number"),400
    
    result_parsed , value_parsed = parse_parameters(request.method)
    
    if result_parsed:
        params_parsed = value_parsed
    else:
        return jsonify(error=f"{value_parsed}"),400
    
    try:
        hackathon_to_update = db.get_or_404(Hackathon,hackathon_id)
        result_validated , returned_parameters = validate_parameters2(params_parsed,request.method,hackathon_to_update)
        if result_validated:
            try:
                for key,value in returned_parameters.items():
                    setattr(hackathon_to_update, key,value)
                db.session.commit()
            except ValueError as e:
                    return jsonify(error=str(e)),400
            except IntegrityError:
                return jsonify(error="invalid data"),400
            return jsonify(success=f"Successfully updated hackathon with an id of : {hackathon_id}"),200
        else:
            return jsonify(error=f"{returned_parameters}"),400
    except NotFound:
        return jsonify(error="Hackathon not found"),404
    
@app.route("/api/hackathons",methods=["POST"])
def add_hackathon():
    
    result_parsed , value_parsed = parse_parameters(request.method)
    
    if result_parsed:
        params_parsed = value_parsed
    else:
        return jsonify(error=f"{value_parsed}"),400
    
    result_validated , value_validated = validate_parameters2(params_parsed,request.method,None)
    
    if result_validated:
        try:
            new_hackathon = Hackathon(name=value_validated["name"],url=value_validated["url"],description=value_validated["description"],startDate=value_validated["startDate"],endDate=value_validated["endDate"],location=value_validated["location"],mode=value_validated["mode"],
                                organizer=value_validated["organizer"],hasPrize=value_validated["hasPrize"],prizeDetails=value_validated["prizeDetails"],tags=value_validated["tags"],status=value_validated["status"],
                                submittedAt=value_validated["submittedAt"],updatedAt=value_validated["updatedAt"],interestCount=value_validated["interestCount"])
        
            db.session.add(new_hackathon)
            db.session.commit()
        except ValueError as e:
            return jsonify(error=str(e)),400
        return jsonify(success=f"Successfully added hackathon:{value_validated["name"]}!"),200
    else:
        return jsonify(error=f"{value_validated}"),400