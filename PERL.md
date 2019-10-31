Perl Environment on Mac os Catalina

Install cpan cpanm and perlbrew
# TODO documentation

perlbrew install <your version> e.g. perl-5.14.4
perlbrew switch perl-5.14.4

IntelliJ IDEA
=

1. preferences >> plugins >> Install perl plugin 
   restart and wait a long time until indexing finishes
1. preferences >> editor >> file types >> associate Perl with file type '*.pl' wildcard 
1. Checkout docker support


-

Open project
=
The bellow is not elegant but works
* create new perl project on directory with project 
* add modules 
* mark lib dirs as perl lib, mark t as test etc.


To enable debugger in intelliJ
Hit debug button and when prompted to install use cpanm to install dependancies


Installing project specific GUI TK libraries on Catalina
-
make sure terminal has access in mac preferences

```
brew install libgd
brew install tcl-tk
echo 'export PATH="/usr/local/opt/tcl-tk/bin:$PATH"' >> ~/.zshrc
sudo gem install tk
```

For compilers to find tcl-tk you may need to set:
```
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
```

test ruby in file
```
 #!/usr/bin/env ruby
 require 'tk'
 root = TkRoot.new do
   title "Ruby/Tk Test"
 end
 Tk.mainloop
```

```
perlbrew switch 5.14.4
cpanm install Try::Tiny
cpam install YAML
cpanm install GD::Simple
cpanm install GD::Graph
```
Download and install XQuartz dmg
https://www.xquartz.org/
```
cpanm install Tk
```

to use GUI you need XQuartz to be running

Kafka
-
```
cpanm install Kafka::Connection
```