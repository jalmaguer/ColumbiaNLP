# script to to run all of the python scripts in the project and generate any files
# that haven't already been generated

if [ -f cfg.counts ]; then
    echo "cfg.counts already exists"
else
    echo "generating cfg.counts"
    python count_cfg_freq.py parse_train.dat > cfg.counts
fi

if [ -f rare.train ]; then
    echo "rare.train already exists"
else
    echo "generating rare.train"
    python replace_rare.py parse_train.dat > rare.train
fi

if [ -f parse_train.counts.out ]; then
    echo "parse_train.counts.out already exists"
else
    echo "generating parse_train.counts.out"
    python count_cfg_freq.py rare.train > parse_train.counts.out
fi

if [ -f parse_dev.out ]; then
    echo "parse_dev.out already exists"
else
    echo "generating parse_dev.out"
    python parser.py parse_train.counts.out parse_dev.dat > parse_dev.out
fi

echo
echo "Parser results:"
python eval_parser.py parse_dev.key parse_dev.out