"""
The file that contains dataclasses
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EmailParams:
    """
    The class EmailParams that
    contains emails arguments fields
    """
    subject: str
    message: str
    from_email: str
    recipient_list: List[str]


@dataclass
class EmailHTMLParams:
    """
    The class EmailParams that
    contains emails arguments fields
    with html template
    """
    subject: str
    html_content: str
    from_email: str
    recipient_list: List[str]
    text_content: Optional[str] = None
