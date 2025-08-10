# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.

# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>


# Unset irrelevant variables.
deactivate nondestructive

setenv VIRTUAL_ENV /home/ing/FOUR_horsemen/ALPHA_FOUR/proto_oanda/wolfpack-lite/venv

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/"bin":$PATH"


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
    set prompt = '(venv) '"$prompt"
    setenv VIRTUAL_ENV_PROMPT '(venv) '
endif

alias pydoc python -m pydoc

rehash
