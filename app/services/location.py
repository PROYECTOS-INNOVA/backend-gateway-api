import os
from typing import List, Optional
from uuid import UUID

import httpx

from app.models.location import (
    CityCreate,
    CityDB,
    CityUpdate,
    CountryCreate,
    CountryDB,
    CountryUpdate,
    LocationCreate,
    LocationDB,
    RegionCreate,
    RegionDB,
    RegionUpdate,
)

USER_SVC_URL = os.getenv("USER_SVC_URL", "http://localhost:8002")


async def create_city(city_in: CityCreate) -> Optional[CityDB]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USER_SVC_URL}/api/v1/cities/", json=city_in.model_dump(mode="json")
        )
        if response.status_code == 201:
            return CityDB(**response.json())
        return None


async def get_cities(name: Optional[str] = None, region_id: Optional[UUID] = None) -> List[CityDB]:
    params = {}
    if name:
        params["name"] = name
    if region_id:
        params["region_id"] = str(region_id)
        
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/cities/", params=params)
        response.raise_for_status()
        return [CityDB(**item) for item in response.json()]


async def get_city(city_id: UUID) -> Optional[CityDB]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/cities/{city_id}")
        if response.status_code == 200:
            return CityDB(**response.json())
        return None


async def update_city(city_id: UUID, city_in: CityUpdate) -> Optional[CityDB]:
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{USER_SVC_URL}/api/v1/cities/{city_id}",
            json=city_in.model_dump(mode="json", exclude_unset=True),
        )
        if response.status_code == 200:
            return CityDB(**response.json())
        return None


async def delete_city(city_id: UUID) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SVC_URL}/api/v1/cities/{city_id}")
        return response.status_code == 204


# Country Service Functions
async def create_country(country_in: CountryCreate) -> Optional[CountryDB]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USER_SVC_URL}/api/v1/countries/", json=country_in.model_dump(mode="json")
        )
        if response.status_code == 201:
            return CountryDB(**response.json())
        return None


async def get_countries(name: Optional[str] = None) -> List[CountryDB]:
    params = {}
    if name:
        params["name"] = name

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/countries/", params=params)
        response.raise_for_status()
        return [CountryDB(**item) for item in response.json()]


async def get_country(country_id: UUID) -> Optional[CountryDB]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/countries/{country_id}")
        if response.status_code == 200:
            return CountryDB(**response.json())
        return None


async def update_country(country_id: UUID, country_in: CountryUpdate) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{USER_SVC_URL}/api/v1/countries/{country_id}",
            json=country_in.model_dump(mode="json", exclude_unset=True),
        )
        return response.status_code in (200, 204)


async def delete_country(country_id: UUID) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SVC_URL}/api/v1/countries/{country_id}")
        return response.status_code == 204


# Region Service Functions
async def create_region(region_in: RegionCreate) -> Optional[RegionDB]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USER_SVC_URL}/api/v1/regions/", json=region_in.model_dump(mode="json")
        )
        if response.status_code == 201:
            return RegionDB(**response.json())
        return None


async def get_regions(country_id: Optional[UUID] = None, name: Optional[str] = None) -> List[RegionDB]:
    params = {}
    if country_id:
        params["country_id"] = str(country_id)
    if name:
        params["name"] = name
        
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/regions/", params=params)
        response.raise_for_status()
        return [RegionDB(**item) for item in response.json()]


async def get_region(region_id: UUID) -> Optional[RegionDB]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/regions/{region_id}")
        if response.status_code == 200:
            return RegionDB(**response.json())
        return None


async def update_region(region_id: UUID, region_in: RegionUpdate) -> Optional[RegionDB]:
    async with httpx.AsyncClient() as client:
        # Convert the model to a dictionary and explicitly include all fields
        update_data = region_in.model_dump(mode="json", exclude_unset=False)

        # Log the data being sent for debugging
        print(f"Sending update data to region service: {update_data}")

        response = await client.patch(
            f"{USER_SVC_URL}/api/v1/regions/{region_id}", json=update_data
        )

        # Handle different status codes
        if response.status_code == 200:
            return RegionDB(**response.json())
        elif response.status_code == 204:
            # If the backend returns 204 No Content, try to get the updated region
            updated_region = await get_region(region_id)
            if updated_region:
                return updated_region

        return None


async def delete_region(region_id: UUID) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SVC_URL}/api/v1/regions/{region_id}")
        return response.status_code == 204


# Location Service Functions
async def create_location(location_in: LocationCreate) -> Optional[LocationDB]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USER_SVC_URL}/api/v1/locations/",
            json=location_in.model_dump(mode="json"),
        )
        if response.status_code == 201:
            return LocationDB(**response.json())
        return None


async def get_locations(device_id: Optional[UUID] = None) -> List[LocationDB]:
    params = {}
    if device_id:
        params["device_id"] = str(device_id)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/locations/", params=params)
        response.raise_for_status()
        return [LocationDB(**item) for item in response.json()]


async def get_location(location_id: UUID) -> Optional[LocationDB]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SVC_URL}/api/v1/locations/{location_id}")
        if response.status_code == 200:
            return LocationDB(**response.json())
        return None


async def get_location_by_device(device_id: UUID) -> Optional[LocationDB]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{USER_SVC_URL}/api/v1/locations/device/{device_id}"
        )
        if response.status_code == 200:
            return LocationDB(**response.json())
        return None


async def delete_location(location_id: UUID) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SVC_URL}/api/v1/locations/{location_id}")
        return response.status_code == 204
