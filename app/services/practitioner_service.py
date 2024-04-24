from ..models.practitioner import Practitioner
from bs4 import BeautifulSoup
from typing import Any, Optional
import httpx 

# TODO: Replace with Practitioner
def fetch_practitioner_data(memberId: str) -> Any:
    url = f"https://cgcom-interno.cgcom.es/RegistroMedicos/PUBBusquedaPublica_busquedaDetalle_ajax.action?numeroColegiado={memberId}"
    cookies = {'JSESSIONID': '0553653B8A1214B92AE4EC97CB948D71'}
    
    try:
        response = httpx.get(url, cookies=cookies)
        response.raise_for_status()
        print('Response body:', response.text)      
          
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

        return data
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None
