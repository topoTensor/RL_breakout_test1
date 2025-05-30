# RL Breakout Test

My first prototype of *evolutionary reinforcement learning model* of a game Breakout using pytorch and pygame. It's yet to be improved. The training process is sequential and built from scratch. It uses pytorch neural network for player movement. Every instance of the game is stored in the environment class.


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
