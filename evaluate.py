from sklearn.metrics import accuracy_score
class Evaluator(object):
    def __init__(self):
        self.score=None
        self.accumualted_score=0

    def evaluate(self,original,generated):
        min_len= min(len(original),len(generated))
        accuracy = accuracy_score(y_true=generated[:min_len], y_pred=original[:min_len])
        # print(f'original : {len(original)}')
        # print(f'generated : {len(generated)}')
        # print(f'original : {original}')
        # print(f'generated : {generated}')
        print(f'accuracy : {accuracy*100 }%')
        self.accumualted_score+=accuracy