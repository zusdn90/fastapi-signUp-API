from datetime import datetime, timezone
from re import L
from typing import Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, validator, Field
from fastapi.param_functions import Query
from app.core.utils.date_utils import KST
from typing import Any, Dict, Optional, List, Union
import datetime
from app.core.utils.date_utils import D

#######################################
# Request Parameter schema
#######################################
# Query parameter
# ::: pydantic모델로 만들면 desscription, example 기능이 안됨. custom class로 적용


#######################################
# Response schema
#######################################
