# script to to get rid of any of the files created by generate_files.sh
# and reset the project directory

if [ -f cfg.counts ]; then
    echo "Removing cfg.counts"
    rm cfg.counts
fi

if [ -f rare.train ]; then
    echo "Removing rare.train"
    rm rare.train
fi

if [ -f parse_train.counts.out ]; then
    echo "Removing parse_train.counts.out"
    rm parse_train.counts.out
fi