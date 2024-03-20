import psutil
import time
import threading
import json

def read_process_names_from_json(file_path):
    """
    Function to read process names from a JSON file.
    
    Args:
        file_path (str): The path to the JSON file containing process names.
    
    Returns:
        list: A list of process names.
    """
    try:
        with open(file_path) as json_file:
            process_names = json.load(json_file)
            if not process_names:
                raise ValueError("JSON file is empty")
            return process_names
    except FileNotFoundError:
        raise FileNotFoundError("JSON file not found")

def kill_process_by_name(process_name):
    """
    Function to kill a process by its name.
    
    Args:
        process_name (str): The name of the process to be killed.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            print(f"Killing process {proc.pid} - {proc.info['name']}")
            proc.kill()

def monitor_processes(process_names, interval=5):
    """
    Function to monitor multiple processes in the background.
    
    Args:
        process_names (list): A list of process names to monitor.
        interval (int): The interval (in seconds) at which to check for the processes.
    """
    while True:
        for process_name in process_names:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    print(f"Process {process_name} is running. Attempting to kill...")
                    kill_process_by_name(process_name)
                    break
        time.sleep(interval)

def main():
    """
    Main function to demonstrate killing and monitoring processes by name.
    """
    try:
        process_names = read_process_names_from_json('process_names.json')
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
        return

    # Display the process names
    print("Process names from JSON file:")
    for process_name in process_names:
        print(process_name)

    # Start the monitor process in a separate thread
    monitor_thread = threading.Thread(target=monitor_processes, args=(process_names,))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Let the user manually terminate the script
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
