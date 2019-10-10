# XS_PYTHON
Collecting project for shipment of python packages as one software component on *Service Marketplace*

## *SAP* packages included
 * sap_instance_manager - client for instance manager.
 * sap_audit_logging - client for audit log service.
 * sap_xssec - XS Advanced Container Security API for python.
 * sap_py_jwt - JSON Web Token (JWT) offline validation.
 * hdbcli - HANA database client.

## Installing an *SAP* package
To install an *SAP* package you need to extract the content of the *XS_PYTHON* zip to some folder.
Then install the package using *pip* in the following way:
```sh
pip install --find-links=<path_to_extracted_XS_PYTHON_folder> <sap_package_name>
```
 **Note:** Make sure you have Internet connection so that *pip* is able to download and install the external dependencies.
