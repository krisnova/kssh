# kSSH
kSSH is a simple utility for managing SSH hosts and tracking aliases in an SSH config file.
kSSH helps managing a large number of SSH hosts by making the process easy. With kSSH the user never needs to remember SSH hostnames again!


#### Installing

MacOS X

    sudo -h pip install kssh

#### Running kSSH

######Quick Start

    kssh <new_alias_name>

This will build a new kSSH record for the given alias. kSSH will then attempt to connect to the host using a defined RSA key. If a key cannot be found kSSH will create one. kSSH will then verify the connection.

Now the user can SSH into the host by using the same command as above.

######Actions

[ACTIONS]

**CONNECT** Will connected to an alias. If no alias is found, will attempt to create one.

    kssh <alias>
    kssh connect <alias>

**LIST** Will list all known aliases.

    kssh list

**GENERATE** Will generate a new RSA key named after the alias.

    kssh GENERATE <alias>

**COPY** Will attempt to copy an RSA key to a remote host.

    kssh copy <user> <host> <path_to_key>

**TEST** Will test a connection no a known alias. If the alias is not found, the test will fail.

    kssh test <alias>

**ADD** Will add a new alias. If the alias already exists, it will be updated.

    kssh add <alias>

**DELETE** Will delete an existing alias if it exists.

    kssh delete <alias>

**PURGE** Will purge the existing SSH config data (This cannot be undone!)

    kssh purge

#### New Release Process
 - Update version in kssh.py
 - Update version in setup.py
 - Push to github
 - Push to PyPi (Use credentials)

       sudo -H python setup.py register sdist bdist upload