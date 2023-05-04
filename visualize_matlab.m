PORT = 5005;
IP_ADD = '127.0.0.1';
delete(instrfindall('RemoteHost', IP_ADD, 'RemotePort', PORT))

u = udp(IP_ADD, PORT, 'LocalPort', PORT);
set(u,'Timeout',30);
fopen(u);

while true
    % read data from the UDP socket
    data = fread(u, 16, 'uint8');

    % unpack the binary data using the typecast function
    int_val = typecast(uint8(data(1:4)), 'int32');
    float_vals = typecast(uint8(data(5:end)), 'single');

    % print the unpacked values to the console
    disp(int_val);
    disp(float_vals);
end
