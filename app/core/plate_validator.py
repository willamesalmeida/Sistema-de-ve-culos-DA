"""
plate_validator.py
Handles Brazilian vehicle plate validation and normalization.

Supported formats:
    - Old format:     ABC-1234  (3 letters + 4 digits)
    - Mercosul:       ABC1D23   (3 letters + 1 digit + 1 letter + 2 digits)
"""

import re 
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Old format: ABC1234 or ABC-1234
_PATTERN_OLD = re.compile(r"^[A-Z]{3}-?\d{4}$")
# Mercosul format: ABC1D23
_PATTERN_MERCOSUL = re.compile(r"^[A-Z]{3}\d[A-Z]\d{2}$")

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class PlateValidationResult:
    """Holds the result of plate validation"""
    is_valid: bool
    normalized: str
    format:str
    message: str

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_plate(raw_input: str) -> PlateValidationResult:
    """
    Validates and normalizes a Brazilian vehivles plate.
    Accepts plates with or without hyphens, spaces and lowercase letters.
    Args:
        raw_input: The plate string typed by the user.

    Returns:
        PlateValidationResult with validation status, normalized plate,
        detected format and a human-readable message.
    """


    normalized = _normalize(raw_input)

    if not normalized:
        return PlateValidationResult(
            is_valid=False,
            normalized="",
            format="unknown",
            message="Placa não pode ser vazia."
        )
    if _PATTERN_OLD.match(normalized):
        return PlateValidationResult(
            is_valid=True, 
            normalized=normalized,
            format="old",
            message="Placa válida (padrão antigo)."
        )

    if _PATTERN_MERCOSUL.match(normalized):
        return PlateValidationResult(
            is_valid=True,
            normalized=normalized,
            format="mercosul",
            message="Placa válida (padrão Mercosul)."
        )
    return PlateValidationResult(
        is_valid=False,
        normalized=normalized,
        format="unknown",
        message="Placa inválida. Use o formato ABC1234 ou ABC1D23."
    )

# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _normalize(raw_input:str) -> str:
     """
    Normalizes raw plate input by removing hyphens, spaces
    and converting to uppercase.

    Example:
        "abc-1234"  → "ABC1234"
        "ABC 1D23"  → "ABC1D23"
        "abc1d23"   → "ABC1D23"
    """
     return raw_input.strip().upper().replace("-","").replace(" ", "")
