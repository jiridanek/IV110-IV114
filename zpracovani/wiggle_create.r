data = scan(file="regulees.txt")

d = density(data, kernel="b", from=1, to=4639675, n=463967, adjust=0.1)

library(signal)
start = 1
end = 4639675
step = 100

values = interp1(d$x, d$y, seq(start,end,step))

f = file("regulees.gff", open="w")
#write(paste("fixedStep chrom=NC_000913 start=0 step=", step, sep=""), file=f, append=TRUE)
#write(as.character(values), f, append=TRUE)
write("##gff-version   3", f, append=TRUE)
i = 1
for (v in values) {
	write(paste("NC_000913","EcoCyc","microarray_oligo",format(i,scientific=FALSE),format(i+step,scientific=FALSE),format(v*1e08,scientific=FALSE),".",".","Name=Expt1", sep="\t"), file=f, append=TRUE)
	i = i+step
}
close(f)

data = scan(file="regulators.txt")

d = density(data, kernel="b", from=1, to=4639675, n=463967, adjust=0.1)

library(signal)
start = 1
end = 4639675
step = 100

values = interp1(d$x, d$y, seq(start,end,step))

f = file("regulators.gff", open="w")
#write(paste("fixedStep chrom=NC_000913 start=0 step=", step, sep=""), file=f, append=TRUE)
#write(as.character(values), f, append=TRUE)
write("##gff-version   3", f, append=TRUE)
i = 1
for (v in values) {
	write(paste("NC_000913","EcoCyc","microarray_oligo",format(i,scientific=FALSE),format(i+step,scientific=FALSE),format(v*1e08,nsmall=5,scientific=FALSE),".",".","Name=Expt2", sep="\t"), file=f, append=TRUE)
	i = i+step
}
close(f)

# glyph     = xyplot
# graph_type     = line
# bgcolor   = red
# fgcolor   = red
# label     = 1
# stranded  = 1
# connector = solid
# balloon hover = $description
# group_on       = display_name
# category    = Custom Tracks:regulees.wiggle
# key         = microarray_oligo:EcoCyc
# show summary = 0