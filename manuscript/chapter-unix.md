###A Crash Course in UNIX-based Commands


####Using the Terminal
------------------

In order to set up your environment learning how to use the *Command
Line Interpreter (CLI)* provided by your Operating System is really
important. Through the course of this tutorial, you will be interacting
with the CLI routinely. If you are already familiar with using the
command line interface you can skip directly to
Installing the Software \<installing-software\> section.

UNIX-based operating systems all use a similar-looking
[terminal](http://www.ee.surrey.ac.uk/Teaching/Unix/unixintro.html).
Descendants, derivatives and clones of UNIX include [Apple's OS
X](http://en.wikipedia.org/wiki/OS_X) and the [many available Linux
distributions](http://en.wikipedia.org/wiki/List_of_Linux_distributions)
available today. All of these operating systems contain a core set of
commands which help you navigate through your filesystem and launch
programs, all without the need of any graphical interface. This section
provides the key commands you should familiarise yourself with.

> **note**
>
> This tutorial is focused towards users of UNIX-based or UNIX-derived
> operating systems. While Python and Django can run in a Windows-based
> environment, many of the commands that we use in this book are for
> UNIX-based terminals. These commands can however be replicated in
> Windows by using the graphical user interface, [using the relevant
> command in a Windows Command
> Prompt](http://www.ai.uga.edu/mc/winforunix.html), or using [Windows
> PowerShell](http://technet.microsoft.com/en-us/library/bb978526.aspx)
> which provides an CLI like similar to a UNIX terminal.



Upon launching a new terminal instance, you'll typically be presented with something like:

```
sibu:~ leif$

```

This is called the *prompt*, and indicates when the system is waiting to
execute your every command. The prompt you see varies depending on the
operating system you are using, but all look generally very similar. In
the example above, there are three key pieces of information to observe:

-   your username and computer name (username of `leif` and computer
    name of `sibu`);
-   your *current working directory* (the tilde, or `~`); and
-   the privilege of your user account (the dollar sign, or `$`).

The dollar sign (`$`) typically indicates that the user is a standard
user account. Conversely, a hash symbol (`#`) may be used to signify the
user logged in has [root
privileges](http://en.wikipedia.org/wiki/Superuser). Whatever symbol is
present is used to signify that the computer is awaiting your input.

Open up a terminal window and see what your prompt looks like.

When you are using the terminal, it is important to know where you are
in the file system. To find out where you are, you can issue the command
`pwd`. This will display your present working directory. For example,
check the example terminal interactions below.


```
Last login: Mon Sep 23 11:35:44 on ttys003
sibu:~ leif$ pwd
/Users/leif
sibu:~ leif$
```

You can see that the present working directory in this example is:

`/Users/leif`.

You'll also note that the prompt indicates that my present working
directory is \~. This is because the tilde (`~`) represents your *home
directory*. The base directory in any UNIX-based file system is the
*root directory*. The path of the root directory is denoted by a single
forward slash (`/`).

If you are not in your home directory you can change directory (`cd`) to
your home directory by issuing the following command.


```
$ cd ~
```


Let's create a directory called `code`. To do thus, use the make
directory command (`mkdir`), as shown below.


```
$ mkdir code
```

To move to the newly-created `code` directory, enter `cd code`. If you
now check your current working directory, you'll notice that you will be
in `~/code/`. This may also be reflected by your prompt. Note in the
example below that the current working directory is printed after the `sibu` computer name.

> **note**
>
> Whenever we refer to `<workspace>`, we'll be referring to your `code` directory.


```
sibu:~ leif$ mkdir code
sibu:~ leif$ cd code
sibu:code leif$
sibu:code leif$ pwd
/Users/leif/code
```

To list the files that are in a directory, you can issue the command
`ls`. You can also see hidden files or directories - if you have any -
you can issue the command `ls -a`, where `a` stands for *all.* If you
`cd` back to your home directory (`cd ~`) and then issue `ls`, you'll
see that you have something called `code` in your home directory.

To find out a bit more about what is in your directory, issue `ls -l`.
This will provide a more detailed *listing* of your files and whether it
is a directory or not (denoted by a `d` at the start of the line).


```
sibu:~ leif$ cd ~
sibu:~ leif$ ls -l

drwxr-xr-x   36 leif  staff    1224 23 Sep 10:42 code
```

The output also contains information on the [permissions associated to
the
directory](http://www.elated.com/articles/understanding-permissions/),
who created it (`leif`), the group (`staff`), the size, the date/time
the file was modified at, and, of course, the name.

You may also find it useful to be able to edit files within your
terminal. There are many editors which you can use - some of which may
already be installed on your computer. The
[nano](http://www.nano-editor.org/) editor for example is a
straightforward editor - unlike [vi](http://en.wikipedia.org/wiki/Vi)
which can take some time to learn. Below are a list of commonly-used
UNIX commands that you will find useful.

### Core Commands

All UNIX-based operating systems come with a series of built-in
commands - with most focusing exclusively on file management. The
commands you will use most frequently are listed below, each with a
short explanation on what they do and how to use them.

-   `pwd`: *Prints* your current *working directory* to the terminal.
    The full path of where you are presently is displayed.
-   `ls`: Prints a list of files in the current working directory to the
    terminal. By default, you do not see the sizes of files - this can
    be achieved by appending `-lh` to `ls`, giving the command `ls -lh`.
-   `cd`: In conjunction with a path, allows you to *change* your
    current working *directory*. For example, the command
    `cd /home/leif/` changes the current working directory to
    `/home/leif/`. You can also move up a directory level without having
    to provide the [absolute
    path](http://www.uvsc.edu/disted/decourses/dgm/2120/IN/steinja/lessons/06/06_04.html)
    by using two dots, e.g. `cd ..`.
-   `cp`: Copies files and/or directories. You must provide the *source*
    and the *target*. For example, to make a copy of the file `input.py`
    in the same directory, you could issue the command
    `cp input.py input_backup.py`.
-   `mv`: Moves files/directories. Like `cp`, you must provide the
    *source* and *target*. This command is also used to rename files.
    For example, to rename `numbers.txt` to `letters.txt`, issue the
    command `mv numbers.txt letters.txt`. To move a file to a different
    directory, you would supply either an absolute or relative path as
    part of the target - like `mv numbers.txt /home/david/numbers.txt`.
-   `mkdir`: Creates a directory in your current working directory. You
    need to supply a name for the new directory after the `mkdir`
    command. For example, if your current working directory was
    `/home/david/` and you ran `mkdir music`, you would then have a
    directory `/home/david/music/`. You will need to then `cd` into the
    newly created directory to access it.
-   `rm`: Shorthand for *remove*, this command removes or deletes files
    from your filesystem. You must supply the filename(s) you wish to
    remove. Upon issuing a `rm` command, you will be prompted if you
    wish to delete the file(s) selected. You can also remove directories
    [using the recursive
    switch](http://www.computerhope.com/issues/ch000798.htm). Be careful
    with this command - recovering deleted files is very difficult, if
    not impossible!
-   `rmdir`: An alternative command to remove directories from your
    filesystem. Provide a directory that you wish to remove. Again, be
    careful: you will not be prompted to confirm your intentions.
-   `sudo`: A program which allows you to run commands with the security
    privileges of another user. Typically, the program is used to run
    other programs as `root` - the
    [superuser](http://en.wikipedia.org/wiki/Superuser) of any
    UNIX-based or UNIX-derived operating system.

> **note**
>
> This is only a brief list of commands. Check out ubuntu's
> documentation on [Using the
> Terminal](https://help.ubuntu.com/community/UsingTheTerminal) for a
> more detailed overview, or the \`Cheat Sheet

> \<<http://fosswire.com/post/2007/08/unixlinux-command-cheat-sheet/>\>\`\_
> by FOSSwire for a quick reference guide.
