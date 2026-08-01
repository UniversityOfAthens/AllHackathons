from flask import Flask,jsonify,request
from database import db,Hackathon,ModeEnum,StatusEnum,MAX_INTERESTCOUNT_VALUE
from sqlalchemy.exc import IntegrityError 
from flask_alembic import Alembic
from werkzeug.exceptions import NotFound
from datetime import datetime,timedelta
import os,json

#NOTE: If interestCount value is a number whether it is integer or string type it will join the db
#NOTE: If hasPrize value is a string or bool type since it is validated as a str.lower() it will join the db
#NOTE: If hasPrize is False then even if we add a value in the prizeDetails field it will throw an error
#NOTE: prizeDetails can only be *ADDED* in db only if hasPrize is True in any other case it will be None
#NOTE: prizeDetails can only be *UPDATED* if hasPrize was set to True and in the PATCH request hasPrize is either True or None
#NOTE: If hasPrize is False while being *UPDATED* then prizeDetails will always be None no matter the values we assign to it
#NOTE: If status and mode, do not contain any of their appropriate values they will throw an error and wont join db.
#NOTE: status and mode are handled as str values at first and then they get converted to StatusEnum or ModeEnum types

#MAX_INTERESTCOUNT_VALUE = 10000
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

def parse_parameters(method:str):
    now = datetime.now().replace(microsecond=0)
    try:
        startDate = datetime.strptime(request.form.get("startDate"), "%Y-%m-%d %H:%M:%S") if request.form.get("startDate") else None
        endDate = datetime.strptime(request.form.get("endDate"), "%Y-%m-%d %H:%M:%S") if request.form.get("endDate") else None
        #submittedAt = datetime.strptime(request.form.get("submittedAt"), "%Y-%m-%d %H:%M:%S") if request.form.get("submittedAt") else None
    except ValueError:
        return False,"Wrong date format"
    
    if method == "POST":
        params = {
            "name": request.form.get("name") or None,
            "url": request.form.get("url") or None,
            "description": request.form.get("description") or None,
            "organizer": request.form.get("organizer") or None,
            "status": request.form.get("status") or None,
            "mode": request.form.get("mode") or None,
            "tags": request.form.get("tags") or None,
            "startDate": startDate,
            "endDate": endDate,
            "location": request.form.get("location") or None,
            "hasPrize": request.form.get("hasPrize") or None,
            "prizeDetails": request.form.get("prizeDetails") or None,
            "submittedAt": now,
            "updatedAt": now,
            "interestCount": 0,
        }
    elif method == "PATCH":
        params = {
            "name": request.form.get("name") or None,
            "url": request.form.get("url") or None,
            "description": request.form.get("description") or None,
            "organizer": request.form.get("organizer") or None,
            "status": request.form.get("status") or None,
            "mode": request.form.get("mode") or None,
            "tags": request.form.get("tags") or None,
            "startDate": startDate,
            "endDate": endDate,
            "location": request.form.get("location") or None,
            "hasPrize": request.form.get("hasPrize") or None,
            "prizeDetails": request.form.get("prizeDetails") or None,
            #"submittedAt": submittedAt, no need to send submittedAt since only once gets a value
            "updatedAt": now,
            "interestCount": request.form.get("interestCount") or None,
        }
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
                    try:
                        value = ModeEnum(value)  #converts string "online" to ModeEnum.online
                    except ValueError:
                        return False,"Wrong mode"
                
                if key == "hasPrize":
                    if str(value).lower() == "true":
                        value = True
                        #params[key] = True
                    elif str(value).lower() == "false":
                        value = False
                        #params[key] = False
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
                    if (validated_parameters["hasPrize"] is None) or (validated_parameters["hasPrize"] is False):
                        return False, f"prizeDetails cannot contain any value when hasPrize is {str(validated_parameters['hasPrize'])}"
                
                validated_parameters[key] = value
                
        return True, validated_parameters
    
    if method == "PATCH":
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
                        
                validated_parameters[key] = value

        if (params["hasPrize"] is False) and (hackathon_to_update.prizeDetails is not None):#or hackathon_to_update.prizeDetails is not None
            validated_parameters["prizeDetails"] = None
        if (params["hasPrize"] is False) and (hackathon_to_update.prizeDetails is None):
            validated_parameters["prizeDetails"] = None
        
        for key,value in validated_parameters.items():
            setattr(hackathon_to_update, key,value)
    
    return True,None
    
@app.route("/api/hackathons",methods=["GET"])
def all_hackathons():
    if request.method == "GET":
        now = datetime.now().replace(microsecond=0) #Formats time like this: YYYY-MM-DD HH:MM:SS example: 2026-05-01 15:12:00
        
        #NOTE: REPLACE SOME PARAM QUERIES (tags,status) WITH ILIKE JUST SO IT IS EASIER TO FIND THE DESIRED PARAM
        
        params = {
            "status" : request.args.get('status'),
            "upcoming" : request.args.get('upcoming').lower() if request.args.get('upcoming') else None,
            "past" : request.args.get('past').lower() if request.args.get('past') else None,
            "tags" : request.args.get('tags'),
            "q" : request.args.get('q'),
            "sort" : request.args.get('sort')
        }
        
        query = db.session.query(Hackathon) # Arxiko query pou kanei build up stin sinexeia
                                            # me vasi ta params pou exoun epistrafei

        #status parameter
        if params["status"]:
            if (params["status"] in (StatusEnum.draft.value, StatusEnum.pending.value, StatusEnum.published.value, StatusEnum.needs_changes.value)):
                query = query.filter(Hackathon.status == params["status"])
            else:
                return jsonify(error="Wrong status"), 404
        
        #upcoming parameter
        if params["upcoming"] == "true":
            query = query.filter(Hackathon.startDate > now)
        elif params["upcoming"] == "false":
            query = query.filter(Hackathon.startDate < now)
        elif params["upcoming"]:
            return jsonify(error="Wrong upcoming"), 404
        
        #past parameter
        if params["past"] == "true":
            query = query.filter(Hackathon.startDate < now)
        elif params["past"] == "false":
            query = query.filter(Hackathon.startDate > now)
        elif params["past"]:
            return jsonify(error="Wrong past"), 404

        #tags parameter
        if params["tags"]:
            query = query.filter(Hackathon.tags == params["tags"])
        
        #q parameter
        if params["q"]:
            like = f"%{params["q"]}%"
            
            query = query.filter(Hackathon.name.ilike(like) | Hackathon.url.ilike(like) | Hackathon.description.ilike(like) |
                                 Hackathon.location.ilike(like) | Hackathon.organizer.ilike(like) | Hackathon.hasPrize.ilike(like) |
                                 Hackathon.prizeDetails.ilike(like) | Hackathon.tags.ilike(like))
        
        #sort parameter
        if params["sort"]:
            if params["sort"] == "name":
                query = query.order_by(Hackathon.name)
            elif params["sort"] == "startDate":
                query = query.order_by(Hackathon.startDate)
            elif params["sort"] == "endDate":
                query = query.order_by(Hackathon.endDate)
            elif params["sort"] == "sumbittedAt":
                query = query.order_by(Hackathon.submittedAt)
            elif params["sort"] == "updatedAt":
                query = query.order_by(Hackathon.updatedAt.desc())
            elif params["sort"] == "interestCount":
                query = query.order_by(Hackathon.interestCount.desc()) #highest to lowest
                
        results = query.all()
        data = [result.to_dict() for result in results]
        return jsonify(data),200

@app.route("/api/hackathons/<hackathon_id>",methods=['GET'])
def find_hackathon(hackathon_id):
    try:
        hackathon = db.get_or_404(Hackathon, hackathon_id)
        print(type(hackathon.startDate))
        return jsonify(hackathon.to_dict()),200
    except NotFound:
        return jsonify(error="Wrong id"),404

@app.route("/api/<hackathon_id>",methods=['PATCH'])
def update_hackathon(hackathon_id):
    
    result_parsed , value_parsed = parse_parameters(request.method)
    
    if result_parsed:
        params_parsed = value_parsed
    else:
        return jsonify(error=f"{value_parsed}"),400
    
    if not(hackathon_id):
        return jsonify(error="id is required"),400
    
    try:
        hackathon_to_update = db.get_or_404(Hackathon,hackathon_id)
        result_validated , error_validated = validate_parameters2(params_parsed,request.method,hackathon_to_update)
        if result_validated and not(error_validated):
            try:
                db.session.commit()
                return jsonify(success=f"Successfully updated hackathon with an id of : {hackathon_id}"),200
            except IntegrityError:
                return jsonify(error="invalid data"),400
        else:
            return jsonify(error=f"{error_validated}"),400
    except NotFound:
        return jsonify(error="Wrong id"),404
    
@app.route("/api/hackathons",methods=["POST"])
def add_hackathon():
    
    result_parsed , value_parsed = parse_parameters(request.method)
    
    if result_parsed:
        params_parsed = value_parsed
    else:
        return jsonify(error=f"{value_parsed}"),400
    
    # if (params_parsed["name"] is None) or (params_parsed["url"] is None):
    #     return jsonify(error="name and url are required"),400
    
    result_validated , value_validated = validate_parameters2(params_parsed,request.method,None)
    #print([i for i in value_validated.to_dict()])
    print(value_validated)
    
    if result_validated:
        new_hackathon = Hackathon(name=value_validated["name"],url=value_validated["url"],description=value_validated["description"],startDate=value_validated["startDate"],endDate=value_validated["endDate"],location=value_validated["location"],mode=value_validated["mode"],
                                organizer=value_validated["organizer"],hasPrize=value_validated["hasPrize"],prizeDetails=value_validated["prizeDetails"],tags=value_validated["tags"],status=value_validated["status"],
                                submittedAt=value_validated["submittedAt"],updatedAt=value_validated["updatedAt"],interestCount=value_validated["interestCount"])
        db.session.add(new_hackathon)
        db.session.commit()
        return jsonify(success=f"Successfully added hackathon:{value_validated["name"]}!"),200
    else:
        return jsonify(error=f"{value_validated}"),400