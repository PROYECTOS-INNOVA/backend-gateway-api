from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from app.models.role import Role, RoleCreate, RoleUpdate
from app.servicios import role as role_service

router = APIRouter()


@router.get("/", response_model=List[Role])
async def list_roles(name: Optional[str] = None):
    """Lista todos los roles. Permite filtrar por nombre."""
    return await role_service.get_roles(name=name)


@router.get("/{role_id}", response_model=Role)
async def get_role(role_id: UUID):
    """Obtiene un rol por su ID."""
    role = await role_service.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role


@router.post("/", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role_endpoint(role: RoleCreate):
    """Crea un nuevo rol."""
    return await role_service.create_role(role)


@router.patch("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_role_endpoint(role_id: UUID, role: RoleUpdate):
    """Actualiza un rol existente."""
    await role_service.update_role(role_id, role)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_endpoint(role_id: UUID):
    """Elimina un rol por su ID."""
    ok = await role_service.delete_role(role_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
