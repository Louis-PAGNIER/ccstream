local url = ""
local port = 3415

local ws, err = http.websocket(url .. ":" .. port)
if not ws then error("Error while connecting to server: " .. err) end
local p = peripheral.wrap("right")

-- TODO: Make a clean init
term.redirect(p)
p.setCursorBlink(false)
p.setTextScale(0.5)
for i = 0, 15 do term.setPaletteColor(2^i, term.nativePaletteColor(2^i)) end
term.setBackgroundColor(colors.black)
term.setTextColor(colors.white)
term.setCursorPos(1, 1)
term.clear()

parallel.waitForAll(function()
    local start = os.epoch "utc"
    while true do
        local json, ok = ws.receive()
        local o = textutils.unserializeJSON(json)

        local image = o["data"]
        local w = o["width"]
        local h = o["height"]
        local spaces = o["spaces"]
        local palette = o["palette"]

        for k, v in pairs(palette) do
            term.setPaletteColor(2^(k-1), v)
        end
        for i = 1, h do
            term.setCursorPos(1, i)
            term.blit(spaces, image[i], image[i])
        end
    end
end)

-- TODO: Make a clean exit
ws.close()
for i = 0, 15 do term.setPaletteColor(2^i, term.nativePaletteColor(2^i)) end
term.setBackgroundColor(colors.black)
term.setTextColor(colors.white)
term.setCursorPos(1, 1)
term.clear()
