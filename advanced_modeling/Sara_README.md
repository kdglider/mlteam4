# Notes on the notebooks

- `Loading data & Testing BERT+LR_SE.ipynb`: run distillBert on our full merged data with a low sequence length. The attributes I merged where the title, author, leading comment and the reply comments.  
The best accuracy I have obtained is ~49%.
- `Tuning_params_multi_class_bert_SE.ipynb`: run Bert-base-uncased on our full merged data while fine tuning the parameters (`num_train_epochs`:[3,4], `max_seq_length`:[128, 256, 512], `train_val_test split`:[60/20/20, 80/10/10]). I only used the `Leading Comment` in this part.
The best accuracy I have obtained is ~70% with `epochs=4`, `max_seq_length=512`and `train_val_test split:80/10/10` .
- `DataPlayBook_multi_class_bert_v1_SE.ipynb`and v2: run Bert-base-uncased on our full merged data while first droping the categories (with their text) that had less than 250 data point. The accuracy has imrpoved by 0.01 which means it became ~71% with same parameters reported before.

Right now I augmented the data 5 times of the categories with less data points (below 250 sample) and I am training the model using the same parameters.
