# from ..models.practitioner import Practitioner
from typing import Any
import httpx 

# TODO: Replace with Practitioner
def fetch_practitioner_data(memberId: str) -> Any:
    url = f"https://cgcom-interno.cgcom.es/RegistroMedicos/PUBBusquedaPublica_busquedaDetalle_ajax.action?numeroColegiado={memberId}"
    cookies = {'JSESSIONID': '7DACF516961B9CDD494526A3D4949DAD'}
    
    try:
        response = httpx.get(url, cookies=cookies)
        response.raise_for_status()
        print('Response body:', response.text)        
        data = response.json()
        # TODO: Implement data parsing
        return data
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while fetching data: {exc.response.text}")
        raise
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        raise
