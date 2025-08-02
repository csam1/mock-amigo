from flask import Blueprint, request, jsonify
from app.schemas.user_schema import SignupSchema
from app.services.user_service import UserService
from marshmallow import ValidationError

bp = Blueprint('user', __name__, url_prefix='/api')

@bp.route('/signup', methods=['POST'])
def signup():
    """
    Signup API endpoint
    Accepts: email, password, full_name, experience_level, preferred_role, is_interviewer, is_candidate
    """
    try:
        # Validate request data
        schema = SignupSchema()
        data = schema.load(request.json)
        
        # Create user service instance
        user_service = UserService()
        
        # Create user
        result = user_service.create_user(data)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "User created successfully",
                "user_id": result["user_id"],
                "email": result["email"],
                "access_token": result["access_token"],
                "refresh_token": result["refresh_token"]
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
            
    except ValidationError as e:
        return jsonify({
            "success": False,
            "error": "Validation error",
            "details": e.messages
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@bp.route('/login', methods=['POST'])
def login():
    """
    Login API endpoint
    Accepts: email, password
    """
    try:
        # Validate request data
        schema = LoginSchema()
        data = schema.load(request.json)

        user_service = UserService()
        result = user_service.login_user(data)

        if result["success"]:
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user_id": result["user_id"],
                "email": result["email"],
                "access_token": result["access_token"],
                "refresh_token": result["refresh_token"]
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500