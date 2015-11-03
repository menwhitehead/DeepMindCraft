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
    
    self.host = "localhost"
    self.port = 9999
    
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
