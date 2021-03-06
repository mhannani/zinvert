import torch.nn as nn
from src.data.config import *


class Encoder(nn.Module):
    """
    The Encoder model.
    """

    def __init__(self, vocab_length, embedding_dim, hidden_dim, n_layers=N_LAYERS, dropout_prob=DROPOUT):
        """
        The class constructor.

        :param vocab_length: The vocabulary length
        :param embedding_dim: embedding dimension
        :param hidden_dim: hidden size dimension
        :param n_layers: number of layer in the encoder
        :param dropout_prob: dropout probability for applying dropout feature to avoid overfitting.
        """

        super().__init__()

        self.vocab_length = vocab_length
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.dropout_prob = dropout_prob

        # convert input tensor to nn.Embeddings with dimension supplied.
        # more info here: https://stackoverflow.com/questions/50747947/embedding-in-pytorch
        self.embedding = nn.Embedding(self.vocab_length, self.embedding_dim)

        # LSTM cell
        self.lstm = nn.LSTM(self.embedding_dim, self.hidden_dim, self.n_layers, dropout=dropout_prob)

        # dropout layer
        self.dropout = nn.Dropout(self.dropout_prob)

    def forward(self, batch):
        """
        Train the Encoder network.
        :param batch: A batch
        :return: hidden state, and cell
        """

        # Apply dropout to the embeddings
        # print('batch: ', batch)
        embed = self.dropout(self.embedding(batch))

        # Get the output from the LSTM (hidden state and cell state).
        outputs, (hidden, cell) = self.lstm(embed)

        return hidden, cell


class EncoderAttention(nn.Module):
    """
    The Encoder variant model for seq2seq with attention mechanism.
    """

    def __init__(self, vocab_length, embedding_dim, hidden_dim, n_layers=N_LAYERS, dropout_prob=DROPOUT):
        """
        The class constructor.

        :param vocab_length: The vocabulary length
        :param embedding_dim: embedding dimension
        :param hidden_dim: hidden size dimension
        :param n_layers: number of layer in the encoder
        :param dropout_prob: dropout probability for applying dropout feature to avoid overfitting.
        """

        super().__init__()

        self.vocab_length = vocab_length
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.dropout_prob = dropout_prob

        # convert input tensor to nn.Embeddings with dimension supplied.
        # more info here: https://stackoverflow.com/questions/50747947/embedding-in-pytorch
        self.embedding = nn.Embedding(self.vocab_length, self.embedding_dim)

        # GRU cell
        self.gru = nn.GRU(self.embedding_dim, self.hidden_dim, self.n_layers, dropout=dropout_prob)

        # dropout layer
        self.dropout = nn.Dropout(self.dropout_prob)

    def forward(self, batch):
        """
        Train the Encoder network.
        :param batch: A batch
        :return: hidden state, and cell
        """

        # Apply dropout to the embeddings
        embed = self.dropout(self.embedding(batch))

        # Get the output from the LSTM (hidden state and cell state).
        outputs, hidden = self.gru(embed)

        return outputs, hidden
