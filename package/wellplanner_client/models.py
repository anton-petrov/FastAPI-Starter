"""
    Project models
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field, PositiveFloat, confloat, conint


class User(BaseModel):
    name: str
