"""
 * @author Idris Adeniji (alvacoder)
 * @email idrisadeniji01@gmail.com
 * @create date 2025-03-18 22:01:56
"""

import requests
import os
import sys
import logging

def get_env_var(name):
    return os.environ.get(f"INPUT_{name}") or os.environ.get(name)

class Defectdojo:

    def __init__(self):
        # Required Secrets for this awesome code to function.
        self.defectdojo_api_key = get_env_var("DEFECTDOJO_API_KEY")
        self.defectdojo_username = get_env_var("DEFECTDOJO_USERNAME")
        self.defectdojo_password = get_env_var("DEFECTDOJO_PASSWORD")
        self.defectdojo_iap_token = get_env_var("DEFECTDOJO_IAP_TOKEN")

        # Required Defectdojo Variables.
        self.defectdojo_url = get_env_var("DEFECTDOJO_URL")
        self.defectdojo_reimport_status = get_env_var("DEFECTDOJO_REIMPORT_STATUS")
        self.defectdojo_product_type = get_env_var("DEFECTDOJO_PRODUCT_TYPE")
        self.defectdojo_product = get_env_var("DEFECTDOJO_PRODUCT")
        self.defectdojo_environment_type = get_env_var("DEFECTDOJO_ENVIRONMENT_TYPE")
        self.defectdojo_scan_type = get_env_var("DEFECTDOJO_SCAN_TYPE")
        self.defectdojo_engagement_name = get_env_var("DEFECTDOJO_ENGAGEMENT_NAME")
        self.defectdojo_engagement_name = get_env_var("DEFECTDOJO_ENGAGEMENT_NAME")
        self.defectdojo_engagement_name = get_env_var("DEFECTDOJO_ENGAGEMENT_NAME")
        self.scan_results_file_path = get_env_var("RESULTS_FILE_PATH")

    def import_scan_results_to_defectdojo(
        self,
        logger: logging.Logger,
        client_certificate_file_path=None,
        client_key_file_path=None
    ) -> int:

        api_endpoint = f"{self.defectdojo_url}/api/v2/import-scan/"

        if self.defectdojo_reimport_status and self.defectdojo_reimport_status.lower() == "true":
            api_endpoint = f"{self.defectdojo_url}/api/v2/reimport-scan/"
            logger.info("Using reimport-scan API endpoint")
        else:
            api_endpoint = f"{self.defectdojo_url}/api/v2/import-scan/"
            logger.info("Using import-scan API endpoint")

        headers = {
            "Authorization": f"Token {self.defectdojo_api_key}",
            "Proxy-Authorization": f"Bearer {self.defectdojo_iap_token}"
            }
        data = {
            "product_type_name": self.defectdojo_product_type,
            "product_name": self.defectdojo_product,
            "environment": self.defectdojo_environment_type,
            "scan_type": self.defectdojo_scan_type,
            "engagement_name": self.defectdojo_engagement_name,
            "auto_create_context": True,
            "deduplication_on_engagement": True,
            "close_old_findings": True,
            "push_to_jira": True,
        }

        try:
            with open(self.scan_results_file_path, "rb") as scan_file:
                files = {"file": scan_file}

                if client_certificate_file_path and client_key_file_path:
                    r = requests.post(
                        api_endpoint,
                        headers=headers,
                        files=files,
                        data=data,
                        verify=True,
                        cert=(client_certificate_file_path, client_key_file_path),
                        timeout=180
                    )
                else:
                    r = requests.post(
                        api_endpoint,
                        headers=headers,
                        files=files,
                        data=data,
                        verify=True,
                        timeout=180
                    )

                if r.status_code == 201 or r.status_code == 200:
                    return r.status_code
                else:
                    logger.error(f"Upload of results failed with status code {r.status_code}")
                    sys.exit(1)
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during scan upload: {e}")
            sys.exit(1)

    def run(self):
        try:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            self.import_scan_results_to_defectdojo(logger)
        except Exception as e:
            print(f"Exception: {e}")
            sys.exit(1)

if __name__ == "__main__":
    Defectdojo().run()
