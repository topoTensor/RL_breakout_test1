# RL Breakout Test

This is my first prototype of an *evolutionary reinforcement learning model* for the game Breakout, built using PyTorch and Pygame. It is still a work in progress. The training process is sequential and implemented from scratch. The player movement is controlled by a PyTorch neural network. Each instance of the game is managed by the environment class.


To start training, just run:

```bash
python main.py
```

After training is done, the best model simulation will open.

To see simulation of the last saved best model, run:
```bash
python run_best_model.py
```

Currently, my last best model is available as best_model.pth file.

---

## 📦 Requirements

Tested with **Python 3.13.3**

Install dependencies:

```bash
pip install -r requirements.txt
