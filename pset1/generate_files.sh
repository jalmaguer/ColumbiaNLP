echo "generating gene.counts"
python count_freqs.py gene.train > gene.counts

echo "generating rare.train"
python replace_rare.py gene.train > rare.train

echo "generating rare.counts"
python count_freqs.py rare.train > rare.counts

echo "running simple tagger"
python simple_tagger.py rare.counts gene.dev > gene_dev.p1.out