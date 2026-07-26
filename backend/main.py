from flask import Flask,jsonify,request
from database import db,Hackathon,ModeEnum,StatusEnum
from flask_alembic import Alembic
from werkzeug.exceptions import NotFound
from datetime import datetime,timedelta
import os

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
            "startDate": datetime.strptime(request.form.get("startDate"), "%Y-%m-%d %H:%M:%S") if request.form.get("startDate") else None,
            "endDate": datetime.strptime(request.form.get("endDate"), "%Y-%m-%d %H:%M:%S") if request.form.get("endDate") else None,
            "location": request.form.get("location") or None,
            "hasPrize": request.form.get("hasPrize") or None,
            "prizeDetails": request.form.get("prizeDetails") or None,
            "submittedAt": request.form.get("submittedAt") or None,
            "updatedAt": now,
            "interestCount": request.form.get("interestCount"),
        }
    return True,params

def validate_parameters(params:dict,method:str,hackathon_to_update:Hackathon = None):
    
    """
    IMPORTANT NOTE: startDate and endDate values are getting validated in parse_parameters() func
    """
    
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
                if value.lower() == "true":
                    value = True
                    params[key] = True
                elif value.lower() == "false":
                    value = False
                    params[key] = False
                    params["prizeDetails"] = None #prizeDetails is None anyways IF hackathon doesnt have a prize
                else:
                    return False,"Wrong hasPrize"

            if hackathon_to_update:
                setattr(hackathon_to_update, key,value)
                
    if method == "PATCH":
        return True,None
    if method == "POST":
        return True,params
    
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

@app.route("/api/<hackathon_id>",methods=['PATCH']) #future api/hackathons endpoint
def update_hackathon(hackathon_id):
    
    result , value = parse_parameters(request.method)
    
    if result:
        params = value
    else:
        return jsonify(error={"error":f"{value}"}),400
    
    if not(id):
        return jsonify(error={"Missing Fields": "id is required."}),400
    
    try:
        hackathon_to_update = db.get_or_404(Hackathon,hackathon_id)
        result , error = validate_parameters(params,request.method,hackathon_to_update)
        if result and not(error):
            db.session.commit()
            return jsonify(response={"Success":f"Successfully updated hackathon with an id of : {hackathon_id}"}),200
        else:
            return jsonify(error={"error":f"{error}"}),400    
    except NotFound:
        return jsonify(error="Wrong id"),404
    
@app.route("/api/hackathons",methods=["POST"])
def add_hackathon():
    
    result , value = parse_parameters(request.method)
    
    if result:
        params = value
    else:
        return jsonify(error={"error":f"{value}"}),400
    
    if (params["name"] is None) or (params["url"] is None):
        return jsonify(error={"Missing Fields": "name and url are required."}),400
    
    result , value = validate_parameters(params,request.method,None)
    if result:
        #with app.app_context():
        new_hackathon = Hackathon(name=value["name"],url=value["url"],description=value["description"],startDate=value["startDate"],endDate=value["endDate"],location=value["location"],mode=value["mode"],
                                organizer=value["organizer"],hasPrize=value["hasPrize"],prizeDetails=value["prizeDetails"],tags=value["tags"],status=value["status"],
                                submittedAt=value["submittedAt"],updatedAt=value["updatedAt"],interestCount=value["interestCount"])
        db.session.add(new_hackathon)
        db.session.commit()
        return jsonify(response={"success":f"Successfully added hackathon:{value["name"]}!"}),200
    else:
        return jsonify(error={"error":f"{value}"}),400