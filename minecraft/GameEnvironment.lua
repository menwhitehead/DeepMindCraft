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

require("socket")

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
    
    self.max_episode_steps = 100
    self.host = "localhost"
    self.port = 9999
    
    self.window_size = 84
    self.total_pixels = self.window_size * self.window_size
    
    -- Count of all legal actions for the agent
    self.total_number_actions = 8  
    
    self:connect()
    
    return self
end


-- Connect to the game server
function gameEnv:connect()
    print("Attempting connection to host '" .. self.host .. "' on port " .. self.port .. "...")
    self.connection = socket.connect(self.host, self.port)
    print("Connected")
    
    --Remove any algorithmic delay from the TCP connection
    self.connection:setoption("tcp-nodelay", true)
    
    -- Send a fake first action to the game server
    assert(self.connection:send("0"))  
end


function gameEnv:getState()
    
    game_frame = self.connection:receive(self.total_pixels + 1)  -- one extra byte for the reward
    
    -- Make a Lua table of the incoming bytes (exclude the last byte because it's the reward)
    t={}     
    for i = 1, string.len(game_frame) - 1 do
        t[i] = string.byte(string.sub(game_frame, i, i))
    end
    
    -- Set the reward value from the last byte
    reward = string.byte(string.sub(game_frame, self.total_pixels+1, self.total_pixels+1))
    --print("REWARD RECEIVED:" .. reward)

    -- Create a Tensor using a Storage created from the Lua table
    -- This is much faster than element-wise assignment
    stor = torch.Storage(t)
    screen = torch.Tensor(stor, 1, torch.LongStorage{self.window_size, self.window_size})

    if self.game_steps >= self.max_episode_steps then
        --print("REACHED END OF GAME")
        term = true
        self.game_steps = 0
    else
        term = false
    end
            
    return screen, reward, term
end



function gameEnv:step(action, training)
    self.game_steps = self.game_steps + 1
    
    --print("PERFORMED ACTION: " .. action)
    assert(self.connection:send(tostring(action) .. "\n"))

    return self:getState()
end


-- Send a reset message to the game server and then receive the first game frame in getState
function gameEnv:newGame()
    assert(self.connection:send("RESET\n"))
    return self:getState()
end


-- All our games are random, so just start a new game
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
    for j=1,self.total_number_actions do
      actions[j] = j
    end    
    return actions
end
