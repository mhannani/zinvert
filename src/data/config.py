SRC_LANGUAGE = 'de'
TGT_LANGUAGE = 'en'
LANGUAGE_INDEX = {'de': 0, 'en': 1}
LANG_SHORTCUTS = {'en': 'en_core_web_sm', 'de': 'de_core_news_sm'}
UNK_IDX, PAD_IDX, SOS_IDX, EOS_IDX = 0, 1, 2, 3
SPECIAL_SYMBOLS = ['<unk>', '<pad>', '<sos>', '<eos>']

EMBEDDING_SIZE = 256
HIDDEN_DIM = 1024
DROPOUT = 0.5
N_LAYERS = 2
EPOCHS = 40
BATCH_SIZE = 256
TEACHER_FORCING_RATIO = 0.5

CHECKPOINT_PATH_WITHOUT_ATT = 'checkpoints/CHECKPOINT__EN__TO__DE__EPOCH_25__AT__2021_12_23__20_06_13__TRAIN_LOSS__2'
