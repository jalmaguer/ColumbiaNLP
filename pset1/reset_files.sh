# script to to get rid of any of the files created by generate_files.sh
# and reset the project directory

if [ -f gene.counts ]; then
    echo "Removing gene.counts"
    rm gene.counts
fi

if [ -f rare.train ]; then
    echo "Removing rare.train"
    rm rare.train
fi

if [ -f rare.counts ]; then
    echo "Removing rare.counts"
    rm rare.counts
fi

if [ -f rare_classes.train ]; then
    echo "Removing rare_classes.train"
    rm rare_classes.train
fi

if [ -f rare_classes.counts ]; then
    echo "Removing rare_classes.counts"
    rm rare_classes.counts
fi

if [ -f gene_dev.p1.out ]; then
    echo "Removing gene_dev.p1.out"
    rm gene_dev.p1.out
fi

if [ -f gene_dev.p2.out ]; then
    echo "Removing gene_dev.p2.out"
    rm gene_dev.p2.out
fi

if [ -f gene_dev.p3.out ]; then
    echo "Removing gene_dev.p3.out"
    rm gene_dev.p3.out
fi