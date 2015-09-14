# script to to run all of the python scripts in the project and generate any files
# that haven't already been generated

if [ -f gene.counts ]; then
    echo "gene.counts already exists"
else
    echo "generating gene.counts"
    python count_freqs.py gene.train > gene.counts
fi

if [ -f rare.train ]; then
    echo "rare.train already exists"
else
    echo "generating rare.train"
    python replace_rare.py gene.train > rare.train
fi

if [ -f rare.counts ]; then
    echo "rare.counts already exists"
else
    echo "generating rare.counts"
    python count_freqs.py rare.train > rare.counts
fi

if [ -f rare_classes.train ]; then
    echo "rare_classes.train already exists"
else
    echo "generating rare_classes.train"
    python replace_rare_classes.py gene.train > rare_classes.train
fi

if [ -f rare_classes.counts ]; then
    echo "rare_classes.counts already exists"
else
    echo "generating rare_classes.counts"
    python count_freqs.py rare_classes.train > rare_classes.counts
fi

if [ -f gene_dev.p1.out ]; then
    echo "gene_dev.p1.out already exists"
else
    echo "running simple tagger"
    python simple_tagger.py rare.counts gene.dev > gene_dev.p1.out
fi

if [ -f gene_dev.p2.out ]; then
    echo "gene_dev.p2.out already exists"
else
    echo "running trigram tagger"
    python trigram_tagger.py rare.counts gene.dev > gene_dev.p2.out
fi

if [ -f gene_dev.p3.out ]; then
    echo "gene_dev.p3.out already exists"
else
    echo "running trigram tagger with classes"
    python trigram_tagger_classes.py rare_classes.counts gene.dev > gene_dev.p3.out
fi

echo
echo "Simple Tagger result:"
python eval_gene_tagger.py gene.key gene_dev.p1.out

echo
echo "Trigram Tagger result:"
python eval_gene_tagger.py gene.key gene_dev.p2.out

echo
echo "Trigram Tagger Classes result"
python eval_gene_tagger.py gene.key gene_dev.p3.out