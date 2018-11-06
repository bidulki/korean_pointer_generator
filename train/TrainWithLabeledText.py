import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing import text, sequence
from model.base_seq2seq import seq2seq


def make_target_input(target):
    target = [x[:-1] for x in target]
    return target


def make_target_output(target):
    target = [x[1:] for x in target]
    return target


def make_onehot_target(target, num_token):
    out = []
    for i, x in enumerate(target):
        x = np.array(x) - 1
        out.append(np.eye(num_token)[x])
    return out


# input sequence length
# seq_len = [len(x) for x in txt]
# print('mean of input sequence length: ', np.mean(seq_len))  # 756.1045454545455
# print('max of input sequence length: ', np.max(seq_len))  # 7959
# print('min of input sequence length: ', np.min(seq_len))  # 73
# need dynamic rnn!!

# revert example: sequence to text
# t_summ.sequences_to_texts(summ[:2])


if __name__ == '__main__':
    text_morph = np.load('text.npy').tolist()
    summary_morph = np.load('summary.npy').tolist()

    # make sequence: text
    t_txt = text.Tokenizer(filters='')
    t_txt.fit_on_texts(text_morph)
    txt = t_txt.texts_to_sequences(text_morph)

    # make sequence: summary
    t_summ = text.Tokenizer(filters='')
    t_summ.fit_on_texts(summary_morph)
    summ = t_summ.texts_to_sequences(summary_morph)

    # make summary output dataset
    summ_input = make_target_input(summ)
    summ_output = make_target_output(summ)

    # make onehot summary output
    summ_output = make_onehot_target(summ_output, num_token=len(t_summ.index_word))

    # to np.array
    txt = np.array(txt)
    summ_input = np.array(summ_input)
    summ_output = np.array(summ_output)

    # model
    model = seq2seq(num_encoder_tokens=len(t_txt.index_word), embedding_dim=64,
                    hidden_dim=128, num_decoder_tokens=len(t_summ.index_word))
    summaryModel = model.get_model()
    summaryModel.compile(optimizer='Adam', loss='categorical_crossentropy')
    summaryModel.fit([txt, summ_input], np.array(summ_output),
                     batch_size=1, epochs=2, validation_split=0.1)