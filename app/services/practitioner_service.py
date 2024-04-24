from ..models.practitioner import Practitioner
from bs4 import BeautifulSoup
from typing import Dict, Optional
import httpx 

def fetch_practitioner_data(member_id: str) -> Practitioner:
    """Query external endpoint for practitioner data."""
    url = f"https://cgcom-interno.cgcom.es/RegistroMedicos/PUBBusquedaPublica_busquedaDetalle_ajax.action?numeroColegiado={member_id}"
    cookies = {'JSESSIONID': '0553653B8A1214B92AE4EC97CB948D71'}
    
    try:
        response = httpx.get(url, cookies=cookies)
        response.raise_for_status()
        
        # Parse the HTML content
        practitioner_data = parse_practitioner_html(response.text)
        if practitioner_data:
            return Practitioner(**practitioner_data)
        else:
            return None
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while fetching data: {exc.response.text}")
        raise
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        raise


def parse_practitioner_html(html_content: str) -> Optional[dict]:
    """Extract content from the html response."""
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
