import requests


class Grafana:
    """
    This class provides methods to interact with Grafana and make API requests.
    Attributes:
    - user_agent: The user agent string used for the HTTP requests.
    - token: The Grafana authentication token used for API requests.
    - domain: The domain of the Grafana server.
    - headers: HTTP headers containing the authentication token and user agent.
    """
    user_agent = "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0"

    def __init__(self, domain, token):
        """
        Initializes the Grafana client with the given domain and token.
        Params:
            -Domain: The domain of the Grafana server.
            -Token: The Grafana authentication token used for API requests.
        """
        self.token = token
        self.domain = domain
        self.headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": self.user_agent
        }

    def list_folders(self):
        """
        Returns a list of folders in Grafana.
        Return: A response object containing the list of folders.
        """
        return requests.get(f"{self.domain}/api/folders", headers=self.headers)

    def list_dashboards(self, folder_id):
        """
        Returns a list of dashboards in a specific folder.
        Param folder_id: The ID of the folder to retrieve dashboards from.
        Return: A response object containing the list of dashboards.
        """
        return requests.get(f"{self.domain}/api/search?folderIds={folder_id}&type=dash-db", headers=self.headers)

    def get_dashboard(self, dashboard_uid):
        """
        Retrieves details of a specific dashboard using its UID.
        Param dashboard_uid: The UID of the dashboard to retrieve.
        Return: A response object containing the dashboard details.
        """
        return requests.get(f"{self.domain}/api/dashboards/uid/{dashboard_uid}", headers=self.headers)

