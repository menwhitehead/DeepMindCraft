--[[ Copyright 2014 Google Inc.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
]]

-- This file defines the minecraft.GameEnvironment class.


-- The GameEnvironment class.
local gameEnv = torch.class('minecraft.GameEnvironment')


function gameEnv:__init(_opt)
    local _opt = _opt or {}
    -- defaults to emulator speed
    self.game_path      = _opt.game_path or '.'
    self.verbose        = _opt.verbose or 0
    self._actrep        = _opt.actrep or 1
    self._random_starts = _opt.random_starts or 1
    self.game_steps     = 0
    --self._screen        = minecraft.GameScreen(_opt.pool_frms, _opt.gpu)
    --self:reset(_opt.env, _opt.env_params, _opt.gpu)
    
    require("socket")
    host = host or "localhost"
    port = port or 9999
    print(host, port)

    print("Attempting connection to host '" ..host.. "' on port " ..port.. "...")
    --self.master_sock = self.socket.tcp()
    --self.connection = assert(self.master_sock.connect(host, port))
    self.connection = socket.connect(host, port)
    print("Connected")
    
    --print("SET NODELAY")
    self.connection:setoption("tcp-nodelay", true)
    
    assert(self.connection:send("0"))  -- send a fake first action

 
    
    return self
end


function gameEnv:_updateState(frame, reward, terminal, lives)
    self._state.reward       = reward
    self._state.terminal     = terminal
    self._state.prev_lives   = self._state.lives or lives
    self._state.lives        = lives
    return self
end


function gameEnv:getState()
    
    -- THIS WORKS FOR FAKE TENSOR CREATION
    --screen = torch.Tensor(3, 84, 84)
    --screen_storage = screen:storage()
    --for i=1,screen_storage:size() do -- fill up the Storage
    --  screen_storage[i] = 0.76
    --end
        
    -- Receive a line of pixel values separated by commas
    -- last number on the line is the reward for the previous action
    game_frame = self.connection:receive("*l")
    
    --print("RECEIVED RESPONSE FROM SERVER:")
    --print(game_frame)
    

    -- PROBABLY SHOULD CHECK THE INDEX CALCULATIONS AGAIN
    reward = 0
    screen = torch.Tensor(3, 84, 84)
    screen_storage = screen:storage()

    i = 1
    for str in string.gmatch(game_frame, "-*%d+") do
        number = tonumber(str)
        if i <= 7056 then
            y = math.floor((i-1)/84)
            x = (i-1)%84
            screen_storage[0*7056+y*84+x+1] = number
            screen_storage[1*7056+y*84+x+1] = number
            screen_storage[2*7056+y*84+x+1] = number
        else
            reward = number
            --print("REWARD: " .. number)
        end
    
        i = i + 1
    end
    
    if self.game_steps >= 100 then
        --print("REACHED END OF GAME")
        term = true
        self.game_steps = 0
    else
        term = false
    end
            
    
    --return self._state.observation, self._state.reward, self._state.terminal
    return screen, reward, term
end


function gameEnv:reset(_env, _params, _gpu)
    local env
    local params = _params or {useRGB=true}
    -- if no game name given use previous name if available
    if self.game then
        env = self.game.name
    end
    env = _env or env or 'ms_pacman'

    self.game       = minecraft.game(env, params, self.game_path)
    self._actions   = self:getActions()

    -- start the game
    if self.verbose > 0 then
        print('\nPlaying:', self.game.name)
    end

    self:_resetState()
    self:_updateState(self:_step(0))
    self:getState()
    return self
end


function gameEnv:_resetState()
    self._screen:clear()
    self._state = self._state or {}
    return self
end


-- Function plays `action` in the game and return game state.
function gameEnv:_step(action)
    assert(action)
    local x = self.game:play(action)
    self._screen:paint(x.data)
    return x.data, x.reward, x.terminal, x.lives
end


-- Function plays one random action in the game and return game state.
function gameEnv:_randomStep()
    return self:_step(self._actions[torch.random(#self._actions)])
end


function gameEnv:step(action, training)
    self.game_steps = self.game_steps + 1
    -- accumulate rewards over actrep action repeats
    --local cumulated_reward = 0
    --local frame, reward, terminal, lives
    --for i=1,self._actrep do
    --    -- Take selected action; ATARI games' actions start with action "0".
    --    frame, reward, terminal, lives = self:_step(action)
    --
    --    -- accumulate instantaneous reward
    --    cumulated_reward = cumulated_reward + reward
    --
    --    -- Loosing a life will trigger a terminal signal in training mode.
    --    -- We assume that a "life" IS an episode during training, but not during testing
    --    if training and lives and lives < self._state.lives then
    --        terminal = true
    --    end
    --
    --    -- game over, no point to repeat current action
    --    if terminal then break end
    --end
    --self:_updateState(frame, cumulated_reward, terminal, lives)
    
    --print("PERFORMED ACTION: " .. action)
    assert(self.connection:send(tostring(action) .. "\n"))

    
    return self:getState()
end


--[[ Function advances the emulator state until a new game starts and returns
this state. The new game may be a different one, in the sense that playing back
the exact same sequence of actions will result in different outcomes.
]]
function gameEnv:newGame()
    assert(self.connection:send("RESET\n"))
    return self:getState()
end


--[[ Function advances the emulator state until a new (random) game starts and
returns this state.
]]
function gameEnv:nextRandomGame(k)
    return self:newGame()
end


--[[ Function returns the number total number of pixels in one frame/observation
from the current game.
]]
function gameEnv:nObsFeature()
    return self.game:nObsFeature()
end


-- Function returns a table with valid actions in the current game.
function gameEnv:getActions()
    actions = {}
    for j=1,8 do
      actions[j] = j
    end    
    return actions
end
