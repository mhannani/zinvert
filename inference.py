from src.utils.inference import inference


if __name__ == "__main__":
    print('Doing inference ...')

    # example sentence from test data
    de_sentence = "Ein Boston Terrier läuft über saftig-grünes Gras vor einem weißen Zaun."

    target_sentence = inference(de_sentence)
    print(target_sentence)
