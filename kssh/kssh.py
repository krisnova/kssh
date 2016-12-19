#!/usr/bin/python
########################################################################################################################
#
# MIT License
#
# Copyright (c) [2016-2017] [Kris Nova]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
########################################################################################################################

import sys
import re
import os
import rlcompleter
import readline
from subprocess import call

# Default configuration
default_key_name = "id_rsa"

# Execution Parameters
version = "1.1.9"
show_errors = False

# Usage for the tool
description = '''
\033[1mkssh [Kris SSH]\033[0m V%s

Author: Kris Nova <kris@nivenly.com>

    Quick Start : kssh <new_ssh_alias>

    \033[1mkssh\033[0m is a simple utility for managing SSH hosts and tracking aliases in an SSH config file.
    This tool is catered to work on OSX. Any other operating systems are currently not supported.

[ACTIONS]

    \033[95m[CONNECT]\033[0m Will connected to an alias. If no alias is found, will attempt to create one.
        kssh <\033[91malias\033[0m>
        kssh connect <\033[91malias\033[0m>

    \033[95m[LIST]\033[0m Will list all known aliases.
        kssh list

    \033[95m[GENERATE]\033[0m Will generate a new RSA key named after the alias.
        kssh GENERATE <\033[91malias\033[0m>

    \033[95m[COPY]\033[0m Will attempt to copy an RSA key to a remote host.
        kssh copy <\033[91muser\033[0m> <\033[91mhost\033[0m> <\033[91mpath_to_key\033[0m>

    \033[95m[TEST]\033[0m Will test a connection no a known alias. If the alias is not found, the test will fail.
        kssh test <\033[91malias\033[0m>

    \033[95m[ADD]\033[0m Will add a new alias. If the alias already exists, it will be updated.
        kssh add <\033[91malias\033[0m>

    \033[95m[DELETE]\033[0m Will delete an existing alias if it exists.
        kssh delete <\033[91malias\033[0m>

    \033[95m[PURGE]\033[0m Will purge the existing SSH config data (This cannot be undone!)
        kssh purge
''' % version

# Available actions
actions = ['connect', 'list', 'generate', 'copy', 'test', 'add', 'delete', 'purge']

# Fix the GNU vs BSD tab completion problem
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


########################################################################################################################
#
# MAIN
#
def main():
    try:
        firstarg = sys.argv[1]
        if firstarg == "-h" or firstarg == "--help":
            sys.exit(1)
    except:
        print description
        sys.exit(1)

    init_datastore()
    try:
        action_function = 'action_' + firstarg
        if firstarg == "list":
            action_list()
        if firstarg == "copy":
            action_copy(sys.argv[2], sys.argv[3], sys.argv[4])
        if firstarg == "purge":
            i = raw_input(
                "Purge all SSH config data?\n(This action cannot be undone)\n\tOnly 'yes' will be accepted : ")
            if i == "yes":
                out("Purging all SSH config data")
                write_data("")
            else:
                out("Retaining SSH config data")
        else:
            f = getattr(sys.modules[__name__], action_function)
            f(sys.argv[2])
    except SystemExit:
        out("Exiting..")
        sys.exit(1)
    except KeyboardInterrupt:
        out("\nSIGTERM detected. Exiting gracefully")
    except IndexError:
        print description
        sys.exit(1)
    except AttributeError:
        if show_errors:
            print sys.exc_info()
        action_connect(firstarg)
    except:
        if show_errors:
            print sys.exc_info()
    out("Bye!")


########################################################################################################################
#
# ADD
#
def action_add(name):
    if exists(name):
        out("Record exists, updating")
        # TODO WE CAN HAVE THIS PRE-POPULATE
    else:
        out("Adding new record")
    # HOST
    readline.set_completer(complete_hosts)
    host = raw_input("HostName: ")

    # USER
    readline.set_completer(complete_users)
    user = raw_input("User: ")

    # KEY
    readline.set_completer(complete_keys)
    key = raw_input("Key: ").rstrip()
    if key == "":
        key = default_key_name

    if ".ssh" not in key:
        key = os.path.expanduser('~') + "/.ssh/" + key
        out("Key absolute path %s" % key)
    if not os.path.exists(key):
        out("Unable to locate key %s" % key)
        key = action_generate(key)
    start = "##<---" + name + "---\n"
    stop = "\n##---" + name + "--->"

    block = '''Host %s
    HostName %s
    User %s
    IdentityFile %s''' % (name, host, user, key)
    block = start + block + stop
    existing_config = get_data()

    if exists(name):
        config = re.sub(start + ".*?" + stop, block, existing_config, flags=re.DOTALL)
        write_data(config)
        out("Updating SSH config with new record")
    else:
        write_data(existing_config + "\n" + block)
        out("Adding new record to SSH config")

    if not action_test(name):
        action_copy(user, host, key)
        if not action_test(name):
            out("Major error, unable to contact host")
            sys.exit(1)
    out("You can now access this host using 'kssh %s'" % name)


########################################################################################################################
#
# COPY
#
def action_copy(user, host, path_to_key):
    out("Copying id for %s@%s with key %s" % (user, host, path_to_key))
    if ".pub" not in path_to_key:
        path_to_key = path_to_key + ".pub"
    if ".ssh" not in path_to_key:
        path_to_key = os.path.expanduser('~') + "/.ssh/" + path_to_key
    with open(path_to_key) as f:
        content = f.read()
    copy_cmd = '''mkdir -p -m 700 ~/.ssh && touch ~/.ssh/authorized_keys \
&& chmod 600 ~/.ssh/authorized_keys && echo '%s' >> ~/.ssh/authorized_keys''' % content
    out(copy_cmd)
    call(["ssh", user + "@" + host, copy_cmd])


########################################################################################################################
#
# GENERATE
#
def action_generate(name):
    out("Generating new RSA key")
    if ".ssh" not in name:
        name = os.path.expanduser('~') + "/.ssh/" + name
    call(["ssh-keygen", "-f", name, "-N", ""])
    return name


########################################################################################################################
#
# TEST
#
def action_test(name):
    out("Testing the alias")
    response = call(["ssh", '-oBatchMode=yes', name, "#"])
    if response == 0:
        out("Success")
        return True
    out("Failure")
    return False


########################################################################################################################
#
# DELETE
#
def action_delete(name):
    start = "##<---" + name + "---\n"
    stop = "\n##---" + name + "--->"
    new_config = re.sub(start + ".*?" + stop, "", get_data(), flags=re.DOTALL)
    if not new_config:
        out("SSH config record %s not found" % name)
    else:
        out("Removing %s SSH config record" % name)
        write_data(new_config.strip())


########################################################################################################################
#
# LIST
#
def action_list():
    data = get_data()
    if data == "":
        out("No hosts found")
        sys.exit(1)
    list = data.split("##<---")
    for k in list:
        for i in k.split("\n"):
            i = i.strip()
            if not i or "---" in i:
                continue
            if "Host " in i:
                alias = i.split(" ")[1]
                continue
            if "User " in i:
                user = i.split(" ")[1]
            if "HostName" in i:
                host = i.split(" ")[1]
            if "Identity" in i:
                id = i.split(" ")[1]
                msg = "     %s@%s (%s)" % (user, host, id)
                out("[%s]" % alias)
                out(msg)
                out("")
    sys.exit(1)


########################################################################################################################
#
# CONNECT
#
def action_connect(name):
    if not exists(name):
        out("Unable to find alias %s" % name)
        action_add(name)
    out("Connecting to %s" % name)
    call(["ssh", name])
    out("Connection closed")


########################################################################################################################
#
# INIT
#
def init_datastore():
    if not os.path.exists(os.path.expanduser('~') + "/.ssh"):
        print "Setting up kssh datastore.."
        os.makedirs(os.path.expanduser('~') + "/.ssh")
    if not os.path.exists(os.path.expanduser('~') + "/.ssh/config"):
        f = open(os.path.expanduser('~') + "/.ssh/config", 'w')
        f.write("")
        f.close()


########################################################################################################################
#
# EXISTS
#
def exists(name):
    start = "##<---" + name + "---\n"
    if start not in get_data():
        return False
    return True


########################################################################################################################
#
# WRITE
#
def write_data(data):
    f = open(os.path.expanduser('~') + "/.ssh/config", 'w')
    f.write(data)
    f.close()


########################################################################################################################
#
# READ
#
def get_data():
    with open(os.path.expanduser('~') + "/.ssh/config") as f:
        return f.read()


########################################################################################################################
#
# OUTPUT
#
def out(message):
    print "\033[1mkSSH : \033[0m \033[95m%s\033[0m" % (message)


########################################################################################################################
#
# CONFIG
#
def get_data_key(key):
    vals = []
    lines = get_data().split("\n")
    for k in lines:
        k = k.strip()
        if k.startswith(key + " "):
            vals.append(k.split(" ")[1])
    return vals


########################################################################################################################
#
# COMPLETE
#
def complete_hosts(text, state):
    for a in get_data_key("HostName"):
        if text in a:
            if not state:
                return a
            else:
                state -= 1


########################################################################################################################
#
# COMPLETE
#
def complete_users(text, state):
    for a in get_data_key("User"):
        if text in a:
            if not state:
                return a
            else:
                state -= 1


########################################################################################################################
#
# COMPLETE
#
def complete_keys(text, state):
    files = os.listdir(os.path.expanduser('~') + "/.ssh/")
    for a in files:
        if text in a:
            if not state:
                return a
            else:
                state -= 1


########################################################################################################################
#
# COMPLETE
#
def complete_aliases(text, state):
    for a in get_data_key("Host"):
        if text in a:
            if not state:
                return a
            else:
                state -= 1


########################################################################################################################
#
# COMPLETE
#
def complete_launcher(text, state):
    for a in actions:
        if text in a:
            if not state:
                return a
            else:
                state -= 1


########################################################################################################################
#
# BOOTSTRAP
#
if __name__ == "__main__":
    main()
