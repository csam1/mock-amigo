from app.extensions import get_supabase_client
from supabase import Client
from typing import Dict, Any

class UserService:
    def __init__(self):
        self.supabase: Client = get_supabase_client()
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user with Supabase Auth and insert profile
        """
        try:
            # Create user with Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": user_data["email"],
                "password": user_data["password"]
            })
            
            if auth_response.user is None:
                raise Exception("Failed to create user account")
            
            user_id = auth_response.user.id
            
            # Insert profile into profiles table
            profile_data = {
                "id": user_id,  # Use the same ID as the auth user
                "full_name": user_data["full_name"],
                "experience_level": user_data["experience_level"],
                "preferred_role": user_data["preferred_role"],
                "is_interviewer": user_data["is_interviewer"],
                "is_candidate": user_data["is_candidate"],
                "email": user_data["email"]
            }
            
            profile_response = self.supabase.table("profiles").insert(profile_data).execute()
            
            if not profile_response.data:
                # If profile creation fails, we should clean up the auth user
                # For now, we'll just raise an exception
                raise Exception("Failed to create user profile")
            
            return {
                "success": True,
                "user_id": user_id,
                "access_token": auth_response.session.access_token,
                "refresh_token": auth_response.session.refresh_token,
                "email": user_data["email"],
                "message": "User created successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def login_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Login user with Supabase Auth
        """
        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": user_data["email"],
                "password": user_data["password"]
            })
            
            if auth_response.user is None:
                raise Exception("Invalid credentials")
            
            return {
                "success": True,
                "user_id": auth_response.user.id,
                "email": user_data["email"],
                "access_token": auth_response.session.access_token,
                "refresh_token": auth_response.session.refresh_token,
                "message": "Login successful"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }