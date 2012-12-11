IV110-IV114
===========

- fcgibubliny - fcgi program v go; zobrazuje bubliny do GBrowse
- zpracovani - skripty v pythonu; příprava dat pro ty bubliny

##složka zpracovani

- load_dat.py je načítadlo pro formát .dat; zatím není na nic potřeba
- ve složce test jsou zkrácená data která používá genes_col.py a load_dat.py pokud se pustí přímo. Slouží k otestování že to dělá co má.

###generegulation.json
> python func_associations_3_toJSON.py > generegulation.json

reads data/genes.col and data/func_associations_3.col

###genes.gff
>python genes.col_print_GFF.py > genes.gff

- genes_col.py je soubor který ty předchozí dva importují

###regulators.gff & regulees.gff
>python wiggle_prepare.py
>R -f wiggle_create.r

reads data/genes.col and data/func_associations_3.col,
creates also intermediate files regulators.txt and regulees.txt

#složka fcgibubliny

##instalace go
http://golang.org/ respektive http://golang.org/doc/install

##kompilace programu
ve slozce fcgibubliny dát `go build fcgibubliny.fcgi.go`

##spušteni
- nakopírovat fcgibubliny.fcgi do složky /var/www/cgi-bin
- otevřít http://localhost/cgi-bin/fcgibubliny.fcgi?gene=nazev_genu ve webovém prohlížeči
- (program není možné spustit samostatně, musí to být přes webový server)