"""
drivers_repository.py
Handles all database operations for the drivers table.
"""

from dataclasses import dataclass
from typing import Optional
from app.core.database import get_connection


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Driver:
    """Represents a driver record from the database."""
    id:         int
    name:       str
    cpf:        Optional[str]
    phone:      Optional[str]
    department: Optional[str]
    photo_path: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]



# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def create_driver(
    name:       str,
    cpf:        Optional[str] = None,
    phone:      Optional[str] = None,
    department: Optional[str] = None,
    photo_path: Optional[str] = None,
) -> Driver:
    """
    Inserts a new driver into the database.

    Args:
        name:       Required. Full name of the driver.
        cpf:        Optional. CPF number.
        phone:      Optional. Phone number.
        department: Optional. Department or sector.
        photo_path: Optional. Path to the driver's photo file.

    Returns:
        The created Driver with the generated ID.
    """
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO drivers (name, cpf, phone, department, photo_path)
            VALUES (?, ?, ?, ?, ?)
        """, (name, cpf, phone, department, photo_path))

        driver_id = cursor.lastrowid

    return get_driver_by_id(driver_id)

# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def get_all_drivers() -> list[Driver]:
    """Returns all drivers ordered by name."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, name, cpf, phone, department, photo_path, created_at, updated_at
            FROM drivers
            ORDER BY name ASC
        """).fetchall()
        return [_row_to_driver(row) for row in rows]


def get_driver_by_id(driver_id: int) -> Optional[Driver]:
    """Returns a driver by ID or None if not found."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, name, cpf, phone, department, photo_path, created_at, updated_at
            FROM drivers
            WHERE id = ?
        """, (driver_id,)).fetchone()
        return _row_to_driver(row) if row else None


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

def update_driver(
    driver_id:  int,
    name:       str,
    cpf:        Optional[str] = None,
    phone:      Optional[str] = None,
    department: Optional[str] = None,
    photo_path: Optional[str] = None,
) -> Optional[Driver]:
    """
    Updates an existing driver record.

    Returns:
        The updated Driver or None if the ID was not found.
    """
    with get_connection() as conn:
        conn.execute("""
            UPDATE drivers
            SET name       = ?,
                cpf        = ?,
                phone      = ?,
                department = ?,
                photo_path = ?,
                updated_at = datetime('now', 'localtime')
            WHERE id = ?
        """, (name, cpf, phone, department, photo_path, driver_id))

        return get_driver_by_id(driver_id)


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

def delete_driver(driver_id: int) -> bool:
    """
    Deletes a driver by ID.

    Returns:
        True if the driver was deleted, False if not found.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM drivers WHERE id = ?", (driver_id,)
        )
        return cursor.rowcount > 0


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _row_to_driver(row) -> Driver:
    """Converts a database row into a Driver dataclass instance."""
    return Driver(
        id=         row["id"],
        name=       row["name"],
        cpf=        row["cpf"],
        phone=      row["phone"],
        department= row["department"],
        photo_path= row["photo_path"],
        created_at= row["created_at"],
        updated_at= row["updated_at"],
    )