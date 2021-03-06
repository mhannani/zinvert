import torch
from typing import List
from torchtext.data.utils import get_tokenizer
from torchtext.datasets import Multi30k
from torchtext.vocab import build_vocab_from_iterator
import json
from .config import *


class Vocabulary:
    """
    Builds and saves vocabulary for a language.
    """

    def __init__(self, freq_threshold=1):
        """
        The class constructor.
        :param dataset: dataset
        :param freq_threshold: int
            The frequency threshold for the processed.
        """

        self.freq_threshold = freq_threshold
        self.vocabulary = self.build_vocab()

    @staticmethod
    def get_tokenizer():
        """
        Get the spacy tokenizer for the lang language.
        :param lang: str
            'en' for English or 'de' for Dutch.
        :return: spacy.tokenizer
        """

        token_transform = {SRC_LANGUAGE: get_tokenizer('spacy', language=LANG_SHORTCUTS['de']),
                           TGT_LANGUAGE: get_tokenizer('spacy', language=LANG_SHORTCUTS['en'])}

        return token_transform

    def _get_tokens(self, data_iterator=None, lang='de'):
        """
        Get token for an iterator containing tuple of string
        :param lang: str
            'en' or 'de' for source and target languages.
        :return: List
            List of tokens.
        """
        tokenizer = self.get_tokenizer()
        for data_sample in data_iterator:
            yield tokenizer[lang](data_sample[LANGUAGE_INDEX[lang]])

    def build_vocab(self):
        """
        Build the processed of the given language.
        :return: List of Vocabs
        """
        vocabulary = {}
        # itos stoi
        for lang in [SRC_LANGUAGE, TGT_LANGUAGE]:
            data_iterator = Multi30k(root='../data/.data', split='train', language_pair=(SRC_LANGUAGE, TGT_LANGUAGE))
            vocabulary[lang] = build_vocab_from_iterator(self._get_tokens(data_iterator, lang),
                                                         min_freq=self.freq_threshold, specials=SPECIAL_SYMBOLS,
                                                         special_first=True)
            vocabulary[lang].set_default_index(vocabulary[lang]['<unk>'])

        return vocabulary

    @staticmethod
    def reverse_token_idx(tokens_idx: List):
        """
        Reverse a list of tokens indices
        :param tokens_idx: List
        :return: List
        """

        tokens_idx.reverse()
        return tokens_idx

    @staticmethod
    def tensor_transform(tokens_idx):
        """
        Builds the representation of numericalized sentence as Tensor.

        Input : A List, [12, 1, 6, 12, 200, 100] this a transformed sentence.
        (apply itos function to get the original text-based sentence).

        Output : The same input with EOS and SOS tensor concatenated
        respectively to the end and the beginning of the input tensor.

        :param tokens_idx: List
            A transformed sentence with indices of each token in it.

        :return: Tensor
            Sentence with SOS and EOS tokens added.
        """

        return torch.cat((
            torch.tensor([SOS_IDX]),
            torch.tensor(tokens_idx),
            torch.tensor([EOS_IDX])
        ))

    @staticmethod
    def pipeline(*transforms):
        """
        Make a pipeline of many transformation to the given input data.

        :param transforms: List
            List of transformation as arguments to the function
        :return: Function with transformation.
        """
        def shot(sentence):
            """
            Applies transformations as input.
            :param sentence:str
            :return: Tensor
                Input as Tensor
            """
            for transform in transforms:
                # print('transform: ', transform)
                sentence = transform(sentence)
                # print('sentence: ', sentence)
            return sentence

        return shot

    def postprocess(self, tensor, lang):
        """
        Postprocess a Tensor and get the corresponding text-based sentence from it.
        :return: str
            A sentence.
        """
        sentence = self.vocabulary[lang].lookup_tokens(tensor.tolist())
        return sentence

    def preprocess(self, inference=False):
        """
        Tokenize, numericalize and turn into tensor a sentence.

        :return: Dict
            The transformation to be applied to a text-based sentence.
        """

        sentence_transform = {}

        if inference:
            sentence_transform['de'] = self.pipeline(
                self.get_tokenizer()['de'],
                self.vocabulary['de'],
                self.tensor_transform
            )
        else:
            sentence_transform['de'] = self.pipeline(
                self.get_tokenizer()['de'],
                self.vocabulary['de'],
                self.reverse_token_idx,
                self.tensor_transform
            )

        sentence_transform['en'] = self.pipeline(
            self.get_tokenizer()['en'],
            self.vocabulary['en'],
            self.tensor_transform
        )

        return sentence_transform

    @staticmethod
    def _save_file(filename, data):
        """
        Saves data to a file
        :param filename: str
            Filename
        :param data:
        :return: None
        """
        # save the processed as json
        with open(filename, 'w') as f:
            json.dump(data, f)

    def save_vocabulary(self, lang=('de', 'en')):
        """
        Save processed to disk
        :return:
        """

        if 'en' not in lang and 'de' not in lang:
            raise ValueError('Not supported language(s) !')

        for language in lang:
            itos = self.vocabulary[language].get_itos()
            stoi = self.vocabulary[language].get_stoi()

            # save itos
            self._save_file(f'../data/processed/index_to_name_{language}', itos)

            # save stoi
            self._save_file(f'../data/processed/name_to_index_{language}', stoi)

    def __call__(self):
        """
        Call the function when instantiation.
        :return: Set
            Set of the processed of the two languages.
        """

        self.save_vocabulary()
