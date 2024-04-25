from bs4 import BeautifulSoup
from fastapi import HTTPException
import httpx 
from typing import Dict, Optional
from ..models.practitioner import Practitioner
import os

def fetch_practitioner_data(member_id: str) -> Practitioner:
    """
    Query external endpoint for practitioner data.

    Args:
    member_id (str): member ID from request parameters.

    Returns:
    dict: A dictionary containing formatted practitioner data if extraction is successful, None otherwise.
    """
    api_url = os.getenv("API_URL")
    session_id = os.getenv("JSESSIONID")
    if not api_url or not session_id:
        raise HTTPException(status_code=500, detail="ENV variables not set up")
    
    url = f"{api_url}?numeroColegiado={member_id}"
    cookies = {'JSESSIONID': session_id}
    
    try:
        response = httpx.get(url, cookies=cookies)
        response.raise_for_status()

        practitioner_data = parse_practitioner_html(response.text)
        if practitioner_data:
            return Practitioner(**practitioner_data)
        else:
            return None
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


def parse_practitioner_html(html_content: str) -> Optional[dict]:
    """
    Extracts and formats practitioner data from HTML content.

    Args:
    html_content (str): HTML content as a string from which data needs to be extracted.

    Returns:
    dict: A dictionary containing formatted practitioner data if extraction is successful, None otherwise.
    """
    soup = BeautifulSoup(html_content, 'lxml')

    data = {}

    try:
        table = soup.find('table', class_='resultados')
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:  # Ensure there are exactly two columns
                label = cells[0].text.strip()
                value = cells[1].text.strip()

                # Mapping labels to data dictionary keys
                if 'Número colegiado' in label:
                    data['memberId'] = value
                elif 'Nombre y Apellidos' in label:
                    data['fullName'] = value
                elif 'Provincia colegiación' in label:
                    data['membershipProvince'] = value
                elif 'Especialidad' in label:
                    data['medicalSpecialty'] = value
                elif 'Estado de colegiación' in label:
                    data['membershipState'] = value
                elif 'Dirección de trabajo' in label:
                    data['workAddress'] = value

        # Format the extracted data before returning
        formatted_data = format_data(data)
        return formatted_data
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None


def clean_text(text: str) -> str:
    """Normalize spaces and strip the text."""
    return ' '.join(text.split())


def format_data(data: Dict[str, str]) -> Dict[str, str]:
    """Format the data dictionary by cleaning text and replacing empty fields."""
    for key, value in data.items():
        # Clean the text if there's any content
        if value.strip():
            data[key] = clean_text(value)
        else:
            # Set undefined if the field is empty
            data[key] = "undefined"

    # Specifically format the full name for proper capitalization if not undefined
    if data["fullName"] != "undefined":
        data["fullName"] = ' '.join(word.capitalize() for word in data["fullName"].split())

    return data
