SRC_LANGUAGE = 'de'
TGT_LANGUAGE = 'en'
LANGUAGE_INDEX = {'de': 0, 'en': 1}
LANG_SHORTCUTS = {'en': 'en_core_web_sm', 'de': 'de_core_news_sm'}
UNK_IDX, PAD_IDX, SOS_IDX, EOS_IDX = 0, 1, 2, 3
SPECIAL_SYMBOLS = ['<unk>', '<pad>', '<sos>', '<eos>']

EMBEDDING_SIZE = 256
HIDDEN_DIM = 1024
DROPOUT = 0.5
N_LAYERS = 1
EPOCHS = 40
BATCH_SIZE = 256
TEACHER_FORCING_RATIO = 0.5

DEVICE = 'cpu'

CHECKPOINT_PATH_WITHOUT_ATT = 'checkpoints/WITHOUT_ATTENTION/CHECKPOINT_WITHOUT_ATT__DE__TO__EN__EPOCH_8__AT__2021_12_30__23_54_17__TRAIN_LOSS__2.pt'
CHECKPOINT_PATH_WITHOUT_ATT_JIT = 'checkpoints/WITHOUT_ATTENTION/JIT/JIT__WITHOUT_ATT_ATT__DE__TO__EN__EPOCH_8__AT__2021_12_30__23_54_17__TRAIN_LOSS__2.pt'

CHECKPOINT_PATH_WITH_ATT = 'checkpoints/ATTENTION_CHECKPOINTS/CHECKPOINT_WITH_ATT__DE__TO__EN__EPOCH_19__AT__2021_12_31__07_45_38__TRAIN_LOSS__1.pt'
CHECKPOINT_PATH_WITH_ATT_JIT = 'checkpoints/ATTENTION_CHECKPOINTS/JIT/JIT__WITH_ATT_ATT__DE__TO__EN__EPOCH_19__AT__2021_12_31__07_45_38__TRAIN_LOSS__1.pt'
