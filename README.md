# MSAL Testing

Simple repo for hacking around with [MSAL](https://learn.microsoft.com/en-us/entra/identity-platform/msal-overview) and some of its issues with [Secret Service](https://specifications.freedesktop.org/secret-service-spec/latest/) and [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager) on Linux.

## Usage

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./msal_testing.py
```

## See Also

- <https://github.com/AzureAD/microsoft-authentication-library-for-dotnet/issues/3033>
- <https://github.com/AzureAD/microsoft-authentication-library-for-dotnet/issues/3814#issuecomment-1322634854>
- <https://github.com/MicrosoftDocs/microsoft-authentication-library-for-python/blob/main/msal-python-conceptual/advanced/linux-broker-py-wsl.md>
