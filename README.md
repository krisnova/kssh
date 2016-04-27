# kSSH

kSSH is a command line utility that makes keeping track of SSH aliases much more convenient. A user can manage SSH aliases easily from the kSSH executable.

kSSH abstracts the user from editing an SSH config file whenever a change is needed. Alias all the things!

 - Want to add a new alias? **kssh [alias]**
 - Forget what you have registered? Want to see them all? **kssh list**
 - Ready to delete an alias? **kssh delete [alias]**
 - Want to wipe the slate clean and start over? **kssh purge**
 - Does this alias still work? It's been a while..? **kssh test [alias]**

## Installing

MacOS X

    sudo -H pip install kssh

## Getting Started

######Quick Start

    kssh <new_alias_name>

This will build a new kSSH record for the given alias. kSSH will then attempt to connect to the host using a defined RSA key. If a key cannot be found kSSH will create one. kSSH will then verify the connection.

Now the user can SSH into the host by using the same command as above.

##Actions

###### These are arguments to the kSSH executable, and examples of how to use them.

**CONNECT** Will connected to an alias. If no alias is found, will attempt to create one.

    kssh <alias>
    kssh connect <alias>

**LIST** Will list all known aliases.

    kssh list

**GENERATE** Will generate a new RSA key named after the alias.

    kssh generate <alias>

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

## New Release Process
    
    sudo -H python setup.py register sdist bdist upload
    
 - Update version in kssh.py
 - Update version in setup.py
 - Push to github
 - Push to PyPi (Use credentials)
