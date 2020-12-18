local kbID = 'PID_FA61';

lmc.minimizeToTray = true
lmc_minimize()
clear()

lmc_device_set_name('MACROS',kbID)
lmc_print_devices()

write_to_file = function (key)
    local file = io.open("G:\\key_exchange_macro", "w")
    file:write(key)
    file:flush()
    file:close()
    lmc_send_keys('{F24}')
end

lmc_set_handler('MACROS' ,function(button, direction)
  if (direction == 1) then return end
  write_to_file(button)
end)
