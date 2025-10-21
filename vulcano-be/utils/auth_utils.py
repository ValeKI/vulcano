from utils.jwt_utils import JwtUtils

class AuthUtils:
    def __init__(self, request):
        self.request = request

    def _get_decoded_token(self):
        auth_header = self.request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith("Bearer ") else None
        if not token:
            return None
        jwt_utils = JwtUtils()
        decoded = jwt_utils.decode_token(token)
        if not decoded:
            return None
        return decoded

    def get_user_id_from_request(self):
        decoded = self._get_decoded_token()
        if not decoded or "id" not in decoded:
            return None
        return decoded["id"]

    def get_username_from_request(self):
        decoded = self._get_decoded_token()
        if not decoded or "username" not in decoded:
            return None
        return decoded["username"]

    def get_email_from_request(self):
        decoded = self._get_decoded_token()
        if not decoded or "email" not in decoded:
            return None
        return decoded["email"]

    def get_user_from_request(self):
        decoded = self._get_decoded_token()
        if not decoded or not all(k in decoded for k in ("id", "username", "email")):
            return None
        return {
            "id": decoded["id"],
            "username": decoded["username"],
            "email": decoded["email"]
        }
