import unittest
import subprocess
import http.client
import os
from server import Server
import threading
import time
import socket


class WebTestCase(unittest.TestCase):
    """tests for socket adventure"""
    
    def setUp(self):
        self.server_process = subprocess.Popen(
            [
                "python",
                "server.py"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
    def tearDown(self):
        self.server_process.kill()
        self.server_process.communicate()
        
    def get_response(self, url):
        """
        Helper function to get a response from a given url, using http.client
        """

        conn = http.client.HTTPConnection('localhost:50000')
        conn.request('GET', url)

        response = conn.getresponse()

        conn.close()

        return response
        
        
    def server_start(self):
        self.server_thread = threading.Thread(target=Server().serve)
        self.server_thread.start()
        time.sleep(0.1)
        
    def server_close(self):
        self.server_thread.join()
    
    def send_message(self, message='testing'):
        client_sock = socket.socket()
        client_sock.connect(("127.0.0.1", 30000))
        response = client_sock.recv(4096).decode()
        
        my_message = message.encode('utf-8') + b'\n'
        client_sock.sendall(my_message)
        
        time.sleep(0.1)
        response = client_sock.recv(4096).decode()
        
        time.sleep(0.1)
        my_message = 'quit'.encode('utf-8') + b'\n'
        client_sock.sendall(my_message)
        
        time.sleep(0.1)
        goodbye = client_sock.recv(4096).decode()
                
        client_sock.close()
        
        return response
        

    def test_01_move_north(self):
        self.server_start()
        
        response = self.send_message('move north')
        
        self.server_close()
        
        self.assertEqual(response, 'OK! You are in the room with the mauve wallpaper.\n')
        
    def test_02_move_south(self):
        self.server_start()
        
        response = self.send_message('move south')
        
        self.server_close()
        
        self.assertEqual(response, 'OK! You are in the room with the white wallpaper.\n')
        
    def test_03_move_east(self):
        self.server_start()
        
        response = self.send_message('move east')
        
        self.server_close()
        
        self.assertEqual(response, 'OK! You are in the room with the brown wallpaper.\n')
        
    def test_04_move_west(self):
        self.server_start()
        
        response = self.send_message('move west')
        
        self.server_close()
        
        self.assertEqual(response, 'OK! You are in the room with the green wallpaper.\n')

    def test_05_welcome_and_goodbye(self):
        self.server_start()
        client_sock = socket.socket()
        client_sock.connect(("127.0.0.1", 30000))
        response = client_sock.recv(4096).decode()
        
        time.sleep(0.1)
        my_message = 'quit'.encode('utf-8') + b'\n'
        client_sock.sendall(my_message)
        
        time.sleep(0.1)
        goodbye = client_sock.recv(4096).decode()
        
        self.server_close()
        client_sock.close()

        self.assertEqual(response, 'OK! Welcome to Realms of Venture! You are in the room with the white wallpaper.\n')
        self.assertEqual(goodbye, 'OK! Goodbye!\n')

    def test_06_echo(self):
        self.server_start()
        
        response = self.send_message('say is anybody there?')
        
        self.server_close()
        
        self.assertEqual(response, 'OK! You say, "is anybody there?\n"\n')
"""
    def test_02(self):
        server_thread = threading.Thread(target=self.run_fake_server)
        server_thread.start()
        
        test_client = socket.socket()
        test_client.connect(("127.0.0.1", 50000))
        response = test_client.recv(4096).decode()
        print(response)
"""
        


        
        
if __name__ == '__main__':
    unittest.main()