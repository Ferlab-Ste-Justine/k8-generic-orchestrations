import json
import os
import sys
import requests


CONFIG_PATH = "/opt/config/realm-config.json"
POLARIS_SERVICE_HOST = os.environ["POLARIS_SERVICE_HOST"]
CATALOG_ENDPOINT = os.environ["CATALOG_ENDPOINT"]

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)


def polaris_api(method, endpoint, realm, token, payload=None):
    url = f"http://{POLARIS_SERVICE_HOST}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Polaris-Realm": realm,
        "Accept": "application/json"
    }
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload)
    else:
        data = None

    resp = requests.request(method, url, headers=headers, data=data)
    if not resp.ok:
        print(f"❌ API request failed for method '{method}' and url '{url}' with payload '{payload}'")
        print(resp.text)
        sys.exit(1)
    return resp.json() if method in ["GET", "POST"] else resp.text


def fetch_token(client_id, client_secret):
    url = f"http://{POLARIS_SERVICE_HOST}/api/catalog/v1/oauth/tokens"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope=PRINCIPAL_ROLE:ALL"
    resp = requests.post(url, headers=headers, data=data)
    if not resp.ok:
        print("❌ Failed to obtain access token")
        print(resp.text)
        sys.exit(1)
    token = resp.json().get("access_token")
    if not token:
        print(f"❌ Failed to parse access token from response: {resp.text}")
        sys.exit(1)
    print("✅ Obtained access token")
    return token


def create_catalog_if_not_exists(realm, token, catalog_name, catalog_endpoint, catalog_warehouse):
    payload = {
        "catalog": {
            "name": catalog_name,
            "type": "INTERNAL",
            "readOnly": False,
            "properties": {
                "default-base-location": catalog_warehouse
            },
            "storageConfigInfo": {
                "storageType": "S3",
                "allowedLocations": [catalog_warehouse],
                "endpoint": catalog_endpoint,
                "pathStyleAccess": True
            }
        }
    }
    catalogs = polaris_api("GET", "api/management/v1/catalogs", realm, token)
    if any(c.get("name") == catalog_name for c in catalogs.get("catalogs", [])):
        print(f"The catalog '{catalog_name}' already exists, skipping creation.")
    else:
        polaris_api("POST", "api/management/v1/catalogs", realm, token, payload)
        print("✅ Catalog created")


def create_namespace_if_not_exists(realm, token, catalog_name, namespace):
    payload = {
        "namespace": [namespace],
        "properties": {}
    }
    namespaces = polaris_api("GET", f"api/catalog/v1/{catalog_name}/namespaces", realm, token)
    if any( namespace in ns for ns in namespaces.get("namespaces", [])):
        print(f"The namespace '{namespace}' already exists in catalog '{catalog_name}', skipping creation.")
    else:
        polaris_api("POST", f"api/catalog/v1/{catalog_name}/namespaces", realm, token, payload)
        print("✅ Namespace created")


def create_principal_if_not_exists(realm, token, principal_name):
    payload = {
        "principal": {
            "name": principal_name,
            "properties": {}
        }
    }
    principals = polaris_api("GET", "api/management/v1/principals", realm, token)
    if any(p.get("name") == principal_name for p in principals.get("principals", [])):
        print(f"The principal '{principal_name}' already exists, skipping creation.")
    else:
        polaris_api("POST", "api/management/v1/principals", realm, token, payload)
        print(f"✅ User '{principal_name}' created")


def reset_principal_credentials(realm, token, principal_name, principal_user, principal_password):
    payload = {
        "clientId": principal_user,
        "clientSecret": principal_password
    }
    polaris_api("POST", f"api/management/v1/principals/{principal_name}/reset", realm, token, payload)
    print(f"✅ Credentials for principal '{principal_name}' reset")


def create_catalog_role_if_not_exists(realm, token, catalog_name, role_name):
    payload = {
        "catalogRole": {
            "name": role_name,
            "properties": {}
        }
    }
    roles = polaris_api("GET", f"api/management/v1/catalogs/{catalog_name}/catalog-roles", realm, token)
    if any(r.get("name") == role_name for r in roles.get("roles", [])):
        print(f"The catalog role '{role_name}' already exists, skipping creation.")
    else:
        polaris_api("POST", f"api/management/v1/catalogs/{catalog_name}/catalog-roles", realm, token, payload)
        print("✅ Catalog role created")


def create_principal_role_if_not_exists(realm, token, role_name):
    payload = {
        "principalRole": {
            "name": role_name,
            "properties": {}
        }
    }
    roles = polaris_api("GET", "api/management/v1/principal-roles", realm, token)
    if any(r.get("name") == role_name for r in roles.get("roles", [])):
        print(f"The principal role '{role_name}' already exists, skipping creation.")
    else:
        polaris_api("POST", "api/management/v1/principal-roles", realm, token, payload)
        print("✅ Principal role created")


def assign_role_to_principal(realm, token, principal_name, role_name):
    payload = {
        "principalRole": {
            "name": role_name,
            "properties": {}
        }
    }
    roles = polaris_api("GET", f"api/management/v1/principals/{principal_name}/principal-roles", realm, token)
    if any(r.get("name") == role_name for r in roles.get("roles", [])):
        print(f"The role '{role_name}' is already assigned to principal '{principal_name}', skipping assignment.")
    else:
        polaris_api("PUT", f"api/management/v1/principals/{principal_name}/principal-roles", realm, token, payload)
        print(f"✅ Role '{role_name}' assigned to principal '{principal_name}'")


def assign_catalog_role_to_principal_role(realm, token, catalog_name, catalog_role_name, principal_role_name):
    payload = {
        "catalogRole": {
            "name": catalog_role_name
        }
    }
    catalog_roles = polaris_api("GET", f"api/management/v1/principal-roles/{principal_role_name}/catalog-roles/{catalog_name}", realm, token)
    if any(r.get("name") == catalog_role_name for r in catalog_roles.get("roles", [])):
        print(f"The catalog role '{catalog_role_name}' is already assigned to principal role '{principal_role_name}', skipping assignment.")
    else:
        polaris_api("PUT", f"api/management/v1/principal-roles/{principal_role_name}/catalog-roles/{catalog_name}", realm, token, payload)
        print(f"✅ Catalog role '{catalog_role_name}' assigned to principal role '{principal_role_name}' for catalog '{catalog_name}'")


def grant_privilege_if_not_exists(realm, token, catalog_name, role_name, privilege):
    payload = {"type": "catalog", "privilege": privilege}
    grants = polaris_api("GET", f"api/management/v1/catalogs/{catalog_name}/catalog-roles/{role_name}/grants", realm, token)
    if any(g.get("privilege") == privilege for g in grants.get("grants", [])):
        print(f"The '{role_name}' role already has the '{privilege}' privilege on catalog '{catalog_name}', skipping grant.")
    else:
        polaris_api("PUT", f"api/management/v1/catalogs/{catalog_name}/catalog-roles/{role_name}/grants", realm, token, payload)
        print(f"✅ Granted '{privilege}' privilege to '{role_name}' role on catalog '{catalog_name}'")


def main():
    config = load_config(CONFIG_PATH)


    for realm in config.get("realms", []):
        realm_name = realm['name']
        print(f"Processing realm: {realm_name}")
        realm_user = os.environ[f"POLARIS_REALM_{realm_name.upper()}_ROOT_USER"]
        realm_password = os.environ[f"POLARIS_REALM_{realm_name.upper()}_ROOT_PASSWORD"]
        token = fetch_token(realm_user, realm_password)

        for catalog in realm.get("catalogs", []):
            create_catalog_if_not_exists(realm_name, token, catalog["name"], CATALOG_ENDPOINT, catalog["warehouse"])
            for ns in catalog.get("namespaces", []):
                create_namespace_if_not_exists(realm_name, token, catalog["name"], ns)
            for role in catalog.get("catalog_roles", []):
                create_catalog_role_if_not_exists(realm_name, token, catalog["name"], role["name"])
                for privilege in role.get("privileges", []):
                    grant_privilege_if_not_exists(realm_name, token, catalog["name"], role["name"], privilege)

        for principal_role in realm.get("principal_roles", []):
            create_principal_role_if_not_exists(realm_name, token, principal_role['name'])
            for catalog_role in principal_role['catalog_roles']:
                assign_catalog_role_to_principal_role(realm_name, token, catalog_role['catalog'], catalog_role['name'], principal_role['name'])

        for principal in realm.get("principals", []):
            principal_name = principal["name"]
            create_principal_if_not_exists(realm_name, token, principal_name)
            principal_user = os.environ[f"POLARIS_REALM_{realm_name.upper()}_{principal_name.upper()}_USER"]
            principal_password = os.environ[f"POLARIS_REALM_{realm_name.upper()}_{principal_name.upper()}_PASSWORD"]

            reset_principal_credentials(realm_name, token, principal_name, principal_user, principal_password)
            for principal_role in principal.get("principal_roles", []):
                assign_role_to_principal(realm_name, token, principal_name, principal_role)

        print(f"Done processing realm {realm_name}\n")


if __name__ == "__main__":
    main()