"""
vehicles_repository.py
Handles all database operations for the vehicles table.
"""

from dataclasses import dataclass
from typing import Optional
from app.core.database import get_connection
from app.core.drivers_repository import Driver, _row_to_driver


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Vehicle:
    """Represents a vehicle record from the database."""
    id:         int
    plate:      str
    model:      Optional[str]
    driver_id:  Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]


@dataclass
class VehicleWithDriver:
    """Represents a vehicle joined with its driver data."""
    vehicle: Vehicle
    driver:  Optional[Driver]


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def get_vehicle_by_plate(plate: str) -> Optional[VehicleWithDriver]:
    """
    Searches for a vehicle by plate and returns it with its driver data.

    Args:
        plate: Normalized plate string (e.g. 'ABC1234').

    Returns:
        VehicleWithDriver if found, None otherwise.
    """
    with get_connection() as conn:
        row = conn.execute("""
            SELECT
                v.id,  v.plate, v.model, v.driver_id, v.created_at, v.updated_at,
                d.id          AS d_id,
                d.name        AS d_name,
                d.cpf         AS d_cpf,
                d.phone       AS d_phone,
                d.department  AS d_department,
                d.photo_path  AS d_photo_path,
                d.created_at  AS d_created_at,
                d.updated_at  AS d_updated_at
            FROM vehicles v
            LEFT JOIN drivers d ON d.id = v.driver_id
            WHERE v.plate = ?
        """, (plate,)).fetchone()

        if not row:
            return None

        vehicle = Vehicle(
            id=         row["id"],
            plate=      row["plate"],
            model=      row["model"],
            driver_id=  row["driver_id"],
            created_at= row["created_at"],
            updated_at= row["updated_at"],
        )

        driver = None
        if row["d_id"]:
            driver = Driver(
                id=         row["d_id"],
                name=       row["d_name"],
                cpf=        row["d_cpf"],
                phone=      row["d_phone"],
                department= row["d_department"],
                photo_path= row["d_photo_path"],
                created_at= row["d_created_at"],
                updated_at= row["d_updated_at"],
            )

        return VehicleWithDriver(vehicle=vehicle, driver=driver)


def get_all_vehicles() -> list[Vehicle]:
    """Returns all vehicles ordered by plate."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, plate, model, driver_id, created_at, updated_at
            FROM vehicles
            ORDER BY plate ASC
        """).fetchall()
        return [_row_to_vehicle(row) for row in rows]


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def create_vehicle(
    plate:     str,
    model:     Optional[str] = None,
    driver_id: Optional[int] = None,
) -> Vehicle:
    """
    Inserts a new vehicle into the database.

    Args:
        plate:     Required. Normalized plate string.
        model:     Optional. Vehicle model description.
        driver_id: Optional. ID of the associated driver.

    Returns:
        The created Vehicle with the generated ID.
    """
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO vehicles (plate, model, driver_id)
            VALUES (?, ?, ?)
        """, (plate, model, driver_id))

        vehicle_id = cursor.lastrowid

    return get_vehicle_by_id(vehicle_id)


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

def update_vehicle(
    vehicle_id: int,
    plate:      str,
    model:      Optional[str] = None,
    driver_id:  Optional[int] = None,
) -> Optional[Vehicle]:
    """
    Updates an existing vehicle record.

    Returns:
        The updated Vehicle or None if the ID was not found.
    """
    with get_connection() as conn:
        conn.execute("""
            UPDATE vehicles
            SET plate     = ?,
                model     = ?,
                driver_id = ?,
                updated_at = datetime('now', 'localtime')
            WHERE id = ?
        """, (plate, model, driver_id, vehicle_id))

        return get_vehicle_by_id(vehicle_id)


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

def delete_vehicle(vehicle_id: int) -> bool:
    """
    Deletes a vehicle by ID.

    Returns:
        True if the vehicle was deleted, False if not found.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM vehicles WHERE id = ?", (vehicle_id,)
        )
        return cursor.rowcount > 0


def get_vehicle_by_id(vehicle_id: int) -> Optional[Vehicle]:
    """Returns a vehicle by ID or None if not found."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, plate, model, driver_id, created_at, updated_at
            FROM vehicles WHERE id = ?
        """, (vehicle_id,)).fetchone()
        return _row_to_vehicle(row) if row else None


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _row_to_vehicle(row) -> Vehicle:
    """Converts a database row into a Vehicle dataclass instance."""
    return Vehicle(
        id=         row["id"],
        plate=      row["plate"],
        model=      row["model"],
        driver_id=  row["driver_id"],
        created_at= row["created_at"],
        updated_at= row["updated_at"],
    )
