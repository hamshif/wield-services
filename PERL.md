
IntelliJ IDEA

1. preferences >> plugins >> Install perl plugin 
   restart and wait a long time until indexing finishes
1. preferences >> editor >> file types >> associate Perl with file type '*.pl' wildcard 
1. Checkout docker support


To enable debugger in intelliJ

```
cpan -i Bundle::Camelcade
cpan -i common::sense
cpan -i Types::Serialiser
```



Installing libraries on Catalina
-
make sure terminall has access in mac preferences

```
brew install libgd
perlbrew switch <version>
cpan (--force) install Try::Tiny
cpan (--force) install Tk



```