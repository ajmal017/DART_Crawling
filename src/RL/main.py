import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from env import StockTradingEnv

import pandas as pd

import pandas_datareader as pdr


ticker = 'AAPL'
start_date = '2018-01-01'

df = pdr.get_data_yahoo(ticker, start_date)
df['Date'] = df.index
df.index = range(len(df))
df = df.sort_values('Date')
df['Date'] = df['Date'].astype('str')


# The algorithms require a vectorized environment to run

env = DummyVecEnv([lambda: StockTradingEnv(df)])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=50)
# model.predict()

obs = env.reset()

for i in range(len(df['Date'][-3:-1])):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    print(info)
    env.render(title=ticker)
