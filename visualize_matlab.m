PORT = 5005;
IP_ADD = '127.0.0.1';
delete(instrfindall('RemoteHost', IP_ADD, 'RemotePort', PORT))

u = udp(IP_ADD, PORT, 'LocalPort', PORT);
set(u,'Timeout',30);
fopen(u);


while true
    % read data from the UDP socket
    data = fread(u, 12, 'uint8');
    
    if numel(data) < 11
        disp('no data');
        continue;
    end
    % unpack the binary data using the typecast function
    heading = typecast(data(1:4), 'single');
    pitch  = typecast(data(5:8), 'single');
    roll  = typecast(data(9:12), 'single');
    
    disp(heading);
    disp(pitch);
    disp(roll);
end
