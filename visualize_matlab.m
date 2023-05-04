PORT = 5005;
IP_ADD = '127.0.0.1';
delete(instrfindall('RemoteHost', IP_ADD, 'RemotePort', PORT))

u = udp(IP_ADD, PORT, 'LocalPort', PORT);
set(u,'Timeout',30);
fopen(u);


while true
    % read data from the UDP socket
    data = fread(u, 28, 'uint8');
    
    if numel(data) < 27
        disp('no data');
        continue;
    end
    % unpack the binary data using the typecast function
    rpm = typecast(uint8(data(1:4)), 'int32');
    vel_x = typecast(uint8(data(5:8)), 'single');
    vel_y = typecast(uint8(data(9:12)), 'single');
    vel_z = typecast(uint8(data(13:16)), 'single');
    heading = typecast(uint8(data(17:20)), 'single');
    pitch  = typecast(uint8(data(21:24)), 'single');
    roll  = typecast(uint8(data(25:28)), 'single');
    
    %legth of car
    car_length = 3;%meters
    
    % define the car coordinate frame
    car_frame = [
        0, 0, 0;
        car_length, 0, 0;
        car_length, car_length/2, 0;
        car_length, car_length/2, car_length/2;
        car_length, 0, car_length/2;
        0, 0, car_length/2;
        0, car_length/2, car_length/2;
        0, car_length/2, 0;
    ];

    % rotate the car coordinate frame based on the heading, pitch, and roll angles
    R = rotationMatrix(heading, pitch, roll);
    car_frame = (R * car_frame').';

    % translate the car coordinate frame based on the velocity vector
    car_frame(:, 1) = car_frame(:, 1) + vel_x;
    car_frame(:, 2) = car_frame(:, 2) + vel_y;
    car_frame(:, 3) = car_frame(:, 3) + vel_z;

    % plot the car coordinate frame
    plot3(car_frame(:,1), car_frame(:,2), car_frame(:,3), 'o-', 'LineWidth', 2);
    axis equal;
    grid on;
    xlabel('x');
    ylabel('y');
    zlabel('z');
end

function R = rotationMatrix(heading, pitch, roll)

% Convert angles to radians
c1 = cosd(heading);
s1 = sind(heading);
c2 = cosd(pitch);
s2 = sind(pitch);
c3 = cosd(roll);
s3 = sind(roll);

% Calculate the rotation matrix
R = [c1*c2, c1*s2*s3 - s1*c3, c1*s2*c3 + s1*s3;     s1*c2, s1*s2*s3 + c1*c3, s1*s2*c3 - c1*s3;     -s2,   c2*s3,            c2*c3];

end