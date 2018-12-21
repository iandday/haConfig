# Home Assistant Configuration

[Home Assistant](https://www.home-assistant.io) configuration files

## Secure Credential Storage

Files containing credentials used in Home Assistant can be securely versioned in GitHub alongside the rest of your configuration files through the use of a pre-commit hook script.  The script utilizes Ansible-Vault to add a current encrypted version of sensitive files to every commit to ensure all configuration files are versioned.  Ansible must be installed on the system running Home Assistant and is available via PIP.

The script will add encrypted versions of the following sensitive files to each commit you make.  Instructions are in the script's header to add additional files.

* `secrets.yaml`
* `phue.conf`
* `known_devices.yaml`
* `options.xml`
* `ecobee.conf`
* `.vaultCredential`
* `.august.conf`
* `.ios.conf`
* `.storage/onboarding`
* `.storage/core.entity_registry`
* `.storage/core.device_registry`
* `.storage/core.config_entries`
* `.storage/auth_provider.homeassistant`
* `.storage/auth`

Once Ansible is installed perform the following steps to safely store credentials alongside the rest of your configuration files.

1. Add the following entries to your `.gitignore` file
    * `secrets.yaml`
    * `phue.conf`
    * `known_devices.yaml`
    * `options.xml`
    * `ecobee.conf`
    * `.vaultCredential`
    * `.august.conf`
    * `.ios.conf`
    * `.storage/onboarding`
    * `.storage/core.entity_registry`
    * `.storage/core.device_registry`
    * `.storage/core.config_entries`
    * `.storage/auth_provider.homeassistant`
    * `.storage/auth`


1. Copy the file [pre-commit.sh](https://raw.githubusercontent.com/iandday/haConfig/master/pre-commit.sh) to the root directory of your configuration repository and set it as executable.
2. Create the file `.vaultCredential` in the root directory of your configuration repository.  There should only be one line in the file containing the password used to encrypt your sensitive files.  Make sure to apply appropriate permissions to this file (0600) or stricter.
3. Enable the pre-commit git hook with the following command from the root of your configuration directory:

    * `ln -s ../../pre-commit.sh .git/hooks/pre-commit`


## Customizations
* [Custom Battery Levels](https://bonani.tech/track-battery-levels-with-home-assistant-and-custom-ui/)