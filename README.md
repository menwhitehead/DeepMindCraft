# DeepMindCraft
Minecraft-like game framework interface for DeepMind DQN


## Installation and setup

* Clone and install the [DeepMind DQN code](https://github.com/kuz/DeepMind-Atari-Deep-Q-Learner).
* Copy this project's *minecraft* folder to your DeepMind installation:

``` cp -r minecraft YOUR_DEEPMIND_DIR/torch/share/lua/5.1/ ```

* Update the FRAMEWORK value in run_cpu and run_gpu:

``` FRAMEWORK="minecraft" ```

* Comment out two lines in Scale.lua:

```
    --x = image.rgb2y(x)
    --x = image.scale(x, self.width, self.height, 'bilinear')
```

* Install luasocket:

``` <PATH>/DeepMind-Atari-Deep-Q-Learner/torch/bin/luarocks install luasocket ```

* Launch the Python Minecraft-like backend:

```
cd minecraft_socket
python game_server.py
```

* Launch either *run_cpu* or *run_gpu* (currently you still have to include the atari game name, but it is ignored!!!!)

``` ./run_cpu breakout ```

* Watch the bot and wait for several days



## Results and Example Videos

* Simple Block-Breaking Bot:

![Break those blocks!](gifs/simple_block_breaking.gif?raw=true "Block Breaker")
