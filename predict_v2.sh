export CUDA_VISIBLE_DEVICES=2
export PYTHONPATH=/root/biatNovo-DDA:$PYTHONPATH
python v2/main.py --search_denovo --train_dir /root/v2/dda_sb_transformer_independent_shuffle
