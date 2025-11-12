import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import UUID

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.config import settings
from app.core.exceptions import SupabaseAuthError, ValidationError
from app.models.domain.user import User
from app.models.requests.user_requests import UserCreate

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_current_user(self, api_token: str) -> Optional[User]:
        """Get current user from API JWT token"""
        user_id = self.verify_api_jwt(api_token)
        if not user_id:
            return None

        return await self.session.get(User, user_id)

    async def authenticate_with_supabase(self, supabase_token: str) -> User:
        """Authenticate using Supabase JWT and return user (for login only)"""
        supabase_user = self.verify_supabase_token(supabase_token)
        if not supabase_user:
            raise SupabaseAuthError()

        return await self.create_or_update_user_from_supabase(supabase_user)

    async def create_or_update_user_from_supabase(self, supabase_user: dict) -> User:
        email = supabase_user.get("email")
        if not email:
            raise ValidationError("Email is required from Supabase token")

        result = await self.session.execute(select(User).where(User.email == email))
        existing_user = result.scalars().first()

        if existing_user:
            return existing_user

        user_metadata = supabase_user.get("user_metadata", {})

        username = (
            user_metadata.get("user_name")
            or user_metadata.get("preferred_username")
            or email.split("@")[0]
        )
        avatar_url = user_metadata.get("avatar_url") or user_metadata.get("picture")

        user_data = UserCreate(
            username=username,
            email=email,
            avatar_url=avatar_url,
        )
        user = User.model_validate(user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        logger.info(f"Created new user from Supabase: {email}")
        return user

    def create_api_jwt(self, user_id: UUID) -> Tuple[str, datetime]:
        expires_at = datetime.utcnow() + timedelta(hours=settings.API_JWT_EXPIRE_HOURS)

        payload = {
            "sub": str(user_id),
            "exp": expires_at,
            "iat": datetime.utcnow(),
            "iss": settings.API_JWT_ISSUER,
        }

        token = jwt.encode(
            payload, settings.API_JWT_SECRET, algorithm=settings.API_JWT_ALGORITHM
        )

        return token, expires_at

    def verify_api_jwt(self, token: str) -> Optional[UUID]:
        """Verify api JWT token and return user ID"""
        try:
            payload = jwt.decode(
                token,
                settings.API_JWT_SECRET,
                algorithms=[settings.API_JWT_ALGORITHM],
                issuer=settings.API_JWT_ISSUER,
            )
            user_id = payload.get("sub")
            if user_id is None:
                return None

            # Check if token is expired (jose handles this, but explicit check)
            exp = payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                return None

            return UUID(user_id)
        except (JWTError, ValueError):
            return None

    def verify_supabase_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
            return payload
        except JWTError:
            return None
