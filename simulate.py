import argparse
import subprocess
import math
import os
from time import sleep

roslaunch_imported = True
try:
    import roslaunch
except ImportError:
    roslaunch_imported = False



current_path = os.path.dirname(os.path.realpath(__file__))
gazebo_path = os.path.join(current_path, 'gazebo/')

run = os.path.join(current_path,"run")
spawn_clever = os.path.join()
spawn_launch = os.path.join(gazebo_path,'single_vehicle_spawn.launch')
gazebo_launch = os.path.join(gazebo_path,'gazebo.launch')
gazebo_plugins_dir = os.path.join(gazebo_path, 'plugins/')
gazebo_models_dir = os.path.join(gazebo_path, 'models/')
spawn_copters_dir = gazebo_path = os.path.join(current_path, 'spawn_copters.txt')
aruco_map_dir = os.path.join(gazebo_models_dir,'aruco_map.txt')

aruco_map = {}
for l in open(aruco_map_dir):
    line = l.split('\t')
    if line[0] != '# id':
        aruco_map[int(line[0])] = (float(line[2]), float(line[3]))
aruco_map = sorted(aruco_map.items(), key=lambda x:x[1])
aruco_map_dict = {aruco_map[i][0]: aruco_map[i][1] for i in range(len(aruco_map))}

spawn_copters = {}
for l in open(spawn_copters_dir):
    line = l.replace('\n', '').split()
    spawn_copters[int(line[0])] = int(line[1])


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("{} is an invalid value, must be positive".format(value))
    return ivalue

def positive_float(value):
    ivalue = float(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("{} is an invalid value, must be positive".format(value))
    return ivalue

def add_path_env(name, path):
    value = os.environ.get(name, '')
    if value:
        value += ':' + path
    else:
        value = path
    os.environ[name] = value
    print("Set {} to {}".format(name, value))

def kill_containers(n):
    print("\nClear containers:")
    for i in range(n):
        subprocess.call("docker kill sim-{}".format(i+1), shell=True)
    print("Cleared!")

if __name__ == "__main__":

    # Set argument parser
    parser = argparse.ArgumentParser(description="Simulate multiple Clover copters")
    parser.add_argument('-n','--number', type=positive_int, default='1',
                        help="Number of copters to simulate. Default is 1.")
    parser.add_argument('-p','--port', type=positive_int, default='14601',
                        help="UDP port for simulation data of the first copter. Default is 14601. UDP port for n-th copter will be equal to <port> + n - 1. This parameter is used only in non headless mode.")
    args = parser.parse_args()

    port = args.port - 1

    # Get xn, yn values for copters arranging
    n = float(args.number)  # Needs for ceiling
    xn = int(math.ceil(math.sqrt(n)))
    yn = int(math.ceil(n/xn))
    n = int(n)
    print("{} copters will be arranged to 2D array".format(args.number))

    output = "\nGenerated copters:\n"

    # Check that roslaunch was successfully imported
    if not roslaunch_imported:
        print("You don't have roslaunch module! Please, check your ROS installation.")
        quit()

    # Add Gazebo paths to environment
    add_path_env('GAZEBO_PLUGIN_PATH', gazebo_plugins_dir)
    add_path_env('GAZEBO_MODEL_PATH', gazebo_models_dir)
    add_path_env('LD_LIBRARY_PATH', gazebo_plugins_dir)
    os.environ['PX4_HOME_LAT'] = str(55.7031751)
    os.environ['PX4_HOME_LON'] = str(37.7248118)

    # Launch Gazebo
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [gazebo_launch])
    launch.start()

    # Run N docker containers with clever-show clients
    # Spawn N models arranged as a 2D array in a shape close to square to Gazebo
    for yi in range(yn-1, -1, -1):
        for xi in range(xn):
            index = xi + yi*xn + 1
            if index > n:
                break
            
            aruco = spawn_copters.get(index)
            x, y = aruco_map_dict[aruco] if aruco != None else (0, 0)
            if aruco == None:
                position = aruco_map[index-1]
                aruco = position[0]
                x, y = positive_ition[1]
            
                
            output += "sim-{} ({} {}, {})\t".format(index, aruco, x, y)
            subprocess.call("{} -i={} -p={}".format(run, index, port), shell=True)
            subprocess.call("roslaunch {} ID:={} port:={} x:={} y:={}".format(spawn_launch, index, port+index, x, y), shell=True)
        output += "\n"
    print(output)

    # Wait for ctrl+c
    try:
        launch.spin()
    finally:
        # After Ctrl+C, stop all nodes and containers from running
        kill_containers(n)
        launch.shutdown()
