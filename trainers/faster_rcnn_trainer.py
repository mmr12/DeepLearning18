import numpy as np
from tqdm import tqdm

from base.base_train import BaseTrain


class FasterRcnnTrainer(BaseTrain):
    def __init__(self, sess, model, data, config,logger):
        super(FasterRcnnTrainer, self).__init__(sess, model, data, config,logger)

    def train_epoch(self):
        loop = tqdm(range(self.config.num_iter_per_epoch))
        losses = []
        accs = []
        for _ in loop:
            loss, acc = self.train_step()
            losses.append(loss)
            accs.append(acc)
        loss = np.mean(losses)
        acc = np.mean(accs)

        cur_it = self.model.global_step_tensor.eval(self.sess)
        summaries_dict = {
            'loss': loss,
            'acc': acc,
        }
        self.logger.summarize(cur_it, summaries_dict=summaries_dict)
        self.model.save(self.sess)

    def train_step(self):  # hello!
        batch_x, batch_y = next(self.data.next_batch())
        feed_dict = {self.model.x: batch_x,
                     self.model.class_y: batch_class_y,
                     self.model.reg_y: batch_reg_y,
                     self.model.is_training: True}
        _, loss, acc = self.sess.run([self.model.train_step, self.model.cross_entropy, self.model.accuracy],
                                     feed_dict=feed_dict)
        return loss, acc