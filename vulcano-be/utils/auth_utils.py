from utils.jwt_utils import JwtUtils

class AuthUtils:
    def __init__(self, request):
        print("[AUTH] AuthUtils initialized")
        self.request = request

    def _get_decoded_token(self):
        print("[AUTH] Decoding token from request")
        auth_header = self.request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
        if not token:
            return None
        jwt_utils = JwtUtils()
        decoded = jwt_utils.decode_token(token)
        print(f"[AUTH] Decoded token: {decoded}")
        return decoded

    def get_user_id_from_request(self):
        print("[AUTH] Getting user_id from request")
        decoded = self._get_decoded_token()
        print(f"[AUTH] user_id: {decoded['id'] if decoded and 'id' in decoded else None}")
        return decoded["id"] if decoded and "id" in decoded else None

    def get_username_from_request(self):
        print("[AUTH] Getting username from request")
        decoded = self._get_decoded_token()
        print(f"[AUTH] username: {decoded['username'] if decoded and 'username' in decoded else None}")
        return decoded["username"] if decoded and "username" in decoded else None

    def get_email_from_request(self):
        print("[AUTH] Getting email from request")
        decoded = self._get_decoded_token()
        print(f"[AUTH] email: {decoded['email'] if decoded and 'email' in decoded else None}")
        return decoded["email"] if decoded and "email" in decoded else None

    def get_user_from_request(self):
        print("[AUTH] Getting user dict from request")
        decoded = self._get_decoded_token()
        print(f"[AUTH] user: {decoded if decoded and all(k in decoded for k in ('id','username','email')) else None}")
        return {
            "id": decoded["id"],
            "username": decoded["username"],
            "email": decoded["email"]
        } if decoded and all(k in decoded for k in ("id", "username", "email")) else None
