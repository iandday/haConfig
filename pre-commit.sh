# !/bin/bash
#
# Pre-commit hook to add ansbile-vault encrypted current versions of the files listed below
#   files will be encrypted with the string located in the file .vaultCredential
#   additional files can be added to the array, space delimited and surrounded in quotes

for i in "secrets.yaml" "phue.conf" "ecobee.conf" ".august.conf" ".ios.conf" ".storage/onboarding" ".storage/core.entity_registry" ".storage/core.device_registry" ".storage/core.config_entries" ".storage/auth_provider.homeassistant" ".storage/auth"
do
   if [ -f "$i" ]
   then
        rm $i.vault
        cp $i $i.vault
        ansible-vault --vault-password-file .vaultCredential encrypt $i.vault
        git add $i.vault
   fi
done
