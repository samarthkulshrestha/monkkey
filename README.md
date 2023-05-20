# monkKey

a terminal-based, locally-stored, [AES](www.aes.com) encrypted password manager

### installation

since you're using a terminal-based password manager,
i expect that you know your way around things in the terminal.

if you don't, open a github issue :D

-   unix-based OSes (GNU+Linux/MacOS)

```
git clone https://github.com/samarthkulshrestha/monkkey.git ~/monkkey
cd ~/monkkey
pip install -r requirements.txt
```

then copy-paste the following in your `~/.bashrc` or `~/.zshrc` or your shell profile:

```
alias monkkey="python ~/monkkey/src/main.py"
```

replace `python` in the above line with whatever your python executable is (maybe `python3`)

then run:

```
source ~/.bashrc
```

replace `~/.bashrc` with your shell config (`~/.zshrc` if you're using zsh)

or just simply close and open your terminal again.

### usage

now that we have _monkKey_ installed, you can run it by running `monkkey`

monkkey will ask you to enter a new master password

```
enter new master password:
```

enter the desired password, and run monkKey again.
enter the password you entered earlier, you should be greeted with something like this:

```
welcome! type 'h' or 'help' and press enter for a help message

>
```

type `help` or `h` and press enter

here's the help message that is shown:

```
init    [in]            initalizes a new database, run this if this is the first time running this program
add     [a]             adds a new password
read    [r]             reads a password
update  [u]             updates a password
info    [i]             returns info associated with the password
master  [m]             changes the master password
help    [h]             shows this help message
```

type `init` and press enter.
you're basically done. read the help message, and start using _monkKey_!

:D

## Licence

Licensed under the **_do whatever the fuck you wanna do_** public licence.

(c) Samarth Kulshrestha, 2021
