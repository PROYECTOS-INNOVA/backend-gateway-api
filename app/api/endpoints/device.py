from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, Query, status
from pydantic import BaseModel

# Imports for Device
from app.models.device import DeviceCreate, DeviceDB, DeviceUpdate

# Imports for Location
from app.models.location import LocationCreate, LocationDB
from app.servicios import device as device_service
from app.servicios import location as location_service

router = APIRouter()


# --- Body Models for Auditability ---


class DeviceUpdateBody(DeviceUpdate):
    applied_by_id: UUID


class DeleteBody(BaseModel):
    applied_by_id: UUID


# --- Device Endpoints ---


@router.post("/", response_model=DeviceDB, status_code=status.HTTP_201_CREATED)
async def create_device(device_in: DeviceCreate):
    return await device_service.create_device(device_in)


@router.get("/", response_model=List[DeviceDB])
async def get_all_devices():
    return await device_service.get_devices()


@router.get("/{device_id}", response_model=DeviceDB)
async def get_device_by_id(device_id: UUID = Path(...)):
    device = await device_service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.patch("/{device_id}", response_model=DeviceDB)
async def update_device(device_id: UUID, body: DeviceUpdateBody):
    device_in = DeviceUpdate(**body.model_dump(exclude={"applied_by_id"}))
    device = await device_service.update_device(
        device_id, device_in, body.applied_by_id
    )
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: UUID, body: DeleteBody):
    success = await device_service.delete_device(device_id, body.applied_by_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")


# --- Location Endpoints (related to Devices) ---


@router.post(
    "/locations/", response_model=LocationDB, status_code=status.HTTP_201_CREATED
)
async def create_location(location_in: LocationCreate):
    return await location_service.create_location(location_in)


@router.get("/locations/", response_model=List[LocationDB])
async def get_all_locations(device_id: Optional[UUID] = Query(None)):
    return await location_service.get_locations(device_id=device_id)


@router.get("/locations/{location_id}", response_model=LocationDB)
async def get_location_by_id(location_id: UUID = Path(...)):
    location = await location_service.get_location(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(location_id: UUID):
    success = await location_service.delete_location(location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
