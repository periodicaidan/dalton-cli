![Dalton-CLi](./dalton_cli_logo.png)

![Version 0.1.0-beta](https://img.shields.io/badge/version-0.1.0%20beta-F44336.svg)
![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)

**Dalton-CLi** is a command line utility to make doing stoichiometry a little less tedious.

## About

Chemistry is so amazingly fascinating, but the sheer amount repetitive, tedious calculation can kill interest and bog
down anyone's workflow. The worst offender of this is stoichiometry: calculating molecular weights, mole ratios, and
so forth.

**Dalton-CLi** exists to ameliorate this. It is a simple but useful command line utility that does much of the math for
for. You don't even need to look at a periodic table, just type in the molecular formula of the compound you're working
with and in less than a second you have its molecular weight, no matter how complicated or obscure it may be.

So what makes **Dalton-CLi** better than a simple Google search? Well for starters, **Dalton-CLi** doesn't require an
Internet connection. Once installed, it's completely local to your machine. You only need Wi-Fi to get updates. But
beyond that, **Dalton-CLi** is highly personalizable. You can define custom chemical symbols for groups you find
yourself using a lot, save chemical formulas on disk for easy access and quick reference (perfect for when you have to
look up the same compound over and over again), and generate theoretical mass spectra for any compound you can imagine.
And as an ongoing open-source project, **Dalton-CLi** is just going to make your chemistry studies easier and easier.

## Installation
**Dalton-CLi** is written in Python with [Click](https://click.palletsprojects.com/en/7.x/), so you can install it
using pip.

```bash
$ pip install dalton-cli
```

If you do not have pip, you can read how to download it [here](https://pip.pypa.io/en/stable/installing/).

You may also clone the GitHub repo, but this is not recommended.

```bash
$ git clone https://github.com/periodicaidan/dalton-cli
```

I am working on a way to install this through Homebrew, APT, and so forth

**Dalton-CLi** requires a Python interpreter run. For Macintosh users, you've no need to install anything as
**Dalton-CLi** will run just fine on the interpreter shipped with every Apple computer.
For everyone else, you can install the latest version of Python [here](https://www.python.org/downloads/).

## Using Dalton-CLi
When you install **Dalton-CLi**, you can view the home page simply by running

```bash
$ dalton
```

This will show you a "splash page" of sorts, and give you a rundown of everything **Dalton-CLi** can do.

### `calc` — Get the Molar Mass of a Compound

The most basic command in **Dalton-CLi** is the `calc` command.

```bash
$ dalton calc H2O
18.015 g/mol
```
You give `calc` a molecular formula and **Dalton-CLi** will instantly give you the molecular weight of the compound you 
entered.

In the current version of **Dalton-CLi**, `calc` can handle *one level of parentheses*. Additionally, formulas
containing parentheses must be placed between quotation marks or the parentheses must be escaped with backslashes.

```bash
$ dalton calc 'O(C2H5)2'  # Correct
74.123 g/mol  # The correct molar weight of diethyl ether

$ dalton calc O\(C2H5\)2  # Using escape sequences
74.123 g/mol

$ dalton calc "O((CH2)2H)2"  # Nesting unsupported
45.061 g/mol  # Incorrect molar weight

$ dalton calc O(C2H5)2  # Parentheses seen as bash tokens
-bash: syntax error near unexpected token `('  # An error
```

`calc` has several options for analyzing chemical formulas. Modifying it with the `-M` or `--mass-spec` flag will print
a theoretical mass spectrum for the compound.

```bash
$ dalton calc C2H5OH --mass-spec
   C : 52.1%
   H : 13.1%
   O : 34.7%

$ dalton calc -M NaHSO4
  Na : 19.1%
   H : 0.8%
   S : 26.7%
   O : 53.3%
```

### `moiety` — Custom Chemical Symbols

Chemical formulas often become long and confusing, so chemists often come up with abbreviations for common *moieties*, 
or groups of atoms in a molecule that are considered as a unit. One of **Dalton-CLi**'s key features is to allow users
to define their own moieties with the `moiety` command.

To define a new moiety, you use the `--add` or `-a` flag, followed by the symbol for your moiety and then the group that
the symbol represents. To demonstrate, one often sees the group C2H5 (ethyl) in chemistry, so we often abbreviate it "Et". 
If we would like to calculate the molecular weight of ethanol by simply saying `dalton calc EtOH`, we would do it as 
follows:

```bash
$ dalton moiety --add Et C2H5  # Define an ethyl moiety
Et added to moiety profile (mass: 29.062 g/mol)

$ dalton calc EtOH
46.069 g/mol  # Correct molar mass of ethanol
```

And the great thing about **Dalton-CLi** is that it will treat these custom moieties, more or less, as their own
entities. So if we would like to get the molecular weight of diethyl ether (which earlier was long and required
specific formatting because of the parentheses), we can now simply say:

```bash
$ dalton calc Et2O
74.123 g/mol
```

Note that the way **Dalton-CLi** parses chemical formulas requires you to begin your moieties with a capital letter. If
you would like to use all lowercase letters, you must wrap the symbol in parentheses (which is good practice anyway,
as it confuses a human as much as it will confuse the parser).

But **Dalton-CLi** lets you do far more with moieties than simply create them. Say that you wanted to add a phenyl
(C6H5, a ring structure) group to your moiety profile, but you made a mistake and entered it in with one too many
hydrogen atoms.

```bash
$ dalton moiety -a Ph C6H6  # Whoops! That's benzene, not phenyl
Ph added to user profile (mass: 78.114 g/mol)  # ~1 gram too heavy
```

Never fear! Simply use the `--change` or `-c` flag to edit an already-registered moiety.

```bash
$ dalton moiety --change Ph C6H5
Changed value of Ph to C6H5 (77.106 g/mol)
```

We all forget things, [even very basic things](https://twitter.com/jobium/status/1036670558539112448?lang=en). Maybe
you've forgotten whether you registered a moiety, or what abbreviation you gave it, or maybe you accidentally
registered the same moiety under two different names. You can pull up a list of all the moieties you've added using the
`--list` or `-l` flag. By default it just shows you the symbol and its mass, but you can view the moiety as well in a
table format with the `--verbose` or `-v` flag.

```bash
$ dalton moiety --list
        Et :     29.062
        Ph :     77.106

$ dalton moiety -lv
MOIETY  | EQUIVALENT FORMULA |       MASS
-----------------------------------------
     Et |               C2H5 |     29.062
     Ph |               C6H5 |     77.106
```

To round out `moiety`'s CRUD functionality, you can use the `--delete` or `-d` flag to delete a moiety.

```bash
$ dalton moiety --delete Ph
Removed Ph from user moieties

$ dalton moiety -l
        Et :     29.062
```

**Dalton-CLi** stores the user moieties in a `user_moieties.yml` file. So even if you log out of your terminal session
or shut down your computer, the moieties you've registered will persist until you delete them.

**Dalton-CLi** ships with several common moieties to get you started, such as ethyl (Et), phenyl (Ph), pyridinium (Pym),
and cyclohexane (Chxn), just to name a few. But of course, if you'd like to start with a clean slate, you may do so by 
issuing `dalton moiety --delete-all`.

### `hist` — Cache Common Compounds

Python requires a lot of computational overhead, and parsing chemical formulas requires a bit of work. So calculating
the same formula over and over again can get annoying (I myself frequently forget the molar mass of water). So
**Dalton-CLi** gives you the option to cache formulas using the `hist` command.

```bash
$ dalton hist --save H2O
H2O saved in user history (mass: 18.015)

$ dalton hist --list
       H2O :      18.015

$ dalton calc H2O
18.015  # Dalton-CLi checks your history before trying to calculate the molecular weight
```

### `opts` — Access and Set User Options

**Dalton-CLi** comes with what I believe are sensible default settings for things like deciding how many significant
figures to output, whether or not history should be cleared after a while, and so on.

But of course, everyone's needs are different, so **Dalton-CLi** comes with several configurable options.

To view the current option configuration, use the `--show-all` flag.

```bash
$ dalton opts --show-all
mass precision : 3
mass-spec precision : 1
units : g/mol
```

By default, **Dalton-CLi** reports 3 places of precision for each molecule. This is good enough for most applications
and doesn't look too unappealing. But if you require more or less precision, you can set the number of decimal places
using the `--sig-figs` option.

```bash
$ dalton calc H3PO4
97.994

$ dalton opts --sig-figs=5
Molecular weights will be reported to 5 decimal places

$ dalton calc H3PO4
97.99376
```

Although Python allows for up to 17 places of precision, you can only set `sig-figs` to between 0 and 10, since no
element on **Dalton-CLi**'s periodic table has a mass more precise than 10 decimal places.

A similar option exists for setting the precision of percentages output by `calc --mass-spec`:
`--mass-spec-precision`. This command gives you one decimal place of precision by default.

```bash
$ dalton calc -M H2CO3
   H : 3.3%
   C : 19.4%
   O : 77.4%

$ dalton opts --mass-spec-precision=3
Mole ratios will be reported to 3 decimal places

$ dalton calc -M H2CO3
   H : 3.250%
   C : 19.365%
   O : 77.385%
```

Although it would have been very apropos for **Dalton-CLi** to report molecular weight as daltons, I have chosen simply 
to let it report it as grams-per-mole (g/mol) by default. This is simply the unit chemists use on a daily basis, 
and is much more clearly understood. If you would prefer that **Dalton-CLi** report units as daltons (maybe you're in 
biology, where reporting in daltons is more common), you may set it with the `--use-daltons` flag, and set it to 
grams-per-mole with `--use-gpm`.

```bash
$ dalton -opts --use-daltons
Units for molecular weight will be reported in daltons (Da)

$ dalton calc C10H13N5O4  # adenosine
267.245 Da

$ dalton opts --use-gpm
Units for molecular weight will be reported in grams-per-mole (g/mol)

$ dalton calc C10H13N5O4
267.245 g/mol
```

If you would ever like to restore the default configuration of all these options at once, you can use the
`--resotre-defaults` flag.

```bash
$ dalton opts --restore-defaults
All settings overwritten with default settings
```

### `update` — Get Newer Versions of Dalton-CLi

**Dalton-CLi** is always a work in progress. I'm always thinking of ways to make doing stoichiometry easier and less
tedious for chemists and chemistry students alike. So to make sure you have the latest version, you can run
`dalton update`.

**Dalton-CLi** will inform you whenever an update is available.

## Citation
You need not cite me or my program as a source of data, any more than you need to cite your calculator for the 
calculations you might do out by hand without **Dalton-CLi**. (If you are a student, you may want to avoid citing it or 
using it, as it may hinder your learning if you're new and your teacher may dock ponts.) However, I certainly welcome
and appreciate acknowledgement for my work :)

If you do wish to cite my program, unfortunately there is no standard way of citing a GitHub repository. One way to do 
it that would satisfy me personally would be:

- Bibliography: Manning, A.T. (2018). *Dalton-CLi*. Version \<the version you're using>. Austin, TX. 
GitHub repository, https://github.com/periodicaidan/dalton-cli\. Commit, \<hash of the commit you are using>. 
- Inline: (Manning, 2018)

To get the version and commit number, issue the command `dalton --version`.

There is a way of generating a DOI for a GitHub repo; if and when this application takes off I will get a DOI and change
this section.

## License
Copyright 2018 Aidan T. Manning

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.