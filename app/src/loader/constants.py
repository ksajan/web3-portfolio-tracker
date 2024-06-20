from collections import defaultdict

"""
This file contains all the constants used in the project.

async_clients: This is a dictionary that stores all the async clients for the project. It is a nested dictionary with the
structure:
    {
            client_type:{
                network_type1: client_function,
                network_type2: client_function
                },
            client_type2:{
                network_type2: client_function
                }
            }

How to access the async_clients:
    async_clients[client_type][network_type] -> client_function
"""
async_clients = defaultdict(lambda: defaultdict(lambda: None))
